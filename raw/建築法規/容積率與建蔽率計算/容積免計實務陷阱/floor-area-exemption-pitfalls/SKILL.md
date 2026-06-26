---
name: floor-area-exemption-pitfalls
description: "This skill should be used when reviewing floor-area-ratio (FAR / 容積) exemption items for buildings in Taiwan and avoiding the gap between nominal drawing dimensions and finished clear dimensions. It covers the elevator/stair lobby (梯廳) FAR-exemption clear-dimension trap and the cross-regulation 'finished clear dimension' pattern where finishing layers (e.g. stone cladding) erode the legally-measured dimension and jeopardize the use permit (使照)."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
metadata:
  audience: architects
  region: taiwan
---

# Floor-Area Exemption Pitfalls (容積免計項目實務陷阱)

## Overview

This skill captures field-level pitfalls in Taiwan's floor-area-ratio (FAR / 容積) exemption items — the practitioner know-how that statutory text omits. Plain code lists the exemption threshold; it does not warn you that a value drawn exactly at the threshold will fail at completion. Invoke this skill when:

- Planning FAR-exempt spaces (elevator/stair lobbies, MEP rooms, etc.)
- Deciding whether drawn clear dimensions must reserve thickness for finishing layers
- FAR is nearly maxed out and any failed exemption causes an overage
- Self-checking before use-permit (使照) inspection to avoid completion-stage failures

---

## Core Principle: Nominal Drawing Dimension ≠ Finished Clear Dimension

Many FAR (and other) exemption/compliance thresholds are checked against the **finished clear dimension**, but drawings often note the **structural / rough nominal dimension**. Finishing layers consume the difference:

```
nominal clear dimension − two-side finishing thickness (stone, tile, substrate) = finished clear dimension (the value the regulator actually measures)
```

When a threshold is "**greater-than-or-equal**", drawing exactly at the threshold guarantees a completion-stage shortfall. The correct practice is to reserve finishing thickness as buffer and draw above the threshold.

This is a **cross-regulation recurring pattern**. The elevator/stair lobby FAR exemption is the most typical and highest-consequence instance — the first card in this series.

---

## Pitfall Card: Elevator/Stair Lobby (梯廳) FAR Exemption — Finished Clear Dimension Trap

| Field | Value |
|---|---|
| **Regulatory basis** | Building Technical Regulations (Design & Construction) **Article 162, Paragraph 1, Subparagraph 1** |
| **Threshold** | The shared stair/elevator lobby **clear depth (淨深度) must be ≥ 2.0 m** (note: *clear* depth — measured at the finished face). Also: exempt lobby area ≤ 10% of that floor's area; balcony + lobby combined ≤ 15% of that floor's area (excess counts toward FAR) |
| **Gap mechanism** | nominal depth − stone-cladding/finishing thickness on both ends = finished clear depth (eroded by finishes; dropping below 2 m forfeits the exemption) |
| **Drawing countermeasure** | Draw nominal **2.1 m**, reserving finishing thickness (≈5 cm per side, adjust to actual build-up), so the **clear depth** stays ≥ 2.0 m after cladding |
| **Failure consequence** | finished face < 2.0 m → lobby area **counts toward FAR gross floor area** → if FAR already maxed, overage → **use permit (使照) inspection fails** |
| **Failure timing** | Surfaces only after finishing is installed; very hard to remediate (may require demolishing finishes or altering structure) |
| **Linked items** | FAR gross-floor-area calculation, interior fit-out, use-permit completion inspection |
| **Severity** | 🔴 High (directly blocks the use permit; a late-stage, post-completion risk) |

> Mnemonic: the 2 m threshold is what must be measurable **after** cladding; draw 2.1 m so the stone's thickness is given away up front.

---

## Cross-Regulation Siblings (to be added)

The same "finishing layer / construction tolerance erodes clear dimension → crosses a critical threshold → blocked" structure recurs elsewhere. Each sibling files under its own regulatory home but reuses this card format and cross-links here:

| Sibling pitfall (TBD) | Likely regulatory home | Threshold direction |
|---|---|---|
| Accessible route / corridor clear width | Accessibility design | ≥ (often fails after cladding) |
| Stair clear width / tread depth | Building Tech Reg (egress) | ≥ |
| Driveway / parking stall clear dimensions | Building Tech Reg (parking) | ≥ |
| Fire door / stair-lobby clearances | Building Tech Reg (fire egress) | ≥ |
| Other FAR-exemption critical/upper limits | FAR & coverage calculation | varies |

---

## To Verify

- Clear-depth determination for **irregularly-shaped lobbies** (how the "> 2 m clear depth" portion is recognized when the lobby is non-rectangular) — see National Land Management Agency interpretation ([nlma 12840](https://www.nlma.gov.tw/ch/titlelist/interpcomp/12840)).
- Article 162 §1 subparagraphs 2–3 (MEP, parking exemptions) carry separate execution interpretations to review alongside the lobby exemption.

### MCP Tool Examples

- `taiwan-building-code_search_building_interpretations(query: "容積免計 梯廳", limit: 5)`
- `taiwan-building-code_search_building_code(query: "容積率", limit: 10)`

## References

- Building Technical Regulations (Design & Construction) Article 162 — FAR gross-floor-area calculation and exemption items ([Laws & Regulations Database](https://law.moj.gov.tw/LawClass/LawSingleRela.aspx?PCODE=D0070115&FLNO=162&ty=L))
- National Land Management Agency interpretation letters (lobby FAR-exemption review)
- Local-government building-permit and use-permit inspection rules
