---
type: Knowledge Entry
title: "Revit AI 目標判定與安全執行"
---

# Revit AI 目標判定與安全執行

## 使用情境

適用於使用 AI、MCP、本機 Agent 或 Revit Add-in 讀取、建立或修改 Revit 模型時，建立一套可追查的工作流程。重點不是教特定產品怎麼安裝，而是避免 AI 在目標不明、執行範圍未確認或結果未讀回時，就宣稱模型工作已完成。

這個知識點涵蓋七個連續階段：讀取目前文件與視圖、證明目標元素、控制唯讀檢查深度、預覽操作風險、安全執行、獨立讀回，以及回報結果與復原方式。

## 0.8.1 帶來的計畫修正

BIM Personal Agent 是本文貢獻者自行開發的個人研究專案；其 v0.8.1 新增唯讀 Element Lens、明確的目標來源與單一目標安全自動追查。這個案例顯示，只談 Transaction、Undo 與執行後驗證仍不完整；安全流程必須把「目標是否已被證明」放在任何模型寫入之前。[BIM Personal Agent v0.8.1](https://github.com/NicheSam/BIM-personal-agent/releases/tag/v0.8.1)

本篇只抽取可重用的工作方法。Element Lens、工具數量、Gateway 名稱與內部狀態值屬於該專案的實作，不是 Autodesk Revit 的官方規範，也不是其他 Revit Agent 必須照搬的介面。

## 學習目標

- 分清楚「找到候選元素」與「已證明操作目標」不是同一件事。
- 依需求逐步讀取摘要、參數與完整關聯，避免一開始掃描整個專案。
- 在模型寫入前確認文件、視圖、元素集合、預期變更與復原方式。
- 分開回報執行成功、模型影響、讀回結果與仍未確認的部分。
- 遇到 timeout、文件切換或證據不一致時停止自動重試，保留不確定狀態。

## 核心流程

| 階段 | 必須回答的問題 | 通過條件 |
|---|---|---|
| 1. 現況讀取 | Revit 版本、active document、active view、selection 與連線是否符合任務？ | 文件與操作上下文可識別，沒有在檢查途中切換 |
| 2. 目標證明 | 目標來自明確 ElementId、目前選取、已審閱候選、前一步回傳或本次建立結果？ | 完整目標集合可列出；名稱、類別或空間猜測只能當候選 |
| 3. 唯讀檢查 | 需要 identity、參數，還是幾何／關聯／視圖資訊？ | 只讀到足以判斷下一步的深度，沒有附帶模型修改 |
| 4. 風險預覽 | 是唯讀、可 Undo 修改、破壞性操作，還是結果可能不可判定？ | 變更前後、元素範圍、確認需求與復原方式已說明 |
| 5. 安全執行 | 是否在 Revit 支援的 API context 與 Transaction 內執行？ | Transaction 狀態與實際模型影響有紀錄 |
| 6. 獨立讀回 | 執行回傳之外，是否重新查詢了必要的模型狀態？ | 每個必要主張都有對應觀測值；不一致時不得標示完整驗證 |
| 7. 證據回報 | 使用者能否知道改了什麼、查了什麼、哪些仍未知？ | 回報目標、影響、驗證、Undo 與不確定性 |

Autodesk Revit 2024 API 文件指出，模型變更必須發生在有效的 Transaction 中；成功提交的命名 Transaction 會出現在 Undo 選單。[Transactions](https://help.autodesk.com/cloudhelp/2024/ENU/Revit-API/files/Revit_API_Developers_Guide/Basic_Interaction_with_Revit_Elements/Revit_API_Revit_API_Developers_Guide_Basic_Interaction_with_Revit_Elements_Transactions_html.html) [Transaction Classes](https://help.autodesk.com/cloudhelp/2024/ENU/Revit-API/files/Revit_API_Developers_Guide/Basic_Interaction_with_Revit_Elements/Transactions/Revit_API_Revit_API_Developers_Guide_Basic_Interaction_with_Revit_Elements_Transactions_Transaction_Classes_html.html)

從非模態介面或非同步 Agent 送入 Revit 的工作，應透過 External Event 或其他 Revit 支援的 API 進入點，在 Revit 可處理時才執行；不能把背景執行緒能排入佇列誤當成它能直接呼叫 Revit API。[External Events](https://help.autodesk.com/cloudhelp/2024/ENU/Revit-API/files/Revit_API_Developers_Guide/Advanced_Topics/Revit_API_Revit_API_Developers_Guide_Advanced_Topics_External_Events_html.html)

## 目標證明規則

可接受的來源包括：使用者提供的 ElementId、與任務一致的目前選取、使用者已審閱的候選集合、同一條執行鏈中工具回傳的元素，以及本次操作剛建立的元素。

只有名稱、類別、族群、型別、最近使用或幾何接近等條件時，得到的是候選，不是已確認目標。應先呈現候選差異，再由使用者確認或由另一個確定性條件收斂。

「只在一個精確目標時自動深入追查」是安全的自動化策略，但不代表所有多元素任務都應拒絕。多目標操作仍可進行，前提是完整集合明確、可預覽、可讀回，且使用者的意圖確實涵蓋整個集合。

## 實務應用範例

任務：「把目前選到的牆，備註改成『待協調』。」

1. 讀取 active document、active view 與 selection，確認只有一個有效牆元素，並保存其 ElementId。
2. 唯讀取得元素 identity、目前備註值與參數是否可寫；若沒有選取、選到多個元素或參數唯讀，就停止寫入並回報原因。
3. 預覽：「目標 1 個牆元素；備註由目前值改為『待協調』；可用 Revit Undo 復原。」
4. 在 Revit 支援的 API context 內開啟具名 Transaction，只修改已證明的 ElementId，檢查 Commit 狀態。
5. Transaction 完成後重新取得同一 ElementId 的備註值。這次重新查詢才是讀回證據，不能用執行函式自己回傳的 `success` 代替。
6. 回報：目標來源、修改元素數與 ID、讀回值、驗證狀態、Transaction 名稱及 Undo 方式。

若 API 呼叫 timeout，而工作可能已進入 Revit UI thread，狀態應標為「不確定」並先重新讀取模型；不能直接重送相同修改。

## 常見陷阱

### 只用名稱或類別找到元素就直接修改

- **錯誤**：搜尋第一個名稱相符的族群或型別後立刻寫入。
- **正確**：把搜尋結果當候選，列出足以區分的 identity、位置或關聯，再取得確定目標。

### 把工具回傳 success 當成模型已驗證

- **錯誤**：執行函式回傳成功，就宣稱模型內容正確。
- **正確**：把執行狀態與獨立讀回分開；必要主張沒有觀測值時，只能標示未驗證或部分驗證。

### timeout 後自動重試

- **錯誤**：沒有確認第一筆工作是否已執行，就再次送出相同模型修改。
- **正確**：先停止、重新讀取文件與目標狀態，再由證據決定是否需要修正。

### 只看摘要數量，不核對元素集合

- **錯誤**：`modified = 5`、`verified = 5` 就視為同一批元素。
- **正確**：同時核對元素 ID 集合、每個必要主張與讀回值；數量相同不代表對象相同。

### 把單一目標策略誤寫成多目標禁令

- **錯誤**：因為自動追查只允許一個元素，就拒絕所有明確的批次任務。
- **正確**：限制自動推論，不限制已審閱且範圍完整的多目標工作。

## 證據與版本邊界

- Autodesk 官方文件證明 Revit API context、Transaction、Rollback、TransactionGroup 與 Undo 的產品行為。
- BIM Personal Agent v0.8.1 是本文貢獻者個人研究專案中的公開實作案例，不是獨立第三方驗證，也不是 Revit 官方標準。
- 自動測試能證明政策分支與資料投影符合程式設計；部署成功只證明檔案與設定到位；真實模型結果仍需要當次 Revit 文件的實機讀回。
- 公開證據不得包含業主名稱、專案路徑、模型檔名、憑證或可識別的專案內容。

詳細的狀態與回報欄位見 [Revit AI 目標與證據契約](revit-ai-targeting-and-safe-execution/references/evidence-contract.md)。

## 資料日期與待確認

- Autodesk Revit 2024 API 文件查證日期：2026-08-28；官方頁面最後修改日期為 2023-10-26。
- BIM Personal Agent v0.8.1 release 查證日期：2026-08-28。
- [ ] Revit 2025、2026 或後續版本的 API 行為未在本篇驗證；使用其他版本時應改查對應版本官方文件。
- [ ] 跨文件、連結模型與不可 Undo 操作需要各自的復原與確認設計，不可直接套用單一文件範例。

## 相關技能與分工

- [不確定性標示與來源管控](../../../../建築顧問方法論/不確定性標示與來源管控/uncertainty-and-source-control/SKILL.md)：負責來源可信度與未驗證事實的表達；本篇負責 Revit 模型操作的目標、執行與讀回流程。
