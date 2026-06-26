---
name: concrete-column-design
description: "This skill should be used when an architect or structural designer needs to verify PDF-backed concrete column requirements such as longitudinal reinforcement ratio, minimum longitudinal-bar count, minimum shear reinforcement, and column splice rules in Taiwan's concrete structure design code."
user-invocable: true
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
metadata:
  audience: architects
  region: taiwan
  class: C
  regulation: 建築物混凝土結構設計規範
---

# Concrete Column Design

## Overview

Design requirements for reinforced concrete columns in Taiwan, limited here to items directly verified against the uploaded PDF: longitudinal reinforcement ratio, minimum longitudinal-bar count, minimum shear reinforcement, and column splice rules. Seismic confinement details that were not fully transcribed remain chapter references only. For cover and splice fundamentals, see [concrete-general-requirements](../混凝土通用規定/concrete-general-requirements/).

---

## Section 1: Column Classification

### 1.1 By Cross-Section Shape

| Type | Section | Reinforcement Type |
|---|---|---|
| Rectangular column (矩形柱) | Square or rectangle | Ties (繫筋) |
| Circular column (圓柱) | Circle | Spirals (螺旋筋) or circular ties |
| L-shaped / irregular | Composite shapes | Combined tie arrangement |

### 1.2 By Primary Loading

| Type | Characteristics | Design Consideration |
|---|---|---|
| Axially loaded | Gravity load dominant | ρg within limits; tie spacing |
| Eccentrically loaded | Combined axial + bending | Interaction diagram (P-M curve) |
| Short column | Slenderness ratio < limit | Direct strength calculation |
| Slender column | Slenderness ratio ≥ limit | Moment magnification required |

---

## Section 2: Main Bar Requirements (主筋)

### 2.1 Gross Reinforcement Ratio (ρg)

$$\rho_g = \frac{A_{st}}{A_g}$$

Where:
- Ast = total area of longitudinal steel
- Ag = gross cross-sectional area of column

| Limit | Value | Reason |
|---|---|---|
| Minimum | **1.0% (0.01)** | Below this, column cannot resist minimum bending; creep becomes excessive |
| Maximum | **8.0% (0.08)** | Above this, bar congestion at splices and joints prevents proper concrete casting |
| Practical note from commentary | Reinforcement ratio is generally not preferred above 4% when all lap splices occur at one location | Constructability warning only |

> **Design Check**: ρg < 1% → ERROR. ρg > 8% → ERROR.

Source: 10.6.1.1 and its commentary.

### 2.2 Minimum Number of Main Bars

| Column Shape | Minimum Bars |
|---|---|
| Rectangular ties | 4 bars (one at each corner) |
| Circular spirals | 6 bars |
| Triangular ties | 3 bars |

Source: 10.7.3.1.

### 2.3 Source-Control Note

Bar-size limits, bundling, and development-length effects must be resolved from Chapter 25 when needed. This skill does not preserve unverified bar-size assumptions.

---

## Section 3: Transverse Reinforcement Clauses

The following clauses were verified in the PDF and should be used instead of inferred detailing rules:

| Topic | Governing Clause |
|---|---|
| Minimum shear reinforcement trigger | 10.6.2.1 |
| Minimum shear reinforcement formula | 10.6.2.2 |
| Minimum bar spacing reference | 10.7.2.1 → Chapter 25.2 |
| Minimum longitudinal-bar count | 10.7.3.1 |
| Tie / spiral / closed-tie detailing | 10.7.6.1.2 → Chapter 25.7 |

Do not infer tie-spacing rules beyond what has been directly transcribed from the PDF.

---

## Section 4: Minimum Shear Reinforcement

When shear reinforcement is required, the PDF gives:

$$A_{v,min} = \max\left(0.062\frac{\sqrt{f'_c}}{f_{yt}}b_ws,\ 0.35\frac{b_ws}{f_{yt}}\right)$$

This reflects clause 10.6.2.2.

Source: 10.6.2.2.

---

## Section 5: Column Splice Rules Verified from the PDF

### 5.1 Compression Lap Splices

If column bars are in compression, compression lap splices may be used. Clause 10.7.5.2.1 allows reduction of lap length, but not below 30 cm:

- tied columns: multiply by 0.83 when the tie confinement requirement inside the splice zone is met
- spiral columns: multiply by 0.75 when the spiral confinement requirement inside the splice zone is met

### 5.2 Tension Lap Splices

Clause 10.7.5.2.2 gives the verified classification:

| Bar Stress Under Factored Load | Detail Condition | Splice Type |
|---|---|---|
| ≤ 0.5fy | at any section, spliced bars ≤ 50% and splice locations staggered by at least ψgld | Class A |
| ≤ 0.5fy | all other cases | Class B |
| > 0.5fy | all cases | Class B |

Source: 10.7.5.2.2, Table 10.7.5.2.2.

### 5.3 Seismic Restrictions

Special seismic column confinement and splice-location restrictions must be checked directly against Chapter 18. This skill does not restate unverified hinge-zone dimensions.

---

## Section 6: Placement and Support Details Verified from the PDF

- bottom tie or closed tie in a story must be placed no farther than one-half tie spacing above the footing or slab top: 10.7.6.2.1
- top tie or closed tie in a story must be placed no farther than one-half tie spacing below the lowest horizontal reinforcement of the slab / capital / drop panel; with beams or brackets on all four sides, not farther than 7.5 cm below the lowest beam or bracket reinforcement: 10.7.6.2.2
- if anchors or precast connectors are placed at a column end, transverse reinforcement must be provided within 12.5 cm of the end: 10.7.6.1.5, 10.7.6.1.6

---

## Section 7: AI Design Check Table — Column

| Check | Condition | AI Action |
|---|---|---|
| ρg minimum | ρg < 1% | ERROR: Insufficient longitudinal reinforcement. Column cannot resist minimum moment. |
| ρg maximum | ρg > 8% | ERROR: Excessive reinforcement — casting impossible at splices. |
| Compression splice reduction | 0.83 or 0.75 reduction applied without clause 10.7.5.2.1 confinement condition | ERROR: Splice reduction not justified. |
| Tension splice class | Class A used when stress/detail condition in 10.7.5.2.2 is not met | ERROR: Upgrade to Class B. |
| Seismic splice location | Column is part of seismic system and Chapter 18 location check not performed | WARNING: Verify Chapter 18 splice restrictions before approval. |
| Min bars (rectangular) | < 4 main bars | ERROR: Minimum 4 bars required for rectangular tied column. |

---

## Section 8: MCP Tool Examples

```python
# Search for column reinforcement ratio requirements
taiwan-building-code_search_building_code(query="柱 縱向鋼筋比 ρg 最小 最大", limit=10)

# Search for tie spacing requirements
taiwan-building-code_search_building_code(query="柱 繫筋間距 橫向鋼筋", limit=10)

# Search for seismic column requirements
taiwan-building-code_search_building_code(query="柱 耐震 特殊圍束筋 塑鉸區 lo", limit=10)

# Search for splice location in columns
taiwan-building-code_search_building_code(query="柱 搭接位置 塑鉸區 禁止", limit=10)

# Official interpretations
taiwan-building-code_search_building_interpretations(query="柱 繫筋 圍束 計算方式")
```

---

## Additional Resources

- General requirements (cover, development length): [concrete-general-requirements](../混凝土通用規定/concrete-general-requirements/)
- Beam design: [concrete-beam-design](../混凝土梁設計/concrete-beam-design/)
