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
| `Cap10` | `F * 0.10`, rounded to two decimals before use |
| `Cap15` | `F * 0.15`, rounded to two decimals before use |

Only include lobby area in `L` after confirming the lobby meets basic eligibility, especially the 2 m finished clear-depth requirement.

## Algorithm

```text
Cap10 = round(F * 0.10, 2)
Cap15 = round(F * 0.15, 2)

balcony_exempt_candidate = min(B, Cap10)
balcony_excess_10 = B - balcony_exempt_candidate

lobby_exempt_candidate = min(L, Cap10)
lobby_excess_10 = L - lobby_exempt_candidate

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

- Round `Cap10 = F * 0.10` to two decimal places before using it as the 10% exemption cap.
- Round `Cap15 = F * 0.15` to two decimal places before using it as the combined 15% exemption cap.
- Use the rounded `Cap10` to split each item, so `exempt area + included excess area = original balcony or lobby area` in the review table.
- Display other output fields to two decimal places.

Use the usual half-up engineering-table convention for midpoint cases.

## Worked Examples

### Example A

```text
F = 752.58
L = 78.69
B = 2.70

Cap10 = round(752.58 * 0.10, 2) = 75.26
Cap15 = round(752.58 * 0.15, 2) = 112.89

lobby_excess_10 = 78.69 - 75.26 = 3.43
balcony_excess_10 = 0

combined_exempt_candidate = 75.26 + 2.70 = 77.96
combined_excess_15 = 0

total_far_included_area = 3.43
```

With two-decimal rounding, report `3.43 m2`.

### Example B

```text
F = 447.48
L = 40.37
B = 36.43

Cap10 = round(447.48 * 0.10, 2) = 44.75
Cap15 = round(447.48 * 0.15, 2) = 67.12

lobby_excess_10 = 0
balcony_excess_10 = 0

combined_exempt_candidate = 40.37 + 36.43 = 76.80
combined_excess_15 = 76.80 - 67.12 = 9.68
```

With two-decimal rounding, report `9.68 m2`.

### Example C: Both Items Exceed 10%

```text
F = 500.00
L = 62.00
B = 58.00

Cap10 = round(500.00 * 0.10, 2) = 50.00
Cap15 = round(500.00 * 0.15, 2) = 75.00

lobby_excess_10 = 12.00
balcony_excess_10 = 8.00

combined_exempt_candidate = 50.00 + 50.00 = 100.00
combined_excess_15 = 25.00

total_far_included_area = 12.00 + 8.00 + 25.00 = 45.00
final_exempt_area = 62.00 + 58.00 - 45.00 = 75.00
```

This preserves the 15% final exempt ceiling without double-counting the 20 m2 that was already included by the separate 10% checks.

## Validation Cases

Use these cases to verify that each 10% item split satisfies `exempt + included = original area` after the 10% cap is rounded.

| Case | F | Cap10 | Item | Original | Exempt | Included | Sum |
|---|---:|---:|---|---:|---:|---:|---:|
| A lobby over 10% | 752.58 | 75.26 | Lobby | 78.69 | 75.26 | 3.43 | 78.69 |
| A balcony under 10% | 752.58 | 75.26 | Balcony | 2.70 | 2.70 | 0.00 | 2.70 |
| B lobby under 10% | 447.48 | 44.75 | Lobby | 40.37 | 40.37 | 0.00 | 40.37 |
| B balcony under 10% | 447.48 | 44.75 | Balcony | 36.43 | 36.43 | 0.00 | 36.43 |
| Exactly rounded 10% cap | 333.35 | 33.34 | Lobby | 33.34 | 33.34 | 0.00 | 33.34 |
| Just above rounded 10% cap | 333.35 | 33.34 | Balcony | 33.35 | 33.34 | 0.01 | 33.35 |
| Both items over 10% | 500.00 | 50.00 | Lobby | 62.00 | 50.00 | 12.00 | 62.00 |
| Both items over 10% | 500.00 | 50.00 | Balcony | 58.00 | 50.00 | 8.00 | 58.00 |

## Output Checklist

- Confirm lobby clear depth and eligibility before including lobby area as an exempt candidate.
- Show `Cap10` and `Cap15` for each floor.
- Show separate balcony and lobby 10% excess values.
- Show combined 15% excess using the capped exempt candidates.
- State the decimal rule: round `Cap10` and `Cap15` to two decimals before using them as caps.

## Tool Examples

- `taiwan-building-code_search_building_code(query: "建築技術規則 第162條 陽臺 梯廳 百分之十五", limit: 5)`
- `taiwan-building-code_search_building_interpretations(query: "陽臺 梯廳 容積 15%", limit: 5)`

## References

- Building Technical Regulations, Design and Construction, Article 162: FAR gross-floor-area calculation and exemption items
- Local building-permit FAR calculation sheets and review conventions
