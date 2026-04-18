# Daylighting Design Skill

## Overview
專業採光設計與分析技能，優化自然光利用率，提升建築能源效率與室內光環境品質。

## Capabilities
- 採光模擬與分析
- 窗戶配置優化
- 遮陽設計
- 眩光評估
- 能源效益分析

## Parameters
```typescript
interface DaylightingParams {
  // 基地條件
  location: string; // TODO: 台灣座標與氣候數據
  orientation: number; // 基地方位
  
  // 幾何條件
  roomGeometry: Room3D;
  windowOpenings: Window[];
  
  // 材料參數
  glazingProperties: {
    Tvis: number; // 可見光穿透率
    SHGC: number; // 太陽得熱係數
  };
  
  // 分析條件
  analysisType: 'DA' | 'UDI' | 'sDA' | 'ASE';
  simulationDate: string; // TODO: 台灣典型氣象日
  
  // 目標值
  target Lux: number; // TODO: 台灣採光標準
  glareLimit: number;
}
```

## Methods
- `calculateDaylightFactor(geometry)` - 採光係數計算
- `simulateDaylight(skyModel)` - 全年採光模擬
- `analyzeGlare(viewpoint)` - 眩光分析
- `optimizeShading(orientation)` - 遮陽優化
- `checkCodeCompliance(room)` - TODO: 台灣採光法規檢查

## Taiwan Adaptation Notes
- TODO: 整合建築技術規則採光規定
- TODO: 台灣典型氣象年數據 (TMY)
- TODO: 台灣採光標準與照明設計规范
- TODO: 台灣氣候的採光策略（高溫高濕、強日照）

## References
- LEED Daylight Credits
- WELL Building Standard
- TODO: 建築技術規則 Chapter 9 (採光)
- TODO: CNS 照度標準
