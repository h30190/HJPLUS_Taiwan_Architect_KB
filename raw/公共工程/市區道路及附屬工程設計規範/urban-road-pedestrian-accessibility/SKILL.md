---
type: Skill
name: urban-road-pedestrian-accessibility
description: "This skill should be used when a building design meets the urban road at the pedestrian interface: sidewalk clear width (人行道淨寬), central green strip splits, cross and longitudinal slope, clear height, vehicle crossings over the sidewalk (車道出入口), public utility strips (公共設施帶), accessible routes and kerb ramps (無障礙通路、路緣斜坡), bollard spacing and kerb type. Invoke it when checking a ground-floor plan or site entrance against 市區道路及附屬工程設計規範, or preparing a building-permit submission that touches the sidewalk. For planting on that sidewalk use urban-road-landscape-planting; for which instrument governs, see urban-road-code-fundamentals."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
status: draft
sources:
  - id: std-2021
    resource: https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=D0070156
    title: 市區道路及附屬工程設計標準
    last_modified: 2021-08-11
  - id: code-2026
    resource: https://www.nlma.gov.tw/%E6%9C%80%E6%96%B0%E6%B6%88%E6%81%AF/%E6%B3%95%E8%A6%8F%E5%85%AC%E5%91%8A/31-%E9%83%BD%E5%B8%82%E5%9F%BA%E7%A4%8E%E5%B7%A5%E7%A8%8B%E7%B5%84/10391-%E5%B8%82%E5%8D%80%E9%81%93%E8%B7%AF%E5%8F%8A%E9%99%84%E5%B1%AC%E5%B7%A5%E7%A8%8B%E8%A8%AD%E8%A8%88%E8%A6%8F%E7%AF%84.html
    title: 市區道路及附屬工程設計規範（115年4月23日修正，完整版）
    last_modified: 2026-04-23
metadata:
  audience: architects
  region: taiwan
  class: C
  status: draft
  data-currency: "2026-08-15"
---

# Urban Road: Pedestrian and Accessibility Interface

## Overview

Where a building meets the street, the architect owns the sidewalk frontage in practice even
though the road authority owns the standard. This skill carries the dimensions an architect checks
when a ground-floor plan, a setback, or a site entrance lands on an urban-road sidewalk.

Before applying any value here, confirm which instrument and version govern and whether the section
is co-aligned with a highway, via
[urban-road-code-fundamentals](../urban-road-code-fundamentals/SKILL.md). The 應/不得/宜/不宜
wording rules defined there apply to every value below: "shall" renders 應 or 不得, "should" renders
宜, "should not" renders 不宜. Note 不宜 is a default prohibition (do not do it unless justified),
not a soft hint, so a 不宜 breach carries a heavier burden to justify than a plain 宜.

Accessibility here is the on-road portion (accessible route, kerb ramps, tactile guidance within
the road right-of-way). Accessibility inside the building follows 建築物無障礙設施設計規範, a
parallel instrument; a compliant design satisfies both.

## Sidewalk Clear Width (§6.1)

Clear width is the sidewalk total minus public facilities, the continuous walkable space.

- Should be 2.5 m or more; shall not be less than 1.5 m in general conditions.
- Where road width is 12 m or less, shall not be less than 1.2 m.
- Where site conditions constrain and the competent authority consents, shall not be less than
  0.9 m.
- Central green strip case: where a green strip sits at the sidewalk centre, the two flanking
  clear widths shall sum to at least 2.1 m, and neither side may be less than 1.2 m. Passing the
  sum does not pass the per-side floor. This is the most common misread.
- Motorcycle bays are as a principle not marked on sidewalks; where marked with consent, remaining
  clear width shall not be less than 1.5 m.

## Sidewalk Slope and Clear Height (§6.2)

- Cross slope: minimum 0.5%, maximum 5%.
- Longitudinal slope: should be 5% or less; shall not exceed 12%.
- Clear height: should be 2.1 m or more, with no 0.1 m projection intruding between 0.6 m and
  2.1 m at the side of the route. This governs street-tree branch height and shrub overhang.

## Vehicle Crossings over the Sidewalk (§6.3)

The point where a site driveway crosses the sidewalk, an architect's item on almost every project.

- Crossing slope should not exceed 16.67% (1:6).
- Platform width should be 1.5 m or more, minimum 1.2 m.
- A mountable kerb should be used.

## Paving and Separation (§6.4, §6.5)

- Permeable paving is allowed provided infiltration does not damage the carriageway subgrade;
  where a planting strip is present, sidewalk runoff should be directed into it.
- Separation from the carriageway is preferred and may be a kerb, bollard, railing, planter or
  hedge (§6.5.1).

## Public Utility Strip (§13.2, §13.3)

- Primary and secondary roads shall provide one; service roads should, subject to need and land.
- Width should be 1.5 m as a principle, and should not be less than 0.8 m.
- Set to the widest facility on the section; consolidate poles and signs into it; put cables
  underground where practical.
- Facilities shall satisfy intersection sight distance and shall not obstruct the accessible route.
- Tree pit kerbs shall as a principle be flush with the paving; after a continuous green strip or
  planter is added, sidewalk clear width still governs per §6.1.

## Kerbs (§15.1)

- By height and slope: mountable (可跨式) where h < 10 cm; between 10 and 15 cm the slope decides
  (V/H ≤ 1 mountable, V/H > 1 barrier); barrier (屏障式) where 15 < h ≤ 20 cm; above 20 cm only in
  special cases.
- Sidewalk kerbs should be barrier type not exceeding 15 cm; median kerbs barrier type not
  exceeding 20 cm.
- Service roads may use mountable kerbs where emergency vehicle access is a consideration.

## Accessibility on the Road (§14)

- Accessible-route clear width follows §6.1, clear height follows §6.2; longitudinal slope should
  be under 5%, and should not exceed 8.33%.
- Where clear width is under 1.5 m, provide a turning platform at each turn and passing platforms
  at intervals; each platform at least 1.5 m by 1.5 m, spacing should be under 60 m.
- Kerb-ramp clear width (excluding flared sides) should be 1.5 m or more; ramp slope should be
  under 8.33%; where the level difference is 20 cm or less, the width may be relaxed per table
  14.2.1.
- At the junction of sidewalk and pedestrian crossing, no bollard as a principle; where required,
  clear spacing between bollards shall be 1.5 m or more, height should be 0.6 to 0.75 m.
- Tactile guidance tiles shall conform to CNS 15933 and CNS 16106.

## Worked Example

Same drawing as the worked example in `urban-road-landscape-planting`; this skill checks the width
half, that skill checks the planting half. Neither half is conclusive alone.

**Input.** A ground-floor plan fronting a 15 m secondary urban road (not highway co-aligned).
Sidewalk total 3.2 m with a 1.0 m green strip at its centre. A site driveway crosses the sidewalk
at 18% slope with a 1.2 m platform. A row of bollards separates the sidewalk from the carriageway,
spaced 1.3 m at the crossing to the pedestrian crossing.

**Check.**

1. Central green strip. 3.2 − 1.0 = 2.2 m across two sides. Sum 2.2 m ≥ 2.1 m passes, but the best
   split (1.2 m and 1.0 m) fails the 1.2 m per-side floor. **ERROR** under §6.1; narrow the strip
   or move it kerbside.
2. Driveway slope. 18% exceeds 16.67%. **ERROR** under §6.3 (uses 宜 for the limit, so strictly a
   strong WARNING; but building-permit reviewers routinely treat 1:6 as a hard gate, so resolve it).
3. Driveway platform. 1.2 m meets the 1.2 m minimum. **PASS**, though below the 1.5 m target.
4. Bollard spacing at the crossing. 1.3 m is below the 1.5 m accessible clearance. **ERROR** under
   §14.2 (不得).

**Result.** Report the green strip and bollard spacing as determinate; flag the driveway slope with
its modal basis so the team knows the reviewer's likely position.

**Carry into the planting check.** The 1.0 m strip is not too narrow to plant — the 1.5 m² figure in
§16.2 is an area duty on a discrete 植穴, not a width floor on a continuous bed. The strip fails on
clear width here, and the fix (moving it kerbside) turns the bed back into discrete pits, which
re-arms that 1.5 m² floor. See `urban-road-landscape-planting`.

## Common Pitfalls

### Pitfall: passing the green-strip sum but failing the per-side floor
- **Severity**: 🔴 rejection risk
- **When it bites**: ground-floor plans with a centred street-tree strip
- **Wrong**: reporting 2.2 m combined as compliant
- **Right**: §6.1 sets both a 2.1 m sum and a 1.2 m per-side floor. Check both.

### Pitfall: treating on-road accessibility and in-building accessibility as one rule
- **Severity**: 🟡 rework risk
- **When it bites**: continuous accessible route from street to lobby
- **Wrong**: applying only 建築物無障礙設施設計規範 across the sidewalk
- **Right**: the sidewalk portion follows §14 of this code; the building portion follows the
  accessibility regulation. Both apply; the stricter governs at the seam.

### Pitfall: quoting the 0.9 m sidewalk floor without the condition
- **Severity**: 🟡 rework risk
- **When it bites**: constrained frontages
- **Wrong**: designing to 0.9 m as if it were generally available
- **Right**: 0.9 m applies only where site conditions constrain **and** the competent authority
  consents (§6.1). Without consent the floor is 1.2 m or 1.5 m.

## AI Design Check Table

| Check | Condition | AI Action |
|---|---|---|
| Sidewalk clear width | < 1.5 m generally, or < 1.2 m on roads ≤ 12 m wide | ERROR: §6.1 不得小於 |
| Central green strip | flanking sum < 2.1 m, or either side < 1.2 m | ERROR: §6.1 |
| Sidewalk clear height | projection over 0.1 m between 0.6 m and 2.1 m | ERROR: §6.2 不得 |
| Vehicle crossing slope | > 16.67% | WARNING on §6.3 wording; treat as gate for permit review |
| Public utility strip width | < 0.8 m | WARNING (default prohibition): §13.2 不宜小於; requires an active justification, not just a note |
| Accessible route obstructed by a facility | any | ERROR: §13.3 不得阻礙 |
| Accessible route slope | > 8.33% | ERROR: §14.1 不得大於 |
| Bollard clear spacing at crossing | < 1.5 m | ERROR: §14.2 |
| Tactile tile standard | not CNS 15933 / CNS 16106 | ERROR: §14.4 應符合 |

## Data Currency

- Source: §6, §13, §14, §15.1 of 市區道路及附屬工程設計規範, as amended 2026-04-23; 設計標準 §16,
  §21, as amended 2021-08-11
- Verified: 2026-08-15; §6/§13/§15.1 values cross-checked against the 2024-09-12 amendment and
  unchanged
- Volatility: MEDIUM to HIGH; re-verify if the last check is over twelve months old

## To Verify

- [ ] Confirm §14 clause numbering against the consolidated text; transcribed from the same PDF but
  not independently cross-checked against the law database.
- [ ] Add the CNS 15933 and CNS 16106 current editions and dates.
- [ ] Cross-check the seam rule against 建築物無障礙設施設計規範 for the street-to-lobby route.

## MCP Tool Examples

```python
taiwan-building-code_search_building_interpretations(query="人行道 淨寬 公共設施帶 爭議")
```

## Related Skills

- [urban-road-code-fundamentals](../urban-road-code-fundamentals/SKILL.md) — apply first to fix
  instrument, version and jurisdiction.
- [urban-road-landscape-planting](../urban-road-landscape-planting/SKILL.md) — planting on the same
  sidewalk, including how a tree pit interacts with the clear-width rules here.

## Additional Resources

- Full clause text: [../urban-road-code-fundamentals/references/ch06-13-15-pedestrian-space.md](../urban-road-code-fundamentals/references/ch06-13-15-pedestrian-space.md)
- Human-facing overview: [domain.md](../domain.md)
