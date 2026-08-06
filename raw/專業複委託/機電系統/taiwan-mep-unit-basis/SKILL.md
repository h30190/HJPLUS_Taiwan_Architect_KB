---
name: taiwan-mep-unit-basis
description: "This skill should be used when you need the correct UNIT for a Taiwan MEP quantity (airflow, static pressure, water pressure, pipe diameter, per-person water demand, storage-tank volume, drainage slope, lighting load) together with its statutory source, OR when you need to know at which DESIGN STAGE a MEP regulation is checked and whether it is MANDATORY / needs a licensed-engineer seal. It owns the cross-system UNIT CONVENTIONS (metric measurement + kgf/cm² pressure + imperial pipe designations) and the regulation→stage→mandatory→responsibility-gap map; per-system detailed design numbers live in the deep-dive skills. Keywords: MEP unit, kg/cm2, m3/h, m/min, 英吋, 度量衡法, design stage, mandatory, 技師簽證."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
metadata:
  audience: architects
  region: taiwan
  class: C
  status: unverified
  data-currency: "2026-08-06"
---

# Taiwan MEP Unit & Regulatory-Stage Basis

## Overview
Give the **correct unit + statutory source**, and the **design stage / mandatory status**, for Taiwan MEP quantities across all systems (HVAC, water supply, drainage, fire, electrical).

This skill owns two things no per-system skill covers:
1. **Unit conventions** — Taiwan MEP is NOT pure SI. Three coexist, all legal (度量衡法 §10): metric measurement + **pressure in kgf/cm²** + **pipe designations of imperial lineage** (the code itself prints "100 公釐(4 英吋)管").
2. **Regulation → design stage → mandatory → engineer seal** map, plus the responsibility gap.

**Division of labor** (see Related Skills): per-system DESIGN NUMBERS live elsewhere — plumbing slopes/seals/tank ratios in `taiwan-plumbing-design-codes`, wiring ampacity in `taipower-indoor-wiring-ampacity`, overall MEP design in `building-services` (this skill fills that skill's "Taiwan codes" TODO for units and stages).

## Execution Steps
1. Identify the quantity/system → return the UNIT **with its statutory citation** (never a bare unit).
2. If asked about enforcement/timing → give the design stage + mandatory status + whose seal (table in domain.md §二).
3. For per-system design NUMBERS (slope, seal depth, tank ratio, ampacity) → defer to the Related Skill and say so.
4. Always surface the relevant trap (kg/cm²↔Pa; imperial inch printed in the code; 寸=inch not 台寸; RT-ton ambiguity).

## Requirements & Constraints
- No external assets. Pairs with MCP tools for verification (see below).

## Worked Example
**Q: "台灣排煙風速用什麼單位?"**
- Rule: 建築技術規則建築設備編 §106 — 排煙管內風速「每分鐘不得小於四五○公尺」.
- Result: **m/min（公尺/分鐘）**, NOT m/s. Revit shows SI m/s → convert: 450 m/min = 7.5 m/s.

**Q: "給水管最低水壓?"**
- Rule: 給水排水設備設計技術規範 3.4.4（水栓≥0.3、沖洗閥≥1.0 kg/cm²）; 設備編 §46（消防栓≥1.7 kg/cm²）.
- Result: unit is **kgf/cm²（工程制）**, NOT Pa/psi. Convert for Revit: 1 kgf/cm² ≈ 98.07 kPa.

## Common Pitfalls

### Pitfall: assuming Taiwan MEP is all-SI / pressure in Pa
- **Severity**: 🟡 rework risk
- **When it bites**: matching Revit output (Pa) to a Taiwan spec sheet (kg/cm²); reading fan curves (mmAq).
- **Wrong**: report pressure in Pa as if that is the statutory unit.
- **Right**: statutory pressure is **kgf/cm²**（設備編 §46; 技術規範 3.4.4/3.4.6）; convert (1 kgf/cm² ≈ 98,067 Pa; fan side mmAq, 1 mmAq ≈ 9.8 Pa).

### Pitfall: treating "寸/吋" pipe as metric or as 台寸
- **Severity**: 🟡 rework risk
- **When it bites**: reading pipe callouts; the code prints "100 公釐(4 英吋)管".
- **Wrong**: 1寸 = 3.03 cm（台寸）, or assuming all-metric with no imperial.
- **Right**: pipe「寸」= English inch (2.54 cm), 分 = ⅛"; 4分=½"=15A, 1寸=1"=25A. Legal per 度量衡法 §10（通用單位）.

## Data Currency
- Source: 建築設備編 §43/§46/§102/§106（D0070117）; 度量衡法 §10（J0100052）; 用戶用電設備裝置規則 §36（J0030018）; 給水排水設備設計技術規範 3.2.3/3.4.4/3.4.6/附錄（nlma.gov.tw / glrs.moi.gov.tw）; 節能標準 D0070208; 計費辦法 §6（A0030077）.
- Verified: 2026-08-06 — units and key thresholds read from primary law text (law.moj.gov.tw; 技術規範 PDF via nlma.gov.tw / glrs.moi.gov.tw, pdftotext).
- Volatility: MEDIUM — article/point numbers shift on amendment; re-verify the clause number before quoting verbatim.

## To Verify
- [ ] Per-building-type per-person water demand values (L/人·日) — unit confirmed; per-type numbers from secondary summaries, confirm against 技術規範 附錄 表 A-1.
- [ ] Exact point numbers for storage-tank ratios and slope tables — cross-check current amendment.
- [ ] Whether HVAC static pressure has any statutory unit (currently practice mmAq only).

## MCP Tool Examples
```python
# Verify the ventilation-airflow clause and its unit
taiwan-building-code_search_building_code(query="建築設備編 第102條 通風量 立方公尺 每小時", limit=10)
# Verify the statutory water-pressure unit
taiwan-building-code_search_building_code(query="給水 水壓 每平方公分公斤 消防栓", limit=10)
# (Revit MCP) dump project pipe segment/size catalog to reconcile CNS callouts
get_mep_segments_and_sizes(includeDuct=true, summaryOnly=true)
```

## Related Skills
- [taiwan-plumbing-design-codes](../taiwan-plumbing-design-codes/SKILL.md) — detailed plumbing DESIGN numbers (drainage slopes, water-seal depth, tank ratios, vent heights). This skill defers those numbers there and adds the unit/stage layer.
- [taipower-indoor-wiring-ampacity](../taipower-indoor-wiring-ampacity/SKILL.md) — electrical ampacity detail (this skill covers only the §36 lighting-load UNIT).
- [building-services](../building-services/SKILL.md) — overall MEP design; this skill supplies the Taiwan unit/stage knowledge that skill marks as TODO.

## Additional Resources
- Human-facing knowledge layer: `domain.md`
