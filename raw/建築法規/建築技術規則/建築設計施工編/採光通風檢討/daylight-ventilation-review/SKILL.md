---
type: Skill
name: daylight-ventilation-review
description: "This skill should be used when reviewing statutory daylighting (採光) and ventilation (通風) compliance under Taiwan's Building Technical Regulations, Design & Construction volume, Chapter 2 Section 8 (Articles 39-1 to 45) and the Building Equipment volume's mechanical-ventilation rules (Articles 100-106): deciding whether a room is a 居室, computing the Article 41 daylight-area ratio (1/5 classrooms, 1/8 dwellings/wards/dormitory bedrooms, openings within 75 cm above floor excluded), applying Article 42 effective-daylight corrections (H/D limits by zoning, road/permanent-open-space exemption, skylight x3, balcony/corridor over 2 m x0.7), checking Article 43 ventilation openings (5% for habitable rooms and toilets/bathrooms, kitchens 1/10 and >= 0.8 m2), sizing Article 44 natural-ventilation ducts, reading the Article 102 mechanical-ventilation rate table, Article 45 opening-to-boundary distances, and the Article 1(35) windowless-room triggers. Trigger words: 採光檢討、通風檢討、採光面積、有效採光、採光補正、居室採光、有效通風面積、浴廁通風、廚房通風、無窗戶居室、機械通風量、自然通風設備、第41條、第42條、第43條、第44條。"
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
verified:
  - { by: human:Archwiz-boss, at: 2026-09-28T00:00:00Z }
sources:
  - id: btr-dc
    resource: https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=D0070115
    title: 建築技術規則建築設計施工編（§1、§39-1～§45）
    last_modified: 2026-02-23
  - id: btr-eq
    resource: https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=D0070117
    title: 建築技術規則建築設備編（§100～§106）
    last_modified: 2022-12-29
metadata:
  audience: architects
  region: taiwan
  class: C
  status: verified
  data-currency: "2026-09-28"
---

# Daylight and Ventilation Review (建築技術規則 採光通風檢討)

## Overview

This skill checks the statutory minimums for daylight and ventilation openings of
rooms in Taiwan. It covers the Design & Construction volume, Chapter 2
"General Design Principles", Section 8 "日照、採光、通風、節約能源"
(Articles 39-1 to 45), plus the definitions in Article 1 and the mechanical
ventilation provisions of the Building Equipment volume (Articles 100-106).

All article text below was transcribed clause-by-clause from 全國法規資料庫 on
2026-09-28 (Design & Construction volume amended 民國 115-02-23; Equipment volume
amended 民國 111-12-29),[^btr-dc][^btr-eq] and re-checked against the official
text by a practicing architect on the same date — see Data Currency.

**Division of labor with other skills:**

- This skill = **statutory minimums** (pass/fail against the code).
- [smoke-exhaust-review](../../../../消防安全/排煙窗法規檢討/smoke-exhaust-review/SKILL.md) =
  what happens **after** a room is found to be a windowless room (無窗戶居室) —
  smoke exhaust and other Chapter 4 consequences.

Invoke this skill when:

- A floor plan needs a 採光／通風 check table for permit submission
- Deciding whether a room is a 居室 and which ratio applies
- A window faces a neighbor boundary, light well, or another block on the same site
- A room has no operable window and needs a natural or mechanical ventilation route
- Checking whether a room falls into 無窗戶居室 status

---

## Section 1: Scope — Is It a Habitable Room (居室)?

Article 1(19) [Verified 2026-09-28][^btr-dc]:

| Counted as 居室 | Not 居室 |
|---|---|
| Rooms used for living, working, assembly, entertainment, cooking (居住、工作、集會、娛樂、烹飪) | Entrance hall, corridor, stair hall, cloakroom, toilet/washroom, bathroom, storage, machine room, garage |

Proviso: in hotels, dwellings, apartment buildings and dormitories, the combined
area of cloakrooms and storage rooms should in principle not exceed 1/8 of that
floor's area (「以不超過該層樓地板面積八分之一為原則」). Oversized "storage" is a
common way a de facto bedroom escapes the daylight check — flag it.

Kitchens are 居室 (烹飪). Toilets and bathrooms are not 居室, but Article 43(1)
still sets their ventilation ratio (Section 5).

Floor area (樓地板面積) for every ratio below = Article 1(5): horizontal
projection within the centerline of the enclosing partitions.

---

## Section 2: Sunlight (日照) — Articles 39-1 and 40

| Article | Rule | Tag |
|---|---|---|
| §40 | A dwelling must have **at least one habitable room** whose window can receive direct sunlight | [Verified 2026-09-28] |
| §39-1 | The part of a new/extended building **above 21 m** must leave adjacent residential/commercial-zone sites **≥ 1 hour** of effective sunlight on the winter solstice | [Verified 2026-09-28] |

§39-1 exemptions (any one): single block whose north-facing projected width
≤ 10 m; facade set back ≥ 6 m from the north boundary with total north-facing
width ≤ 20 m (blocks whose outer-edge connecting angle ≥ 12.5° may be counted
separately); both sites commercial and a ≥ 3 m yard already left on the north
boundary under the urban plan. A boundary counts as "north" when its normal is
within 45° of true north. Multiple blocks on one site are checked together unless
the separation conditions of §39-1 paragraph 2 are met. Shadow-diagram method is
out of scope here.

---

## Section 3: Required Daylight Area — Article 41

Every 居室 must have daylight windows or openings. Minimum daylight area
[Verified 2026-09-28][^btr-dc]:

| Use | Min. daylight area / room floor area |
|---|---|
| Kindergarten and school classrooms | **1/5** |
| Dwelling habitable rooms, dormitory bedrooms, hospital wards, child-welfare facilities (health centers, orphanages, nurseries, elderly homes) | **1/8** |
| Any opening portion **within 75 cm above floor level** | **Not counted** |

Other 居室 (offices, shops, assembly rooms): §41 requires a daylight opening but
gives **no ratio**. Do not invent one. Their practical threshold is the
windowless-room test in Section 8 (effective daylight < 5% of floor area).

---

## Section 4: Effective Daylight Area — Article 42

Only openings inside the **effective daylight range** count, adjusted as follows
[Verified 2026-09-28][^btr-dc]:

### 4.1 H/D limit

H = height of the exterior wall of the building containing the 居室 (where the
opening has an eave above it, measured to the top of that part).
D = horizontal distance from that part to the facing neighbor boundary, another
block on the same site, or the facing part of the same block (e.g., a light well).

| Zoning | Max H/D |
|---|---|
| Residential, administrative, cultural-educational (住宅區、行政區、文教區) | **4** (D ≥ H/4) |
| Commercial (商業區) | **5** (D ≥ H/5); once D ≥ **5 m** no further increase is needed (§42(5)) |

### 4.2 Adjustments

| Condition | Effect | Clause |
|---|---|---|
| Wall faces a road, or permanent open space **≥ 6 m deep** | No setback needed; opening counts as effective | §42(2) |
| Skylight (天窗) | Effective area = opening area **× 3** | §42(3) |
| Balcony or external corridor **wider than 2 m** outside the opening (露臺 excluded) | Effective area = opening area **× 0.7** | §42(4) |
| Residential zone, building depth **> 10 m** | Rear/side windows on every floor must also be within the effective range | §42(6) |

Terrace (露臺) vs balcony (陽臺) follows Article 1(20): no cover directly above =
露臺; covered = 陽臺. A covered balcony > 2 m triggers ×0.7; an uncovered terrace
does not.

### 4.3 Calculation

```typescript
type Zone = "residential" | "administrative" | "cultural-educational" | "commercial";

interface Opening {
  area: number;             // m2, only the portion higher than 75 cm above floor
  isSkylight: boolean;
  deepBalconyOutside: boolean; // balcony or external corridor > 2 m, not a terrace
  facesRoadOrOpenSpace6m: boolean;
  H: number;                // m, per §42(1)
  D: number;                // m, per §42(1)
}

function inEffectiveRange(o: Opening, zone: Zone): boolean {
  if (o.facesRoadOrOpenSpace6m) return true;               // §42(2)
  if (zone === "commercial") return o.D >= 5 || o.H / o.D <= 5; // §42(1),(5)
  return o.H / o.D <= 4;                                    // §42(1)
}

function effectiveArea(o: Opening, zone: Zone): number {
  if (!inEffectiveRange(o, zone)) return 0;
  if (o.isSkylight) return o.area * 3;                      // §42(3)
  if (o.deepBalconyOutside) return o.area * 0.7;            // §42(4)
  return o.area;
}
// Pass §41 when sum(effectiveArea) >= floorArea * ratio (1/5 or 1/8)
```

Worked example (dwelling bedroom, residential zone): floor area 12 m² →
required 12 × 1/8 = 1.50 m². Window 1.8 m wide × 1.2 m high, sill at 0.9 m
→ whole window above 75 cm → 2.16 m². A 2.4 m-deep covered balcony outside →
2.16 × 0.7 = 1.51 m² ≥ 1.50 → passes, but only just. Same window with sill at
0.45 m: the lowest 0.30 m is excluded → 1.8 × 0.9 × 0.7 = 1.13 m² → fails.

Zones not in the table (工業區、農業區、非都市土地 etc.) and the exact starting
point for measuring H are not resolved by the article text alone — see To Verify.

---

## Section 5: Ventilation Openings — Article 43

Each 居室 needs windows/openings open directly to outside air, **or** a natural
ventilation device (§44), **or** mechanical ventilation per the Equipment volume
[Verified 2026-09-28][^btr-dc]:

| Room | Min. effective ventilation area | Waiver |
|---|---|---|
| General 居室, **and toilets/bathrooms** | **5%** (1/20) of room floor area | Compliant natural or mechanical ventilation installed |
| Kitchen | **1/10** of floor area **and ≥ 0.8 m²** | Compliant mechanical ventilation installed |
| Kitchen ≥ **100 m²** | Additionally needs a grease/fume exhaust system (排除油煙設備) per Equipment volume §103-106 | — (air-pollution law or local rules prevail if they provide otherwise, §43 para. 2) |
| Theater/cinema/performance/assembly seating, boiler rooms and workrooms with combustion equipment, whose ventilation area < 1/10 | **Must** have mechanical ventilation | Combustion appliances that take air directly from outside and exhaust directly outside without polluting indoor air |

"Effective ventilation area" (有效通風面積) is **not defined** in the article
text. Treat the operable, openable portion as the working assumption only and
label it — see To Verify.

---

## Section 6: Natural Ventilation Device — Article 44

When a room relies on a natural ventilation device instead of windows
[Verified 2026-09-28][^btr-dc]:

1. Inlet, outlet, and exhaust duct must be rain- and insect-proof.
2. Exhaust duct: non-combustible, as vertical as possible, straight to outside;
   no openings other than the top and one exhaust inlet.
3. Minimum duct effective cross-section:

```text
Av = Af / (250 × √h)

Av = effective duct cross-section (m²)
Af = room floor area (m²); if the room has other effective ventilation openings,
     Af = floor area − 20 × (that effective ventilation area)
h  = height from inlet center to duct top outlet center (m)
```

4. Inlet and outlet effective area each ≥ Av.
5. Inlet: in the part **below 1/2 of the ceiling height**, opening to space with
   direct air flow.
6. Outlet: **within 80 cm below the ceiling**, permanently open.

Worked example: windowless 20 m² room, h = 4 m →
Av = 20 / (250 × 2) = 0.040 m². Same room with a 0.5 m² effective window →
Af = 20 − 20 × 0.5 = 10 → Av = 10 / 500 = 0.020 m². (A 1.0 m² window already
meets 5% by itself and needs no device.)

---

## Section 7: Mechanical Ventilation — Equipment Volume §100-106

§100: mechanical ventilation referenced by §43 must follow this section.
§101 systems: (1) mechanical supply + mechanical exhaust; (2) mechanical supply +
natural exhaust; (3) natural supply + mechanical exhaust.
[Verified 2026-09-28][^btr-eq]

§102 minimum ventilation rate, m³/h per m² of floor area:

| Room use | Systems (1)(2) | System (3) |
|---|---|---|
| Bedroom, living room, private office (few occupants) | 8 | 8 |
| Office, reception room | 10 | 10 |
| Janitor, guard, mail, information rooms | 12 | 12 |
| Meeting room, waiting rooms (many occupants) | 15 | 15 |
| Exhibition room, barber/beauty salon | 12 | 12 |
| Department store, dance/chess/ball-game rooms, low-dust workrooms, printing/packing works | 15 | 15 |
| Smoking room, school and designated-occupancy dining halls | 20 | 20 |
| Commercial restaurant, bar, café | 25 | 25 |
| Theater/cinema/performance/assembly seating | 75 | 75 |
| Kitchen — commercial / non-commercial | 60 / 35 | 60 / 35 |
| Pantry — commercial / non-commercial | 25 / 15 | 25 / 15 |
| Cloakroom, changing room, washroom, generator/switch room > 15 m² | — | 10 |
| Tea room (茶水間) | — | 15 |
| Dwelling bathroom or toilet, darkroom, projection room | — | 20 |
| Public bathroom/toilet, workshops that may emit toxic or flammable gas | — | 30 |
| Battery room | — | 35 |
| Car garage | — | 25 |

"—" = the table gives no value for systems (1)(2); these rooms are listed only
under system (3) (natural supply + mechanical exhaust).

Worked example: dwelling bathroom 4 m², exhaust fan (system 3) →
4 × 20 = 80 m³/h minimum.

§103-106 (kitchen fume exhaust, relevant to §43(2)): hood steel ≥ 1.27 mm or
stainless ≥ 0.95 mm, hood lower edge ≤ 210 cm above floor, hood height ≥ 60 cm,
≥ 45 cm from combustibles; duct steel ≥ 1.58 mm or stainless ≥ 1.27 mm, shortest
route outside, rises ≥ 1 m above roof, outlet ≥ 3 m from neighbor boundary,
air inlets and ground; duct velocity ≥ 450 m/min; kitchens with a hood must have
mechanical make-up air. [Verified 2026-09-28][^btr-eq]

---

## Section 8: Windowless Room (無窗戶居室) — Article 1(35)

A 居室 is a windowless room if **any** of the following holds
[Verified 2026-09-28][^btr-dc]:

| # | Test | Threshold |
|---|---|---|
| 1 | Effective daylight area per §42 | **< 5%** of floor area |
| 2 | Openings to outside or to an effective fire-escape route | Height < 1.2 m **or** width < 75 cm (round: diameter < 1 m) |
| 3 | Room floor area **> 50 m²**: effective ventilation area at or within 80 cm below the ceiling | **< 2%** of floor area |

Note the gap: a dwelling bedroom needs 1/8 = 12.5% (§41), but the windowless
threshold is 5%. An office with 4% effective daylight has no §41 ratio to fail,
yet it becomes a windowless room and pulls in Chapter 4 obligations → hand off
to [smoke-exhaust-review](../../../../消防安全/排煙窗法規檢討/smoke-exhaust-review/SKILL.md).

---

## Section 9: Opening Position vs Boundaries — Article 45

[Verified 2026-09-28][^btr-dc]

| Situation | Rule |
|---|---|
| Door/window swing | Must not obstruct public traffic |
| Exterior wall directly on the neighbor boundary | No doors, windows, openings or balconies toward the neighbor — unless wall/balcony edge is **≥ 1 m** from the boundary, or built of non-see-through fixed glass block |
| Facing openings between blocks on one site, or facing parts of one block | Horizontal clear distance **≥ 2 m**; **≥ 1 m** if only one side has openings (fixed non-see-through glass block exempt) |
| Exhaust outlet toward neighbor / facing block | **≥ 2 m** from boundary or facing part |
| Operable windows in H-2, D-3, F-3 uses | Sill **≥ 1.10 m**; **≥ 1.20 m** on the 10th floor and above (exempt if adjacent to terrace, balcony, external corridor/stair, indoor light well, or with §38 railing or §108 emergency entry) |

The 1 m/2 m distances are a separate test from the §42 H/D range: a window 1 m
from the boundary may be allowed to exist (§45) and still not count as effective
daylight (§42).

---

## Section 10: AI Check Table

| Check | Condition | Level |
|---|---|---|
| Opening below 75 cm counted | Daylight area includes the portion ≤ 75 cm above floor | ERROR (§41(3)) |
| Ratio short | Dwelling/ward/dorm bedroom effective daylight < 1/8, classroom < 1/5 | ERROR (§41) |
| Out of range | Opening outside H/D limit and not facing road / ≥ 6 m open space, still counted | ERROR (§42(1)(2)) |
| Correction missed | Skylight not ×3, or balcony/corridor > 2 m not ×0.7 | ERROR (§42(3)(4)) |
| Toilet unventilated | Toilet/bathroom < 5% ventilation area and no exhaust fan/device | ERROR (§43(1)) |
| Kitchen short | Kitchen ventilation < 1/10 or < 0.8 m² and no mechanical ventilation | ERROR (§43(2)) |
| Fan undersized | Mechanical rate < §102 table × floor area | ERROR (Equipment §102) |
| Windowless drift | Office/shop effective daylight < 5%, or > 50 m² with < 2% high-level ventilation | WARNING → route to smoke-exhaust-review (§1(35)) |
| Oversized storage | Cloakroom + storage > 1/8 of floor in a dwelling | WARNING — possible disguised 居室 (§1(19)) |
| H measured ambiguously | H start point or zoning not in §42 table | WARNING — gray zone, see To Verify |
| Local add-on unchecked | Municipal review rules not consulted | INFO — declare the unchecked track |

---

## Section 11: Common Pitfalls

1. **Whole window area counted** — the part within 75 cm of the floor is excluded
   (§41(3)); floor-to-ceiling glazing loses its bottom 75 cm.
2. **Deep balcony ignored** — a covered balcony or external corridor over 2 m
   cuts effective area to 70%; a terrace (no roof) does not.
3. **Light-well windows counted at full value** — the light well is "the facing
   part of the same block"; D is the well width and H/D must still hold.
4. **Bathroom forgotten** — not a 居室, but §43(1) names 浴廁 explicitly: 5% or a
   fan sized at 20 m³/h·m² (dwelling) / 30 (public).
5. **Kitchen 0.8 m² floor** — small kitchens hit the absolute minimum before
   the 1/10 ratio.
6. **Office treated as exempt** — no §41 ratio, but the 5% windowless-room test
   still bites.
7. **Using design-guide ratios as law** — 1/6, 1/7, window-to-wall ratios, daylight
   factors are not in §41-§44.

---

## Data Currency

- Source: 建築技術規則建築設計施工編 §1(5)(19)(20)(35), §39-1～§45（修正日期 民國 115-02-23）；
  建築技術規則建築設備編 §100～§106（修正日期 民國 111-12-29）— 全國法規資料庫
- Transcribed: 2026-09-28 by an AI agent from the official consolidated text;
  re-checked by a practicing architect (human:Archwiz-boss) on 2026-09-28
- Per-article amendment history was **not** confirmed (the history page returned
  identical content for §41-§44 and was discarded)
- Volatility: MEDIUM — the Design & Construction volume is amended frequently;
  re-verify before permit submission

## To Verify

- [ ] §42 attachment (附件 figure) not transcribed — it likely defines where H is
  measured from (floor, sill, or ground). Searched: article text only. Next:
  download the §42 attachment from 全國法規資料庫, or `taiwan-building-code_search_building_interpretations(query="有效採光 H/D 外牆高度 起算")`.
- [ ] Zones not in the §42 table (工業區、農業區、特定專用區、非都市土地) — no rule
  found in the article. Next: search 內政部函釋; otherwise 函詢 local building authority.
- [ ] Definition of 有效通風面積 (sliding vs casement windows, louvers) — not
  in §1 or §43. Next: interpretations search / local review standards.
- [ ] §42(4) wording 「寬度超過二公尺以上」 — whether exactly 2.00 m triggers ×0.7.
  Treat as gray zone; conservative lean: apply ×0.7 at 2.00 m.
- [ ] Municipal review standards (e.g., 臺北市、新北市、臺中市 建管審查基準) on
  daylight/ventilation drawing formats and interpretations — unchecked track.
- [ ] Interaction with Chapter 17 (綠建築) of the same volume — out of scope here,
  not checked.

## MCP Tool Examples

```python
taiwan-building-code_search_building_code(query="採光 第41條", limit=5)
taiwan-building-code_search_building_code(query="有效通風面積 第43條", limit=5)
taiwan-building-code_search_building_interpretations(query="有效採光面積 陽臺 天井")
taiwan-building-code_search_building_interpretations(query="無窗戶居室 採光 百分之五")
```

## Related Skills

- [smoke-exhaust-review](../../../../消防安全/排煙窗法規檢討/smoke-exhaust-review/SKILL.md) — consequences once a room is 無窗戶居室
- [height-ratio-front-road-review](../../高度比與面前道路認定/height-ratio-front-road-review/SKILL.md) — road-facing and setback geometry that also feeds §42 "faces a road"
- [regulation-currency-check](../../../../../建築顧問方法論/法規時效性查證/regulation-currency-check/SKILL.md) — re-verify before permit use
- [boundary-cases-and-escalation](../../../../../建築顧問方法論/邊界案例與函詢時機/boundary-cases-and-escalation/SKILL.md) — format for the To Verify gray zones

[^btr-dc]: 建築技術規則建築設計施工編，全國法規資料庫 https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=D0070115 （修正日期 民國 115-02-23；擷取 2026-09-28）
[^btr-eq]: 建築技術規則建築設備編，全國法規資料庫 https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=D0070117 （修正日期 民國 111-12-29；擷取 2026-09-28）
