---
name: building-sustainability
description: "This skill should be used when designing green building and sustainable architecture, integrating environmental assessment, energy efficiency, and resource circularity."
user-invocable: true
---

# Building Sustainability Skill

## Overview
專業綠建築與永續設計技能，整合環境評估、能源效率、資源循環等永續策略。

## Capabilities
- 綠建築評估（EEARD/LEED）
- 節能效益分析
- 碳排放估算
- 水資源管理
- 材料環境評估

## Parameters
```typescript
interface BuildingSustainabilityParams {
  // 評估體系
  assessmentSystem: 'EEARD' | 'LEED' | 'BREEAM' | 'WELL';
  
  // 能源
  energyConsumption: number; // kWh/m²/year
  renewableEnergy: number; // %
  carbonEmission: number; // kgCO2e/m²/year
  
  // 水資源
  waterConsumption: number; // Liter/capita/day
  recycledWater: number; // %
  rainwaterHarvest: number; // %
  
  // 材料
  localMaterials: number; // % (within 500km)
  recycledContent: number; // %
  certifiedWood: number; // % (FSC)
  
  // 環境
  greenRoof: boolean;
  biodiversity: number; // 綠化面積比
  heatIslandReduction: boolean;
  
  // TODO: 台灣相關參數
  taiwanGreenBuilding: {
    categories: string[]; // TODO: 台灣綠建築 7 大指標
    targetRating: string; // TODO: 銀級/金級/鑽石級
  };
}
```

## Methods
- `calculateEnergyScore(building)` - 能源績效計算
- `calculateWaterScore(consumption, recycled)` - 水資源績效計算
- `estimateCarbonEmission(construction, operation)` - 碳排放估算
- `assessGreenBuilding(building)` - TODO: 台灣綠建築評估
- `generateRecommendations(current, target)` - 改善建議

## Taiwan Adaptation Notes
- TODO: 台灣綠建築評估體系 (EEARD)
- TODO: 建築能效證書 (EEC)
- TODO: 淨零建築推動方案
- TODO: 再生利用材料認證

## References
- LEED v4.1
- WELL Building Standard
- TODO: 台灣綠建築協會 EEARD
- TODO: 內政部綠建築評估手法
