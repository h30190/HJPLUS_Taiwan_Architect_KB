# Taiwan Fire Safety Skill

## Overview
台灣建築消防安全法規專業技能，整合各類場所消防安全設備設置標準、防火區劃、避難設施等規定。

## Capabilities
- 消防系統設計要求查詢
- 防火區劃規定檢查
- 避難設施配置分析
- 消防設備設置檢查
- 法規合規性評估

## Parameters
```typescript
interface TaiwanFireSafetyParams {
  // 建築條件
  buildingType: string; // 使用類組（A-E）
  floorCount: number;
  buildingHeight: number; // m
  floorArea: number; // m²
  
  // 樓層資訊
  underground: number; // 地下層數
  storiesAboveGround: number;
  occupancy: Occupancy[]; // 各樓層用途
  
  // 消防系統
  fireSystem: {
    sprinkler: boolean; // 火灑水系統
    fireHose: boolean; // 消防栓
    alarm: boolean; // 警報系統
    smokeControl: boolean; // 防排煙設備
    emergencyLight: boolean; // 緊急照明
  };
  
  // 避難設施
  evacuation: {
    stairCount: number; // 樓梯數量
    stairWidth: number; // 樓梯寬度
    evacuationRoute: string; // 避難路線
  };
}
```

## Methods
- `getFireSystemRequirements(building)` - 取得消防系統設置要求
- `calculateFireZone(area, usage)` - 防火區劃計算
- `checkStairwidth(evacuees)` - 樓梯寬度檢查
- `calculateSprinklerHeadCount(area)` - 灑水頭數量計算
- `checkFireCodeCompliance(building)` - 消防法規合規檢查
- `getEvacuationRequirements(building)` - 避難設施要求

## 台灣消防法規

### 主要法規
- **各類場所消防安全設備設置標準**
- **建築技術規則第 2 章（防火）**
- **消防法**

### 使用類組分類
```
A 類：社教、禮堂、觀覽
B 類：辦公
C 類：商肆、餐飲
D 類：住宿
E 類：廠房、倉庫
```

### 消防系統設置基準

#### 消防栓（室內）
```
樓地板面積 > 100 m²: 需設置
每一處需有 2 條以上水管到達
服務半徑: ≦30m
```

#### 火灑水系統
```
地下 1 層以下: 強制設置
高層建築 (31m 以上): 強制設置
樓地板面積 > 1,000 m²: 強制設置
特定場所: 依規定設置
```

#### 防火門
```
防火區劃開口: 需設防火門
樓梯間出入口: 需設防火門
防火時效：1-3 小時
```

## 防火區劃規定

### 面積限制
```
設置火灑水: ≦ 2,000 m²
未設置火灑水: ≦ 1,000 m²
地下室: ≦ 500 m²
```

### 防火牆
```
耐火時效: 2-4 小時
不得有開口
開口處需設防火門
```

## 避難設施標準

### 安全梯
```
3 層以上：需設安全梯
11 層以上：需設防火安全梯
31m 以上：需設耐煙緩衝間
```

### 樓梯寬度
```
最小寬度：1.1m
避難人數 > 50 人：≧ 1.2m
高層建築：≧ 1.5m
```

### 避難通道
```
最小寬度：1.2m
無障礙通道：≧ 1.5m
走廊長度限制：依場所類别
```

## 參考資源
- 各類場所消防安全設備設置標準
- 建築技術規則防火編
- 消防法
- 室內消防安全設備維護管理办法
