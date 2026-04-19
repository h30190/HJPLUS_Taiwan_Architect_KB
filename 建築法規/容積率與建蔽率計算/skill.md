---
name: taiwan-programming
description: "This skill should be used when calculating floor area ratio (FAR), building coverage, and容积奖励 in Taiwan building projects."
user-invocable: true
---

# Taiwan Programming Skill

## Overview
台灣容積計算專業技能，整合建築技術規則容積設計章節、容積獎勵規定、容積檢討等計算方法。

## Capabilities
- 容積率計算
- 建蔽率檢查
- 容積獎勵計算
- 挑空與夾層規定
- 容積檢討報告

## Parameters
```typescript
interface TaiwanProgrammingParams {
  // 基地條件
  city: string; // 縣市
  landUseZone: string; // 土地使用分區
  siteArea: number; // m²
  siteShape: string; // 基地形狀（正方形/長方形/不規則）
  frontage: number; // 臨路寬度 m
  
  // 法定條件
  statutoryCoverage: number; // 法定建蔽率 %
  statutoryFAR: number; // 法定容積率 %
  maxFloors: number; // 法定層數限制
  maxHeight: number; // 法定高度限制 m
  
  // 設計條件
  designFloors: number; // 設計層數
  designFootprint: number; // 設計投影面積 m²
  floorHeights: number[]; // 各層高度
  
  // 容積項目
  volumeItems: {
    mainBuilding: number; // 主體建築
    balcony: number; // 陽台
    voidFloor: number; // 挑空
    mezzanine: number; // 夾層
    parking: number; // 停車位
    equipmentRoom: number; // 設備間
  };
  
  // 獎勵項目
  incentives: {
    greenBuilding: boolean; // 綠建築
    publicSpace: boolean; // 開放空間
    heritage: boolean; // 文化資產
    urbanRenewal: boolean; // 都市更新
    seismicImprove: boolean; // 耐震升級
  };
}
```

## Methods
- `calculateTotalFAR(items)` - 計算總容積
- `checkCoverageLimit(footprint, siteArea)` - 建蔽率檢查
- `checkFARLimit(totalVolume, siteArea, farLimit)` - 容積率檢查
- `calculateIncentiveBonus(incentives)` - 容積獎勵計算
- `calculateMaxFloors(coverage, far)` - 最大可建層數
- `checkVoidFloorCompliance(voidFloor)` - 挑空規定檢查
- `generateFARReport(design)` - 容積檢討報告

## 台灣容積法規

### 基本定義（第 161 條）
```
容積率 = 總樓地板面積 / 基地面積

總樓地板面積 = 各層面積總和 - 不計容積部分
```

### 不計容積項目
```
法定停車位（第 162 條）
陽台≦6m²（第 167 條）
屋頂機械室（第 181 條）
避難層（第 300 條）
```

### 容積獎勵
```
綠建築：最高 5%
開放空間：最高 100%（限基地面積）
都市更新：最高 25-30%
耐震補強：最高 10-15%
```

### 挑空規定（第 164-1 條）
```
住宅挑空:
- 每戶限 1 處
- 面積≧15m²
- 高度≦6m
- 合計≦總容積 1/10
```

## 容積計算公式

### 基本容積
```
可用容積 = 基地面積 × 法定容積率
```

### 獎勵容積
```
獎勵容積 = 可用容積 × 獎勵百分比
總容積 = 可用容積 + 獎勵容積
```

### 最大層數
```
最大層數 = 總容積 / (基地面積 × 建蔽率)
```

## 參考資源
- 建築技術規則第九章容積設計
- 各都市計畫容積獎勵辦法
- 都市更新條例
- 建築技術規則容積計算解釋函
