---
name: generator-room-fire-safety
description: "This skill should be used when reviewing the architectural and MEP designs of a generator room, specifically checking the fuel tank capacity, maintenance clearances, and ventilation requirements according to Taiwan fire safety interpretations."
user-invocable: true
---

# Generator Room Fire Safety & Fuel Tank Capacity

## Context & Purpose
This skill encodes the regulations from the Ministry of Interior Fire Agency (內政部消防署) interpretation letters regarding emergency generator rooms, focusing on fire compartments, maintenance clearances, exhaust routing, and fuel tank capacity requirements.

## Parameters & Thresholds

### 1. Clearances (維護與操作距離)
| Area | Minimum Clearance | Description |
|------|-------------------|-------------|
| Operation Side (前面操作部) | ≧ 1.0 m | Front side of the generator. |
| Maintenance Side (供檢修之面) | ≧ 0.6 m | Sides required for maintenance access. |

### 2. Fuel Tank Capacity (燃料槽容量)
- **Effective Capacity**: Calculated as **90%** of the internal volume (內容積).
- **Duration**: The fuel capacity must support continuous operation for **≧ 2 hours** at the rated load.
- **Exception**: This requirement does not apply if there is a main fuel tank (主油槽) supplying the daily/sub fuel tank.

### 3. Compartment & Ventilation (區劃與通風排氣)
- **Compartment**: Must be a dedicated space enclosed by fire-rated walls and floors (防火構造區劃專用空間).
- **Ventilation**: Intake and exhaust ducts must be dedicated. Ducts should generally not penetrate fire compartments; if they must, fire dampers or code-compliant protections are required.
- **Engine Exhaust (排氣管)**: Must be dedicated and discharge directly to the outdoors or connect to a chimney. It **cannot** connect to general exhaust ducts.
- **Power Auto-Switch**: Ventilation equipment and room lighting must automatically switch to generator power during an outage.

## Execution Logic for AI
When reviewing a generator room plan:
1. Verify the clearance in front (≧1m) and sides (≧0.6m).
2. Check the fuel tank specification: verify if `tank_volume * 0.9` provides enough fuel for 2 hours of runtime based on the engine's consumption rate.
3. Confirm the generator room is a fire compartment and exhaust pipes are routed outdoors separately.
