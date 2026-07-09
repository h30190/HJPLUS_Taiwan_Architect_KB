# 美國 ASHRAE 空調系統與設備手冊

## 概述

依據 **ASHRAE Handbook—HVAC Systems and Equipment（空調系統與設備手冊）** 之專業空調工程知識。

適用於：

- 空調系統選型
- 中央廠房設計
- 空氣分配設計
- 末端裝置選用
- 控制與自動化
- 工程教育

---

# 能力項目

## 空調處理系統

- 全空氣系統
- 空氣—水系統
- 全水系統
- 單元式系統
- 變風量（VAV）系統

## 空氣處理設備

- 空調箱（AHU）
- 風機與風機選用
- 冷卻與加熱盤管
- 加濕器
- 空氣過濾器與過濾

## 末端裝置

- VAV 末端箱
- 風機盤管
- 誘導型末端裝置
- 輻射板
- 對流器與踢腳型散熱器

## 中央廠房設備

- 冰水機（離心式、螺旋式、渦卷式、吸收式）
- 鍋爐
- 冷卻水塔
- 熱交換器
- 蓄熱系統

## 熱泵與單元式設備

- 氣冷式熱泵
- 水冷式熱泵
- 地源熱泵
- 單元式包裝設備
- VRF 變頻多聯式系統

## 分配系統

- 風管系統設計
- 配管系統設計
- 泵浦與抽水系統
- 水處理
- 蒸汽系統

## 控制與自動化

- 建築自動化系統（BAS）
- 直接數位控制（DDC）
- 操作程序（Sequence of Operations）
- 感測器與驅動器
- 系統整合

## 馬達與驅動裝置

- 馬達類型與效率
- 變頻驅動器（VFD）
- 馬達選用準則

## 系統選型與設計

- 系統選型準則
- 生命週期成本分析
- 備援與可靠度
- 噪音與振動控制

---

# 參數

- 系統型式
- 建築負荷曲線
- 設備容量
- 氣流量
- 水流量
- 靜壓
- 揚程
- 部分負荷比
- 控制策略
- 備援等級

---

# 方法

- selectSystemType()（選擇系統型式）
- calculateFanPerformance()（計算風機性能）
- calculatePumpPerformance()（計算泵浦性能）
- calculateChillerCapacity()（計算冰水機容量）
- calculateBoilerCapacity()（計算鍋爐容量）
- calculateCoolingTowerPerformance()（計算冷卻水塔性能）
- sizeDuctSystem()（風管系統尺寸計算）
- sizePipeSystem()（配管系統尺寸計算）
- calculateCoilPerformance()（計算盤管性能）
- evaluateControlSequence()（評估控制程序）
- calculateLifeCycleCost()（計算生命週期成本）
- selectMotorAndDrive()（選用馬達與驅動裝置）

---

# 工作流程

1. 依據負荷計算結果確定系統需求
2. 選擇空氣分配系統型式
3. 選擇中央廠房設備型式
4. 決定空調處理設備尺寸
5. 決定末端裝置尺寸
6. 設計風管與配管分配系統
7. 選用泵浦、風機與馬達
8. 擬定控制操作程序
9. 評估生命週期成本與備援需求
10. 完成設備表與系統文件

---

# 台灣在地化調整

- 台灣建築法規
- EEWH（綠建築評估系統）
- CNS 國家標準
- 台灣節能法規
- 台灣設備能效標示

---

# 參考資料

- ASHRAE Handbook—HVAC Systems and Equipment
- ASHRAE Standard 90.1
- ASHRAE Standard 62.1
- ASHRAE Standard 15
- AHRI 標準
