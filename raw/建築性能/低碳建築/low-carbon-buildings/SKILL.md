---
name: low-carbon-buildings
description: "This skill should be used when applying for Taiwan Low Embodied Carbon Building Label (低碳建築標示/LEBR) or calculating embodied carbon in construction."
user-invocable: true
---

# Low Embodied Carbon Buildings (LEBR)

## Overview
低碳（低蘊含碳）建築標示制度是由內政部建築研究所於2024年實施的建築蘊含碳排評估系統，評估建築物在建材生產、運輸、施工、維護、更新及拆除階段之蘊含碳排放（Embodied Carbon）。

## Applicable Scenarios
- 申請低碳建築標示（已取得使用執照之建築物）
- 申請候選低碳建築證書（取得建造執照之建築物）
- 建材碳足跡計算
- 低碳營造策略規劃

## Assessment Focus
建築全生命週期碳排放分為兩部分：
- **使用碳排**：營運階段（已有建築能效制度管理）
- **蘊含碳排**：營建階段（本制度管理）

## Rating Levels (7級 + 4級低碳)

| 能效等級 | 碳排減碳率 | 備註 |
|---------|-----------|------|
| 第1級 | 最佳 | - |
| 第2級 | - | - |
| 第3級 | - | - |
| 第4級 | - | 低碳建築門檻 |
| 第5級 | - | - |
| 第6級 | - | - |
| 第7級 | 最差 | - |

### 低碳分級
| 低碳等級 | 條件 |
|---------|------|
| 低碳第4級 | 第4級 |
| 低碳第3級 | 第3級 |
| 低碳第2級 | 第2級 |
| 低碳第1級 | 第1級 |
| 低碳第1+級（超低碳）| 第1級+碳排減碳率≧20% |

## Key Calculation (EN 15978)

### 蘊含碳排放計算
```
EC = Σ (Mi × EF_i) + EC_transport + EC_construction

其中：
- EC = 建築蘊含碳排放（kgCO2e）
- Mi = 材料i用量（kg 或 m³）
- EF_i = 材料i碳足跡因子（kgCO2e/kg 或 m³）
- EC_transport = 運輸碳排放
- EC_construction = 施工碳排放
```

### 碳足跡因子參考
| 材料類別 | 碳足跡因子 |
|---------|-----------|
| 鋼筋 | 1.4 kgCO2e/kg |
| 混凝土 | 0.15 kgCO2e/kg |
| 鋁門窗 | 8.5 kgCO2e/kg |
| 玻璃 | 7.5 kgCO2e/kg |
| 鋼結構 | 2.5 kgCO2e/kg |
| 木材 | 0.5 kgCO2e/kg |

## Assessment Manual
- 低碳（低蘊含碳）建築評估手冊（2023年版/2025年版）

## Reduction Strategies

### 材料選擇
- 使用低碳建材（再生材料、在地材料）
- 選擇低碳預拌混凝土
- 使用鋼量優化設計

### 營造工法的
- 預鑄工法的（減少施工損耗）
- 乾式施工（減少濕作業）

### 設計策略
- 結構系統優化（減少材料用量）
- 標準化設計（批量生產）
- 簡化幾何（減少複雜立面）

## References
- 低碳（低蘊含碳）建築評估手冊
- 建築蘊含碳排標示申請審核認可及使用作業要點
- [台灣建築中心LEBR](https://lebr.tabc.org.tw/)

## MCP Tool Integration
- 查詢低碳建築法規：`taiwan-building-code_search_building_code(query: "低碳建築")`