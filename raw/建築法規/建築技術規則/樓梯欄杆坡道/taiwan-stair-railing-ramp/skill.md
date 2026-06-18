---
name: taiwan-stair-railing-ramp
description: "This skill should be used when checking stair dimensional compliance for buildings in Taiwan — minimum stair-and-landing width, riser height, tread depth by building-use category, and the critical handrail-encroachment rule (clear width must remain >= 75 cm regardless of handrails), per Taiwan Building Technical Regulations (Design & Construction) Article 33, Chapter 2 Section 7 (Stairs, Railings, Ramps, Articles 33-39). Railings (Art. 38), handrails (Art. 37) and ramps (Art. 39) are stubbed for later completion."
user-invocable: true
---

# Taiwan Stair / Railing / Ramp Compliance (建築技術規則 §33–39)

## Overview

This skill evaluates stair geometry compliance under Taiwan's Building Technical
Regulations (Design & Construction), Chapter 2 "General Design Principles",
Section 7 "Stairs, Railings, Ramps" (Articles 33–39). It should be invoked when:

- Determining the minimum required stair / landing width for a building
- Checking riser height (級高) and tread depth (級深) limits
- Resolving whether a handrail eats into the legally required width
- Classifying a building into the correct Article 33 use category

**Current scope:** Article 33 (stair dimensions) is fully documented. Articles
34/37/38/39 (exemptions, handrails, railings, ramps) are stubs — see Section 4.

---

## Section 1: Article 33 — Width / Riser / Tread Table

Minimum dimensions depend on the building-use category. Pick the matching row.

| # | Use category (用途類別) | Stair & landing width | Riser (級高) | Tread (級深) |
|---|--------------------------|-----------------------|--------------|--------------|
| 1 | Stairs for children (elementary schools etc.) | >= 140 cm | <= 16 cm | >= 26 cm |
| 2 | School halls, hospitals, theaters, cinemas, dance halls, markets, department stores, assembly halls, amusement venues, etc. | >= 140 cm | <= 18 cm | >= 26 cm |
| 3 | Floors where any single floor's habitable area > 200 m², or a basement floor > 200 m² | >= 120 cm | <= 20 cm | >= 24 cm |
| 4 | All other buildings (incl. ordinary residences / 住宅) | **>= 75 cm** | <= 20 cm | >= 21 cm |

Residences fall into category 4 — the 75 cm baseline.

---

## Section 2: The Handrail-Encroachment Rule (the part people get wrong)

Article 33 proviso (verbatim):

> 「樓梯及平臺寬度二側各十公分範圍內，得設置扶手或高度五十公分以下供行動不便者
> 使用之昇降軌道；樓梯及平臺最小淨寬仍應為七十五公分以上。」

Translated mechanism:

1. The table width (140 / 120 / 75) is the **nominal** stair-and-landing width.
2. A handrail (or a <=50 cm assistive lift rail) may sit **within 10 cm on each
   side** of that nominal band — i.e. the handrail is *allowed to be counted into*
   the nominal width, not added on top of it.
3. **But in every case the actual clear (net) width must stay >= 75 cm.**

```typescript
interface StairWidthCheck {
  nominalWidth: number;          // cm — required by Article 33 category
  handrailEncroachLeft: number;  // cm — handrail projection into the band (<=10)
  handrailEncroachRight: number; // cm — (<=10)
}

function clearWidth(s: StairWidthCheck): number {
  return s.nominalWidth - s.handrailEncroachLeft - s.handrailEncroachRight;
}

// Compliant only if BOTH conditions hold:
//   each encroachment <= 10 cm  AND  clearWidth >= 75 cm
function isCompliant(s: StairWidthCheck): boolean {
  const encroachOk = s.handrailEncroachLeft <= 10 && s.handrailEncroachRight <= 10;
  return encroachOk && clearWidth(s) >= 75;
}
```

### Why 75 behaves differently from 120/140

- **Category 4 (75 cm):** the clear-width floor (75) *equals* the nominal width.
  Any handrail encroachment would push clear width below 75 → fails. So a handrail
  must sit **outside** the 75 → the 75 is effectively a *clear* dimension and the
  structural opening = 75 + handrails. (Practitioner rule of thumb: "75 是有效淨寬，
  扶手突出後不足 75 就不行".)
- **Categories 1–3 (120 / 140):** plenty of slack. 120 − 10 − 10 = 100 >= 75, so
  handrails on both sides *may* be counted into the nominal width.

### Caution: 90 cm outdoor stairs are not "always count the handrail"

Outdoor direct stairs may be reduced to >= 90 cm (separate provision). But
90 − 10 − 10 = 70 < 75 → you cannot discount handrails on both sides; at most one
side (90 − 10 = 80 >= 75). The real test is always "clear width after handrails
>= 75 cm", not the width tier.

---

## Section 3: Related Article 33 notes (verify exact text before relying)

- Outdoor direct stairs (戶外直通樓梯) may be reduced to **>= 90 cm**.
- Stairs **>= 3 m wide** generally require an intermediate handrail, unless riser
  <= 15 cm and tread >= 30 cm. (Commonly cited with §33/§37 — confirm placement
  when Section 7 is fully built out.)

---

## Section 4: Stubs — to be completed

| Article | Topic | Status |
|---------|-------|--------|
| §34 | Cases where Art. 33 width does not apply | TODO |
| §37 | Handrails (扶手) — height, continuity, intermediate rails | TODO |
| §38 | Railings / guards (欄杆) — height, anti-climb | TODO |
| §39 | Ramps (坡道) — slope, surface, width | TODO |

---

## Cross-references

- Accessible stairs / accessible handrails → `taiwan-accessibility`
  (`raw/建築法規/無障礙設計/`). Do not duplicate here; link there.
- Means-of-egress stairs (直通樓梯 / 特別安全梯) and evacuation →
  `raw/建築法規/消防安全/`.
- General spatial / circulation planning → `spatial-planning`
  (`raw/建築設計與規劃/設計理論/`).

## MCP Tool Examples

- `taiwan-building-code_search_building_interpretations(query: "樓梯寬度 第33條", limit: 5)`
- `taiwan-building-code_search_building_code(query: "樓梯", limit: 10)`

## Source

- 建築技術規則建築設計施工編 §33 — 全國法規資料庫
  https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=D0070115&flno=33
