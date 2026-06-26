---
name: taichung-livable-building-incentive
description: "Use this skill when working with Taichung City's municipal regulation on incentivized livable building facilities (宜居建築), including vertical greening, shading walls, multi-level terraces, floor area exemptions, design review thresholds, maintenance obligations, and feedback deposit mechanisms."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
metadata:
  audience: architects
  region: taiwan
---

# Taichung Livable Building Incentive Regulations

## Overview

This skill covers the **臺中市鼓勵宜居建築設施設置及回饋辦法** (Taichung City Regulations on Incentivized Livable Building Facility Installation and Feedback), a Taichung-specific municipal self-governing rule (自治規則) under the authority of 都市計畫法臺中市施行自治條例 Article 50, Paragraph 4. Use this skill when designing projects in Taichung City that involve vertical greening, external shading elements, multi-level terraces, or when evaluating floor area exemption strategies unique to Taichung.

**This regulation does not apply outside Taichung City jurisdiction.**

---

## Section 1: Quick Reference

| Item | Value |
|------|-------|
| Governing authority | 臺中市政府都市發展局 (Urban Development Bureau) |
| Promulgated | 2019-03-26 |
| Last amended | 2021-08-05 |
| Official source | https://law.taichung.gov.tw/LawContent.aspx?id=GL003620 |
| Skill class | C — Taiwan municipal specific |

---

## Section 2: Eligible Facility Types (Article 3)

| Facility | Chinese term | Key characteristic |
|----------|-------------|-------------------|
| Vertical greening (balcony) | 垂直綠化設施（陽臺） | Plant-integrated balcony design |
| Double-layer shading wall | 雙層遮陽牆體 | Projects ≤ 2 m from external wall; transparency ≥ 33% |
| Green planted wall | 植生牆體 | Plant-covered wall surface; transparency ≥ 33% |
| Decorative shading panel | 造型遮陽牆板 | Projects ≤ 3 m; must accompany other livable facilities |
| Multi-level terrace | 複層式露臺 | Shared, double-height open terrace; green rate ≥ 40% |
| Other | 其他 | Requires Urban Development Bureau approval |

---

## Section 3: Vertical Greening Requirements (Articles 4–7)

Applicable to buildings **6 floors and above** only.

| Requirement | Value |
|-------------|-------|
| Max exempt area per floor | ≤ 8% of floor area |
| Min unit area | ≥ 80 m² |
| Min space diameter | ≥ 2.5 m |
| Min clear height | ≥ 5 m |
| Min greening coverage | ≥ 50% of facility area |

Exception: proximity to designated facilities may waive the 2.5 m diameter requirement (Article 6).

---

## Section 4: Shading Walls (Article 8)

- Protrusion from external wall: ≤ **2 m**
- Must use lightweight construction
- Transparency (透空率): ≥ **33%**

---

## Section 5: Multi-Level Terrace (Articles 9–10)

Applicable to buildings **6 floors and above** only.

| Requirement | Value |
|-------------|-------|
| Ownership classification | Must be designated as **common area** (共用部分) |
| Min clear height | ≥ 8 m |
| Min greening rate | ≥ 40% |
| Ground-floor placement | Exempt from floor area calculation |

May combine with balconies and vertical greening facilities on the same floor.

---

## Section 6: Urban Design Review Threshold (Article 13)

Projects meeting **both** of the following conditions must undergo urban design committee (都審委員會) or pre-review committee review **before** applying for a construction permit:

| Condition | Threshold |
|-----------|-----------|
| Site area | ≥ 1,500 m² |
| Total exempt floor area | ≥ 1,000 m² |

---

## Section 7: Structural and Maintenance Requirements (Article 12)

- All livable facilities must be **incorporated into structural design**
- Planted areas require an **automatic drip irrigation system**
- Greening facilities require a **structural safety certification** signed by a licensed engineer

---

## Section 8: Management Obligations (Articles 14–18)

| Stage | Obligation |
|-------|-----------|
| Construction permit application | Submit a maintenance execution plan |
| After completion | Include in condominium rules (公寓大廈規約) |
| Management committee formation | Transfer execution plan to committee |
| Non-condominium buildings | Transfer plan upon ownership transfer or lease |
| Annual reporting | Submit maintenance report by **June 30 each year**; timely reporters receive subsidy priority |

The Urban Development Bureau may audit registered livable buildings and conduct spot checks (Article 19).

---

## Section 9: Feedback Deposit Mechanism (Article 21)

| Step | Rule |
|------|------|
| Timing | Pay feedback contribution before receiving occupancy permit |
| Deposit ratio | 60% of total feedback amount held as deposit |
| First refund | After 2 full years post-occupancy permit; requires architect inspection and certification |
| Refund amount per tranche | 25% of deposit |
| Additional tranches | Every 2 additional years; repeat inspection required |

---

## Section 10: Design Checklist

- [ ] Building is 6 floors or above? (prerequisite for vertical greening and multi-level terrace)
- [ ] Exempt area per floor within the 8% cap for vertical greening?
- [ ] Greening rate ≥ 50% (vertical) and ≥ 40% (terrace)?
- [ ] Shading walls: protrusion ≤ 2 m, transparency ≥ 33%?
- [ ] Decorative shading panels: protrusion ≤ 3 m, accompanying other livable facility?
- [ ] Site ≥ 1,500 m² AND exempt area ≥ 1,000 m²? → Urban design review required before permit application
- [ ] Maintenance execution plan included in construction permit documents?
- [ ] Feedback deposit amount and refund schedule communicated to client?
- [ ] Structural loads for all livable facilities incorporated into structural design?
- [ ] Automatic drip irrigation system included in drawings?
- [ ] Structural safety certification for greening facilities arranged?

---

## Section 11: Transitional Provision (Article 20)

Buildings that obtained a construction permit **before** this regulation was promulgated may apply for a design change to comply with this regulation before receiving the occupancy permit, provided the **site area and total floor area remain unchanged**.

---

## Section 12: Taiwan-Specific Notes

- This is a Taichung City municipal regulation; do not apply it to projects in other jurisdictions.
- The legal basis (都市計畫法臺中市施行自治條例 Article 50(4)) is specific to Taichung's urban planning self-governance framework.
- Other major cities (Taipei, Kaohsiung, New Taipei) may have analogous incentive schemes under different names and with different numeric thresholds — always verify the applicable municipal rule for the project site.
- Attachment drawings (附圖一～十五) containing detailed dimensional diagrams are referenced in the official regulation but must be retrieved directly from the Taichung municipal law database.

---

## Section 13: Integration Points

Connect this skill with:

- `taichung-paperless-building-permit-documents` — for Taichung construction permit application workflow
- `floor-area-exemption-pitfalls` — for general floor area exemption calculation traps
- `taiwan-programming` — for FAR and site coverage base calculations before applying exemptions
- Urban design review (都市設計審議) workflow for large-scale projects
