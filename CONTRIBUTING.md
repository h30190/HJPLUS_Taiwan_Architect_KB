# 貢獻指南

歡迎來到 HJPLUS 台灣建築師技能知識庫！這個儲存庫是為台灣建築師社群打造的共同資源。

## 如何貢獻

1. **Fork 儲存庫**
   - 建立您自己的儲存庫副本進行操作

2. **建立新內容**
   - 在適當的分類目錄中新增檔案
   - 遵循既有的格式和結構
   - 包含適當的引用和參考資料

3. **更新現有內容**
   - 改善和擴展既有的文件
   - 更正錯誤或過時的資訊
   - 新增範例或案例研究

## 檔案命名慣例

- 使用描述性的名稱給檔案和目錄
- 目錄名稱使用標題格式（Title Case）
- 檔案名稱使用小寫與連字號（例如：`building-permit-process.md`）
- 在檔案名稱中包含相關關鍵字以便於搜尋

## 技能模組架構

### 技能分類

| 分類 | 特徵 | 數量 | 位置 |
|-----|------|-----|-|-|
| **A 類通用技能** | 國際通用標準，無需台灣適配 | 5 個 | Design & Planning、Technical Knowledge |
| **B 類適配技能** | 國際規範→台灣適配，保留 TODO 注記 | 8 個 | Design & Planning、Technical Knowledge、性能 |
| **C 類台灣法規技能** | 完全台灣法規，MCP 工具對接 | 5 個 | Building Codes & Regulations |

### 雙語言架構

每個技能包含兩個文件：

1. **skill.md（AI 用，英文）**
   - 使用英文專業技術術語
   - 定義核心能力與 AI 操作指南
   - 支援 AI 精確調動與理解

2. **domain.md（人類用，繁體中文）**
   - 使用繁體中文專業術語
   - 說明技能用途與學習重點
   - 支援人類學習與知識內化

### 技能目錄結構

```
建築設計與規劃/
├── 設計理論/
│   ├── concept-design/
│   │   ├── skill.md              # AI 英文
│   │   └── domain.md             # 人類繁體中文
│   ├── design-theory/
│   ├── building-typology/
│   └── spatial-planning/
└── 建築基礎/
    └── architect-foundations/

專業複委託/
├── 材料設備/
│   ├── material-selection/
│   └── building-envelope/
├── 結構系統/
│   └── structural-systems/
└── 機電系統/
    └── building-services/

建築性能/
├── 光環境設計/
│   └── daylighting-design/
├── 音環境設計/
│   └── acoustic-design/
├── 永續建築/
│   └── building-sustainability/
└── 計算工具/
    └── architect-calculator/

建築法規/
├── 建築法規/
│   └── taiwan-building-codes/
├── 消防安全/
│   └── taiwan-fire-safety/
├── 無障礙設計/
│   └── taiwan-accessibility/
├── 施工文件/
│   └── taiwan-construction-docs/
└── 容積計算/
    └── taiwan-programming/
```

### 8 大分類架構

| 分類 | 技能數 | 說明 |
|-----|-|-|-|
| 建築設計與規劃 | 5 | 設計理論、建築基礎 |
| 專業複委託 | 4 | 材料設備、結構系統、機電系統 |
| 建築性能 | 4 | 光環境、音環境、永續建築、計算工具 |
| 建築法規 | 5 | 台灣建築法規 5 項 |
| 專案管理 | 14 | 事務營運、業務開發、酬金管理、專業倫理與證照 |
| 經營管理 | 14 | 契約與倫理、創業指南、商業發展、專業行銷與財務 |
| 建築施工與材料 | 0 | 待擴充 |
| 建築執照 | 0 | 待擴充 |

## 文件結構

每個文件應包含：
- 清晰的標題
- 簡短的介紹
- 用章節組織的主內容
- 相關的引用或參考資料
- 聯絡資訊（如適用）

## 審查流程

所有貢獻都將由維護人員審查後才會合併。請確保您的內容：
- 精確且最新
- 與台灣建築實務相關
- 有適當的引用來源
- 以專業語言編寫

### 驗證工具

我們提供驗證腳本幫助您在提交前檢查內容。使用方式：

```bash
bash .opencode/skills/validate-commit/scripts/validate.sh
```

腳本提供三種檢查模式：

1. **檢查 PR / 新增檔案** — 驗證特定的新增檔案
2. **檢查單一檔案** — 驗證某一個特定檔案
3. **全量儲存庫** — 對整個知識庫執行完整檢查

詳細說明請見 [skills/validate-commit/skill.md](../skills/validate-commit/skill.md)。

> 建議在提交 PR 前使用驗證腳本檢查，確保內容符合格式規範。

## 授權

此知識庫採用**分層授權**模式：

| 內容 | 授權條款 |
|--|------|
| **文字內容**（`.md` 文件、知識文件） | [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-Hant) |
| **腳本程式碼**（`.sh`、`.py`、`.js`、`.ts` 等） | [PolyForm Noncommercial 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0) |

詳細授權條款請見 [LICENSE](LICENSE) 與 [LICENSE-CODE](LICENSE-CODE) 檔案。

### 貢獻者授權同意

當您提交 Pull Request 時，即表示您同意您的貢獻內容（文字與程式碼）均採用上述條款授權。

> 授權條款不可撤銷；一旦貢獻並合入主分支，其授權持續生效至著作權消滅為止。