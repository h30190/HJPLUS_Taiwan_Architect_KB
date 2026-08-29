---
type: Skill
name: urban-road-landscape-planting
description: "This skill should be used when designing or checking road-fronting planting under 市區道路及附屬工程設計規範: street-tree pit clear area (植穴淨面積), tree spacing by canopy size, soil depth for survival versus growth, species selection and root-form and canopy-size classification, sight-line planting limits within 25 m of a stop line, planting on medians and channelising islands, and the qualitative landscape and ecology provisions for drainage, bridges, slopes, lighting and noise barriers. Invoke it for landscape drawings, green-coverage checks, or planting review on an urban road. For sidewalk clear width and accessibility use urban-road-pedestrian-accessibility; for which instrument governs, see urban-road-code-fundamentals."
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

# Urban Road: Landscape and Planting

## Overview

Road-fronting planting is where a landscape architect's design meets the urban-road code. This
skill carries the planting dimensions and the species classification needed to apply them, plus
the qualitative landscape-and-ecology provisions that belong in the design narrative.

Before applying any value, confirm which instrument and version govern via
[urban-road-code-fundamentals](../urban-road-code-fundamentals/SKILL.md), and note the live
standard-versus-code discrepancy on the tree pit recorded there. The 應/不得/宜/不宜 wording rules
from that skill apply throughout: "shall" renders 應 or 不得, "should" renders 宜, "should not"
renders 不宜. 不宜 is a default prohibition (do not do it unless justified), not a soft hint, so a
不宜 breach carries a heavier burden to justify than a plain 宜.

A tree pit also consumes sidewalk width, so a planting check and a clear-width check are two halves
of the same drawing. The width side lives in
[urban-road-pedestrian-accessibility](../urban-road-pedestrian-accessibility/SKILL.md).

## Planting Design (§16.2)

- Tree pit clear area shall exceed 1.5 m², with priority given to crown development space and
  continuous linear configuration (item 6). Note 設計標準 §21(4) states area "1.5 m² or more"; the
  standard outranks the code where they differ.
- The 1.5 m² floor attaches to the discrete pit (植穴). Item 6 names 植穴 and 植栽帶 separately and
  puts the numeric duty on the former, while naming continuous linear beds as the preferred
  configuration. In a continuous bed the qualifying area accrues along the run, so a bed narrower
  than a compliant square pit is not thereby non-compliant. Never back-convert 1.5 m² into a width
  floor of about 1.22 m; that inference holds only for a square discrete pit.
- Spacing: large-canopy species 8 m to 10 m; small-canopy species 4 m to 7 m (item 6).
- Planting shall not obstruct sight lines or driving safety (item 3).
- Within 25 m of the stop line at intersections, and at sidewalk intersection sections and vehicle
  crossings, beds should use ground flora or turf, with shrub height below 0.5 m (items 10, 11).
- Large-canopy trees should be planted on sidewalks 4 m wide or wider, or adjoining building
  setbacks (item 12).
- Species should favour native, tolerant, low-maintenance species and should avoid invasive,
  malodorous, toxic-pollen, heavy-sap or heavy-fruit-drop species (item 4). Shallow-, buttress- and
  prop-rooted species require assessment of long-term adverse effects (item 5).

## Soil Depth (§16.2 items 7 and 8)

Two distinct sets. Always state which set is being applied; the gap reaches 60 cm.

| Plant type | Minimum for survival | Adequate for growth |
|---|---|---|
| Herbaceous | 15 cm | 30 cm |
| Shrubs | 30 cm | 45 cm |
| Large shrubs and small trees | 45 cm | 60 cm |
| Shallow-rooted trees | 60 cm | 90 cm |
| Deep-rooted trees | 90 cm | 150 cm |

## Species Classification (Appendix 4 items 19 and 20)

Classify a proposed species first: canopy size drives the spacing and sidewalk-width rules, and
root form drives the §16.2 item 5 assessment and the soil-depth table.

- Root form: shallow 小葉欖仁, 黑板樹, 莿桐; buttress 鳳凰木, 吉貝, 銀葉板根; prop 榕樹, 印度橡膠樹,
  雀榕, 垂榕
- Large canopy (mature crown ≥ 6 m): 榕樹, 樟樹, 臺灣欒樹, 茄苳, 楓香, 欖仁樹, 風鈴木
- Small canopy (mature crown ≤ 5 m): 臺灣肖楠, 海檬果, 臺灣海桐, 福木, 厚皮香

## Island Planting (§15.2)

- Planted median width should exceed 1.2 m (a planted median narrower than this is a WARNING).
- Channelising island area should be 7 m² or more, minimum 5 m²; planting must not compromise the
  sight triangle.

## Qualitative Landscape and Ecology (§16.1, §16.3 to §16.8)

No numeric thresholds, mostly 宜. These support the design narrative and review comments, never a
pass-or-fail finding.

- §16.1 principles: beautification, cultural landscape with resident participation, ecological
  conservation (habitat diversity, green-corridor networks, wildlife passages, native site-adapted
  species, soil permeability and retention), facility reduction and consolidation.
- §16.3 drainage: earth, grass or cobble channels from local materials where subgrade and sidewalk
  quality allow; planting to screen concrete slope structures; compound culvert sections as wildlife
  passages with diameter rising as length rises; less culverting and concreting, detention basins
  where the setting allows.
- §16.4 to §16.6 bridges, tunnels, slopes: slim structures, integrate form and texture, conceal
  deck drainage, reserve wall and three-dimensional greening space, retain natural landform and
  rock, reduce cut and fill, use porous materials for habitat.
- §16.7 lighting: combined poles at intersections, light and maintainable fittings, reduce light
  pollution, keep high-mast lighting clear of tree crowns. Numeric illuminance sits in Ch.19, held
  at chapter level in the fundamentals references.
- §16.8 noise barriers: integrate with landscape, reserve planting space, pattern transparent
  barriers against bird strike, treat terminal ends, anti-glare design.

Full clause text in
[../urban-road-code-fundamentals/references/ch16-landscape-ecology.md](../urban-road-code-fundamentals/references/ch16-landscape-ecology.md).

## Worked Example

Same drawing as the worked example in `urban-road-pedestrian-accessibility`; this skill checks the
planting half, that skill checks the width half. Neither half is conclusive alone.

**Input.** A 3.2 m sidewalk on a 15 m secondary road, with a 1.0 m green strip running along the
sidewalk centre. Proposed: 臺灣欒樹 in that strip at 6 m spacing, soil depth 60 cm, first tree 18 m
from the intersection stop line.

**Check.**

1. Classify. 臺灣欒樹 is large canopy and deep-rooted (Appendix 4). This sets spacing to 8 to 10 m,
   sidewalk-width preference to 4 m, and soil depth to 90 cm survival / 150 cm growth.
2. Configuration and area. A 1.0 m continuous strip is a 植栽帶, not a discrete 植穴, and item 6
   names continuous linear beds as the preferred form. Area per tree is 1.0 × 6 = 6 m², well over
   1.5 m². **PASS**. The strip being narrower than a compliant 1.22 m square pit is not a finding:
   the 1.5 m² floor is an area duty on a discrete pit, not a width floor on a bed.
3. Spacing. Proposed 6 m against 8 to 10 m. **WARNING**, item 6 uses 宜. Widening to 8 m would also
   raise area per tree to 8 m².
4. Canopy versus sidewalk width. Large canopy on a 3.2 m sidewalk; item 12 wants 4 m. Uses 宜, so
   **WARNING** with a stated reason in the design report.
5. Soil depth. Deep-rooted needs 90 cm to survive; 60 cm is below even survival. **ERROR** against
   §16.2 item 7. This, not the strip width, is what makes the 1.0 m centre strip a poor host for a
   deep-rooted large-canopy species.
6. Sight line. 18 m is inside the 25 m zone. **WARNING** on item 10 wording, escalating to **ERROR**
   under item 3 (不得) if the crown or trunk blocks the sight triangle (Appendix 3 item 35).

**Result.** The planting rules yield one determinate violation (soil depth) and three items needing
justification. Nothing here prohibits the centre strip. What kills it is §6.1: the two flanking
clear widths total 2.2 m and the better side can only reach 1.2 m if the other drops to 1.0 m,
breaching the 1.2 m per-side floor — checked in `urban-road-pedestrian-accessibility`.

**The loop that matters.** Moving the strip kerbside fixes the §6.1 failure, but it also converts
the planting from a continuous bed back into discrete pits, at which point the 1.5 m² pit floor does
bind: a 1.2 m by 1.2 m pit gives 1.44 m² and becomes an **ERROR** under §16.2 item 6 and 設計標準
§21(4). Changing the width answer changes the planting answer. Re-run both skills after any
re-section.

## Common Pitfalls

### Pitfall: mixing the two soil depth tables
- **Severity**: 🟡 rework risk
- **When it bites**: detailed design and quantity take-off
- **Wrong**: quoting 60 cm for a deep-rooted street tree because it appears in the code
- **Right**: 60 cm is the survival minimum for shallow-rooted trees only. Deep-rooted trees need
  90 cm to survive, 150 cm to grow properly (§16.2 items 7 and 8). Name the table in the note.

### Pitfall: quoting a 宜 value as mandatory
- **Severity**: 🔴 rejection risk
- **When it bites**: submittal review, design review meetings
- **Wrong**: rejecting 6 m spacing as non-compliant with the 8 to 10 m rule
- **Right**: item 6 uses 宜; deviation is permitted with justified reason. Request the justification.

### Pitfall: reading the 1.5 m² pit floor as a minimum planting-bed width
- **Severity**: 🔴 rejection risk
- **When it bites**: centre or kerbside green strips narrower than about 1.22 m, planter boxes
- **Wrong**: computing √1.5 ≈ 1.22 m and rejecting a 1.0 m continuous green strip as too narrow to
  plant, or concluding that trees are not permitted in it
- **Right**: item 6 puts the 1.5 m² duty on 喬木植穴 and separately endorses 連續性帶狀 beds. In a
  bed the qualifying area accrues along the run: 1.0 m at 6 m spacing is 6 m² per tree. Judge a
  narrow bed on crown space (item 12), soil depth (items 7 and 8) and the §6.1 clear width it
  consumes — not on a width figure back-derived from a pit-area rule.

### Pitfall: treating §16.3 to §16.8 as checkable criteria
- **Severity**: 🟢 minor
- **When it bites**: automated checking, review checklists
- **Wrong**: raising a finding because a bridge does not reserve greening space
- **Right**: those clauses carry no thresholds and mostly use 宜. Narrative, not pass or fail.

### Pitfall: checking planting without checking the resulting sidewalk width
- **Severity**: 🟡 rework risk
- **When it bites**: continuous planters or green strips
- **Wrong**: sizing the pit to 1.5 m² and stopping
- **Right**: a pit or continuous bed consumes clear width; re-check §6.1 in
  urban-road-pedestrian-accessibility after placing planting.

## AI Design Check Table

| Check | Condition | AI Action |
|---|---|---|
| Tree pit clear area (discrete pit only) | ≤ 1.5 m² | ERROR: §16.2 item 6 and 設計標準 §21(4) |
| Continuous planting bed | width below √1.5 ≈ 1.22 m | NOT a finding on area; compute actual area per tree as bed width × spacing, then apply the row above only if the result is ≤ 1.5 m² |
| Soil depth | below the survival figure for that root type | ERROR: §16.2 item 7 |
| Soil depth | between survival and adequate-growth figures | INFO: viable, below growth standard (§16.2 item 8) |
| Planting within 25 m of stop line | shrubs above 0.5 m, or canopy obstructing sight triangle | ERROR where sight line obstructed (§16.2 item 3, 不得); else WARNING (item 10, 宜) |
| Tree spacing | outside 8–10 m (large) or 4–7 m (small) | WARNING: item 6 宜, request justification |
| Large canopy on sidewalk < 4 m | proposed | WARNING: item 12 宜 |
| Planted median width | ≤ 1.2 m | WARNING: §15.2.3 宜大於 |
| §16.1, §16.3 to §16.8 provisions | not addressed | INFO only, never ERROR |

## Data Currency

- Source: §15.2, §16 of 市區道路及附屬工程設計規範, as amended 2026-04-23; 設計標準 §21, as amended
  2021-08-11. §16.2 values cross-checked against the 2024-09-12 amendment and unchanged.
- Verified: 2026-08-15
- Volatility: MEDIUM to HIGH; re-verify planting dimensions if the last check is over twelve months
  old.

## To Verify

- [ ] Cross-check §16.2 against 建築基地綠化設計技術規範 where a road frontage counts toward building
  greening (green-coverage double counting).
- [ ] Confirm whether any municipality sets stricter planting values; Appendix 5 lists Taipei and
  Kaohsiung instruments, so local variation is likely.

## MCP Tool Examples

```python
taiwan-building-code_search_building_code(query="市區道路 植穴 喬木 土壤厚度", limit=10)
pcc-downloader_download_specification(chapter="02", keyword="植栽", format="pdf")
```

## Related Skills

- [urban-road-code-fundamentals](../urban-road-code-fundamentals/SKILL.md) — apply first to fix
  instrument, version and jurisdiction.
- [urban-road-pedestrian-accessibility](../urban-road-pedestrian-accessibility/SKILL.md) — the
  sidewalk-width side of the same drawing.

## Additional Resources

- Full clause text: [../urban-road-code-fundamentals/references/ch16-landscape-ecology.md](../urban-road-code-fundamentals/references/ch16-landscape-ecology.md)
- Human-facing overview: [domain.md](../domain.md)
