---
name: concrete-general-requirements
description: "This skill should be used when an architect needs to verify PDF-backed common concrete detailing rules such as concrete cover, reinforcement terminology, minimum spacing references, development-length clauses, and splice clauses in Taiwan's concrete structure design code."
user-invocable: true
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
metadata:
  audience: architects
  region: taiwan
  class: C
  regulation: 建築物混凝土結構設計規範
---

# Concrete General Requirements

## Overview

Foundational knowledge for reinforced concrete design in Taiwan, limited to content directly verified against the uploaded 112-code PDF. This skill focuses on reinforcement nomenclature, concrete cover, and where to look in the code for development length and splice requirements. This skill is the prerequisite for all component-specific concrete skills (beam, column, slab, wall).

---

## Section 1: Code Navigation

### 1.1 Where to Verify Shared Rules

| Topic | Governing Clause in PDF |
|---|---|
| Minimum bar spacing | Chapter 25.2 |
| Concrete cover | Chapter 20.5.1 |
| Development length | Chapter 25.4 |
| Rebar splices | Chapter 25.5 |
| Bundled bars | Chapter 25.6 |
| Stirrups, ties, spirals | Chapter 25.7 |

This skill intentionally does **not** restate unverified material-strength tables or development-length formulas unless they have been transcribed clause-by-clause from the PDF.

---

## Section 2: Reinforcement Cover (C)

### 2.1 What is Concrete Cover?

Concrete cover (C) is the minimum distance from the concrete surface to the **outermost reinforcing steel**, as described in Chapter 20.5.1.1. When transverse reinforcement surrounds the main bars, the cover is measured to the outside face of the stirrup, tie, or spiral.

Source: 20.5.1.1, 20.5.1.3.1.

### 2.2 Minimum Cover by Exposure Condition

<!-- PDF aligned to Chapter 20.5.1.3.1 -->

| Exposure Condition | Member Type | Rebar Type | Min. Cover (mm) |
|---|---|---|---|
| Cast against earth and permanently in contact with earth | All members | All reinforcement | 75 |
| Exposed to weather or contact with earth | All members | D19-D57 | 50 |
| Exposed to weather or contact with earth | All members | D16 and smaller, wire 16 mm and smaller | 40 |
| Not exposed to weather and not in contact with earth | Slabs, joists, walls | D43-D57 | 40 |
| Not exposed to weather and not in contact with earth | Slabs, joists, walls | D36 and smaller | 20 |
| Not exposed to weather and not in contact with earth | Beams, columns, column pedestals, tension ties | Main bars, stirrups, ties, spirals, closed ties | 40 |
| In contact with seawater or corrosive environment | All members | All reinforcement | 100 |

> **Design Check Triggers**:
> - Cover < minimum → ERROR: Insufficient cover. Cite applicable table.
> - Cover specified to main bar face (not stirrup face) → WARNING: Clarify measurement convention.

### 2.3 Fire Resistance Cover

Fire-resistance cover may be controlled by 建築技術規則 rather than Chapter 20.5.1 alone. Check both requirements when fire rating is part of the design brief.

Source: 20.5.1.1.

---

## Section 3: Reinforcement Nomenclature

### 3.1 Main Bars (主筋)

- Primary load-carrying reinforcement used to resist flexure, axial force, or both depending on member type
- Typically placed near the tension or compression faces that govern the design section

### 3.2 Stirrups (箍筋) — Beams

- Transverse reinforcement used in beams
- Detailed requirements are governed by beam clauses and Chapter 25.7

### 3.3 Ties (繫筋) — Columns

- Transverse reinforcement used in columns
- Detailed spacing and support requirements are governed by Chapter 10.7 and Chapter 25.7

### 3.4 Relationship between C, Ties/Stirrups, and Main Bars

```
Concrete surface
│← C (cover to stirrup/tie face) →│
                                   ├── Stirrup/Tie (D10)
                                   │← D_stirrup →│← D_main/2 →│
                                                               ← Main bar centroid
```

The drawing and section calculations must distinguish between:
- cover to the outermost transverse steel, and
- bar-centroid locations used in effective-depth calculations.

> **Design Check**: Do not trade off cover against effective depth. Cover below Chapter 20.5.1 is a direct code violation.

---

## Section 4: Development Length (錨定長度)

Development length is governed by Chapter 25.4. Because the exact formulas, factors, and exceptions were not fully transcribed from the PDF in this pass, this skill deliberately avoids restating numerical development-length equations here.

Verified shared rules from Chapter 25.4:
- bars must be developed on both sides of the design section by embedment length, hooks, headed bars, mechanical devices, or combinations: 25.4.1.1
- hooks and heads do not count toward compression-bar development: 25.4.1.2
- development length is computed without using strength-reduction factor $\phi$: 25.4.1.3
- the $\sqrt{f'_c}$ term used for development-length calculations is capped by 700 kgf/cm² [70 MPa] concrete strength, expressed in 25.4.1.4 as a calculation limit on $\sqrt{f'_c}$: 25.4.1.4
- for bars with $f_y \ge 550$ MPa and center spacing less than 15 cm, transverse reinforcement must provide $K_{tr} \ge 0.5d_b$: 25.4.2.2

Use this rule for source control:
- if a design check depends on a numeric ld value, the AI must first resolve it from Chapter 25.4 or from a verified table transcribed from that chapter.

---

## Section 5: Splice Requirements (搭接與續接)

Splice design is governed by Chapter 25.5, with additional member-specific rules in the component chapters, such as Chapter 10.7.5 for columns.

Verified shared rules from Chapter 25.5:
- bars larger than D36 may not be lap-spliced except as allowed for compression cases in 25.5.5.3: 25.5.1.1
- for contact lap splices, minimum clear spacing to adjacent splices or bars follows 25.2.1: 25.5.1.2
- for noncontact lap splices in flexural members, lateral center-to-center spacing must not exceed the smaller of one-fifth of required splice length and 15 cm: 25.5.1.3
- development-length reduction under 25.4.10.1 does not apply to splice-length calculation: 25.5.1.4
- for bars with $f_y \ge 550$ MPa and center spacing less than 15 cm, transverse reinforcement must provide $K_{tr} \ge 0.5d_b$: 25.5.1.5
- tension lap splices are Class A or Class B according to Table 25.5.2.1: 25.5.2.1
- compression lap splices are governed by 25.5.5.1 through 25.5.5.4
- mechanical or welded splices must develop at least $1.25f_y$ in tension or compression: 25.5.7.1

Use this rule for source control:
- if a splice class, lap length factor, or seismic restriction is not explicitly transcribed from the PDF, do not infer it from general practice.

---

## Section 6: AI Design Check Table — General Requirements

Use this table to auto-check submitted structural drawings or design parameters:

| Check | Condition | AI Action |
|---|---|---|
| Minimum spacing | Parallel bars do not satisfy 25.2.1, 25.2.2, or 25.2.3 | ERROR: Rebar spacing violates Chapter 25.2. |
| Cover — interior slab | C < 20 mm (#5 and smaller) | ERROR: Insufficient cover |
| Cover — exterior | C < 50 mm (exposed to weather, #6 and smaller) | ERROR: Insufficient cover |
| Cover — soil contact | C < 75 mm (cast against soil) | ERROR: Insufficient cover |
| Development length | Numeric ld needed but Chapter 25.4 not yet resolved | WARNING: Resolve from verified Chapter 25.4 source before checking |
| Splice class | Numeric splice class or factor not yet resolved from Chapter 25.5 | WARNING: Resolve from verified Chapter 25.5 source before checking |

---

## Section 7: MCP Tool Examples

```python
# Search for concrete material requirements
taiwan-building-code_search_building_code(query="混凝土強度 f'c 最低值", limit=10)

# Search for cover requirements
taiwan-building-code_search_building_code(query="鋼筋保護層厚度 最小值", limit=10)

# Search for development length
taiwan-building-code_search_building_code(query="錨定長度 development length 拉力", limit=10)

# Search for lap splice
taiwan-building-code_search_building_code(query="搭接長度 A類 B類 splice", limit=10)

# Official interpretations for cover disputes
taiwan-building-code_search_building_interpretations(query="保護層 不足 修正")
```

---

## Additional Resources

- For beam-specific design checks: [concrete-beam-design](../混凝土梁設計/concrete-beam-design/)
- For column-specific design checks: [concrete-column-design](../混凝土柱設計/concrete-column-design/)
- For slab-specific design checks: [concrete-slab-design](../混凝土版設計/concrete-slab-design/)
- For wall-specific design checks: [concrete-wall-design](../混凝土牆設計/concrete-wall-design/)
