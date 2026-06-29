---
name: taiwan-plumbing-design-codes
description: "This skill should be used when verifying indoor plumbing designs in Taiwan, including water tank capacities, pipe sizing, trap seals, drainage slopes, and ventilation pipes."
user-invocable: true
---

# Taiwan Building Plumbing System Design Codes

## Context & Purpose
This skill encodes the Taiwan "Building Water Supply and Drainage Equipment Design Technical Specifications" (建築物給水排水設備設計技術規範). Use it to validate MEP plumbing drawings.

## Design Parameters & Constraints

### 1. Water Tank Capacity (水箱/水塔容量)
- **Total Storage (地下水池 + 屋頂水塔)**: Should generally hold 1 to 2 days of the building's estimated daily water demand.
- **Ratio**: Typically, the roof tank holds 1/10 to 1/3 of the daily demand, and the underground reservoir holds the rest.

### 2. Water Supply Pipe Sizing (給水管徑計算)
- Sized based on Fixture Units (F.U.).
- **Velocity Limits**:
  - Main/Branch pipes: 0.9 m/s to 2.0 m/s. (Max 2.0 m/s to prevent water hammer and noise).

### 3. Traps & Water Seals (存水彎與水封)
- **Water Seal Depth (水封深度)**: Must be between **5 cm and 10 cm**.
- Every sanitary fixture must have a trap. Double trapping (雙重存水彎) is strictly prohibited.

### 4. Drainage Pipe Slopes (排水管洩水坡度)
- Pipe Diameter ≦ 65mm: Slope ≧ 1/50
- Pipe Diameter 75mm - 150mm: Slope ≧ 1/100
- Pipe Diameter ≧ 200mm: Slope ≧ 1/200

### 5. Vent Pipe Systems (通氣管路)
- **Stack Vent (伸頂通氣管)**: Must extend at least **15 cm** above the roof. If the roof is accessible, it must extend at least **2 meters** above the roof.
- Vent pipes must not connect to HVAC exhaust or chimney flues.

## Execution Logic for AI
When reviewing plumbing plans:
1. Verify drainage slopes match the pipe diameter (e.g., a 100mm pipe must have at least 1/100 slope).
2. Check water seal depth specifications (must be 5~10 cm).
3. Confirm roof vent pipe heights.
