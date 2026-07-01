---
name: balcony-lobby-far-recalculation
description: "This skill should be used when calculating Taiwan FAR gross-floor-area inclusion for balcony and shared stair/elevator lobby areas under Building Technical Regulations Article 162, including the separate 10% balcony cap, separate 10% lobby cap, combined 15% balcony-plus-lobby cap, and avoiding double-counting already-included excess area."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
metadata:
  audience: architects
  region: taiwan
---

# Balcony and Lobby FAR Recalculation

## Overview

Use this skill when reviewing Taiwan building-permit FAR calculations for:

- Balcony area (陽臺面積) exemption up to 10% of the floor area
- Shared stair/elevator lobby area (梯廳面積) exemption up to 10% of the floor area
- Combined balcony plus lobby exemption up to 15% of the floor area
- Recalculated area that must be included in FAR gross floor area (回計容積面積)

The key practitioner issue is avoiding double-counting: once balcony or lobby area has already exceeded its own 10% cap and has been included in FAR, the combined 15% check should use only the remaining exempt candidates, not the original raw balcony plus lobby total.

## Legal Basis

Building Technical Regulations, Design and Construction, Article 162, Paragraph 1, Subparagraph 1:

- Balcony area within 10% of that floor's area may be excluded from FAR gross floor area.
- Shared stair/elevator lobby area within 10% of that floor's area may be excluded, provided the lobby clear depth is at least 2 m.
- If balcony plus lobby area exceeds 15% of that floor's area, the excess must be included.

Always verify local review-sheet conventions and current official text before final filing.

## Inputs

| Symbol | Meaning |
|---|---|
| `F` | Floor area for the reviewed story |
| `B` | Total balcony area for the story |
| `L` | Total eligible shared stair/elevator lobby area for the story |
| `Cap10` | `F * 0.10` |
| `Cap15` | `F * 0.15` |

Only include lobby area in `L` after confirming the lobby meets basic eligibility, especially the 2 m finished clear-depth requirement.

## Algorithm

```text
Cap10 = F * 0.10
Cap15 = F * 0.15

balcony_excess_10 = max(B - Cap10, 0)
lobby_excess_10 = max(L - Cap10, 0)

balcony_exempt_candidate = min(B, Cap10)
lobby_exempt_candidate = min(L, Cap10)

combined_exempt_candidate = balcony_exempt_candidate + lobby_exempt_candidate
combined_excess_15 = max(combined_exempt_candidate - Cap15, 0)

total_far_included_area =
  balcony_excess_10
  + lobby_excess_10
  + combined_excess_15

final_exempt_area = B + L - total_far_included_area
```

## Review Logic

1. Check balcony against the 10% cap and record balcony excess.
2. Check lobby against the 10% cap and record lobby excess.
3. Cap each item at its 10% exempt candidate before the combined 15% check.
4. Check `min(B, Cap10) + min(L, Cap10)` against `Cap15`.
5. Add the two separate 10% excess values and the combined 15% excess value.

Do not calculate separate 10% excess first and then check raw `B + L` against 15%, because that can include the same excess area twice.

## Decimal Handling

Use one decimal convention throughout the calculation sheet:

- Calculate formulas with raw unrounded values.
- Display output fields to two decimal places.
- Round to the nearest two decimal places; do not truncate (無條件捨去).

If `Cap10` or `Cap15` is rounded before downstream formulas, the result can differ by 0.01 m2 from calculating with raw values and rounding only at output. Prefer raw-value calculations first, then final output rounding.

## Worked Examples

### Example A

```text
F = 752.58
L = 78.69
B = 2.70

Cap10 = 75.258
Cap15 = 112.887

lobby_excess_10 = 78.69 - 75.258 = 3.432
balcony_excess_10 = 0

combined_exempt_candidate = 75.258 + 2.70 = 77.958
combined_excess_15 = 0

total_far_included_area = 3.432
```

With two-decimal rounding, report `3.43 m2`.

### Example B

```text
F = 447.48
L = 40.37
B = 36.43

Cap10 = 44.748
Cap15 = 67.122

lobby_excess_10 = 0
balcony_excess_10 = 0

combined_exempt_candidate = 40.37 + 36.43 = 76.80
combined_excess_15 = 76.80 - 67.122 = 9.678
```

With two-decimal rounding, report `9.68 m2`.

### Example C: Both Items Exceed 10%

```text
F = 500.00
L = 62.00
B = 58.00

Cap10 = 50.00
Cap15 = 75.00

lobby_excess_10 = 12.00
balcony_excess_10 = 8.00

combined_exempt_candidate = 50.00 + 50.00 = 100.00
combined_excess_15 = 25.00

total_far_included_area = 12.00 + 8.00 + 25.00 = 45.00
final_exempt_area = 62.00 + 58.00 - 45.00 = 75.00
```

This preserves the 15% final exempt ceiling without double-counting the 20 m2 that was already included by the separate 10% checks.

## Output Checklist

- Confirm lobby clear depth and eligibility before including lobby area as an exempt candidate.
- Show `Cap10` and `Cap15` for each floor.
- Show separate balcony and lobby 10% excess values.
- Show combined 15% excess using the capped exempt candidates.
- State the decimal rule: calculate with raw values first, then round output fields to two decimal places.

## Tool Examples

- `taiwan-building-code_search_building_code(query: "建築技術規則 第162條 陽臺 梯廳 百分之十五", limit: 5)`
- `taiwan-building-code_search_building_interpretations(query: "陽臺 梯廳 容積 15%", limit: 5)`

## References

- Building Technical Regulations, Design and Construction, Article 162: FAR gross-floor-area calculation and exemption items
- Local building-permit FAR calculation sheets and review conventions
