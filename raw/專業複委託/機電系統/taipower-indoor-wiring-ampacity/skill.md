---
name: taipower-indoor-wiring-ampacity
description: "This skill should be used when calculating or verifying the allowable ampacity (current-carrying capacity) of indoor electrical wiring and conduit fill limits according to the Taipower Indoor Wiring Regulations (屋內線路裝置規則)."
user-invocable: true
---

# Taipower Indoor Wiring Ampacity & Conduit Fill

## Context & Purpose
This skill encodes the regulations for indoor electrical wiring (屋內線路裝置規則) specifically focusing on the allowable ampacity of wires inside conduits (PVC or Metal) and ambient temperature corrections.

## Parameters & Tables (Based on Article 16)

### 1. Baseline Conditions
- **Standard Ambient Temperature**: 35°C
- **Standard Conductor Insulation Temp**: 60°C (e.g., PVC), 75°C (e.g., XLPE/PE), or 90°C.
- **Wire Material**: Copper (銅)

### 2. Ampacity for PVC Wire in Conduit (60°C Insulation, 35°C Ambient) - Partial Table (Table 16-7)
| Wire Size (mm²) | Ampacity for ≤ 3 wires | Ampacity for 4 wires | Ampacity for 5-6 wires |
|-----------------|------------------------|----------------------|------------------------|
| 2.0 mm (Solid)  | 19 A                   | 16 A                 | 14 A                   |
| 3.5 mm²         | 19 A                   | 16 A                 | 14 A                   |
| 5.5 mm²         | 25 A                   | 23 A                 | 20 A                   |
| 8 mm²           | 33 A                   | 30 A                 | 25 A                   |
| 14 mm²          | 50 A                   | 40 A                 | 35 A                   |
| 22 mm²          | 60 A                   | 55 A                 | 50 A                   |
| 38 mm²          | 85 A                   | 75 A                 | 65 A                   |
| 50 mm²          | 100 A                  | 90 A                 | 80 A                   |
| 100 mm²         | 160 A                  | 150 A                | 125 A                  |

*(Note: Neutral wire, grounding wire, and control wires are generally not counted in the "number of wires" for ampacity derating, unless harmonics are present).*

### 3. Voltage Drop (Article 9)
- **Feeder + Branch Circuit**: Total voltage drop must not exceed **5%** of the nominal voltage.
- **Feeder only or Branch only**: Voltage drop must not exceed **3%**.

## Execution Logic for AI
When reviewing a single-line diagram (單線圖) or wiring schedule:
1. Identify the wire size (e.g., 8 mm²) and the number of current-carrying conductors in the conduit.
2. Cross-reference with the ampacity table to find the maximum allowed current.
3. Compare the allowed current with the specified breaker size (AT/AF). The wire's ampacity must be ≧ the breaker's trip setting (AT), with exceptions for motor loads.
4. Verify voltage drop calculations do not exceed 3% for branches or 5% total.
