---
name: acoustic-design
description: "This skill should be used when designing architectural acoustics, including room acoustics, noise control, and sound insulation."
user-invocable: true
---

# Acoustic Design Skill

## Overview
專業建築聲學設計技能，涵蓋室內音質、噪音控制、隔音設計等。

## Capabilities
- 室內混響時間計算
- 隔音性能評估（STC/IIC）
- 噪音模擬與控制
- 音質優化建議
- 法規符合性檢查

## Parameters
```typescript
interface AcousticDesignParams {
  // 空間條件
  roomVolume: number; // m³
  surfaceAreas: Surface[];
  
  // 聲學參數
  targetReverberation: number; // 秒
  frequencyRange: number[]; // Hz
  
  // 噪音來源
  noiseSources: {
    external: NoiseSource[]; // 交通、飛機
    internal: NoiseSource[]; // 設備、人員
  };
  
  // 隔音要求
  stcRequirement: number; // Sound Transmission Class
  iicRequirement: number; // Impact Insulation Class
  
  // TODO: 台灣噪音標準
  taiwanNoiseLimits: {
    residential: number; // TODO: 住宅噪音標準
    commercial: number; // TODO: 商業噪音標準
  };
}
```

## Methods
- `calculateReverberationTime(room)` - 混響時間計算 (Sabine)
- `calculateSTC(wallAssembly)` - 隔音等級計算
- `calculateIIC(floorAssembly)` - 衝擊音絕緣計算
- `simulateNoiseMap/sources)` - 噪音分佈模擬
- `optimizeAcoustics(program)` - 聲學優化建議
- `checkCodeCompliance(location)` - TODO: 台灣噪音法規檢查

## Taiwan Adaptation Notes
- TODO: 整合噪音管制法
- TODO: 台灣各區域噪音標準
- TODO: 建築技術規則隔音規定
- TODO: 交通噪音特別規定（捷運、飛機）

## References
- ISO 16283 (Field Measurement)
- ASTM E90 (Lab Measurement)
- TODO: 噪音管制法
- TODO: 建築技術規則設備編
