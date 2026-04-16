# Structural Systems Skill

## Overview
專業建築結構系統設計與分析技能，涵蓋耐震設計、結構體系選擇、荷重計算等。

## Capabilities
- 結構體系規劃與比選
- 荷重計算（dead/live/wind/seismic）
- 耐震設計檢視
- 構件尺寸初估
- 基礎型式建議

## Parameters
```typescript
interface StructuralSystemsParams {
  // 基地條件
  siteConditions: SiteCondition;
  
  // 地震參數 - TODO: 需要整合台灣地震區分區
  seismicZone: string; // TODO: 台灣地震區分（1-4 級）
  soilType: string;    // TODO: 台灣地盤分類（E1-E5）
  
  // 風載參數 - TODO: 需要台灣基本風速圖
  basicWindSpeed: number; // TODO: 台灣各地基本風速
  
  // 建築條件
  buildingHeight: number;
  buildingArea: number;
  occupancyType: string;
  
  // 結構材枓
  structuralMaterial: 'RC' | 'SC' | 'Steel' | 'Timber' | 'Hybrid';
  
  // 設計規範
  designCodes: string[]; // TODO: 台灣混凝土/鋼結構設計規範
}
```

## Methods
- `calculateDeadLoad(elements)` - 計算靜荷重
- `calculateLiveLoad(occupancy)` - 計算活荷重
- `calculateSeismicForce(structure)` - TODO: 台灣耐震設計力計算
- `calculateWindLoad(building, location)` - TODO: 台灣風荷重計算
- `sizeBeam(span, load)` - 樑尺寸估算
- `sizeColumn(stories, load)` - 柱尺寸估算
- `checkSlenderness(column)` - 長細比檢查

## Taiwan Adaptation Notes
- TODO: 整合建築技術規則構造編第 2 章（抗震）
- TODO: 整合 NHA 耐震设计规范
- TODO: 台灣風壓地圖整合
- TODO: 地盤分類與地震係數表

## References
- AISC 360
- ACI 318
- TODO: 建築技術規則建築構造編
- TODO: 混凝土建築物構造規準
- TODO: 鋼構造物設計規準
