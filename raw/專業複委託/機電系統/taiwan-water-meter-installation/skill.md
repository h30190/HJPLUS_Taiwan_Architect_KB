---
name: taiwan-water-meter-installation
description: "This skill should be used when planning, designing, or reviewing the water meter installation locations, types, and configurations for buildings in Taiwan according to the Taiwan Water Corporation guidelines."
user-invocable: true
---

# Taiwan Water Meter Installation Principles

## Context & Purpose
This skill defines the operational parameters and constraints for installing water meters (總表, 分表, 獨立表) in Taiwan, as regulated by the Taiwan Water Corporation (台灣自來水股份有限公司用戶表位設置原則).

## Parameters & Classification
| Meter Type | Size (Diameter) | Description |
|------------|-----------------|-------------|
| Large Meter (大表) | ≧ 50 mm | - |
| Small Meter (小表) | ≦ 40 mm | - |
| Master Meter (總表) | - | Meter followed by other meters for individual billing. |
| Sub Meter (分表) | - | Meter following a master meter. |
| Independent Meter (獨立表) | - | Directly supplies user, no subsequent billing meters. |
| Smart Meter (智慧表) | - | Part of AMR system, transmits signals to TWC. |

## Location Rules
- **General Safety**: Must be in safe spaces allowing easy meter reading, replacement, maintenance, and good drainage.
- **Prohibited Areas**: Inside toilets, bathrooms, underground basements (for master/independent meters), or back of the house. Must not obstruct traffic/pedestrians.
- **Master/Independent Meters**:
  - Should be placed within the property line, adjacent to the road building line.
  - Allowed on open spaces behind arcades, flower beds, green areas, or beside stairways.
  - Prohibited in driveways or parking spaces.
- **Sub Meters (Apartments/Condos)**:
  - Default location is the **roof** (must have a fixed stairway and railing).
  - If roof access is impossible, meters can be grouped in a dedicated **Meter Room** on specific floors (NOT in the basement). The room needs a 4-inch floor drain and a 35cm threshold.

## Clearances & Dimensions
- **Vertical Clearance**: Meter bottom must be ≧ 2 cm above the ground.
- **Recessed Spaces (崁入式表位)**:
  - Axis to roof/gas meter clearance: ≧ 30 cm
  - Axis to wall clearance: ≧ 10 cm
  - For ≦25mm meters: Space ≧ 50(W) x 55(H) x 20(D) cm
  - For 40mm meters: Space ≧ 70(W) x 65(H) x 22(D) cm

## Execution Logic for AI
When checking MEP plans:
1. Verify meter location against prohibited areas (basement, toilets, driveways).
2. Check if sub-meters are placed on the roof. If not, verify the existence of a valid meter room.
3. Validate clear dimensions for recessed meters.
