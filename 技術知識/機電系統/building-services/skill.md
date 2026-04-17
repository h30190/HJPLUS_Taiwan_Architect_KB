# Building Services Skill

## Overview
專業建築機電系統設計技能，涵蓋空調、給排水、電氣、弱電、消防等系統整合。

## Capabilities
- 空調系統負載計算
- 管線規劃與整合
- 設備空間配置
- 機電負載估算
- 系統整合協調

## Parameters
```typescript
interface BuildingServicesParams {
  // 建築條件
  buildingType: string;
  floorArea: number;
  roomSchedule: Room[];
  
  // 空調系統
  hvacSystem: 'VRF' | 'AHU' | 'FCU' | 'Chiller' | 'DistrictCooling';
  coolingLoad: number; // W
  heatingLoad: number; // W
  
  // 給排水
  plumbingFixtures: Fixture[];
  waterDemand: number; // Liter/day
  sewageSystem: string;
  
  // 電氣系統
  electricalLoad: number; // kVA
  powerDistribution: string;
  emergencyPower: boolean;
  
  // 弱電系統
  lowVoltageSystems: string[]; // 網路、監控、防火警報
  
  // 消防系統
  fireProtection: FireSystem[];
  
  // TODO: 台灣機電法規參數
  taiwanCodes: {
    fireCode: string; // TODO: 各類場所消防安全設備設置標準
    elecCode: string; // TODO: 用戶用電設備規程
    plumbingCode: string; // TODO: 建筑技術設備編
  };
}
```

## Methods
- `calculateCoolingLoad(room)` - 冷負載計算
- `calculateHeatingLoad(room)` - 熱負載計算
- `sizeDuct(flow, velocity)` - 風管尺寸計算
- `sizePipe(flow, pressure)` - 水管尺寸計算
- `calculatePanelLoad(circuits)` - 電盤負載計算
- `checkEquipmentSpace(requirements)` - TODO: 台灣機房空間法規檢查

## Taiwan Adaptation Notes
- TODO: 整合建築技術規則設備編
- TODO: 各類場所消防安全設備設置標準
- TODO: 用戶用電設備規程
- TODO: 省水標章與環保法規
- TODO: 台灣 VRF 空調系統設計慣例

## References
- ASHRAE Handbook
- NEC (National Electrical Code)
- TODO: 建築技術規則設備編
- TODO: 各類場所消防安全設備設置標準
- TODO: 省水器具規範
