---
name: accessible-door-clear-width
description: "This skill should be used when checking accessible-route door/opening clear-width compliance for buildings in Taiwan, and avoiding the gap between the code's nominal frame-to-frame distance and the effective passable clear width after the door leaf, hardware and finishes intrude. Covers Taiwan Accessible Facilities Design Specification §205.2.3 (entrances/doors): hinged-door frame-to-frame distance ≥ 90 cm, sliding/folding-door clear width ≥ 80 cm, no thresholds, and the §205.4.1 ban on revolving/spring doors."
user-invocable: true
---

# Accessible Door Clear Width Pitfalls (無障礙出入口門淨寬實務陷阱)

## Overview

The code measures the **frame-to-frame distance**; a person passes through the **effective clear width after the door opens**. The difference is consumed by the door leaf, hardware and finishing layers. Invoke this skill when:

- Sizing door openings on an accessible route
- Deciding whether to reserve width for door-leaf intrusion and finishes
- Self-checking before accessible-facility completion inspection

---

## Core Principle: Nominal Opening ≠ Effective Passable Clear Width

The provision measures the **frame-to-frame distance** (hinged door ≥ 90 cm), but the usable dimension is the **effective clear width with the door open 90°** (inner face of the open leaf to the opposite frame). The difference:

```
nominal frame-to-frame distance − door-leaf/hardware intrusion (at 90°) − two-side finishing = effective passable clear width
```

The threshold is "≥", so an opening drawn exactly at 90 cm almost certainly fails after the leaf and finishes are installed.

---

## Pitfall Card: Accessible Door Clear Width — Effective-Clear-Width Trap

| Field | Value |
|---|---|
| **Regulatory basis** | Taiwan Accessible Facilities Design Specification **§205.2.3 (entrances/doors)**; revolving/spring doors banned (§205.4.1) |
| **Threshold** | Hinged door: **frame-to-frame distance ≥ 90 cm**; sliding/folding door: **clear width after opening ≥ 80 cm**. Floor flush, no threshold |
| **Measurement nuance** | Code text measures "frame-to-frame distance"; practice/inspection commonly judges by **effective clear width** (door open 90°, inner leaf face to opposite frame). Leaf thickness, stops, handles and finishes all erode it |
| **Gap mechanism** | nominal frame-to-frame − leaf/hardware intrusion − two-side finishing = effective passable clear width (forfeits compliance below 90 cm) |
| **Drawing countermeasure** | Draw the opening at **100 cm**, reserving for leaf intrusion and finishing, so effective clear width stays ≥ 90 cm |
| **Failure consequence** | effective clear width < 90 cm → accessible-facility inspection fails → use permit blocked |
| **Failure timing** | Surfaces after the door and finishes are installed; hard to remediate (requires changing door type or rebuilding the frame) |
| **Linked items** | accessible-route clear width along the whole path, interior fit-out, use-permit completion inspection |
| **Severity** | 🔴 High (directly blocks the use permit; a late-stage, post-completion risk) |

> Mnemonic: the 90 cm must be measurable after the door is hung and finishes applied; draw 100 cm so the leaf and cladding are given away up front.

---

## Design Checks

- [ ] Hinged-door opening reserves leaf intrusion + finishing (frame-to-frame ≈95–100 cm so effective ≥ 90 cm)?
- [ ] No revolving/spring doors (§205.4.1)?
- [ ] Floor flush, no threshold?
- [ ] Sliding/folding door clear width ≥ 80 cm after opening?
- [ ] Handle leaves 4–6 cm anti-pinch space (§205.4.3)?

## To Verify

- The "effective clear width judged at 90° open" is a practice/inspection convention; the code text states "frame-to-frame distance". Confirm against local-government inspection interpretations.

## References

- Taiwan Accessible Facilities Design Specification §205 (entrances/doors) — Ministry of the Interior regulation system
- Local-government use-permit accessible-facility inspection rules
