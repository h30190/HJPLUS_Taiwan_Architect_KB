# Taiwan Accessibility Skill

## Overview
台灣無障礙設計法規專業技能，整合身心障礙者權益保障法、無障礙設計規範、建築技術規則無障礙相關條文。

## Capabilities
- 無障礙設施設計要求查詢
- 無障礙路線分析
- 無障礙停車位計算
- 無障礙浴室配置
- 法規合規性檢查

## Parameters
```typescript
interface TaiwanAccessibilityParams {
  // 建築條件
  buildingType: string; // 公共/住宅/辦公
  floorArea: number; // m²
  floorCount: number;
  
  // 基地條件
  siteArea: number; // m²
  parkingSpaces: number; // 停車位數量
  entranceCount: number; // 入口數量
  
  // 無障礙設施
  accessibility: {
    entrance: boolean; // 無障礙入口
    route: boolean; // 無障礙通路
    elevator: boolean; // 無障礙電梯
    restroom: boolean; // 無障礙廁所
    parking: boolean; // 無障礙停車位
    bedroom: boolean; // 無障礙套房（飯店）
  };
  
  // 使用者類別
  users: {
    wheelchair: boolean; // 輪椅使用者
    visuallyImpaired: boolean; // 視障人士
    hearingImpaired: boolean; // 聽障人士
    elderly: boolean; // 高齡者
  };
}
```

## Methods
- `getAccessibilityRequirements(buildingType)` - 取得無障礙設施要求
- `calculateParkingSpaces(totalSpaces)` - 計算無障礙停車位數量
- `calculateRestroomCount(occupancy)` - 計算無障礙廁所數量
- `checkRouteCompliance(path)` - 無障礙通路檢查
- `getElevatorRequirements(floorCount)` - 無障礙電梯要求
- `checkCodeCompliance(building)` - 無障礙法規合規檢查

## 台灣無障礙法規

### 主要法規
- **身心障礙者權益保障法**
- **建築技術_rule_無障礙設計**
- **公共建築無障礙設施規範**

### 適用範圍
```
公共建築物（A/B/C/D/E 類建築）
社會住宅
集合住宅（10 户以上）
學校教育機構
醫療機構
商業設施
公共運輸設施
```

### 無障礙通路

#### 坡道
```
坡度：≦ 1/12
寬度：≧ 1.5m
平臺：每 1.5m 垂直高度設 1.5m 平臺
扶手：雙側設置，高度 0.7-0.9m
防滑：防滑條
```

#### 電梯
```
廂深度：≧ 1.4m
廂寬度：≧ 1.1m
按鈕高度：0.9-1.2m
點字標示：有
語音報站：有
鏡子：後壁斜鏡
```

### 無障礙廁所

#### 一般大小
```
最小尺寸：1.5m × 1.5m
轉動直徑：1.5m
門檻：無
門寬：≧ 0.9m
扶手：U 型扶手兩側
```

#### 家庭厕所
```
尺寸：2.0m × 2.0m
可容納照顧者
折疊扶手
緊急按鈕
```

### 無障礙停車位

#### 設置數量
```
10-50 车位：至少 1 個
51-100 车位：至少 2 個
101 车位以上：至少 3 個
```

#### 尺寸要求
```
停車位寬：3.5m
通道寬：1.5m
總寬度：5.0m
標誌：明顯標示
```

## 無障礙設計原則

### 通用設計 7 大原則
1. 公平使用
2. 使用弹性
3. 直觀簡單
4. 資訊可感知
5. 容許錯誤
6. 省力操作
7. 適當尺寸空間

### 視覺友善設計
- 高低色彩對比
- 點字與語音引導
- 警示地面鋪面
- 清晰標示系統

### 聽覺友善設計
- 視覺警報
- 閃光通知
- 手語視訊服務
- 輔助聽力系統

## 參考資源
- 身心障礙者權益保障法
- 建築技術規則無障礙設計編
- 通用設計建築法規
- 內政部無障礙環境規範
