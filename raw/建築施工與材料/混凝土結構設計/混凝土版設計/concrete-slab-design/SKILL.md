---
name: concrete-slab-design
description: "This skill should be used when an architect or structural designer needs to verify PDF-backed concrete slab requirements such as minimum slab thickness, minimum flexural reinforcement, and shrinkage/temperature reinforcement rules in Taiwan's concrete structure design code."
user-invocable: true
license: CC-BY-NC-SA-4.0
compatibility: claude-code,opencode,agent-skills
metadata:
  audience: architects
  region: taiwan
  class: C
  regulation: 建築物混凝土結構設計規範
---

# Concrete Slab Design

## Overview

Design requirements for reinforced concrete slabs in Taiwan, limited here to items directly verified against the uploaded PDF: minimum slab thickness, minimum flexural steel, and shrinkage/temperature reinforcement rules. Slab-step, opening, and splice details are preserved only as chapter references unless directly transcribed from the source. For cover and splice fundamentals, see [concrete-general-requirements](../混凝土通用規定/concrete-general-requirements/).

---

## Section 1: Code Navigation

| Topic | Governing Clause |
|---|---|
| One-way slab minimum thickness | 7.3.1.1 |
| One-way slab minimum flexural steel | 7.6.1.1 |
| One-way shrinkage and temperature steel | 7.6.4, 7.7.6 |
| Two-way slab minimum thickness | 8.3.1.1 |
| Slab cover | 20.5.1.3.1 |

Structural classification between one-way and two-way slab systems should follow the designer's analysis model and the applicable chapter, rather than an unverified shorthand rule.

---

## Section 2: Minimum Slab Thickness

### 2.1 One-Way Slab Minimum Thickness (Deflection Control)

For non-prestressed one-way slabs with fy = 420 MPa:

| Support Condition | Minimum h |
|---|---|
| Simply supported | L/20 |
| One end continuous | L/24 |
| Both ends continuous | L/28 |
| Cantilever | L/10 |

> Multiply by (0.4 + fy/700) for fy ≠ 420 MPa. L = clear span length.

Source: 7.3.1.1, Table 7.3.1.1, 7.3.1.1.1.

### 2.2 Two-Way Slab Minimum Thickness

For non-prestressed two-way slabs, the minimum thickness depends on panel position and column head condition.

| Condition | fy = 420 MPa |
|---|---|
| No column head, outer panel, no edge beam | ln/30 |
| No column head, outer panel, with edge beam | ln/33 |
| No column head, inner panel | ln/33 |
| With column head, outer panel | ln/36 |
| With column head, inner panel | ln/36 |

Minimum absolute thickness:
- No column head: 125 mm
- With column head: 100 mm

Source: 8.3.1.1, Table 8.3.1.1.

### 2.3 Practical Minimum for Fire Resistance

Fire-resistance thickness may be governed by 建築技術規則 rather than slab-structure clauses alone. This skill does not restate fire-thickness numbers not transcribed from the governing fire code.

---

## Section 3: Flexural Reinforcement

### 3.1 Minimum Flexural Reinforcement

For non-prestressed slabs, minimum flexural steel is:

$$A_{s,min} = 0.0018A_g$$

This is the same base ratio used for slab shrinkage and temperature reinforcement.

Source: 7.6.1.1.

### 3.2 Maximum Bar Spacing

Maximum bar spacing for slab flexural reinforcement:
- Critical sections: min(3h, 450 mm)
- Other sections: min(3h, 450 mm)

Where h = total slab thickness.

---

## Section 4: Temperature and Shrinkage Reinforcement (溫度收縮筋)

### 4.1 Purpose

Temperature and shrinkage reinforcement controls cracking due to:
- Concrete drying shrinkage (乾縮)
- Seasonal temperature changes
- Creep effects

It is placed **perpendicular to the flexural reinforcement** in one-way slabs, and in **both directions** in slabs with equal reinforcement.

> **Key concept**: Temperature/shrinkage steel is NOT structural — it does not increase load capacity. Its sole purpose is crack width control.

### 4.2 Minimum Temperature/Shrinkage Reinforcement Ratio

$$\rho_{t\&s} = \frac{A_s}{b \cdot h}$$ (gross slab area)

| Bar Type | Minimum ρt&s |
|---|---|
| Deformed bars and welded wire reinforcement | **0.0018** (0.18%) |
| Prestressed slab steel used for shrinkage/temperature control | See Chapter 24.4.3 |

Source: 7.6.4.1, 7.7.6.2.1.

### 4.3 Maximum Spacing for Temperature/Shrinkage Bars

Maximum spacing: **min(5h, 450 mm)**

---

## Section 5: Development, Splice, and Opening Checks

This audit pass did **not** verify any slab-specific high-low-slab rule, opening-reinforcement rule, or numeric splice-length rule directly from the PDF. Therefore, this skill intentionally does not preserve those items as technical requirements.

When a project needs those checks, the AI should:
- resolve the applicable slab clause from the PDF if one exists,
- otherwise fall back to the general rebar development and splice clauses in Chapters 25.4 and 25.5,
- and avoid inventing slab-step or opening details not explicitly supported by the source.

---

## Section 7: AI Design Check Table — Slab

| Check | Condition | AI Action |
|---|---|---|
| Min thickness (one-way) | h < L/20 (simply supported) | ERROR: Slab may not control deflection — verify thickness |
| Min thickness (two-way) | h below table 8.3.1.1 or 100/125mm minimum | ERROR: Two-way slab below minimum thickness |
| Temp/shrinkage ratio | ρt&s < 0.0018 | ERROR: Insufficient temperature/shrinkage reinforcement |
| Temp/shrinkage spacing | Bar spacing > min(5h, 450mm) | ERROR: Temperature/shrinkage bars too widely spaced |
| Flexural spacing | Bar spacing > min(3h, 450mm) at critical section | ERROR: Flexural bar spacing exceeds limit |
| Development / splice | Numeric ld or lap check required | WARNING: Resolve Chapter 25.4 and 25.5 from the PDF before checking. |
| Cover — interior slab | C < 20mm for slabs not exposed | ERROR: Insufficient cover for interior slab |

---

## Section 8: MCP Tool Examples

```python
# Search for slab minimum thickness
taiwan-building-code_search_building_code(query="版 最小厚度 撓度 one-way two-way", limit=10)

# Search for temperature/shrinkage reinforcement
taiwan-building-code_search_building_code(query="溫度收縮鋼筋比 版 最小量", limit=10)

# Search for slab opening requirements
taiwan-building-code_search_building_code(query="版 開口 開孔 補強 鋼筋", limit=10)

# Search for high-low slab (if referenced specifically in Taiwan code)
taiwan-building-code_search_building_code(query="高低版 搭接 版高差 段差", limit=10)

# Official interpretations
taiwan-building-code_search_building_interpretations(query="版 高低差 搭接 斜筋補強")
```

---

## Additional Resources

- General requirements (cover, development length, lap splice fundamentals): [concrete-general-requirements](../混凝土通用規定/concrete-general-requirements/)
- Beam design (connected to slab as T-beam): [concrete-beam-design](../混凝土梁設計/concrete-beam-design/)
