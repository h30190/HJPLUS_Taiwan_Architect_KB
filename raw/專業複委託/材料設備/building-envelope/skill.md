---
name: building-envelope
description: "This skill should be used when designing and analyzing building envelope systems, including wall assemblies, roofs, glazing, thermal performance, and waterproofing."
user-invocable: true
---

# Building Envelope Skill

## Overview
專業建築皮殼（Building Envelope）設計與分析技能，專注於外牆、屋頂、窗戶等建築外殼系統的熱性能、防水、氣密性設計。

## Capabilities
- 建築外殼熱工性能計算
- 傳熱係數（U-value）分析
- 熱橋效應評估
- 防水與氣密系統設計
- 窗牆比（WWR）優化

## Parameters
```typescript
interface BuildingEnvelopeParams {
  // 牆體參數
  wallAssemblies: WallAssembly[];
  
  // 屋頂參數  
  roofAssemblies: RoofAssembly[];
  
  // 窗戶參數
  glazingSystems: GlazingSystem[];
  
  // 氣候條件 - TODO: 需要增加台灣七代表站氣候數據
  climateZone: string;
  
  // 熱性能目標
  targetUValues: TargetUValue;
}
```

## Methods
- `calculateUValue(assembly)` - 計算構件傳熱係數
- `analyzeThermalBridge(detail)` - 熱橋分析
- `checkCodeCompliance(assembly, location)` - TODO: 台灣建築能效法規檢核
- `optimizeEnvelope(climate, program)` - 外殼系統優化

## Taiwan Adaptation Notes
- TODO: 整合台灣建築能效標準（CNS 3815）
- TODO: 增加台灣氣候分區（7 個代表站）
- TODO: 整合台灣建築材料產品規格
- TODO: 颱風負壓與防水設計考量

## References
- ASHRAE 90.1
- CNS 3815 建築物能效標準
- TODO: 台灣住宅性能評估制度
