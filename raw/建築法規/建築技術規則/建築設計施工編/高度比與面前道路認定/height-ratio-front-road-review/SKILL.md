---
name: height-ratio-front-road-review
description: "This skill should be used when reviewing Taiwan building-height limits controlled by front-road width and FAR-area 3.6:1 height-slope rules: determining the legal front road, calculating Article 14 1.5W+6m where applicable, Article 164 H<=3.6(Sw+D) and shadow-area caps, selecting conservative floor-area-line control points, handling private passages, multiple roads, permanent open space, road-end, residential/non-FAR/cross-zoning checks under Articles 1, 8, 14-19, 23, 24, 27, 29, 160, 164, and 166."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
metadata:
  audience: architects
  region: taiwan
---

# Height Ratio and Front-Road Review

## Overview

This skill evaluates Taiwan building-height limits commonly referred to in
practice as "height ratio" review.

For non-FAR-control contexts, or when Article 166 does not exclude the height
limit, the common front-road-width rule is Building Technical Regulations,
Design & Construction volume (建築技術規則建築設計施工編) Article 14:

```text
maximum building height = adopted front road width x 1.5 + 6 m
```

For FAR-control areas, Chapter 9 applies. The practical "1:3.6" / "3.6"
height-slope review comes from Article 164:

```text
H <= 3.6 x (Sw + D)
As <= L x Sw / 2
```

In current practice, most common urban-planned building sites are FAR-control
areas. In those cases, Article 166 usually excludes Article 14(1)'s
`1.5W + 6m` height-limit part and the under-7m-frontage 9 m height cap. Do not
apply those as primary height limits in FAR-control reviews. Still use Article
14(1) to determine `Sw` for Article 164.

Invoke this skill when:

- A project needs a building-height or front-road-width review
- A FAR-control-area Article 164 height-slope or road-shadow-area review is
  needed
- The site fronts multiple roads, a designated existing lane, a private passage,
  a planned roundabout, a road-end condition, a greenbelt, a river, or permanent
  open space
- Floor-area boundary lines vary by floor or mass, requiring conservative
  control-point selection
- Residential-zone, non-FAR-area, cross-zoning, or local height limits may also
  control the result
- A permit memo must explain which road width, which article, and which control
  point were used

Do not stop at a single formula. The legally important questions are which width
may be recognized as the front road width, which article applies, and whether a
more conservative floor-area-line control point governs the result.

---

## Article Coverage

| Article | Topic | Use in review |
|---|---|---|
| Art. 1 | Definitions | Building height, site ground, road, private passage, similar passage, permanent open space, floor area, setback depth |
| Art. 8 | Existing lanes | Existing-lane frontage and wider-road corner-lot exception |
| Art. 14 | Base height ratio | `H <= 1.5W + 6m` where not excluded; front-road width recognition cases for `Sw` |
| Art. 15 | Permanent open space | Height limits when the site touches or faces permanent open space |
| Art. 16 | Multiple roads | Depth-zone method for sites fronting two or more roads |
| Art. 17 | Deleted | No current substantive rule |
| Art. 18 | Deleted | No current substantive rule |
| Art. 19 | Road end | Dead-end frontage rule and wider-road exception |
| Art. 23 | Residential zone | 21 m / 7-story cap and exceptions |
| Art. 24 | Non-FAR-control area | 36 m / 12-story cap and exceptions |
| Art. 27 | Added height and open space | Extra open-space rule; still cannot exceed Section 3 height limits where applicable |
| Art. 29 | Cross-zoning site | Height must be calculated separately by zoning district |
| Art. 160 | FAR-control areas | FAR-control-area design follows Chapter 9 unless urban-plan rules say otherwise |
| Art. 164 | 3.6:1 height slope | `H <= 3.6(Sw + D)`, road-shadow-area limit, and opposite-road-boundary cap |
| Art. 166 | FAR-control exclusions | Art. 14(1) height-limit part, Arts. 15, 23, 26, 27, etc. do not apply to FAR-control areas |

---

## Required Inputs

Ask for or identify:

- Site boundary, building line, and all roads or access routes touching the site
- Whether the site is in a FAR-control area, because this usually controls
  whether Article 14 height limits and the under-7m 9 m cap are excluded
- Urban-plan road width, existing-lane designation, and any wall line
- Whether any access is through a private passage or similar passage
- Whether the site fronts two or more roads and each road width
- Whether the site touches or faces permanent open space, greenbelt, river, park,
  square, lake, ocean, or other legally nonbuildable land
- Whether the site touches a road end
- Land-use zoning, residential-zone status, non-FAR-control status, and
  cross-zoning
- Proposed building height, stories, and the zone or building portion tested
- Floor-area boundary lines for each floor or mass being tested
- Candidate Article 164 control points, especially the outermost floor-area-line
  points facing the building line
- Article 164 projection direction, opposite front-road boundary, frontage
  length `L`, and any road-shadow-area drawing or area calculation
- Whether the opposite side of the front road has legally confirmed permanent
  open space for Article 164 shadow-area doubling
- Local zoning, urban-plan, local-government, or special-building restrictions

If building-line or road-width evidence is missing, mark the conclusion as
"requires authority confirmation" rather than treating measured pavement width
as final.

---

## Review Algorithm

1. Determine the legal nature of every frontage.
   - Article 1 roads include legally announced roads and existing lanes with
     designated building line.
   - Private passages and similar passages are not roads unless a specific rule
     treats them as a front road for height review.

2. Confirm the building height being tested.
   - Use Article 1's building-height definition.
   - Flag roof projections, parapets, roof equipment, non-flat roofs, and site
     ground differences for separate Article 1 review.

3. Decide whether Chapter 9 FAR-control-area rules govern.
   - If the site is in a FAR-control area, Article 160 points to Chapter 9
     unless urban-plan law or plan text says otherwise.
   - Article 166 excludes Article 14(1)'s height-limit part, Article 15,
     Article 23, Article 26, and Article 27 from FAR-control areas.
   - In common current urban-planned projects, assume FAR-control is likely
     until checked. If confirmed, do not use `1.5W + 6m` or the under-7m 9 m
     cap as primary height limits unless a separate urban-plan, local, or
     authority requirement says so.
   - In FAR-control areas, run Article 164 and still flag stricter urban-plan or
     local rules.

4. Apply Article 14 where applicable.
   - If Article 166 excludes the Article 14 height-limit part, do not run
     `H <= 1.5W + 6m` as a governing height cap.
   - Still use Article 14(1)'s front-road-width recognition rules to determine
     `Sw` for Article 164.
   - Normal frontage: use front road width.
   - Wall line: measure road width to the wall line.
   - Planned roundabout: use the widest road intersecting the roundabout, then
     check Article 16 if another side also fronts a road.
   - Private passage used as main access to the building line: treat it as the
     front road, but if wider than the connected road, use the connected road
     width.
   - Private passage left inside a site touching the building line: apply
     Article 16(1) to the portion near the building line; apply Article 14(3) to
     the remaining portion.
   - Road separated by greenbelt or river: combine both road widths, capped at
     twice the width of the road directly touching the site.

5. Add the under-7m road rule only where Article 14's height-limit part applies.
   - If adopted front road width is under 7 m, the building height within 3.5 m
     from the road centerline is capped at 9 m.
   - In FAR-control areas, this cap is usually excluded by Article 166 together
     with Article 14(1)'s height-limit part.

6. Run Article 164 in FAR-control-area reviews as one integrated geometry
   check.
   - Establish the front road, building line, opposite front-road boundary,
     projection direction perpendicular to the building line, `Sw`, and `L`.
   - Use `Sw` based on Article 14(1)'s front-road-width recognition rules.
   - Mark the floor-area boundary line for each tested floor or mass.
   - For `D`, use the conservative control point on the floor-area boundary
     line: the closest / outermost point facing the building line for the
     building part being tested.
   - Pair that control point with the corresponding building-part height `H`.
   - Check height by `H <= 3.6(Sw + D)`.
   - Project each tested building part at the 3.6:1 slope in the direction
     perpendicular to the building line and calculate the road-shadow area `As`
     falling on the front road.
   - Check `As <= L x Sw / 2`.
   - Confirm the shadow maximum does not exceed the opposite front-road
     boundary.
   - If the opposite side of the front road has legally confirmed permanent
     open space, the allowable shadow area may be doubled.
   - If floor-area boundary lines vary by floor, bend, curve, or step back, test
     all relevant outer points and use the smallest `D`, largest `As`, or
     strictest result.

7. Check Article 15 permanent open space where not excluded by Article 166.
   - Opposite-side permanent open space: height is capped by
     `(road width + open-space depth) x 1.5`, and also by
     `widest road width x 2 + 6 m`.
   - Site touching surrounding permanent open space: open-space width and depth
     or depth sum must reach 20 m; height is capped by
     `widest road width x 2 + 6 m`.
   - Partial frontage/facing: only the matching extension zone, up to 30 m,
     benefits from the rule.
   - If Article 14(5) also applies, use the wider applicable result.

8. Check Article 16 multiple-road zoning.
   - Zone from the widest road boundary: depth `2 x Wmax`, capped at 30 m, uses
     the widest road.
   - Outside that zone, within 10 m from other road centerlines, the next-road
     zone uses depth `2 x Wnext`, capped at 30 m; repeat in road-width order.
   - Remaining area outside the first two categories uses the widest road.
   - Compute height separately for each zone.
   - For four-frontage sites, use the `B`, `B1`, `B2`, `B3`, `B4` workflow in
     the Article 16 method below.

9. Check Article 19 road-end condition.
   - If the site touches a road end, use that road width as the front road.
   - If another side touches a wider road, height is not limited by the road-end
     width; continue with the wider-road analysis.

10. Check related height restrictions.
   - Article 8: if the site touches an existing lane but also touches a wider
     road and is a corner lot, height is not limited by the existing-lane width.
   - Article 23: residential-zone buildings are generally capped at 21 m and 7
     stories unless the road-width/open-space exceptions apply; over 36 m also
     requires Article 24 review.
   - Article 24: non-FAR-control areas are generally capped at 36 m and 12
     stories unless the listed site, road, and open-space conditions apply.
   - Article 27: added stories/height may require added open space where
     applicable, and cannot exceed Section 3 height limits where applicable.
   - Article 29: if the site crosses multiple zoning districts, calculate height
     separately by district.
   - Always flag stricter urban-plan, zoning, local-government, special-use, and
     special-building rules.

11. Output the conclusion.
   - State evidence, adopted width, applicable article, control point, formula,
     height cap, proposed height, result, and any authority-confirmation item.

---

## Key Formulas

```text
Article 14 base:
Hmax = Wfront x 1.5 + 6 m
Use only where Article 14's height-limit part is not excluded by Article 166.
```

```text
Article 14 under-7m frontage:
Within 3.5 m from the road centerline, Hmax = 9 m
Usually excluded in FAR-control areas by Article 166.
```

```text
Article 15 opposite permanent open space:
Hmax <= (road width + permanent open-space depth) x 1.5
Hmax <= widest road width x 2 + 6 m
```

```text
Article 15 surrounding permanent open space:
If open-space width and depth/depth-sum >= 20 m,
Hmax <= widest road width x 2 + 6 m
```

```text
Article 164 FAR-control-area height slope:
H <= 3.6 x (Sw + D)
As <= L x Sw / 2
```

```text
Article 164 shadow-depth quick check:
horizontal projection depth from control point = H / 3.6
road-shadow depth ~= max(0, H / 3.6 - D)
```

When conservative office-standard review is requested, measure `D` from the
outermost floor-area boundary line control point facing the building line.

---

## Conservative Article 164 Control-Point Method

Use this method when the user says the office reviews from the strictest point,
or when floor-area boundary lines vary by point:

1. Extract each floor or mass floor-area boundary line.
2. Find the side facing the relevant building line.
3. Mark every turn point, curve tangent, local protrusion, and closest point to
   the building line.
4. Measure `D` from each candidate point toward the building line, in the
   direction used for Article 164's perpendicular projection to the building
   line.
5. Pair each control point with that building part's `H`.
6. Use the smallest `D`, lowest `3.6(Sw + D)`, or most unfavorable
   exceedance as the controlling result.

Do not use average distance, centroid distance, the most recessed point, or the
largest setback to increase allowed height.

---

## Article 16 Four-Frontage Method

Use this method when a site fronts four roads or when the user describes the
whole site as `B` and asks how to identify front-road control areas.

The plain-language rule is: give the widest road first priority, then treat the
remaining area controlled by the other roads as an undecided pool. Do not assign
`B3` or `B4` before `B2` is calculated. `B2` first takes from the undecided
pool; then `B3` takes from what remains; the final remainder becomes `B4`.

1. Name the whole site `B`.
2. Sort all frontage roads by width: `W1 > W2 > W3 > W4`.
3. From the `W1` road boundary or building line, offset into the site by
   `min(2W1, 30 m)`.
4. Assign that first area to `B1`.
5. Define the remaining site as `B - B1`.
6. Inside `B - B1`, use the 10 m road-centerline zones of `W2`, `W3`, and `W4`
   to identify the undecided pool `U` that may be governed by the other roads.
7. Any part of `B - B1` outside `U` returns to `B1` under Article 16's
   remaining-area rule.
8. Keep `U` undecided. Do not pre-assign it to `B2`, `B3`, and `B4`.
9. For `W2`, offset from the `W2` road boundary or building line by
   `min(2W2, 30 m)`. The portion of `U` reached by that offset becomes `B2`.
   This may consume area that visually seems like future `B3` or `B4`, because
   those areas are not yet decided.
10. Define the remaining undecided pool as `U - B2`.
11. For `W3`, offset from the `W3` road boundary or building line by
    `min(2W3, 30 m)`. The portion of `U - B2` reached by that offset becomes
    `B3`; this may cut into the area that would otherwise remain for `B4`.
12. Assign the final remaining undecided area to `B4`.
13. Use each final area with its own front road: `B1 -> W1`, `B2 -> W2`,
    `B3 -> W3`, `B4 -> W4`.

Practical output should show the whole site `B`, road-width order, the
undecided pool `U`, areas returned to `B1`, the sequential `min(2W, 30 m)`
offset cuts for `B2` and `B3`, and the final `B1` through `B4` boundaries.

---

## Article 164 Road-Shadow-Area Method

Treat the road-shadow-area review as part of the same Article 164 geometry, not
as a detached checklist.

1. Confirm the front road, building line, opposite road boundary, `Sw`, and `L`.
2. Confirm the projection direction perpendicular to the building line.
3. Mark each tested floor-area boundary line and its conservative control
   point.
4. Measure `D` from the control point to the building line and pair it with
   that building part's `H`.
5. Use `H / 3.6 - D` as a quick check for whether the projected shadow enters
   the front road, but do not use it as a substitute for area calculation.
6. Draw or calculate the 3.6:1 projection onto the front road and compute `As`.
7. Check both limits:
   - `H <= 3.6(Sw + D)`
   - `As <= L x Sw / 2`
8. Confirm no shadow extends beyond the opposite front-road boundary.
9. If claiming shadow-area doubling, verify the opposite-side permanent open
   space under the legal definition before using `As <= L x Sw`.

If the height formula passes but `As` fails, or if `As` passes but the projection
extends past the opposite road boundary, the Article 164 result is still not
clean.

---

## Decision Checklist

| Question | Why it matters |
|---|---|
| Is each frontage a legal road, designated existing lane, private passage, or similar passage? | Article 1 controls the baseline classification. |
| Is the site in a FAR-control area? | Article 160 points to Chapter 9 and Article 166 usually excludes Article 14 height limits, including `1.5W + 6m` and the under-7m 9 m cap. |
| Is a wall line designated? | Article 14 measures road width to the wall line. |
| Does the site face a planned roundabout? | Article 14 uses the widest road intersecting the roundabout. |
| Is main access through a private passage? | Article 14 may treat it as the front road, capped by connected road width. |
| Is there a greenbelt or river between roadways? | Article 14 allows combined width, capped at twice the directly adjacent road width. |
| Does the site front more than one road? | Article 16 creates depth zones. |
| Does the site face or touch permanent open space? | Article 15 may change the height limit and applicable area, unless excluded by Article 166. |
| Is the adopted road width under 7 m? | Article 14 adds a 9 m cap in the 3.5 m centerline zone only when Article 14's height-limit part is not excluded by Article 166. |
| Is the road a dead end? | Article 19 controls unless another side touches a wider road. |
| Is the site in a residential zone or non-FAR-control area? | Articles 23 and 24 may impose separate caps. |
| Does the site cross zoning districts? | Article 29 requires separate calculation. |
| Does Article 164 apply? | Test `H`, `D`, `Sw`, `As`, and the opposite road boundary. |
| Which floor-area-line point is most conservative? | Use the closest / outermost point to the building line, not average or maximum setback. |
| Is the opposite front-road boundary shown? | Article 164 requires the shadow maximum not to exceed that boundary. |
| Was `As` calculated from the projected road shadow? | Passing `H <= 3.6(Sw + D)` alone does not complete Article 164 review. |
| Is opposite-side permanent open space legally confirmed? | Article 164 shadow-area doubling depends on this condition. |

---

## Common Pitfalls

- Using actual pavement width without checking building-line designation or
  urban-plan road width.
- Treating a private passage or similar passage as a road without an Article 14
  basis.
- Applying Article 14, Article 15, or Article 23 in a FAR-control area without
  checking Article 166.
- Treating `1.5W + 6m` or the under-7m 9 m cap as the governing height limit in
  a FAR-control area, instead of switching to Article 164.
- Running Article 164 with average setback, largest setback, inner wall line, or
  centroid distance instead of the outermost floor-area-line control point.
- Using one `D` for the whole building when different floors or masses have
  different floor-area boundary lines and heights.
- Applying the widest road to the whole site even though Article 16 requires
  depth-zone review.
- Combining road widths across a greenbelt or river but forgetting the two-times
  direct-frontage cap.
- Forgetting the 9 m cap when the adopted front road width is under 7 m and
  Article 14 applies.
- Treating permanent open space as simple road widening without Article 15's
  depth, width, partial-application, and cap checks.
- Reviewing residential-zone buildings only by `1.5W + 6m` and missing Article
  23 where it applies.
- Running only `H <= 3.6(Sw + D)` and forgetting the Article 164
  road-shadow-area check `As`.
- Treating a passing `As` value as sufficient when the projected shadow still
  exceeds the opposite front-road boundary.
- Doubling Article 164 allowable shadow area without legally confirming
  opposite-side permanent open space.
- Ignoring cross-zoning, local urban-plan text, or stricter local rules.

---

## Output Format

Use this format for permit memos or design checks:

```text
Site / lot:
Zoning:
FAR-control area: yes / no
Article 166 exclusions: Article 14 height limit / under-7m 9 m cap / Article 15 / Article 23 / Article 27 / other:
Frontages reviewed:
Road-recognition basis:
Special conditions:
Applicable article(s):
Adopted front road width:
Height cap:
Article 164 control point / D / As / opposite-boundary check, if applicable:
Article 164 opposite permanent open-space doubling, if applicable:
Proposed building height:
Related height restrictions:
Result:
Open items / authority confirmation needed:
```

For multiple-road sites, add a zone table:

| Zone | Road basis | Depth range | Adopted width | Formula | Height cap | Proposed height | Result |
|---|---|---|---|---|---|---|---|

For Article 164 reviews, add:

| Floor / mass | Floor-area-line control point | Sw | D | H | 3.6(Sw+D) | Shadow beyond opposite boundary? | As | LxSw/2 | Opposite open-space doubling | Result |
|---|---|---:|---:|---:|---:|---|---:|---:|---|---|

---

## MCP Tool Examples

- `taiwan-building-code_search_building_code(query: "建築技術規則 建築物高度 面前道路", limit: 10)`
- `taiwan-building-code_search_building_interpretations(query: "面前道路 私設通路 建築物高度", limit: 10)`
- `taiwan-building-code_search_building_interpretations(query: "建築技術規則 第14條 面前道路 綠帶 河川", limit: 10)`
- `taiwan-building-code_search_building_interpretations(query: "建築技術規則 第16條 臨接兩條以上道路 高度", limit: 10)`
- `taiwan-building-code_search_building_code(query: "建築技術規則 第164條 三點六比一", limit: 10)`
- `taiwan-building-code_search_building_interpretations(query: "第164條 樓地板面積線 建築線 D", limit: 10)`

## Sources

- 建築技術規則建築設計施工編第 1 條 — Definitions for building height, road, private passage, similar passage, permanent open space, and setback depth
  https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=D0070115&flno=1
- 建築技術規則建築設計施工編第 8 條 — Existing lanes and wider-road corner-lot exception
  https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=D0070115&flno=8
- 建築技術規則建築設計施工編第 14 條 — Base height ratio and front-road-width recognition
  https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=D0070115&flno=14
- 建築技術規則建築設計施工編第 15 條 — Permanent-open-space height rules
  https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=D0070115&flno=15
- 建築技術規則建築設計施工編第 16 條 — Multiple-road-site depth zones
  https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=D0070115&flno=16
- 建築技術規則建築設計施工編第 19 條 — Road-end conditions
  https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=D0070115&flno=19
- 建築技術規則建築設計施工編第 23 條 — Residential-zone height rules
  https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=D0070115&flno=23
- 建築技術規則建築設計施工編第 24 條 — Non-FAR-control-area height rules
  https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=D0070115&flno=24
- 建築技術規則建築設計施工編第 27 條 — Added height, stories, and open space
  https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=D0070115&flno=27
- 建築技術規則建築設計施工編第 29 條 — Cross-zoning height calculation
  https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=D0070115&flno=29
- 建築技術規則建築設計施工編第 160 條 — FAR-control-area design follows Chapter 9
  https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=D0070115&flno=160
- 建築技術規則建築設計施工編第 164 條 — 3.6:1 height slope and road-shadow-area limits
  https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=D0070115&flno=164
- 建築技術規則建築設計施工編第 166 條 — FAR-control-area exclusions from several height rules
  https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=D0070115&flno=166
