---
type: Knowledge Entry
title: "代碼字典快照治理"
---

# 代碼字典快照治理

本知識條目處理舊式 CPAMI 案件交換所依賴的代碼字典快照：如何標記來源版本、限制使用範圍，以及避免把歷史資料誤稱為現行官方代碼。內容是逆向工程／實作證據的整理，不是代碼主管機關的公告。

## 使用情境

當轉換、檢視或比對案件中的用途、行政區、樓層、構造或表單代碼，且手邊只有特定版本的舊式字典快照時使用。

## 學習目標

- 將快照的來源、日期與內容版本寫入可追溯紀錄。
- 將歷史快照的查詢結果與現行官方資料分開處理。
- 對未知代碼採保留與待查，而不是自行補碼或覆寫。

## 實務應用

以快照只做重現、比對與技術診斷；需要辦理或確認現行代碼時，應另查詢相應機關當期資料。與案件封包文字格式的保存規則，請搭配 `legacy-permit-data-interchange` 使用。

## 相關技能

- [permit-codebook-snapshot-governance](permit-codebook-snapshot-governance/SKILL.md)
- [legacy-permit-data-interchange](../舊式案件交換格式/legacy-permit-data-interchange/SKILL.md)
