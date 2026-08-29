# Bundle history

本檔為 OKF §9 的 bundle 更新紀錄，是這個知識庫**機器可讀的正式沿革**；
`README.md` 的「最近更新」區塊是同一份歷史的人類閱讀版本。
兩者都由維護者在合併 PR 後更新，日期標題必須是 ISO 8601 `YYYY-MM-DD`，最新在最上面。

## 2026-08-21

- **Creation**: 新增 `建築執照/建造執照/申請文件/圖面要求/臺北市建照圖說繪製與圖冊編排` (taipei-permit-drawing-standards)——臺北市建造執照標準圖冊編排（A101–A7）、44 項建照申請書圖檢核清單、無紙化系統 N 系列檔名前綴編碼規則、結構外審線上壓章與公會對副本校對 SOP。

## 2026-08-13

- **Update**: 統一 24 份 `domain.md` 的顯示標題（[#58](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pull/58)，解決 [#40](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/issues/40)）。7 個英文 H1 中文化、混凝土「版」改「板」、建築執照四類帶執照別；`title` 與 H1 同步修正，`validate_okf.py` 的重複標題警告由 12 降為 0。
- **Creation**: 新增 `建築執照/建造執照/變更設計報備/design-change-filing`——臺北市建照變更設計報備流程（[#51](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pull/51)）。內容僅適用臺北市，已於 `domain.md` 標註限定警語。合併後由維護者補上 OKF `type` frontmatter。

## 2026-08-07

- **Creation**: 新增 `建築施工與材料/綠建材/綠建材檢索與選用工具/green-material-search-toolkit`——TABC 綠建材本機檢索平台與選用說明書產生器（[#47](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pull/47)）。TABC 認證資料與使用者成品刻意不隨庫散布（授權不相容），由技能層 `.gitignore` 擋下，首次使用依 SKILL.md「Setup」於本機取得或重新抓取。合併後由維護者補上 OKF `type` frontmatter。
- **Creation**: 新增 `專業複委託/機電系統/台灣機電物料百科/tw-mep-spec-wiki`——台灣機電物料規格百科，目前收錄高興昌配管 1,180 筆（[#38](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pull/38)）。合併後由維護者重新產生 `MEP品項百科.json`（原提交版全部 1,180 筆的 `資料來源` 仍指向已移除的廠商型錄 PDF 路徑）、修正 pre-commit hook 的相依宣告，並補上 OKF `type` frontmatter。
- **Creation**: 新增 `專業複委託/機電系統/taiwan-mep-unit-basis`——台灣機電單位慣例與法規設計階段對應（[#46](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pull/46)）。該 PR 早於 OKF v0.2，合併後由維護者補上 `type` frontmatter 與 `SECTION_CLASS` 覆寫。
- **Update**: 清理 B 類分類債。8 個實為台灣本土法規／標章的技能（台電屋內線路與受電室、台灣給排水／電信／水表規範、EEWH 綠建築標章、低碳建築標示、室內環境）由 B 改為 C；其餘 10 個確為國際規範的技能補上 `<!-- TODO: Taiwan adaptation needed -->` 標記，指明所依國際標準與尚未在地化的區塊。`scripts/update_readme_counts.py` 的 `SECTION_CLASS` 同步覆寫，分類統計由 A 10／B 18／C 53 變為 A 10／B 10／C 61。
- **Update**: 建築執照 4 種執照別（使用／建造／拆除／雜項）下的 16 個技能改用執照別專屬名稱並移入英文技能目錄，解除 4 組 `name` 重複；內容仍四份相同，已於各檔標註 TODO 待專業者依執照別分化。2 份參考資料補 `type: Reference`，`scripts/validate_okf.py` 新增重複 `name` 檢查。
- **Update**: 全庫升級至 OKF v0.2。81 份 `domain.md` 補上 `type: Knowledge Entry`、81 份 `SKILL.md` 補上 `type: Skill`；8 份標記 `metadata.status: verified` 的技能改以 OKF `verified` 家族記錄查證者與查證日期；新增本檔與 `scripts/validate_okf.py`。
- **Update**: 修復文化資產分類 11 個檔案的編碼損壞，並補齊全庫 `metadata.class`（[#45](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pull/45)）。

## 2026-08-04

- **Update**: 修正智慧建築標章 4.2.2 空調系統智慧化節能計算範例的積分加總值（49→59，已向台灣智慧建築協會確認）（[#43](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pull/43)）。
- **Update**: 臺中市地址地號查詢新增建築線免指地區／軍事禁限建、文化資產查詢與快速摘要，查詢來源由 9 個增為 11 個（[#42](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pull/42)）；都市計畫管制 PDF 的配對邏輯與報告警示於 [#44](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pull/44) 補強。

## 2026-07-27

- **Creation**: 新增臺北市建築物附置裝飾性構造物設計範例彙編技能（113 年 9 月 25 日發布實施）（[#41](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pull/41)）。

## 2026-07-24

- **Creation**: 新增建築物給水排水設備設計技術規範技能，涵蓋水箱容量、管徑坡度、存水彎、通氣管與截留器（[#39](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pull/39)）。

## 2026-07-23

- **Update**: 智慧建築標章更新至評估手冊 2024 年版（6 大指標整併、等級門檻、22 項基本規定），並修正建築能效標示 BEE→BERS（[#36](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pull/36)）。

## 2026-07-14

- **Creation**: 新增建築顧問方法論橫向層 5 技能：諮詢流程、法源位階、時效查證、不確定性標示、邊界案例函詢（[#34](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pull/34)）。
- **Creation**: 新增高度比與面前道路認定檢討技能，涵蓋 §14-19、23-24、27 等 11 條法規（[#31](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pull/31)）。
- **Creation**: 新增臺中市地址地號一鍵查詢土地資料技能（[#35](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pull/35)）。
- **Update**: Autodesk Construction Cloud 更名為 Autodesk Forma（[#32](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pull/32)）。

## 2026-07-04

- **Creation**: 新增陽臺梯廳回計容積計算技能（§162 陽臺 10%、梯廳 10%、合計 15%）（[#27](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pull/27)）。
- **Creation**: 新增無障礙電梯機道尺寸對應表技能，涵蓋三菱、永大、崇友三品牌 P8–P13（[#25](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pull/25)）。
- **Creation**: 新增自來水、台電與發電機消防等 5 項機電相關技能（[#24](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pull/24)）。

## 2026-06-26

- **Creation**: 新增地方自治法規分類，首篇為臺中市宜居建築設施設置及回饋辦法（[#22](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pull/22)）。

## 2026-06-25

- **Creation**: 新增公共工程品質資料庫技能（[#19](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pull/19)）。
- **Creation**: 新增新北市建造執照申請文件清單（[#21](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pull/21)）。

## 2026-06-19

- **Creation**: 新增設計軟體與工具分類，含 Archicad 4 個技能模組（[#14](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pull/14)）。
- **Creation**: 新增樓梯欄杆坡道技能（建築技術規則 §33 樓梯寬度）（[#11](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pull/11)）。
- **Creation**: 新增容積免計實務陷阱技能（[#10](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pull/10)）。

## 2026-06-18

- **Creation**: 新增文化資產保存法分類，含 9 個 C 類技能（[#15](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pull/15)）。

## 2026-06-17

- **Creation**: 新增混凝土結構設計分類，含 5 個 C 類技能（[#9](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pull/9)）。
- **Creation**: 新增無障礙出入口門淨寬實務陷阱技能（[#12](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pull/12)）。

## 2026-05-17

- **Creation**: 新增公共工程分類（公開招標、公開閱覽）（[#4](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pull/4)）。

## 2026-05-03

- **Creation**: 新增排煙窗法規檢討技能，為本知識庫第一個技能（[#1](https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pull/1)）。
