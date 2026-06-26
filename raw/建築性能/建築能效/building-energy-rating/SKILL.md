---
name: building-energy-rating
description: "This skill should be used when applying for Taiwan Building Energy Efficiency Label (建築能效標示) or calculating building energy performance."
user-invocable: true
---

# Building Energy Rating (BEE)

## Overview
建築能效標示（Building Energy Efficiency, BEE）是內政部建築研究所於2022年實施的建築能效評估制度，主要評估建築物使用階段之能源使用效率，為達成2050年淨零建築願景的重要政策工具。

## Applicable Scenarios
- 申請建築能效標示（已取得使用執照之建築物）
- 申請候選建築能效證書（取得建造執照之建築物）
- 公有建築能效評估（法規要求）
- 建築能效診斷與改善

## Assessment Scope (3大項目)

| 評估項目 | 內容 | 權重 |
|---------|------|------|
| 建築外殼節能效率 | 外牆、窗戶、屋頂帷幕 | 30% |
| 空調系統節能效率 | 冷氣主機、管道、保溫 | 40% |
| 室內照明系統節能效率 | 照明設備、照明控制 | 30% |

## Rating Levels (7級)

| 能效等級 | 能效表現 | 近似節能效果 |
|---------|---------|-------------|
| 第1級 | 最優 | 較基準節能50%以上 |
| 第2級 | 優 | 較基準節能35-50% |
| 第3級 | 良 | 較基準節能20-35% |
| 第4級 | 中 | 較基準節能5-20% |
| 第5級 | 普通 | 基準±5% |
| 第6級 | 較差 | 較基準耗能5-20% |
| 第7級 | 最差 | 較基準耗能20%以上 |

### Special Labels
- **第1+級（近零碳建築）**：第1級且能效評分尺度前50%
- **0級（淨零建築）**：近零碳建築+再生能源碳中和

## Key Formulas

### 建築能效指標 (BEI)
```
BEI = 實際用電量密度 / 標準用電量密度

標準用電量密度（kWh/m².year）：
- 住宅：65
- 辦公：120
- 學校：85
- 醫院：180
- 百貨：250
```

### 能效評分
```
能效分數 =（1 - BEI/標準值）× 100
```

## Application Requirements

### 公有建築時程（分階段實施）
| 實施日期 | 適用對象 | 能效要求 |
|---------|---------|---------|
| 2023/7/1 | 公辦、服務類（G-1, G-2）| ≧2級，2026起≧1級 |
| 2024/7/1 | 商業、集會類（A-1, B類, D類）| ≧2級 |
| 2025/7/1 | 衛生、福利、住宿類（F-1, H類）| ≧2級 |

### ，民營建築（鼓勵申請）

## References
- 建築能效評估手冊
- 綠建築標章及建築能效標示申請審核認可及使用作業要點
- [內政部建築研究所](https://www.abri.gov.tw/cp.aspx?n=804)

## MCP Tool Integration
- 查詢建築能效法規：`taiwan-building-code_search_building_code(query: "建築能效")`