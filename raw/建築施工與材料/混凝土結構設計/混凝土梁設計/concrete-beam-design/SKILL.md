---
name: concrete-beam-design
description: "This skill should be used when an architect or structural designer needs to verify PDF-backed concrete beam requirements such as minimum beam depth, T-beam effective flange width, minimum shear reinforcement, and the governing clause locations for beam detailing in Taiwan's concrete structure design code."
user-invocable: true
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
metadata:
  audience: architects
  region: taiwan
  class: C
  regulation: 建築物混凝土結構設計規範
---

# Concrete Beam Design

## Overview

Design requirements for reinforced concrete beams in Taiwan, limited to items directly verified against the uploaded PDF in this pass. This skill preserves the minimum beam-depth table, T-beam effective flange-width limits, and the verified clause references for beam reinforcement and detailing. For fundamental cover and splice concepts, see [concrete-general-requirements](../混凝土通用規定/concrete-general-requirements/).

---

## Section 1: Beam Geometry and Effective Depth

### 1.1 Key Dimensions

```
┌─────────────────────────── b ───────────────────────────┐
│  ┌───────────────────────────────────────────────────┐  │
│  │  ← C → ┌─────────┐ stirrup ← sbar → ┌─────────┐  │  │
│  │         │ main bar│                  │ main bar│  │  │
│  │         └────┬────┘                  └────┬────┘  │  │
│  │              │← d (effective depth) ────→ ┤       │  │ h (total depth)
│  │              ↓                            ↓       │  │
│  │  ─────────────────────────────────────────────── │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

- **h** = total beam depth (全深度)
- **d** = h − C − d_stirrup − d_main/2 (effective depth to main bar centroid)
- **b** = beam web width (梁寬)
- **C** = concrete cover (to stirrup face) — see concrete-general-requirements

### 1.2 Minimum Beam Depth (Non-Seismic, Simply Supported)

| Support Condition | Minimum h (normal weight concrete, fy=420) |
|---|---|
| Simply supported | L/16 |
| One end continuous | L/18.5 |
| Both ends continuous | L/21 |
| Cantilever | L/8 |

> These are deflection-control minimums. Seismic design may govern a larger section.

Source: 9.3.1.1, Table 9.3.1.1.

---

## Section 2: Reinforcement Limits and Detailing Clauses

The following beam clauses are relevant, but their full numerical expressions were not transcribed clause-by-clause in this pass:

| Topic | Governing Clause |
|---|---|
| Minimum flexural reinforcement | 9.6.1 |
| Minimum shear reinforcement | 9.6.3 |
| Beam detailing and bar termination | 9.7 |
| Development length and splices | 25.4, 25.5 |

If a numeric beam check depends on one of these clauses, the AI should resolve it from the PDF before issuing a pass/fail result.

---

## Section 3: Beam Detailing Notes

Beam bar spacing, bundling, and related detailing must be checked against Chapter 25.2 and Chapter 9.7. This skill does not preserve unverified spacing formulas or example widths.

---

## Section 4: Shear Reinforcement (Stirrups)

### 4.1 Stirrup Spacing

Beam stirrup spacing and seismic hinge-zone detailing must be checked directly from Chapter 9.7 and Chapter 18 when applicable. This skill intentionally avoids restating unverified spacing limits.

### 4.2 Minimum Shear Reinforcement

$$A_{v,min} = \max\left(\frac{0.062\sqrt{f'_c}}{f_{yt}} b_w s,\ \frac{0.35}{f_{yt}} b_w s\right)$$

This formula is taken from the PDF-backed beam clause for minimum shear reinforcement. Member-specific exceptions and exemptions must still be checked directly against the chapter text.

Source: 9.6.3.4, Table 9.6.3.4.

---

## Section 5: T-Beam Effective Flange Width

When a beam is cast monolithically with a slab, it acts as a T-beam in positive moment regions. Effective flange width (bf) is the beam web width plus the effective overhang from the slab.

| Flange Side Condition | Effective Overhang Limit |
|---|---|
| Flange on both sides | min(8h, sw/2, ln/8) |
| Flange on one side | min(6h, sw/2, ln/12) |

Where h is slab thickness, sw is adjacent web clear spacing, and ln is clear span.

Source: 6.3.2.1, Table 6.3.2.1.

---

## Section 6: AI Design Check Table — Beam

| Check | Condition | AI Action |
|---|---|---|
| Min flexural steel | Numeric check needed under 9.6.1 | WARNING: Resolve clause 9.6.1 from the PDF before checking. |
| Stirrup spacing | Numeric spacing check needed under 9.7 or Chapter 18 | WARNING: Resolve the applicable clause from the PDF before checking. |
| Clear spacing | Spacing check required under Chapter 25.2 | WARNING: Resolve Chapter 25.2 before checking. |
| Effective depth | d not calculated from C + stirrup + d_main/2 | WARNING: Verify d calculation method. |
| Development at supports | Numeric ld-based support check needed | WARNING: Resolve Chapter 25.4 before checking. |
| Bar termination | Beam bar cut-off or support extension not checked to 9.7 | WARNING: Resolve clause 9.7 from the PDF before checking. |

---

## Section 7: MCP Tool Examples

```python
# Search for beam flexural reinforcement limits
taiwan-building-code_search_building_code(query="梁 最小鋼筋量 ρmin 彎矩", limit=10)

# Search for stirrup spacing requirements
taiwan-building-code_search_building_code(query="梁 箍筋間距 剪力鋼筋", limit=10)

# Search for seismic beam requirements
taiwan-building-code_search_building_code(query="特殊抗彎矩構架 梁 耐震", limit=10)

# Official interpretations
taiwan-building-code_search_building_interpretations(query="梁 鋼筋 最小量 計算")
```

---

## Additional Resources

- General requirements (cover, development length, splice): [concrete-general-requirements](../混凝土通用規定/concrete-general-requirements/)
- Column design: [concrete-column-design](../混凝土柱設計/concrete-column-design/)
