---
name: architect-calculator
description: "This skill should be used when performing architect calculations including floor area analysis, structural estimation, MEP load calculation, and cost estimation."
user-invocable: true
---

# Architect Calculator Skill

## Overview
建築師專用計算工具箱，整合常用設計計算、法規檢查與成本估算功能。

## Capabilities
- 面積計算（建蔽率、容積率）
- 結構初估（樑柱尺寸、樓板厚度）
- 機電負載估算
- 採光照度計算
- 成本估算

## Parameters
```typescript
interface ArchitectCalculatorParams {
  // 專案條件
  projectType: 'Residential' | 'Commercial' | 'Industrial' | 'Public';
  siteArea: number; // m²
  floors: number;
  
  // 設計條件
  buildingCoverage: number; // 建蔽率 %
  floorAreaRatio: number; // 容積率
  floorHeight: number; // m
  
  // 結構參數
  structuralSystem: 'RC' | 'Steel' | 'SC';
  span: number; // m
  seismicZone: number; // TODO: 台灣地震區 1-4
  
  // 機電參數
  coolingLoad: number; // W/m²
  electricalLoad: number; // VA/m²
  
  // TODO: 台灣法規參數
  taiwanZoning: {
    zoneType: string; // TODO: 土地使用分區
    coverageLimit: number; // TODO: 各分區建蔽率上限
    farLimit: number; // TODO: 各分區容積率上限
  };
}
```

## Methods
- `calculateMaxBuildingArea(site, coverage)` - 最大建構面積
- `calculateMaxFARArea(site, far)` - 最大樓地板面積
- `estimateBeamSize(span, load)` - 樑尺寸估算
- `estimateColumnSize(stories, load)` - 柱尺寸估算
- `estimateSlabThickness(span)` - 樓板厚度估算
- `calculateCoolingLoad(area, usage)` - 冷負載計算
- `estimateCost(area, quality)` - TODO: 台灣建築成本估算

## Taiwan Adaptation Notes
- TODO: 台灣建蔽率 / 容積率法規
- TODO: 台灣土地使用分區規定
- TODO: 台灣建築成本基準
- TODO: 台灣結構設計基準值

## References
- Architecture Graphic Standards
- TODO: 建築法
- TODO: 都市計劃法
- TODO: 建築費用估價表
