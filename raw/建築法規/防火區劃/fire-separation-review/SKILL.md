---
type: Skill
name: fire-separation-review
description: "This skill should be used when reviewing fire separation compliance under Taiwan's Building Technical Regulations, Design & Construction volume, Article 79-2, particularly for calculating the total floor area subject to fire separation requirements where vertical penetrations (elevator shafts, stairwells, pipe chases) and atriums are present."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
metadata:
  audience: architects
  region: taiwan
  class: C
  status: unverified
  data-currency: "2024-07-15"
---

# Fire Separation Review (建築技術規則 第79條之2 防火區劃)

## Overview

This skill assists in calculating the total floor area that triggers fire separation requirements under Taiwan's Building Technical Regulations (設計施工編) Article 79-2, which mandates a fire separation measure (e.g., fire-rated wall, fire door) for every 1,500 square metres of floor area.

Key considerations:
- Vertical penetrations that pass through multiple storeys (elevator shafts, stairwells, emergency staircases, pipe chases, etc.) are counted **once only** in the total floor area, per 內政部國土管理署解釋函（國署建管字第1131109943號）。
- Atrium (挑空) spaces **are included** in the total floor area, but their fire separation treatment depends on existing interpretations and the presence of automatic fire suppression systems.
- The skill does **not** automatically add fire separation measures; it provides the correct total floor area for the user to determine how many 1,500 m² increments apply (round up).

Trigger words: 防火區劃、第79條之2、樓地板面積限制、昇降階梯、安全梯、昇降機道、垂直管道、挑空、國署建管字第1131109943號。

## Execution Steps

1. **Identify all floor plates**  
   For each storey, measure the horizontal area enclosed by the outer walls or fire compartments (以不超過該層樓地板面積八分之一為原則的儲藏室除外)。  
   Record each storey’s floor area (樓地板面積) in square metres.

2. **Identify vertical penetrations**  
   List all spaces that penetrate vertically through two or more storeys: elevator shafts, stairwells (including emergency staircases), machine rooms, pipe chases, duct chases, etc.  
   For each such space, measure its **horizontal cross‑sectional area** (the area seen in a typical floor plan) in square metres.

3. **Identify atrium spaces**  
   List all atrium (挑空) spaces that are open to the storeys above.  
   For each atrium, measure its **horizontal footprint** at each storey it opens to (the area of the opening in the floor plate) in square metres.

4. **Calculate total floor area for fire separation**  
   - Sum the floor areas of all storeys.  
   - Add the horizontal footprint of each atrium (挑空) **once per storey it opens to**.  
   - Add the horizontal cross‑sectional area of each vertical penetration **once only** (do not multiply by the number of storeys it passes through).
   - The result is the total floor area (in square metres) to be used for fire separation calculation.

5. **Determine required fire separations**  
   Divide the total floor area by 1,500 and round **up** to the nearest integer.  
   This integer is the number of fire separation measures (e.g., fire-rated walls, fire doors, or equivalent fire-resisting construction) required under Article 79-2.

6. **Consider automatic fire suppression systems**  
   If the building is equipped with an approved automatic fire suppression system, consult the relevant authority or interpretation to determine whether the fire separation requirement may be relaxed. This skill does not apply such relaxations; it only provides the base calculation.

## Worked Example

**Scenario**: A five‑storey office building. Each storey has a floor area of 800 m². The building contains:
- One elevator shaft (horizontal cross‑section 6 m²) that passes through all five storeys.
- One atrium that opens onto storeys 2 through 5\Facade opening footprint: 20 m² on each of those storeys.
- No automatic fire suppression system is installed.

**Calculation**:
- Storey floors: 5 × 800 = 4,000 m²
- Atrium footprint: 20 m² × 4 storeys = 80 m² (added per storey it opens to)
- Elevator shaft: 6 m² (added once only, despite passing through five storeys)
- **Total floor area for fire separation** = 4,000 + 80 + 6 = **4,086 m²**
- Required fire separations = 4,086 ÷ 1,500 = 2.724 → **3** (round up)

**Result**: The building requires **3** fire separation measures under Article 79-2 (e.g., two fire-rated walls and one fire-resistant door assembly, or equivalent fire-resisting construction distributed to satisfy the 1,500 m² rule).

## Common Pitfalls

### Pitfall: Multiplying vertical penetration area by number of storeys
- **Severity**: 🔴 rejection risk  
- **When it bites**: Design stage, permit application  
- **Wrong**: Calculating the elevator shaft area as 6 m² × 5 storeys = 30 m² and adding it to the total floor area.  
- **Right**: Add the elevator shaft’s horizontal cross‑section (6 m²) **once only**, per 內政部解釋函（國署建管字第1131109943號）【^interp】.  

### Pitfall: Forgetting to include atrium footprint per storey
- **Severity**: 🟡 rework risk  
- **When it bites**: Design stage  
- **Wrong**: Adding the faculty footprint only once, or omitting it entirely.  
- **Right**: Add the atrium’s horizontal footprint **for each storey it opens to** (e.g., a 20 m² atrium opening onto storeys 2, 3, 4, 5 contributes 20 × 4 = 80 m²). Atriums are treated like regular floor area for the purpose of the 1,500 m² threshold.  

### Pitfall: Using storey‑by‑storey comparison instead of cumulative total
- **Severity**: 🔴 rejection risk  
- **When it bites**: Permit review  
- **Wrong**: Checking each storey individually: “Each storey is 800 m² (< 1,500 m²), so no fire separation is needed.”  
- **Right**: The rule applies to the **cumulative** floor area. Even if each storey is under 1,500 m², the sum may exceed the threshold and require fire separation.  

### Pitfall: Relying solely on the article text without the interpretation
- **Severity**: 🟡 rework risk  
- **When it bites**: Design stage  
- **Wrong**: Reading Article 79-2 and assuming vertical penetrations must be counted per storey because the article does not explicitly state otherwise.  
- **Right**: The article does not specify how to treat vertical penetrations; the 內政部解釋函 provides the authoritative execution method. Always pair the regulation with the latest interpretation.  

## AI Design Check Table

| Check | Condition | AI Action |
|---|---|---|
| Vertical penetration counted per storey | Sum of (penetration area × number of storeys it passes through) > penetration area | ERROR: Vertical penetrations that pass through multiple storeys must be counted **once only** in the total floor area for fire separation calculation, per 內政部解釋函（國署建管字第1131109943號）【^interp】. |
| Atrium footprint omitted or counted once | Total floor area does not include the atrium’s horizontal footprint for each storey it opens to | ERROR: Atrium (挑空) spaces are included in the total floor area for fire separation; their footprint must be added **once per storey they open to**. |
| Total floor area < 1,500 m² but individual storeys exceed | Any single storey’s floor area ≥ 1,500 m² while the summed total is < 1,500 m² (impossible in practice, but included for completeness) | ERROR: If any storey’s floor area is ≥ 1,500 m², that storey alone triggers at least one fire separation requirement, regardless of the total. |
| Automatic fire suppression assumed to waive requirement | Skill output interpreted as final fire separation count without checking for suppression system relaxations | WARNING: The skill provides the base calculation. If an approved automatic fire suppression system is present, consult the relevant authority to determine whether the fire separation requirement may be relaxed. This skill does not apply such relaxations. |
| Atrium treated as void space | Atrium footprint excluded from total floor area calculation | ERROR: Atrium spaces **are included** in the total floor area for fire separation, though their fire separation treatment depends on existing interpretations and suppression systems. |

## Data Currency

- Source: 內政部國土管理署解釋函：建築技術規則建築設計施工編第79條之2 防火區劃樓地板面積限制疑義一案（國署建管字第1131109943號）  
- Verified: 2024-07-15, via 內政部國土管理署網站  
- Volatility: MEDIUM — the Building Technical Regulations are amended periodically; interpretations may be issued to clarify application. Re‑verify before permit submission if the regulation or its interpretations have been updated since the date above.

## To Verify

- [ ] Confirm whether the 內政部國土管理署 has issued any subsequent interpretation or letter that modifies the treatment of vertical penetrations or atriums under Article 79-2.
- [ ] Check with the local building authority (縣市政府建管局) for any municipal‑specific rules or practices regarding fire separation calculations for vertical penetrations and atriums.
- [ ] Verify the current text of Article 79-2 and Article 79 in the Building Technical Regulations (設計施工編) to ensure no amendments have altered the 1,500 m² threshold or the scope of spaces included.
- [ ] If the building includes an automatic fire suppression system, confirm the system’s approval status and consult the relevant fire authority to determine whether any relaxation of the fire separation requirement applies.

## MCP Tool Examples

```python
taiwan-building-code_search_building_code(query="第79條之2 防火區劃", limit=5)
taiwan-building-code_search_building_code(query="建築技術規則 第79條", limit=5)
taiwan-building-code_search_building_interpretations(query="國署建管字第1131109943號 防火區劃", limit=5)
taiwan-building-code_search_building_interpretations(query="79條之2 昇降機道 不加總", limit=5)
```

## Related Skills

- [building-area-review](../../建築性能/建築面積檢討/building-area-review/SKILL.md) — for calculating gross floor area and identifying what counts as 建築面積 vs 樓地板面積  
- [stairwell-review](../../消防安全/排煙窗法規檢討/smoke-exhaust-review/SKILL.md) — for evaluating stair and elevator shaft compliance with smoke exhaust and fire safety regulations  
- [regulation-currency-check](../../../../建築顧問方法論/法規時效性查證/regulation-currency-check/SKILL.md) — re‑verify before permit use  
- [boundary-cases-and-escalation](../../../../建築顧問方法論/邊界案例與函詢時機/boundary-cases-and-escalation/SKILL.md) — format for the To Verify gray zones