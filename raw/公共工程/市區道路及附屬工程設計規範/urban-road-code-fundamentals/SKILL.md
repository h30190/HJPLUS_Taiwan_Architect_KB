---
type: Skill
name: urban-road-code-fundamentals
description: "This skill should be used to establish which instrument and which version govern before applying any Taiwan Urban Road Design Code (市區道路及附屬工程設計規範) dimension: the standard-versus-code hierarchy, the 應/不得/宜/不宜 wording rules, the provincial-highway co-alignment rule, road classification and design speed, and the full chapter map. Invoke it when a reviewer cites 市區道路及附屬工程設計標準 or 設計規範 and it is unclear which applies, when a road section is shared with a highway, or as the shared basis before the pedestrian-accessibility or landscape-planting skills. It does not carry the pedestrian or planting dimensions themselves."
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

# Urban Road Design Code: Fundamentals

## Overview

Taiwan regulates urban roads through a tiered instrument stack, and most wrong answers come not
from misreading a clause but from applying the wrong instrument, the wrong version, or the wrong
jurisdiction. This skill is the shared basis for every urban-road question: it settles which
document governs before any dimension is quoted.

It carries the horizontal rules only. Pedestrian and accessibility dimensions live in
`urban-road-pedestrian-accessibility`; planting and landscape dimensions in
`urban-road-landscape-planting`. Both of those open by applying the rules defined here.

For an architect, the usual entry point is not designing a road but confirming that a
building-side interface (sidewalk frontage, vehicle crossing, road-fronting planting) does not
conflict with the code, or reading a civil consultant's drawings on a development that includes
road works. This skill answers "which rule governs, and is this even an urban-road question."

## Legal Hierarchy

| Tier | Instrument | Nature | Binding force |
|---|---|---|---|
| 1 | 市區道路條例 §32(1) | Statute, delegating authority | Binding |
| 2 | 市區道路及附屬工程設計標準 | Regulation issued by MOI[^std-2021] | Binding, directly enforceable |
| 3 | 市區道路及附屬工程設計規範 | Technical code issued under 設計標準 §29[^code-2026] | Flexible, principle-based; values set at the lower bound of the applicable range |

When Tier 2 and Tier 3 conflict on the same item, Tier 2 prevails. Flag the discrepancy rather than
silently picking one. The known live example is the tree pit: 設計標準 §21(4) says pit area shall
be 1.5 m² **or more**, while 設計規範 §16.2 says clear area shall **exceed** 1.5 m². The standard
outranks the code.

For multi-regime conflicts beyond this code (fire, accessibility dual-track, national-versus-local),
defer to the KB methodology skill
[regulation-hierarchy-and-conflicts](../../../建築顧問方法論/法源位階與衝突處理/regulation-hierarchy-and-conflicts/SKILL.md).

## Normative Language Rules

Appendix 4 item 1 defines the code's own modal vocabulary.[^code-2026] Apply it before quoting any
value, in this skill or the two that build on it.

| Term | Default position | Exception | How to report it |
|---|---|---|---|
| 應 | Must do | None | Requirement; cite the clause |
| 不得 | Must not do | None | Prohibition; cite the clause |
| 宜 | Should do (default duty to comply) | Deviation allowed with justified reason | Recommended, not mandatory; ask for the reason if deviated |
| 不宜 | Should not do (default prohibition) | Deviation allowed with justified reason | Discouraged as a default ban, not a soft hint; the burden to justify is heavier than a plain 宜 |

The four terms are not two soft and two hard. The real split is whether an exception exists:
應/不得 have **no** exception; 宜/不宜 carry a default position that holds unless a justified reason
is shown. Within that pair, 宜 and 不宜 are mirror images, not a positive-versus-negative
suggestion: 宜 means do it by default, 不宜 means do not do it by default. Treat a 不宜 breach as a
default prohibition the designer must actively justify, not merely as something "not encouraged".

"以上" and "以下" are inclusive of the stated number. Never convert a 宜 or 不宜 value into an
ERROR-level finding: both keep the justified-reason opening, which is the difference from 應/不得.
That is the single most common way an AI answer becomes indefensible in a design review.

## Jurisdiction: Is This an Urban Road?

Urban roads sit under MOI (國土管理署); highways under MOTC (公路局). The two systems have different
authorities, legal bases and dimensions, so the first question is always which system applies.

**Co-alignment rule.** Where an urban road runs shared with a provincial highway, the governing
design standard is determined by 公路修建養護管理規則 §31 and 市區道路條例 §18, per Appendix 4
item 2.[^code-2026] Resolve jurisdiction with those two provisions before quoting any dimension.
This is a determinate rule, not a judgement call.

**Local variation.** Appendix 5 lists Taipei's and Kaohsiung's own road design instruments as
source literature, and the code allows competent authorities to issue their own manuals and
standard drawings. A municipality may set stricter values. Confirm local rules before treating a
national floor as the final answer.

## Road Classification and Cross-Section (Part 1)

Needed to pick the right value in the downstream skills, since several thresholds vary by road
class.

- Functional classes: expressway (快速道路), primary (主要道路), secondary (次要道路), service road
  (服務道路). Design speed and cross-section elements follow the class (§5, §7).
- Cross-section is assembled from defined units: carriageway, shoulder, bicycle lane, sidewalk,
  traffic island, public utility strip, parking bay, drainage, underground ducts (§7).
- Right-of-way may be widened beyond the running-lane need to provide space for stormwater
  retention, ecological corridors, school-zone walking, commercial activity, landmarks and
  landscape features (§7, planning principles).

Detailed geometric values (lane widths, sight distance, superelevation, vertical curves,
intersections, bicycle facilities) are civil-engineering scope and are held at chapter level in
`references/chapter-map.md`, not carried here.

## Chapter Map

The code runs to three parts, twenty chapters and five appendices. Full map, plus chapter-level
summaries for every chapter an architect does not routinely design but may need to read on a
civil consultant's drawings (drainage, subgrade, pavement, bus stops, pedestrian bridges, traffic
calming, bridges, tunnels, lighting, traffic devices, ducts), is in
[references/chapter-map.md](references/chapter-map.md).

Which skill owns what:

| Topic | Owning skill |
|---|---|
| Which instrument or version governs, wording, co-alignment, classification | this skill |
| Sidewalk clear width, slope, vehicle crossings, public utility strip, accessibility, kerbs | `urban-road-pedestrian-accessibility` |
| Tree pits, spacing, soil depth, species, sight-line planting, island planting, landscape/ecology | `urban-road-landscape-planting` |
| Geometry, drainage, structure, road furniture (reference only) | `references/chapter-map.md` |

## Data Currency

- Source: 市區道路及附屬工程設計規範, consolidated text as amended 2026-04-23; 市區道路及附屬工程
  設計標準 §2, §16, §21, §29, as amended 2021-08-11
- Verified: 2026-08-15, by clause-by-clause comparison against the consolidated code text and the
  Ministry of Justice law database entry for the regulation
- Code amendment history: issued 1998-04-29 (台內營字第0980803106號); amended 2015-07-22
  (台內營字第1040810606號); 2022-02-10 (台內營字第1100819869號); 2024-09-12 (台內國字第1130808877號);
  2026-04-23
- Volatility: MEDIUM to HIGH. Four amendments in twelve years, three since 2022.

## To Verify

- [ ] Add the MOI order number and official file URL for the 2026-04-23 amendment; the consolidated
  text was supplied by a contributor, and the agency listing consulted on 2026-08-15 still showed
  2024-09-12 as the latest entry.
- [ ] Add law database URLs for 市區道路條例 §18 and §32, and 公路修建養護管理規則 §31, to `sources`,
  so the co-alignment rule is independently traceable.
- [ ] Confirm the current text of 設計標準 §16 and §29 against the law database; only §2 and §21 were
  checked directly.

## MCP Tool Examples

```python
# Confirm the delegating regulation
taiwan-building-code_search_building_code(query="市區道路及附屬工程設計標準 第29條 授權", limit=10)

# Resolve a co-aligned section before applying dimensions
taiwan-building-code_search_building_code(query="公路修建養護管理規則 第31條 市區道路條例 第18條")
```

## Related Skills

- [urban-road-pedestrian-accessibility](../urban-road-pedestrian-accessibility/SKILL.md) — sidewalk,
  public utility strip, accessibility and kerb dimensions at the building-side interface.
- [urban-road-landscape-planting](../urban-road-landscape-planting/SKILL.md) — road-fronting
  planting, tree pits, soil depth and sight-line limits.
- [regulation-hierarchy-and-conflicts](../../../建築顧問方法論/法源位階與衝突處理/regulation-hierarchy-and-conflicts/SKILL.md)
  — the general method for multi-regime conflicts.

## Additional Resources

- Human-facing overview in Traditional Chinese: [domain.md](../domain.md)

[^std-2021]: 市區道路及附屬工程設計標準, amended 2021-08-11.
[^code-2026]: 市區道路及附屬工程設計規範, consolidated text as amended 2026-04-23, issued by the Ministry of the Interior.
