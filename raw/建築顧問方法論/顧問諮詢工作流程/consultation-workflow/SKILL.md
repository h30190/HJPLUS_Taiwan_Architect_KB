---
name: consultation-workflow
description: "This skill should be used when answering any Taiwan architecture consulting question — code compliance, FAR/area calculation, permits, fire safety, accessibility, procurement, structural checks — as the entry point that defines the seven-step consulting procedure (classify, locate governing law, route and combine KB skills, verify currency, resolve conflicts, detect boundary cases, format the answer) and the standard answer format with certainty labels."
user-invocable: true
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
metadata:
  audience: architects
  region: taiwan
  class: C
  status: verified
  data-currency: "2026-07-10"
---

# Consultation Workflow (顧問諮詢工作流程)

## Overview

This is the **master routing skill** of the knowledge base. When the task is *answering a Taiwan architecture question* (as opposed to maintaining this repository), start here. It chains the four horizontal methodology skills and the topical skills into one procedure, and defines the output format every answer must follow.

The failure modes this procedure prevents, in order of damage: quoting a stale or unsourced number confidently; answering from one skill when the question spans several; giving a determinate answer in a gray zone that belongs to the local 建管處.

---

## Section 1: The Seven-Step Procedure

### Step 1 — Classify the question
Identify the topic(s): 法規檢討 / 面積・容積計算 / 執照流程 / 消防 / 無障礙 / 結構 / 性能・標章 / 採購 / 文資 / 軟體操作. A single question frequently spans 2+ topics (e.g., "頂樓加蓋電梯" = FAR + 屋突認定 + permit + accessibility).

### Step 2 — Locate the governing law layers
For each topic, determine: national statute → delegated regulation → **which municipality** (local ordinances and review standards differ) → known interpretations. Ask the user for the municipality if permits are involved and it wasn't stated.

### Step 3 — Route and COMBINE skills
Discover skills via `raw/index.md` (per this repo's OKF convention) and frontmatter `metadata.class`. Load **every** skill in the matching cluster, not just the first hit:

| Question smells like… | Load together (cluster) |
|---|---|
| 容積免計 / 陽台 / 梯廳 / §162 | `floor-area-exemption-pitfalls` **+** `balcony-lobby-far-recalculation`（建築法規/容積率與建蔽率計算） |
| 排煙 / 防火避難 | `smoke-exhaust-review` + fire-related 機電 skills（專業複委託/機電）— dual-track domain |
| 無障礙 | `accessible-door-clear-width` + `accessible-elevator-shaft-dimensions`（vendor data — currency check mandatory） |
| RC 結構檢核 | `concrete-general-requirements` first, then the member skill (beam/column/slab/wall) |
| 執照申辦 | 建築執照 skills — **all marked `status: unverified`**: structure usable, numbers must be re-verified |
| 政府採購 | 公共工程 skills + 工程會 threshold currency check |
| 文資建物 | 文化資產保存法 skills + hierarchy skill (special law overrides general) |

Maintenance rule: when a consultation reveals a cluster not in this table, add it.

### Step 4 — Verify currency
Apply [regulation-currency-check](../../法規時效性查證/regulation-currency-check/SKILL.md): any trigger (stale/undated data, money, vendor specs, versioned standards, unverified upstream, permit-facing use) → re-verify via MCP / 全國法規資料庫 before using the number.

### Step 5 — Resolve conflicts
If the loaded skills/laws point in different directions, apply [regulation-hierarchy-and-conflicts](../../法源位階與衝突處理/regulation-hierarchy-and-conflicts/SKILL.md): scope check → rank → special-over-general → later-over-earlier → dual-track-take-stricter.

### Step 6 — Detect boundary cases
Scan for the gray-zone signals in [boundary-cases-and-escalation](../../邊界案例與函詢時機/boundary-cases-and-escalation/SKILL.md) (discretionary wording, undefined measurement, conflicting/absent interpretations, municipal divergence, at-the-cap arithmetic). If found, the answer must carry the lean + authority + escalation format — never a bare yes/no.

### Step 7 — Format the answer
Per Section 2, with certainty labels per [uncertainty-and-source-control](../../不確定性標示與來源管控/uncertainty-and-source-control/SKILL.md).

## Section 2: Standard Answer Format

```markdown
**結論**（先行，一句話——含確定性等級）

**法源依據**：逐條列出（條號＋要旨；函釋附機關字號日期）[Verified 日期 / Secondary / Unverified]

**計算過程**（如適用）：輸入 → 公式 → 結果，可稽核

**待查證**（To Verify）：本次未能解決的點、查過什麼、下一步去哪查

**函詢建議**（如為灰區）：認定權機關＋建議行動＋猜錯的代價

**時效聲明**：資料查證日期；高變動項目的再查提醒
```

Rules: conclusion first; every load-bearing number carries article + label; calculations always show work; disclaimers are specific (which point is uncertain and why), not boilerplate appended to everything.

## Section 3: Anti-Patterns (negative rules)

| # | Never do this | Because |
|---|---|---|
| 1 | Answer a multi-topic question from the single first-matching skill | Cross-topic interactions (FAR × 屋突 × permit) are where designs fail review |
| 2 | Quote a number from a `status: unverified` skill as fact | Those numbers were never clause-verified — treat as hypotheses |
| 3 | Compute sub-caps separately then compare the sum to a combined cap using original bases | The balcony-lobby skill documents this exact double-counting error (§162 10%+10% vs 15%) |
| 4 | Emit a compliance ERROR from an unverified rule | Strongest permitted level is WARNING（see uncertainty skill §3） |
| 5 | Give a determinate yes/no on a question with discretionary wording | The determination belongs to the local authority — use the escalation format |
| 6 | Skip asking which municipality when permits are involved | Local ordinances/review standards routinely change the answer |
| 7 | Append a generic 「建議洽主管機關」 to every answer | Escalation is a specific judgment (Section 6), not a disclaimer of convenience — overuse destroys its signal value |

## Section 4: Worked Example (abbreviated walk-through)

**Question**: 「15 層集合住宅，梯廳想做大一點，能免計容積到多少？」（台中案）

1. **Classify**: FAR exemption + possible local add-on.
2. **Layers**: 建築技術規則設計施工編 §162；台中市 → check 宜居建築辦法 and local review standards.
3. **Route**: load the §162 cluster — `floor-area-exemption-pitfalls` + `balcony-lobby-far-recalculation` + `taichung-livable-building-incentive`.
4. **Currency**: §162 is high-churn — verify current text via MCP before quoting the 10%/15% caps.
5. **Conflicts**: none expected; local rules add, not relax.
6. **Boundary scan**: lobby **net-depth measurement on irregular plans is a known gray zone** → answer must carry the escalation caveat for the depth-recognition point, while the percentage caps themselves are determinate arithmetic.
7. **Format**: conclusion with caps [Verified + date], worked calculation on the project's areas, To-Verify for the depth measurement, 函詢建議 naming 台中市都發局建管單位.

## Section 5: MCP Tool Examples

```python
# Step 4 verification for the worked example
taiwan-building-code_search_building_code(query="第162條 梯廳 免計 百分之十", limit=10)

# Step 6 boundary scan
taiwan-building-code_search_building_interpretations(query="梯廳 淨深 認定")
```

## Related Skills

The four horizontal methodology skills this workflow chains:

- [regulation-hierarchy-and-conflicts](../../法源位階與衝突處理/regulation-hierarchy-and-conflicts/SKILL.md) — step 5
- [regulation-currency-check](../../法規時效性查證/regulation-currency-check/SKILL.md) — step 4
- [boundary-cases-and-escalation](../../邊界案例與函詢時機/boundary-cases-and-escalation/SKILL.md) — step 6
- [uncertainty-and-source-control](../../不確定性標示與來源管控/uncertainty-and-source-control/SKILL.md) — steps 3, 7

Gold-standard topical skills to imitate when extending the KB:

- [concrete-general-requirements](../../../建築施工與材料/混凝土結構設計/混凝土通用規定/concrete-general-requirements/SKILL.md) — source control done right
- [smoke-exhaust-review](../../../建築法規/消防安全/排煙窗法規檢討/smoke-exhaust-review/SKILL.md) — multi-entry decision tree, dual-track handling
- [balcony-lobby-far-recalculation](../../../建築法規/容積率與建蔽率計算/陽臺梯廳回計容積計算/balcony-lobby-far-recalculation/SKILL.md) — worked examples + negative rules
