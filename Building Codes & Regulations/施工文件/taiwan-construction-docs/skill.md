# Taiwan Construction Docs Skill

## Overview
台灣建築施工文件專業技能，整合施工圖說、預算書、規格書等施工階段文件編製要求與規範。

## Capabilities
- 施工圖說審查
- 預算書編製基準
- 施工規範查詢
- 材料設備規格
- 工程契約要項

## Parameters
```typescript
interface TaiwanConstructionDocsParams {
  // 專案條件
  projectName: string;
  projectType: 'Residential' | 'Commercial' | 'Industrial' | 'Public';
  scale: 'S' | 'M' | 'L'; // 工程規模
  
  // 文件類別
  docType: {
    drawings: boolean; // 施工圖說
    specs: boolean; // 施工規範
    budget: boolean; // 預算書
    schedule: boolean; // 時程表
  };
  
  // 設計階段
  designPhase: 'Basic' | 'Detailed' | 'Construction';
  
  // TODO: 台灣施工文件要求
  taiwanRequirements: {
    drawingsStandard: string; // TODO: 中華民國施工圖表標準
    budgetStandard: string; // TODO: 台灣工程預算標準
    contractType: string; // TODO: 中華民國工程契約範本
  };
}
```

## Methods
- `getDrawingChecklist(category)` - 取得圖說檢查表
- `calculateBudgetItems(items)` - 預算項目計算
- `getSpecificationTemplate(trade)` - 施工規範範本
- `generateSchedule(phases)` - TODO: 施工時程生成
- `checkDocCompliance(docs, standards)` - 文件合規性檢查
- `getMaterialSpecs(material)` - 材料規格查詢

## 台灣施工文件體系

### 圖說文件
- **建築圖**
  - 平面圖
  - 立面圖
  - 剖面圖
  - 細部圖

- **結構圖**
  - 基礎圖
  - 構件配筋圖
  
- **機電圖**
  - 給排水圖
  - 電氣圖
  - 空調圖

### 規範文件
- **施工綱要規範**（CSI 格式）
- **材料設備規範**
- **驗收標準**

### 預算文件
- **工程量表**（Bill of Quantities）
- **分析估價單**
- **材料價格表**

## 施工圖編製標準

### 圖面內容
```
基本項目:
- 圖名與圖號
- 尺寸標註
- 材料說明
- 節點詳圖
- 備註說明
```

### 圖面比例
```
平面圖：1/50, 1/100
立面圖：1/50, 1/100
剖面圖：1/50, 1/100
詳圖：1/20, 1/10
```

### 標註要項
```
尺寸單位：mm
標髙單位：m
角度單位：°
面積單位：m²
```

## 施工規範結構

### CSI 18 章分類
```
00 招標文件
01 施工管理
02 existing 拆除
03 混凝土
04 木材
05 金屬
06 木作
07 隔熱防水
08 門窗
09 飾面塗料
10 設備
11 識別
12 活動設備
13 特殊施工
14 清潔
15 機電
16 電氣
20 專用項目
```

### 規範格式
```
第 1 部分 一般規定
- 範圍
- 引用標準
- 品質控制

第 2 部分 產品
- 材料
- 設備
- 製造廠

第 3 部分 施工
- 安裝
- 施工程序
- 驗收
```

## 台灣預算基準

### 工程量計算
```
混凝土體積：m³
鋼筋重量：kg
模板接觸面：m²
粉刷面積：m²
油漆面積：m²
```

### 單價組成
```
材料費：材料原價 + 運費
人工費：工資 + 雜費
機械費：租金 + 操作費
管理費：5-10%
利潤：5-15%
稅金：5%
```

### 風險考量
```
價格波動：預留調整機制
工程變更：保留款
天候因素：時程緩衝
```

## 參考資源
- 中華民國施工圖說基準
- 建築工程估價表
- 公共工程招標範本
- 營建工程規範手冊
