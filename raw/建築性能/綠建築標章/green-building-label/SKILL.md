---
name: green-building-label
description: "This skill should be used when applying for Taiwan Green Building Label (綠建築標章) or Candidate Green Building Certificate (候選綠建築證書) through the EEWH system."
user-invocable: true
---

# Green Building Label (EEWH)

## Overview
台灣綠建築標章（EEWH, Ecology, Energy Saving, Waste Reduction, Health）是由內政部建築研究所於1999年建立的綠建築評估系統，是全球第4個實施的綠建築評估系統，適用於亞熱帶氣候。

## Applicable Scenarios
- 申請綠建築標章（已取得使用執照之建築物）
- 申請候選綠建築證書（取得建造執照之建築物）
- 設計符合綠建築指標之建築
- 既有建築改善評估

## Assessment Indicators (9項指標)

| 指標代碼 | 指標名稱 | 權重 | 必備條件 |
|---------|---------|------|---------|
| EA | 生物多樣性 | 6% | - |
| GB | 綠化量 | 6% | - |
| BS | 基地保水 | 6% | - |
| EE | 日常節能 | 21% | 必需達標 |
| CO2 | CO2減量 | 6% | - |
| WR | 廢棄物減量 | 6% | - |
| IEQ | 室內環境 | 21% | 必需達標 |
| RW | 水資源 | 6% | - |
| SC | 污水垃圾改善 | 6% | - |
{line}

## Building Categories (建築類型)

| 類型 | 適用對象 | 指標要求 |
|-----|---------|---------|
| 基本型 | 一般建築物 | 9項指標 |
| 住宿類 | 住宅、宿舍、旅館 | 9項指標 |
| 廠房類 | 工廠、倉庫 | 9項指標 |
| 舊建築改善類 | 既有建築改善 | 6項指標 |
| 社區類 | 社區、住宅社區 | 7項指標 |
| 既有建築類 | 已使用建築 | 7項指標 |

## Rating Levels

| 等級 | 分數門檻 | 標章 |
|-----|---------|------|
| 合格級 | 通過基本指標 | 綠建築標章 |
| 銅級 | 13-19分 | 銅級標章 |
| 銀級 | 20-25分 | 銀級標章 |
| 黃金級 | 26-31分 | 黃金級標章 |
| 鑽石級 | 32分以上 | 鑽石級標章 |

## Key Thresholds

### 日常節能指標 (EE)
```
| 建築類型 | 節能效率基準 |
|---------|-----------|
| 住宿類 | EPI ≦ 65 |
| 辦公類 | EPI ≦ 50 |
| 商場類 | EPI ≦ 85 |
```

### 室內環境品質 (IEQ)
```
| 項目 | 基準 |
|-----|------|
| 採光 | 係數 ≧ 1.0% |
| 通風 | 平均風速 ≧ 0.2 m/s |
| 噪音 | ≦ 45 dB(A) |
```

## Application Process

1. 取得建造執照後 → 申請候選綠建築證書
2. 施工期間 → 依據評估手冊施工
3. 取得使用執照後 → 申請綠建築標章評定
4. 向評定專業機構（台灣建築中心）申請評定
5. 取得評定書後 → 向內政部申請認可

## Evaluation Manual
- 綠建築評估手冊（基本型、住宿類、廠房類、舊建築改善類、社區類、既有建築類）
- 建築能效評估手冊

## References
- [內政部建築研究所 - 綠建築標章](https://www.abri.gov.tw/cp.aspx?n=804)
- [台灣建築中心](https://gb.tabc.org.tw/)
- 綠建築標章及建築能效標示申請審核認可及使用作業要點

## MCP Tool Integration
- 查詢相關法規：`taiwan-building-code_search_building_code(query: "綠建築")`
- 查詢解釋函：`taiwan-building-code_search_building_interpretations(query: "綠建築標章")`