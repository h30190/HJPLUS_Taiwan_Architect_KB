---
type: Skill
name: accessible-bathroom-grab-bars
description: "This skill should be used when reviewing accessible bathroom and shower grab bar (handrail) compliance for Taiwan buildings, including horizontal and vertical grab bar heights, minimum lengths, wall clearances, structural anchorage, and coordination with shower seats, faucets, and emergency call buttons under Taiwan Accessible Facilities Design Specification Chapter 6 (§606) and Chapter 2 (§207)."
user-invocable: true
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
verified:
  - { by: human:Jacky820507, at: 2026-11-19T00:00:00Z }
sources:
  - id: btr-167
    resource: https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=D0070115&flno=167
    title: 建築技術規則建築設計施工編 第167條
    last_modified: 2024-03-14
  - id: btr-167-4
    resource: https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=D0070115&flno=167-4
    title: 建築技術規則建築設計施工編 第167-4條
    last_modified: 2024-03-14
  - id: nlma-barrier-free-606
    resource: https://www.nlma.gov.tw/
    title: 建築物無障礙設施設計規範 第六章 浴室 (第606節 淋浴間)
    last_modified: 2021-08-01
  - id: nlma-barrier-free-207
    resource: https://www.nlma.gov.tw/
    title: 建築物無障礙設施設計規範 第二章 無障礙通路 (第207節 扶手)
    last_modified: 2021-08-01
metadata:
  audience: architects
  region: taiwan
  class: C
  status: verified
  data-currency: "2026-11-19"
---

# Accessible Bathroom Grab Bars Compliance (無障礙浴室扶手設計檢討)

## Overview

In Taiwan building code compliance, accessible bathrooms and shower stalls are top inspection failure hotspots during final building permit inspections (使用執照竣工勘驗). Unlike decorative handrails, grab bars in accessible bathrooms act as critical fall-prevention and transfer-support structures. Dimension gates such as minimum lengths, height ranges, and wall clearance distances are rigidly enforced by municipal inspection committees with zero tolerance for negative field deviations.

Invoke this skill when:
- Designing or auditing accessible bathrooms, public shared bathrooms, or accessible hotel guest rooms.
- Checking drawing dimensions for horizontal and vertical grab bars in shower stalls.
- Coordinating wall-framing backing reinforcement (pre-embedded steel plates in stud walls) before tiling.
- Conducting pre-inspection audits before the official barrier-free completion walkthrough.

---

## Governing Law & Code Hierarchy

1. **National Building Technical Regulations (建築技術規則建築設計施工編 第十章 無障礙建築物)**:
   - **§167**: Barrier-free facilities must comply with central authority specifications.[^btr-167]
   - **§167-4**: Buildings equipped with common/shared bathrooms must provide at least one accessible bathroom per building.[^btr-167-4]
2. **Design Specifications for Accessible Facilities in Buildings (建築物無障礙設施設計規範)**:
   - **Chapter 6 Bathrooms §606 (Shower Stalls 淋浴間)**: Specifies horizontal/vertical grab bar placement, bath seats, faucets, and emergency call buttons.[^nlma-barrier-free-606]
   - **Chapter 2 Accessible Routes §207 (Handrails 扶手)**: Specifies tube outer diameters, perimeter lengths, wall clearances, and overhead clearance.[^nlma-barrier-free-207]

---

## Core Regulatory Constraints: Shower Grab Bars (§606.5)

Shower stalls must provide **both horizontal and vertical grab bars** to support seated transfer and standing stability:

### 1. Grab Bar Dimensions & Placement Limits

| Parameter | Regulatory Threshold | Engineering & Ergonomic Purpose | Constraint Type |
| :--- | :--- | :--- | :--- |
| **Horizontal Bar Height** | Top edge **75 to 85 cm** above finished floor (FL) | Supports forearms during seated transfer from wheelchair to shower seat. | Range gate (75–85 cm) |
| **Horizontal Bar Length** | **Not less than 120 cm** ($\ge 120\text{ cm}$) | Continuous gripping path along side wall. | **Hard minimum** (no negative tolerance) |
| **Vertical Bar Top Edge** | Height **not greater than 150 cm** ($\le 150\text{ cm}$) | Reaching grip limit for standing shower or pulling up. | **Hard maximum** ($\le 150\text{ cm}$) |
| **Vertical Bar Bottom Edge** | Gap to horizontal bar top **$\le 10\text{ cm}$** | Prevents open hand slip-through when transitioning between bars. | **Hard maximum** ($\le 10\text{ cm}$) |
| **Vertical Bar to Faucet** | Center-to-center horizontal distance **$\le 40\text{ cm}$** | Enables user to grip bar firmly with one hand while operating water valve. | **Hard maximum** ($\le 40\text{ cm}$) |
| **Vertical Bar to Wall Corner** | Clear distance from internal corner **$\ge 30\text{ cm}$** | Prevents hand knuckles and elbows from colliding with corner walls. | **Hard minimum** ($\ge 30\text{ cm}$) |

### 2. Grab Bar Profile & Wall Clearance (§207)

* **Cross-Section Profile (§207.2.1)**:
  * **Circular Tube**: Outer diameter must be **2.8 to 4.0 cm** (optimal grip circumference for adult hands).
  * **Non-Circular (Oval/Flat-oval)**: Outer perimeter length must be **9 to 13 cm** with rounded edges.
* **Wall Clearance (§207.3.2)**:
  * Clear spacing between the grab bar and finished wall surface **must not be less than 5.0 cm** ($\ge 5.0\text{ cm}$).
* **Overhead Clearance (§207.3.2)**:
  * A vertical clear space of at least **45 cm** must be preserved above the grab bar (no shelves, ledges, or soap dispensers).
* **Surface & Finish (§207.3.1)**:
  * Must be smooth, non-slip, and free of burrs or sharp hooks. Stainless steel (SUS304/316) core with textured nylon/antibacterial resin coating is recommended to eliminate cold-touch shock.

---

## Coordinated Facility Requirements (§606)

A shower stall cannot function compliant with grab bars alone; the following items must be integrated:

1. **Shower Seat (§606.3)**:
   - Must provide a bath seat with **armrests and a backrest** (座面高度 40～45 cm, slip-resistant).
   - Horizontal grab bar runs continuously along the seat side to facilitate wheelchair slide-in transfer.
2. **Faucet & Showerhead (§606.4)**:
   - Operating lever and showerhead must be positioned **40 to 120 cm** above FL, at least **30 cm** away from wall corners.
   - Must use single-lever mixer valves or thermostatic valves (rotary knob valves are prohibited).
3. **Dual Emergency Call Buttons (§606.6)**:
   - **High call button**: Center point **90 to 120 cm** above FL.
   - **Low fall call button**: Center point **15 to 25 cm** above FL (operable by person lying on floor).
4. **Turning Space & Access (§606.2, §604)**:
   - Turning clear circle with diameter **$\ge 150\text{ cm}$** must be provided inside the stall/bathroom.
   - Door must be sliding type with clear passable opening width **$\ge 80\text{ cm}$** and zero threshold step.

---

## Standard Elevation & Layout Schematics

### 1. Side Wall Elevation (Design Specification Fig. 606.5.1 / 606.5.2)

```text
 Wall Corner (Inside)
  │◀───── ≧ 30 cm ─────▶│ 
  │                     │ Vertical Bar Top Edge ≦ 150 cm
  │                     │ 
  │                     │ [Vertical Grab Bar]
  │                     │ ◀──── ≦ 40 cm ────▶ [Faucet / Lever]
  │                     │                     (Height 40–120 cm)
  │                     │ Vertical Bottom to Horizontal Top ≦ 10 cm
  │           ┌─────────┴─────────────────────────────────────────┐
  │           │            Horizontal Grab Bar (Length ≧ 120 cm)  │ Top Edge 75–85 cm
  │           └───────────────────────────────────────────────────┘
  │                                                ┌─────────────┐
  │  [High SOS Button]                             │ Shower Seat │
  │  (Height 90–120 cm)                            │ (Seat 40-45)│
  │                                                └──────┬──────┘
  │  [Low Fall SOS Button]                                │
  │  (Height 15–25 cm)                                    │
──┴───────────────────────────────────────────────────────┴────── FL ±0
```

### 2. Cross-Section & Wall Anchorage Detail (§207)

```text
              │                  │
              │ Overhead Clear   │ ≧ 45 cm (no obstructions)
              │                  ▼
              │             ┌─────────┐ ◄── Circular OD: 2.8 – 4.0 cm
              │   Bracket   │         │    (Non-circular perim: 9 – 13 cm)
       Wall   ├───┐ ┌───────┤ SUS304  │
     Finishes │   │ │       │ + Nylon │
     (Tiles)  │   └─┴───────┤ Coating │
              │             └─────────┘
              │   Gap ≧ 5cm      ▲
              │◀───────────────▶│ (Anti-pinch clearance)
              │                  │
    ─────────────────────────────────────────────
    [Structural Anchorage Rules]
    - Drywall stud partitions: Pre-embed 2.0mm thick galvanized steel plate
      between framing studs (elevation 70–160 cm) prior to gypsum board enclosing.
    - Pull-out testing standard: Must withstand instantaneous load ≧ 150 kgf.
```

---

## Pitfall Card & Field Failure Prevention

| Risk / Pitfall | Mechanism & Failure Mode | Prevention Countermeasure |
| :--- | :--- | :--- |
| **Negative Length Variance** | Horizontal bar fabricated at 120 cm nominal, but wall tiling subtracts 2–3 cm $\rightarrow$ net length 118 cm $\rightarrow$ **Permit Inspection Fails**.[^nlma-barrier-free-606] | Specify **125 cm** on drawings; order custom bars with tolerance margin. |
| **Drywall Anchor Tear-Out** | Grab bar anchored only into drywall / tile with plastic plugs $\rightarrow$ tears out under user weight or inspector pull test. | Mandate **pre-embedded 2.0 mm galvanized steel backing plate** across studs. |
| **Insufficient Wall Gap** | Deep-relief wall tiles or thick adhesive eat into the 5.0 cm clearance $\rightarrow$ net gap 4.5 cm $\rightarrow$ non-compliant (finger pinching). | Verify grab bar bracket standoff; ensure mounting base plate offsets bar $\ge 5.5\text{ cm}$ from substrate. |
| **Merged Toilet / Shower Clash** | Combining accessible toilet and shower in a compact room $\rightarrow$ swing-down toilet armrest collides with the 120 cm shower horizontal bar or infringes the 150 cm turning circle. | Split toilet and shower zones to opposing walls; ensure 150 cm turning circle remains clear of unfolded fixtures. |

---

## Design Audit Checklist

- [ ] Horizontal grab bar top edge is between 75 and 85 cm above FL.
- [ ] Horizontal grab bar net length is $\ge 120\text{ cm}$ (reserving for tile thickness).
- [ ] Vertical grab bar top edge is $\le 150\text{ cm}$ above FL.
- [ ] Vertical grab bar bottom edge is $\le 10\text{ cm}$ from horizontal bar top.
- [ ] Vertical grab bar is $\le 40\text{ cm}$ horizontally from the faucet lever.
- [ ] Vertical grab bar is $\ge 30\text{ cm}$ away from internal wall corners.
- [ ] Bar outer diameter is 2.8 to 4.0 cm (or perimeter 9 to 13 cm).
- [ ] Clear distance from bar inner edge to tile surface is $\ge 5.0\text{ cm}$.
- [ ] Overhead vertical space above bar is clear for $\ge 45\text{ cm}$.
- [ ] Pre-embedded 2.0mm steel backing plate is specified for stud walls.
- [ ] Two emergency call buttons (high 90–120 cm, low 15–25 cm) are provided.
- [ ] Shower seat with backrest and armrests (height 40–45 cm) is specified.
- [ ] Clear turning diameter $\ge 150\text{ cm}$ is maintained inside the stall.

---

## Boundary Cases & Escalation

* **Existing Buildings (既有公共建築物)**: For buildings permitted prior to July 1, 2008 where existing structural columns or shafts make achieving 120 cm grab bar length or 150 cm turning space physically impossible, do not attempt unauthorized deviations. Submit a formal *Alternative Barrier-Free Facilities Improvement Plan* (既有公共建築物無障礙設施替代改善計畫) to the municipal architectural review committee for discretionary approval.
* **Pre-inspection Verification**: Always measure from the finished surface of installed tiles, not rough concrete or drywall framing.

---

## Related Skills

- [accessible-door-clear-width](../../無障礙出入口門淨寬實務陷阱/accessible-door-clear-width/SKILL.md) — Door clear width and opening hardware clearance.
- [accessible-elevator-shaft-dimensions](../../無障礙電梯機道尺寸對應/accessible-elevator-shaft-dimensions/SKILL.md) — Elevator shaft and car accessibility compliance.
- [consultation-workflow](../../../建築顧問方法論/顧問諮詢工作流程/consultation-workflow/SKILL.md) — Master consulting workflow and cluster routing.

---

[^btr-167]: 建築技術規則建築設計施工編 第167條 (無障礙建築物通用規定).
[^btr-167-4]: 建築技術規則建築設計施工編 第167-4條 (共用浴室設置規定).
[^nlma-barrier-free-606]: 內政部國土管理署 建築物無障礙設施設計規範 第六章 浴室 第606節 淋浴間.
[^nlma-barrier-free-207]: 內政部國土管理署 建築物無障礙設施設計規範 第二章 無障礙通路 第207節 扶手.

