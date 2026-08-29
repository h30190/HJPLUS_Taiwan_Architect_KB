---
type: Reference
title: "Revit AI 目標與證據契約"
---

# Revit AI 目標與證據契約

使用這份契約分開保存規劃、執行與驗證證據。欄位名稱只是示意，可配合實際 Revit 整合方式調整，但不得因此降低各檢查閘的要求。

## 必要檢查閘

| 檢查閘 | 必要證據 | 停止條件 |
|---|---|---|
| G0 — 執行情境 | Revit 版本、文件綁定，以及任務需要時的視圖與選取資訊 | 沒有 active document、版本錯誤、連線過期或文件已切換 |
| G1 — 目標 | 目標來源、精確 ID 或已審閱候選集合，以及來源追蹤 | 目標為空、含糊、由猜測產生或集合不完整 |
| G2 — 預覽 | 風險、變更前後意圖、預期範圍、確認與復原方式 | 破壞範圍未知，或錯誤假設操作可以復原 |
| G3 — 執行 | API 進入點、Transaction 名稱與狀態、實際模型影響 ID | 把 Rejected、Pending 或未知狀態表示為成功 |
| G4 — 讀回 | 必要主張、另一筆查詢取得的觀測值、證據涵蓋率 | 把執行結果的回音表示成獨立證據 |
| G5 — 回報 | 結果狀態、模型影響、驗證、Undo／rollback 與不確定性 | 遺漏不一致、timeout 或未涵蓋主張 |

## 最小證據格式

```yaml
context:
  revit_version: "2024"
  document_binding: "去識別化的文件指紋"
  active_view_id: 12345
target:
  source: current_selection
  element_ids: [67890]
  reviewed: true
operation:
  risk: reversible_write
  preview: "備註：<原值> -> 待協調"
  transaction_name: "更新選取牆的備註"
  transaction_state: committed
impact:
  created_ids: []
  modified_ids: [67890]
  deleted_ids: []
verification:
  status: verified
  claims:
    - target: "ElementId 67890／備註"
      expected: "待協調"
      actual: "待協調"
      source: independent_revit_readback
recovery:
  undo: "Revit Undo > 更新選取牆的備註"
uncertainty: []
```

## 目標來源規則

- `explicit_element_id`：確認元素存在、屬於綁定文件，且符合要求的類別或型別。
- `current_selection`：保留完整選取集合，不得默默只取第一個元素。
- `reviewed_candidates`：記錄已審閱的 ID 與用來區分候選的欄位。
- `tool_returned_ids`：保留產生這些 ID 的 request 與工具來源追蹤。
- `created_ids`：保留建立操作與 Transaction 來源追蹤。
- `heuristic_candidates`：未經審閱或加入確定性條件前，不得直接執行。

## 結果狀態規則

- `verified`：每個必要主張都有獨立觀測值，而且全部通過。
- `partially_verified`：執行完成，但必要證據尚未完整涵蓋。
- `verification_failed`：至少一個已觀測的必要主張失敗。
- `not_verified`：執行完成，但沒有進行必要讀回。
- `uncertain`：派送、timeout、文件切換或缺少最終狀態，導致不能安全宣稱已執行。
- `rolled_back`：相關 Transaction 或 TransactionGroup 已 rollback，且已觀測復原結果。

不得只因總數相同就推論為 `verified`。必須比較不重複的 ElementId 集合與逐項主張證據。

## 公開前的隱私處理

把證據放入 issue、pull request、release note 或公開知識庫之前：

- 移除業主與專案名稱。
- 移除本機絕對路徑與模型檔名。
- 移除憑證、token、prompt、生成原始碼與專有幾何資料。
- 當版本識別、source hash、數量、狀態轉換與合成範例已足夠時，只保留這些證據。
- 明確標示證據來自原始碼審查、自動測試、部署檢查、實機冒煙測試或獨立模型讀回。
