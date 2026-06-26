---
name: smoke-exhaust-review
description: "This skill should be used when evaluating smoke exhaust compliance for buildings in Taiwan, including windowless floor determination, smoke compartment partitioning, smoke exhaust window effective area calculations, and supplementary code checks per Taiwan Building Technical Regulations §100-102 and Fire Safety Equipment Standards §28."
user-invocable: true
---

# Smoke Exhaust Compliance Review

## Overview

This skill provides comprehensive smoke exhaust code compliance evaluation for buildings under Taiwan's dual regulatory framework. It should be invoked when:

- Determining whether a building requires smoke exhaust systems
- Calculating effective smoke exhaust window areas
- Evaluating windowless floor or windowless room classifications
- Reviewing smoke compartment partitioning requirements
- Checking supplementary requirements under §101 (exhaust volume, central control room)

---

## Section 1: Regulatory Framework

Taiwan smoke exhaust obligations are governed by two parallel regulatory systems. Both must be satisfied; the stricter requirement prevails.

| System | Source | Trigger Provisions | Design Provisions |
|--------|--------|--------------------|-------------------|
| **Building Act** | Building Technical Regulations (Design & Construction) | §100 | §101, §102 |
| **Fire Act** | Fire Safety Equipment Standards for Various Premises | §28 | §188, §189 |

---

## Section 2: Trigger Conditions

Three independent entry points trigger the smoke exhaust obligation. If **any one** is met, smoke exhaust systems are required.

### Entry A: Windowless Floor (Fire Safety §4 + §28③)

```typescript
interface WindowlessFloorCheck {
  floorArea: number;           // m² — gross floor area
  effectiveOpeningArea: number; // m² — sum of qualifying openings
  // Qualifying opening criteria:
  //   - inscribed circle diameter ≥ 50cm
  //   - sill height ≤ 120cm above floor
  //   - faces road or ≥ 1m wide passage
  //   - no grilles; glass thickness ≤ 6mm
  //   - floors ≤ 10F: at least 2 large openings (diameter ≥ 1m)
}
```

| Condition | Threshold | Reference |
|-----------|-----------|-----------|
| Windowless floor determination | effectiveOpeningArea < floorArea / 30 | Fire Safety §4 |
| Smoke exhaust required | floorArea ≥ 1,000 m² AND windowless | Fire Safety §28③ |

### Entry B: Designated Occupancy (Building Tech Reg §100① + Fire Safety §28①)

| Condition | Threshold | Reference |
|-----------|-----------|-----------|
| Building Tech Reg §100① | Occupancy types per §69 (Groups 1, 4), floor area > 500 m² | §100① |
| Fire Safety §28① | Designated premises per §12-1, area ≥ 500 m² | §28① |

### Entry C: Windowless Room (Building Tech Reg §1-35-3 + §100②)

| Condition | Threshold | Reference |
|-----------|-----------|-----------|
| Room floor area | > 50 m² | §1 Definition 35-3 |
| Ventilation area within 80cm below ceiling | < floor area × 2% | §1 Definition 35-3 |
| Smoke exhaust required | Both conditions met | §100② |

---

## Section 3: Smoke Compartment Partitioning

| Parameter | Value | Reference |
|-----------|-------|-----------|
| Maximum compartment area | 500 m² | §101 |
| Smoke barrier minimum depth | 50cm below ceiling | §101 |
| Smoke barrier material | Non-combustible | §101 |

---

## Section 4: Effective Smoke Exhaust Area Calculation

Per National Fire Agency Interpretation Letter No. 0920093655 (2003-09-01), Proposal 1:

```typescript
interface SmokeExhaustWindowCalc {
  ceilingHeight: number;        // m — ceiling height
  effectiveZoneTop: number;     // m — equals ceilingHeight
  effectiveZoneBottom: number;  // m — ceilingHeight - 0.8
  windows: WindowData[];
}

interface WindowData {
  sillHeight: number;           // m — window sill elevation
  headHeight: number;           // m — window head elevation
  width: number;                // m — window width
  openingCategory: OpeningCategory;
  openingAngleDeg?: number;     // degrees — required for 'rotary' category
}

type OpeningCategory =
  | 'rotary'    // pivot, awning, hopper, tilt-and-turn, louver — uses angle formula
  | 'sliding'   // sliding, hung, casement (bi-fold) — So = S
  | 'fixed';    // cannot open — So = 0
```

### Effective Opening Area Formula

Per Fire Safety Equipment Standards §189, §190 and Interpretation Letter:

**Category 1: Rotary windows** (pivot, awning, hopper, tilt-and-turn, louver):

| Opening Angle α | Effective Area So | Formula |
|-----------------|-------------------|---------|
| 90° ≥ α ≥ 45° | So = S | Full area (angle ≥ 45°) |
| 45° > α ≥ 0° | So = (α / 45°) × S | Proportional reduction |

**Category 2: Sliding/bi-fold windows** (sliding, hung, casement):
- So = S (opening area = effective area)

**Category 3: Fixed windows**:
- So = 0 (cannot open, no exhaust value)

### Calculation Steps

1. Define effective zone: `[ceilingHeight - 0.8, ceilingHeight]`
2. Per window:
   - Clamp head to ceiling: `effectiveHead = min(headHeight, ceilingHeight)`
   - Height in zone: `zoneHeight = effectiveHead - max(sillHeight, effectiveZoneBottom)`
   - Area in zone (S): `S = width × max(zoneHeight, 0)`
   - Effective area (So):
     - If `openingCategory === 'rotary'`: apply angle formula
     - If `openingCategory === 'sliding'`: `So = S`
     - If `openingCategory === 'fixed'`: `So = 0`
3. Sum all effective areas
4. **Compliance**: `Σ So ≥ compartmentArea × 0.02`

### Angle Formula Function

```typescript
function calcEffectiveArea(S: number, angleDeg: number): number {
  if (angleDeg >= 45) return S;
  if (angleDeg > 0) return (angleDeg / 45) * S;
  return 0;
}
```

### Additional Constraint

| Parameter | Threshold | Reference |
|-----------|-----------|-----------|
| Maximum horizontal distance from exhaust opening to farthest point of smoke compartment | ≤ 30m | §101 |

---

## Section 5: Supplementary Requirements (§101)

### 5-1: Mechanical Exhaust Volume

| Parameter | Minimum | Reference |
|-----------|---------|-----------|
| Exhaust fan capacity | 120 m³/min per exhaust port | §101 |

### 5-2: Central Control Room

| Trigger Condition | Threshold | Reference |
|-------------------|-----------|-----------|
| Building height | > 30m | §101 |
| Underground floor total area | > 1,000 m² | §101 |

When either condition is met, smoke exhaust controls must be located in a central control room (防災中心).

---

## Section 6: MCP Integration

### Taiwan Building Code Search

```typescript
// Query smoke exhaust regulations
taiwan-building-code_search_building_code(query: "排煙設備")
taiwan-building-code_search_building_code(query: "建技規 第一百條 排煙")
taiwan-building-code_search_building_code(query: "防煙區劃 防煙壁")

// Query windowless floor and room definitions
taiwan-building-code_search_building_code(query: "無開口樓層")
taiwan-building-code_search_building_code(query: "無窗居室 第三十五款")

// Query official interpretations
taiwan-building-code_search_building_interpretations(query: "排煙窗 有效面積")
taiwan-building-code_search_building_interpretations(query: "防煙區劃 面積計算")
```

---

## Section 7: References

- Building Technical Regulations (Design & Construction) §1, §69, §100-102
- Fire Safety Equipment Standards for Various Premises §4, §28, §188-190
- National Fire Agency Interpretation Letter No. 0920093655 (2003-09-01), Proposal 1: Effective opening area determination for smoke exhaust windows
