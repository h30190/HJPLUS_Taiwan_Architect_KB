---
type: Skill
name: taipei-building-decorative-structures
description: "This skill should be used when reviewing Taipei City facade design (臺北市新建案立面檢討/外牆立面規畫), building attached non-structural decorative elements (外牆附置物/裝飾物/附屬物), frames, beams, columns, panels, louvers, railings, canopy/balcony/terrace/facade decorative features in Taipei City per the 2024 Taipei City Building Attached Decorative Structure Design Exemplar Compilation (臺北市建築物附置裝飾性構造物設計範例彙編, Effective 2024-09-25). Includes porosity, projection, emergency opening, building area, FAR exemption, and height-slope restriction review."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
verified:
  - { by: human:CWLin0518, at: 2026-07-28T00:00:00Z }
metadata:
  audience: architects
  region: taiwan
  class: C
  status: verified
  data-currency: "2026-07-28"
---

# Taipei City Building Attached Decorative Structures Review

## Overview

This skill provides step-by-step compliance evaluation for non-structural decorative elements attached to building facades, balconies, terraces, canopies, roof structures, and main entrances in Taipei City.

Effective **September 25, 2024** (Doc No. 北市都授建字第 1136163958 號 / 113年度彙編第045號編號第016號), this regulation replaces and repeals Section IV of the 2017 Taipei Building Permit Sample Inspection Resolution Compilation (106年9月6日北市都授建字第10634955700號函).

---

## Interactive Web Tool & Visualization (互動檢討網頁與全套圖例)

When responding to queries regarding Taipei City facade design, building attached decorative structures, louvers, fins, or balcony/terrace regulations, **ALWAYS include the link to the interactive calculation webpage**:
- **Interactive Calculation & Blueprint Webpage**: [臺北市建築物附置裝飾性構造物互動檢討與全套圖例系統](../index.html)（頁面依賴 Google Fonts 與 MathJax CDN，離線時公式顯示原始 LaTeX、字體退回系統預設）

---

## Scope & Non-Combustibility Requirement


- **Definition**: Non-structural decorative frames, beams, columns, panels, railings, louvers/shutters attached to the exterior of buildings or miscellaneous structures.
- **Material Mandate**: All decorative elements **MUST be constructed of non-combustible materials (不燃材料)**.

---

## Quantitative Review Rules by Element Type

### 1. Balcony Decorative Structures (陽台裝飾物)

| Check Item | Threshold / Limit | Area & Height/Rear Yard Restriction |
| :--- | :--- | :--- |
| **Porosity Rate (透空率)** | $\ge 2/3$ (excluding railing height) | N/A |
| **Emergency Opening (緊急開口)** | At least 1 per unit: Rectangular $\ge 75\text{ cm} \times 1.2\text{ m}$ OR Circular $\varnothing \ge 1.0\text{ m}$ | Must be un-obscured |
| **L-shaped / Multi-fold Balcony Columns/Panels** | Combined width $\le \frac{1}{3} L_{\text{balcony}}$ (excluding structural column width) | Exceeding 1/3 is prohibited |
| **Piping Enclosure Porosity** | $\ge 1/2$ | Enclosed area is included in balcony area |
| **Balcony Sunshade / Canopy Exceeding 2m** | Porosity $\ge 1/2$. Total depth (balcony + sunshade) $> 2.0\text{ m}$ | Portion exceeding 2.0m **MUST BE INCLUDED** in Building Area & FAR, subject to Height-Slope & Rear Yard rules |
| **Balcony / Entrance Canopy Overlap** | Overlapped area evaluated under balcony rules | If evaluated as canopy, cannot name room or register title |

### 2. Terrace Decorative Structures (露台裝飾物)

- **Height Limit**: Must not exceed the height of the current floor (當層為限).
- **Porosity Rate**: $\ge 1/2$ (calculated on remaining area above railing height).
- **Extension Limits**:
  - Inward extension from railing centerline: $D_1 \le 50\text{ cm}$.
  - Outward extension from railing centerline: $D_2 \le 1.0\text{ m}$.

### 3. Canopy Decorative Structures (雨遮裝飾物)

- **Maximum Canopy Depth**: $\le 1.0\text{ m}$.
- **Decorative Railing Height**: $\le 90\text{ cm}$.
- **Decorative Louver Porosity**: $\ge 2/3$.
- **Emergency Entry Opening**: Must provide at least 1 emergency entry ($\ge 75\text{ cm} \times 1.2\text{ m}$ or $\varnothing \ge 1.0\text{ m}$).
- **Window Sill Height Rule**: Exterior wall window sills behind decorative railings/louvers must be $> 1.2\text{ m}$ high or equipped with fixed windows (固定窗).

### 4. Exterior Wall Facade Decorative Structures (外牆裝飾物)

| Sub-type | Dimension & Porosity Rules | Building Area & FAR Treatment |
| :--- | :--- | :--- |
| **Enclosing Louvers / Perforated Panels** | Outward projection $\le 2.0\text{ m}$ from wall centerline; Porosity $\ge 2/3$ | Projected area (incl. horizontal ties) **INCLUDED in Building Area** & subject to Height/Rear Yard rules |
| **Horizontal / Vertical Fins & Plates** | Projection $\le 2.0\text{ m}$ from wall centerline | Portion $\le 1.0\text{ m}$: **EXEMPT from Building Area**. Portion $> 1.0\text{ m}$ up to $2.0\text{ m}$: **INCLUDED in Building Area** & subject to Height/Rear Yard rules |
| **Enclosed Fin + Louver / Glass Combo** | Must meet Porosity $\ge 2/3$ | Projected area (incl. panels & ties) **INCLUDED in Building Area** |
| **Solid Decorative Columns / Panels** | Solid filled, width $< 1.5\text{ m}$ | **EXEMPT from Floor Area**. Clear gap between continuous columns $\ge 1.5\text{ m}$. Columns on structural column sides: combined width $\le 1.5\text{ m}$ (no openings allowed) |
| **Wall Centerline Determination** | Hollow interior: measured to outer wall centerline. Solid interior: measured to volumetric center $(d_1-d_2)/2$ | Used for exact dimension and setback calculations |

### 5. Structural Spandrel / Structural Beams (結構性過樑)

- **Max Outward Projection**: $\le 10\text{ cm}$ from beam outer edge.
- **Porosity Requirement**: $\ge 2/3$.
- **Area & Height Limits**: **MUST BE INCLUDED in Building Area**, subject to Height-Slope & Rear Yard rules.

### 6. Perimeter Wall Gate Openings (圍牆出入口)

- **Depth Limit**: $\le 2.0\text{ m}$.
- **Lateral Extension**: $\le 1.0\text{ m}$ outwards from gate sides.
- **Prohibitions**: Cannot cross building line (建築線), cannot connect to building or other decorative features.

### 7. Roof Level & Roof Appurtenances (屋頂層及屋突)

- **Night Lighting Systems ($\le 2.0\text{ m}$)**: Evaluated per Building Technical Regulations Art. 1-10-3 (露天機電設備); **EXEMPT** from roof appurtenances height & area.
- **Roof Appurtenances Horizontal Fin ($\le 50\text{ cm}$)**: Projections $\le 50\text{ cm}$ from wall centerline are **EXEMPT** from the 1/8 roof appurtenance area cap.
- **Roof Appurtenances Projections ($> 50\text{ cm}$)**: Deduct 50 cm from outer edge to set the evaluation centerline for 1/8 roof appurtenance area; if directly projecting to ground, projected area **INCLUDED in Building Area** & subject to Height/Rear Yard rules.

### 8. Main Entrance Canopies & Decorative Portals (出入口雨遮與造型框架)

1. **1F Main Entrance Canopies**: Canopy depth $\le 2.0\text{ m}$ extended on left/right sides.
2. **Entrance Decorative Portals / Frames**:
   - Projected Area: **INCLUDED in Building Area** & subject to Height/Rear Yard rules.
   - Enclosed Volume / Coverage: Must be $< 30\%$ of maximum allowable Building Area (設計建蔽率 30%).
   - Porosity: $\ge 2/3$ open; **NO TOP COVER (無頂蓋)** allowed on porous parts.
   - Legal Requirement: Developer affidavit (起造人切結), incorporated into condominium rules (規約草約), drawing notes, and property transfer documents.

---

## Discretionary Pre-Review Process (預審機制)

If a project cannot comply with this compilation due to special functional needs, structural uniqueness, or environmental/landscape requirements:
- The project may submit an application to the **Taipei Building Permit Pre-Review Committee (臺北市建造執照預審小組)** for approval of partial or full exemption.

---

## Checklist for Plan Reviewers & Architects

- [ ] Are all decorative materials non-combustible?
- [ ] Balcony openings: Is porosity $\ge 2/3$? Is an emergency opening ($\ge 75 \times 120\text{ cm}$ or $\varnothing \ge 100\text{ cm}$) reserved?
- [ ] Balcony sunshade total depth: Does it exceed 2.0m? If yes, is the excess included in FAR & Building Area?
- [ ] Exterior wall fins: Is the projection $\le 1.0\text{ m}$ for building area exemption? If between $1.0\text{ m}$ and $2.0\text{ m}$, is it included in Building Area?
- [ ] Exterior wall solid columns: Is width $< 1.5\text{ m}$ with net spacing $\ge 1.5\text{ m}$?
- [ ] Entrance portal frame: Is enclosed area $< 30\%$ of building area? Is porosity $\ge 2/3$? Is no-top-cover affidavit prepared?

---

## Worked Examples

### Example 1: Balcony Decorative Sunshade & Column Review

```text
Inputs:
  L_balcony = 6.0 m (Balcony length)
  D_balcony = 1.5 m (Balcony depth)
  D_sunshade = 0.8 m (Decorative sunshade projection beyond balcony outer edge)
  Sunshade Porosity = 60% (3/5)
  Emergency Opening = 80 cm (W) x 130 cm (H)
  Decorative Column Width = 1.2 m

Evaluation & Rules Applied:
  1. Material: Non-combustible (Compliant).
  2. Emergency Opening: 80 cm >= 75 cm AND 130 cm >= 120 cm (Compliant).
  3. Decorative Column Width: 1.2 m <= (1/3)*6.0 m = 2.0 m (Compliant).
  4. Sunshade Porosity: 60% >= 50% (Compliant per Section 1.5).
  5. Combined Projection & Area Treatment:
     Total Depth D_total = 1.5 m + 0.8 m = 2.3 m > 2.0 m.
     Excess Depth = 2.3 m - 2.0 m = 0.3 m.
     Excess Area to Include = 6.0 m x 0.3 m = 1.80 m²

Result:
  - Balcony Structure: PASS.
  - Action Required: Include 1.80 m² in Building Area and Floor Area Ratio (FAR) calculation, and verify 3.6:1 height-slope restriction.
```

### Example 2: Exterior Wall Facade Vertical Solid Fins & Enclosing Louver Panel Review

```text
Inputs:
  Wall Length = 12.0 m
  Type A (Solid Vertical Fin):
    Outward Projection = 0.8 m
    Fin Solid Width = 0.4 m
    Net Spacing between Fins = 1.8 m
  Type B (Enclosing Louver Panel):
    Outward Projection = 1.5 m
    Louver Porosity = 70% (7/10)

Evaluation & Rules Applied:
  1. Type A Solid Fin:
     Projection 0.8 m <= 1.0 m, Solid Width 0.4 m < 1.5 m, Net Spacing 1.8 m >= 1.5 m.
     Rule: Projection <= 1.0 m and solid width < 1.5 m -> EXEMPT from Building Area.
  2. Type B Enclosing Louver Panel:
     Projection 1.5 m <= 2.0 m, Porosity 70% >= 2/3 (66.7%).
     Rule: Projection > 1.0 m up to 2.0 m for enclosing louvers -> Projected Area INCLUDED in Building Area.
     Projected Area to Include = 12.0 m x 1.5 m = 18.00 m²

Result:
  - Type A Fins: EXEMPT from Building Area & FAR.
  - Type B Panel: PASS conditionally (Must include 18.00 m² in Building Area & verify Height/Rear Yard setback).
```

---

## Related Skills
* [height-ratio-front-road-review](../../../../建築技術規則/建築設計施工編/高度比與面前道路認定/height-ratio-front-road-review/SKILL.md)
* [floor-area-exemption-pitfalls](../../../../容積率與建蔽率計算/容積免計實務陷阱/floor-area-exemption-pitfalls/SKILL.md)
* [balcony-lobby-far-recalculation](../../../../容積率與建蔽率計算/陽臺梯廳回計容積計算/balcony-lobby-far-recalculation/SKILL.md)

