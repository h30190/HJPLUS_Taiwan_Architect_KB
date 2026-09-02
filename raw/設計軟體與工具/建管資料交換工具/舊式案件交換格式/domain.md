---
type: Knowledge Entry
title: "舊式案件交換格式"
---

# 舊式案件交換格式

本知識條目說明舊式 CPAMI 建照案件封包中 `data.txt` 的互通風險與保全原則。它是依逆向工程與實作紀錄整理的技術參考，並非主管機關公布的檔案規格、申請程序或審查依據。

## 使用情境

當既有案件需要在舊系統、轉換程式或內部資料模型之間往返，且必須盡量維持封包可讀性與案件資料完整性時使用。本條目不授權變更已簽章內容，也不取代主管機關受理測試。

## 學習目標

- 辨識表集合、列與欄位文字格式的保留需求。
- 區分空字串與數字零、民國日期字串與一般日期格式。
- 將未知、擴充或簽章相關內容保留原樣，避免以推測資料覆寫。

## 實務應用

實作時先以去識別化的合成案件建立測試樣本，再以嚴格編碼、換行與結構檢查驗證。若需要解讀欄位或將內部資料映射至案件表，另參閱 [permit-report-data-mapping](../書表與資料群組對照/permit-report-data-mapping/SKILL.md)；若需定義不可變更邊界，另參閱 [permit-data-fidelity-model](../保真資料儲存模型/permit-data-fidelity-model/SKILL.md)。

## 相關技能

- [legacy-permit-data-interchange](legacy-permit-data-interchange/SKILL.md)
- [permit-codebook-snapshot-governance](../代碼字典快照治理/permit-codebook-snapshot-governance/SKILL.md)
