# Taiwan Building Codes Skill

## Overview
台灣建築法規專業技能，整合建築技術規則、建築法、都市計劃法等台灣建築法規條文與實務應用。

## Capabilities
- 建築法規條文查詢
- 容積率 / 建蔽率計算
- 高度限制檢查
- 防火區劃規定
- 法規合規性檢查

## Parameters
```typescript
interface TaiwanBuildingCodesParams {
  // 基地條件
  siteLocation: string; // 縣市
  landUseZone: string; // 土地使用分區
  siteArea: number; // m²
  
  // 建築條件
  buildingType: string; // 用途類組
  floorCount: number;
  buildingHeight: number; // m
  
  // 法規參數
  coverageRate: number; // 建蔽率 %
  floorAreaRatio: number; // 容積率 %
  setback: number; // 退縮深度 m
  
  // 檢查項目
  checkItems: {
    coverage: boolean; // 建蔽率檢查
    far: boolean; // 容積率檢查
    height: boolean; // 高度檢查
    fireSafety: boolean; // 防火檢查
    accessibility: boolean; // 無障礙檢查
  };
}
```

## Methods
- `getCoverageLimit(zone, city)` - 取得建蔽率上限
- `getFARLimit(zone, city)` - 取得容積率上限
- `calculateMaxHeight(coverage, far)` - 計算法定最大高度
- `checkFloorAreaRatio(designArea, siteArea, farLimit)` - 容積率檢查
- `getFireCodeRequirements(buildingType)` - 取得消防法規要求
- `getAccessibilityRequirements(buildingType)` - 取得無障礙規定

##台灣法規結構

### 主要法規
- **建築法**: 建築管理基本法
- **建築技術規則**:
  - 設計施工編
  - 構造編
  - 設備編
- **都市計劃法**: 土地使用管制
- **區域計劃法**: 非都市土地管制

### 建築技術規則章節
```
第一章 總則
第二章 基地
第三章 設計原則
第四章 建築設備
第五章 構造
第六章 防火
第七章 衛生
第八章 構造要項
第九章 容積設計
```

### 关键條文

#### 第 161 條（容積率定義）
```
容積率 = 總樓地板面積 / 基地面積
基地面積包括法定騎樓面積
```

#### 第 268 條（建築高度限制）
```
H ≦ (法定最大容積率 / 法定最大建蔽率) × 3.6 × 2
```

#### 第 164-1 條（挑空設計）
```
住宅挑空位置、面積、高度限制:
- 每戶限 1 處
- 面積≧15 m²
- 合計≦總容積 1/10
- 高度≦6m
```

## 實務應用說明

### 設計流程
1. 確認基地使用分區
2. 查詢建蔽率 / 容積率
3. 計算最大可建面積
4. 檢查高度限制
5. 確認其他法規要求

### 注意事項
- 各地直轄市有自治條例
- 容積獎勵需另行申請
- 歷史建築 / 景觀區額有限制

## 參考資源
- 建築技術規則建築設計施工編
- 建築技術規則建築構造編
- 建築技術規則設備編
- 建築法
- 內政部建築技術規則查詢系統
