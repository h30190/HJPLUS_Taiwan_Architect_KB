---
name: concrete-wall-design
description: "This skill should be used when an architect or structural designer needs to verify PDF-backed concrete wall requirements such as minimum wall thickness, high-shear minimum reinforcement, bar spacing, and opening reinforcement in Taiwan's concrete structure design code."
user-invocable: true
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
metadata:
  audience: architects
  region: taiwan
  class: C
  regulation: 建築物混凝土結構設計規範
---

# Concrete Wall Design

## Overview

Design requirements for reinforced concrete walls in Taiwan, limited here to clauses directly verified against the uploaded PDF: minimum wall thickness, high-shear minimum reinforcement, spacing limits, and opening reinforcement. Special seismic-wall and boundary-element checks remain chapter references only unless directly transcribed from Chapter 18. For cover and splice fundamentals, see [concrete-general-requirements](../混凝土通用規定/concrete-general-requirements/).

---

## Section 1: Wall Classification

### 1.1 By Function

| Type | Primary Load | Design Focus |
|---|---|---|
| Bearing wall (承重牆) | Axial (gravity) loads | Axial capacity, slenderness |
| Structural wall (結構牆 / 剪力牆) | Lateral (seismic/wind) in-plane shear | Shear capacity, Chapter 11 and Chapter 18 checks |
| Retaining wall (擋土牆) | Earth pressure (out-of-plane) | Refer to foundation and retaining-wall clauses when applicable |
| Non-structural wall (非結構牆) | Self-weight only | Minimum reinforcement, crack control |

### 1.2 By Reinforcement Layout

| Type | Condition | Minimum Layers |
|---|---|---|
| Single layer | General wall cases per detailing layout | 1 layer when permitted by design and detailing clauses |
| Double layer | Wall thickness > 25 cm, except stated exceptions in 11.7.2.3 | 2 layers near each face |

---

## Section 2: Minimum Wall Thickness

### 2.1 Bearing Wall Minimum Thickness

$$h_{wall} \geq \max\left(\frac{l_c}{25},\ 100\ \text{mm}\right)$$

Where lc = unsupported height or length (whichever is shorter).

For a wall with clear height = 3000 mm: h_min = 3000/25 = **120 mm**

Source: 11.3.1.1, Table 11.3.1.1.

### 2.2 Shear Wall Minimum Thickness

- Non-seismic: same as bearing wall (lc/25, min 100 mm)
- Special structural walls: follow Chapter 18 requirements directly

---

## Section 3: Minimum Reinforcement Ratios

### 3.1 Minimum Vertical Reinforcement (縱向鋼筋比 ρl)

$$\rho_l = \frac{A_{sv}}{A_g}$$

For general walls with low shear demand, minimum vertical reinforcement must be taken directly from Table 11.6.1.

For higher shear demand, the verified requirement is:

$$\rho_l \geq 0.0025 + 0.5(2.5 - h_w/l_w)(\rho_t - 0.0025)$$

and not less than 0.0025.

Source: 11.6.2(a).

### 3.2 Minimum Horizontal Reinforcement (橫向鋼筋比 ρt)

$$\rho_t = \frac{A_{sh}}{A_g}$$

For general walls with low shear demand, minimum horizontal reinforcement must be taken directly from Table 11.6.1.

For higher shear demand, the verified requirement is:

$$\rho_t \geq 0.0025$$

> **Note**: When shear demand is high, use the Chapter 11.6.2 equation:  
> $\rho_l \geq 0.0025 + 0.5(2.5 - h_w/l_w)(\rho_t - 0.0025)$ and $\rho_t \geq 0.0025$.

Source: 11.6.2(b).

### 3.3 Maximum Bar Spacing

For cast-in-place walls:
- vertical bar spacing $s \leq \min(3h, 45\text{ cm})$
- horizontal bar spacing $s \leq \min(3h, 45\text{ cm})$

If in-plane strength requires shear reinforcement:
- vertical spacing $s \leq l_w/3$
- horizontal spacing $s \leq l_w/5$

If wall thickness is greater than 25 cm, distributed reinforcement in each direction must be in at least two layers near the wall faces, except for the exceptions listed in 11.7.2.3.

Source: 11.7.2.1, 11.7.3.1, 11.7.2.3.

---

## Section 4: Opening Supplementary Reinforcement (開口補強)

### 4.1 Opening Reinforcement Rules Verified from the PDF

For each interrupted bar:
1. Add supplementary bars around the opening so that the interrupted reinforcement is replaced
2. Double-layer walls: add at least **2 D16** bars in both directions around the opening
3. Single-layer walls: add at least **1 D16** bar in both directions around the opening
4. Anchorage must develop **fy** at the opening corners

These requirements are taken from clause 11.7.5.1.

Source: 11.7.5.1.

---

## Section 5: Special Seismic Wall Requirements

Special structural walls, boundary elements, and other seismic wall detailing must be checked directly against Chapter 18. This skill intentionally does not retain unverified boundary-element trigger formulas.

---

## Section 6: Splice and Development Checks

Wall bar development and splices must be checked directly against Chapters 25.4 and 25.5, plus Chapter 18 when the wall is part of the seismic-force-resisting system.

---

## Section 7: AI Design Check Table — Wall

| Check | Condition | AI Action |
|---|---|---|
| Min thickness (bearing) | h < lc/25 or 100mm | ERROR: Wall too thin for bearing wall requirement. |
| Min thickness (non-bearing) | h < lc/30 or 100mm | ERROR: Wall too thin for non-bearing wall requirement. |
| Min vert. rebar ratio | High-shear wall does not satisfy 11.6.2 vertical-steel equation | ERROR: Insufficient vertical reinforcement. |
| Min horiz. rebar ratio | High-shear wall has ρt < 0.0025 | ERROR: Insufficient horizontal reinforcement. |
| Vertical spacing | Cast-in-place wall s > min(3h, 45cm) or, if shear steel required, s > lw/3 | ERROR: Vertical bar spacing exceeds code limit. |
| Horizontal spacing | Cast-in-place wall s > min(3h, 45cm) or, if shear steel required, s > lw/5 | ERROR: Horizontal bar spacing exceeds code limit. |
| Double layer required | h > 25cm and distributed steel not arranged in at least two layers near faces | ERROR: Two layers required by 11.7.2.3. |
| Opening — bars | Opening interrupts wall bars with no D16 replacement bars | ERROR: Add supplementary bars around opening. |
| Seismic wall check | Wall is part of the seismic system but Chapter 18 review not performed | WARNING: Verify special structural wall rules directly from Chapter 18. |

---

## Section 8: MCP Tool Examples

```python
# Search for wall minimum reinforcement requirements
taiwan-building-code_search_building_code(query="牆 最小鋼筋比 垂直 水平 牆板", limit=10)

# Search for opening supplementary reinforcement
taiwan-building-code_search_building_code(query="牆 開口 開孔 補強 對角鋼筋", limit=10)

# Search for shear wall seismic requirements
taiwan-building-code_search_building_code(query="剪力牆 耐震 邊緣構件 boundary element", limit=10)

# Search for wall thickness requirements
taiwan-building-code_search_building_code(query="牆 最小厚度 承重牆 淨高", limit=10)

# Official interpretations
taiwan-building-code_search_building_interpretations(query="剪力牆 邊緣構件 判斷 圍束")
```

---

## Additional Resources

- General requirements (cover, development length, splice): [concrete-general-requirements](../混凝土通用規定/concrete-general-requirements/)
- Column confinement (referenced by boundary elements): [concrete-column-design](../混凝土柱設計/concrete-column-design/)
