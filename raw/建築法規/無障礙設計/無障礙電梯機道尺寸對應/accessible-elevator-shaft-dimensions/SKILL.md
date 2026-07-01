---
name: accessible-elevator-shaft-dimensions
description: "Use when determining the minimum elevator shaft (hoistway) dimensions required for accessibility compliance in Taiwan. Covers Taiwan Accessible Facilities Design Specification §406.1: general buildings (door clear width ≥ 90 cm, car depth ≥ 135 cm) and the H-2 residential proviso (door clear width ≥ 80 cm, car depth ≥ 125 cm). Provides pre-verified shaft dimension lookup tables for Mitsubishi, Yung Ta, and Chung Yu elevators (P8–P13), eliminating the need to cross-reference manufacturer spec sheets during floor plan layout."
user-invocable: true
---

# Accessible Elevator Shaft Dimensions (無障礙電梯機道尺寸對應)

## Overview

Taiwan's accessibility code specifies **car interior dimensions**; building plans must show **elevator shaft (hoistway) clear dimensions**. The mapping between the two depends on the manufacturer, capacity, and door type.

Invoke this skill when:
- Laying out elevator cores on a floor plan and need to know how much shaft space to reserve
- Checking whether a selected elevator model meets §406.1 accessibility requirements
- Preparing building permit drawings involving elevator shafts

---

## Regulatory Basis

Both thresholds derive from **§406.1 of the Taiwan Accessible Facilities Design Specification** (建築物無障礙設施設計規範). The H-2 residential relaxation is a proviso clause within the same article.

| Building Type | Door Clear Width | Car Depth |
|---|---|---|
| General buildings | ≥ 90 cm | ≥ 135 cm |
| H-2 Residential / Apartment (proviso) | ≥ 80 cm | ≥ 125 cm |

**Statutory text (§406.1, excerpt, translated):**
> Car dimensions: elevator door clear width shall not be less than 90 cm; car depth shall not be less than 135 cm (handrail space excluded). *However, for buildings of use class H-2 (residential/apartment), the door clear width shall not be less than 80 cm and the car depth shall not be less than 125 cm (handrail space excluded); voice systems may add a switch.*

---

## Core Principle: Code Measures the Car; Plans Show the Shaft

The regulatory threshold applies to **car interior dimensions** (door clear width, car depth). The dimensions drawn on building plans are the **elevator shaft (hoistway) clear dimensions (width × depth)**.

Shaft dimensions vary by manufacturer, capacity, and door type. Direct substitution of code values into the plan is incorrect.

> **The tables below have completed three-layer verification: regulatory threshold → manufacturer car-spec confirmation → corresponding shaft dimension** (data date: 2023-03-29).

---

## Shaft Dimension Table — General Buildings (Door ≥ 90 cm, Car Depth ≥ 135 cm)

| Brand | Type | Capacity | Shaft W × D (cm) | Door Type |
|-------|------|----------|-----------------|-----------|
| Mitsubishi (三菱) | Machine-room-less | P8  | **170 × 180** | 2S Side-opening bi-fold |
| Mitsubishi (三菱) | Machine-room-less | P8  | 205 × 180 | CO Centre-opening |
| Mitsubishi (三菱) | Machine-room-less | P10 | 180 × 190 | 2S Side-opening bi-fold |
| Mitsubishi (三菱) | Machine-room-less | P10 | 205 × 185 | CO Centre-opening |
| Mitsubishi (三菱) | Machine-room-less | P12 | 200 × 185 | 2S Side-opening bi-fold |
| Mitsubishi (三菱) | Machine-room-less | P12 | 215 × 180 | CO Centre-opening |
| Mitsubishi (三菱) | Machine-room | P13 | 220 × 205 | — |
| Yung Ta (永大) | Machine-room | P13 | 215 × 195 | — |
| Yung Ta (永大) | Machine-room-less | P13 | 215 × 182 | — |
| Chung Yu (崇友) | Machine-room | P13 | 210 × 205 | — |
| Chung Yu (崇友) | Machine-room-less | P13 | 225 × 200 | — |

> **Smallest shaft**: Mitsubishi machine-room-less P8 side-opening bi-fold — **170 × 180 cm**

---

## Shaft Dimension Table — H-2 Residential / Apartment (Door ≥ 80 cm, Car Depth ≥ 125 cm)

All P8 configurations from all three brands are compliant. The table lists the minimum shaft size per brand:

| Brand | Type | Capacity | Shaft W × D (cm) |
|-------|------|----------|-----------------|
| Mitsubishi (三菱) | Machine-room | P8 | 185 × 170 |
| Mitsubishi (三菱) | Machine-room-less | P8 | **170 × 180** (2S) |
| Yung Ta (永大) | Machine-room | P8 | 190 × 163 |
| Yung Ta (永大) | Machine-room-less | P8 | 185 × 172 |
| Chung Yu (崇友) | Machine-room | P8 | **180 × 170** |
| Chung Yu (崇友) | Machine-room-less | P8 | 205 × 165 |

> **Smallest shaft**: Mitsubishi machine-room-less P8 2S (170 × 180) or Chung Yu machine-room P8 (180 × 170) — similar footprint, different orientation; select based on floor plan.

---

## Notes

- Mitsubishi machine-room-less P11 and P13 are not available in Taiwan
- OH (overhead clearance) and PIT (pit depth) vary by speed rating — refer to manufacturer spec sheets
- Machine-room types require additional machine room with minimum clear height: 220 cm (Mitsubishi, Chung Yu) or 200 cm (Yung Ta at 60 m/min)

## Design Checks

- [ ] Confirm building use type (general or H-2 residential) to select the correct table
- [ ] Verify shaft dimensions are reserved on the floor plan for the selected brand and capacity
- [ ] Confirm structural beams and columns do not intrude into the shaft clear dimensions
- [ ] For machine-room-less type: verify OH and PIT depths meet manufacturer requirements

## Data Currency

- Manufacturers: Mitsubishi Electric Taiwan, Yung Ta Elevator, Chung Yu Elevator
- Data date: 2023-03-29
- **Manufacturer specifications may be updated. Verify against the latest spec sheet before permit submission.**

## References

- Taiwan Accessible Facilities Design Specification §406 (Elevating Equipment) — Ministry of the Interior regulation system: https://glrs.moi.gov.tw/
- Taiwan Building Technical Regulations — Design and Construction Chapter §55 (Elevator Equipment)
