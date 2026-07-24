---
name: regulation-hierarchy-and-conflicts
description: "This skill should be used when two or more Taiwan regulations appear to conflict, when deciding which rule governs (national law vs. local ordinance vs. administrative interpretation), when a regulation was amended and it is unclear which version applies, or before answering any compliance question that touches more than one body of law (e.g., building code vs. fire code, national code vs. municipal ordinance)."
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

# Regulation Hierarchy & Conflict Resolution (法源位階與衝突處理)

## Overview

Taiwan building practice is governed by multiple layers of law that frequently overlap: national statutes, delegated regulations, municipal ordinances, and administrative interpretations. Most wrong consulting answers come not from misreading a single article, but from **applying the wrong layer** or **failing to notice that two regimes apply simultaneously**.

This skill defines (1) the hierarchy of legal sources, (2) an ordered conflict-resolution procedure, and (3) time-axis rules for amended regulations. It is a horizontal rule: apply it to every multi-regulation question, regardless of topic.

---

## Section 1: Hierarchy of Legal Sources (法源位階)

From highest to lowest binding force:

| Rank | Layer | Chinese | Examples | Notes |
|---|---|---|---|---|
| 1 | Constitution | 憲法 | — | Rarely invoked directly in building practice |
| 2 | Statute (law) | 法律（法、律、條例、通則） | 建築法、都市計畫法、消防法、文化資產保存法、政府採購法、建築師法 | Enacted by Legislative Yuan（中央法規標準法 §2） |
| 3 | Delegated regulation | 法規命令（規則、細則、辦法、標準、準則等） | 建築技術規則（依建築法 §97 授權）、建築物使用類組及變更使用辦法、各類場所消防安全設備設置標準 | Issued by agencies under statutory delegation（中央法規標準法 §3、行政程序法 §150） |
| 4 | Local self-government ordinance | 自治條例 | 臺北市建築管理自治條例 | Passed by local council; **void where it contradicts the Constitution, statutes, or delegated regulations**（地方制度法 §30） |
| 5 | Local self-government rule | 自治規則 | 各縣市建造執照預審作業要點類 | Issued by local executive |
| 6 | Administrative rule / interpretation | 行政規則、解釋函令（函釋） | 內政部國土管理署（前營建署）函釋 | See Section 2 — no formal rank as law, but governs review practice |

Core rank rules（中央法規標準法 §11）: a statute may not contradict the Constitution; a regulation may not contradict the Constitution or a statute; a lower agency's order may not contradict a higher agency's order.

> **Practice note**: Local governments may lawfully impose *stricter or additional* requirements within their delegated authority (e.g., 臺中市宜居建築設施設置及回饋辦法). "Local rule is lower rank" does NOT mean it can be ignored — it means it cannot *relax* a national requirement. A compliant design satisfies both.

## Section 2: Administrative Interpretations (解釋函令)

- Interpretations (函釋) clarify how the issuing agency reads a provision. They bind subordinate agencies and shape 建管 review practice, but they are **not statutes**: courts are not bound by them (J.Y. Interpretation No. 216 — Secondary source, verify before quoting verbatim).
- In consulting output, always cite an interpretation with its **issuing agency, document number, and date** (e.g., 內政部營建署 92.09.20 營署建管字第0920093655號), and distinguish it from the article it interprets.
- If an interpretation appears to *contradict* its parent article, the article prevails — flag the contradiction explicitly instead of silently picking one.
- Interpretations are the primary tool for boundary cases — see [boundary-cases-and-escalation](../../邊界案例與函詢時機/boundary-cases-and-escalation/SKILL.md).

## Section 3: Conflict-Resolution Procedure

Apply these steps **in order**. Stop at the first step that resolves the question.

1. **Confirm it is a real conflict.** Most "conflicts" are two rules with different scopes (different building use groups, different floor areas, different trigger conditions). Read the applicability clause (適用範圍) of each rule first.
2. **Different ranks → higher rank prevails.** A 自治條例 cannot relax 建築技術規則; an interpretation cannot override an article.
3. **Same rank, one is special law → special law prevails**（特別法優於普通法，中央法規標準法 §16）. E.g., 文化資產保存法 provisions for historic buildings override general 建築法 requirements within their scope.
4. **Same rank, same nature → later law prevails**（後法優於前法）. Check amendment dates via the Laws & Regulations Database.
5. **Parallel regimes (dual-track) → both must be satisfied; the stricter prevails.** See Section 4. This is not a conflict to resolve but a double requirement to meet.
6. **Interpretation vs. parent article → article prevails**; state the discrepancy in your answer.

If none of the steps resolves it, treat the question as a boundary case and escalate per [boundary-cases-and-escalation](../../邊界案例與函詢時機/boundary-cases-and-escalation/SKILL.md).

## Section 4: Dual-Track Regimes (雙軌並行，取嚴者)

These domains are governed by two independent bodies of law with **different competent authorities**. Compliance with one does NOT imply compliance with the other.

| Domain | Track 1 (building authority 建管) | Track 2 (other authority) | Working example in this KB |
|---|---|---|---|
| Fire / smoke | 建築技術規則建築設計施工編 | 各類場所消防安全設備設置標準（消防主管機關） | [smoke-exhaust-review](../../../建築法規/消防安全/排煙窗法規檢討/smoke-exhaust-review/SKILL.md) — "both must be satisfied; the stricter prevails" |
| Accessibility | 建築技術規則設計施工編第十章 | 建築物無障礙設施設計規範 | 無障礙 skills under 建築法規 |
| Structural fire cover | 建築物混凝土結構設計規範 Ch. 20.5 | 建築技術規則 fire-resistance provisions | [concrete-general-requirements](../../../建築施工與材料/混凝土結構設計/混凝土通用規定/concrete-general-requirements/SKILL.md) §2.3 |
| National vs. local add-ons | 建築技術規則 | 各地自治條例／宜居建築辦法等 | 台中市宜居建築 skill under 建築法規 |

> **Rule**: when a question touches a dual-track domain, your answer MUST cite both tracks or explicitly state which track you have not checked.

## Section 5: Time-Axis Rules (新舊法適用)

| Situation | Governing rule | Effect |
|---|---|---|
| Permit application pending while the regulation changes | 從新從優（中央法規標準法 §18） | Apply the new rule, unless the old rule favors the applicant and the applied-for matter is not abolished/prohibited |
| Administrative penalty, law changed after the act | 從新從輕（行政罰法 §5） | Apply the law at time of sanction, unless an earlier version is more favorable |
| Lawfully completed existing building（既有合法建築物） | Generally not retroactive | A valid 使用執照 under old law remains valid; **change of use (建築法 §73) or major alteration triggers current law** |
| Amendment with transitional clauses（過渡條款） | Read the amendment's 附則 | Transitional clauses override the defaults above — always check them |

> **WARNING trigger**: if the project timeline spans a known amendment date (design started before, permit filed after), do not answer from a single version — identify which version applies via §18 logic, and say so explicitly.

## Section 6: AI Check Table

| Check | Condition | AI Action |
|---|---|---|
| Scope check skipped | Two rules cited as "conflicting" without comparing applicability clauses | WARNING: Verify scopes before invoking hierarchy rules |
| Local relaxation | Answer relies on a local rule that is *less strict* than the national code | ERROR: 自治條例 cannot relax national requirements（地方制度法 §30） |
| Dual-track omission | Question touches fire/accessibility/local-add-on domains but only one track cited | ERROR: Cite both tracks or declare the unchecked one |
| Interpretation as law | 函釋 cited without agency/number/date, or presented as statutory text | WARNING: Re-cite with full document identity and label as interpretation |
| Version ambiguity | Project timeline spans a known amendment | WARNING: Resolve applicable version via 中央法規標準法 §18 before answering |

## Section 7: MCP Tool Examples

```python
# Find the governing article before resolving any conflict
taiwan-building-code_search_building_code(query="容積 免計 梯廳", limit=10)

# Check whether an interpretation exists on the disputed point
taiwan-building-code_search_building_interpretations(query="梯廳 淨深 認定")

# Dual-track fire check: search both regimes
taiwan-building-code_search_building_code(query="排煙 設備 居室", limit=10)
taiwan-building-code_search_building_interpretations(query="排煙 消防 適用")
```

For amendment history and current text, direct the user to the Laws & Regulations Database (https://law.moj.gov.tw/) — see [regulation-currency-check](../../法規時效性查證/regulation-currency-check/SKILL.md).

## Related Skills

- [consultation-workflow](../../顧問諮詢工作流程/consultation-workflow/SKILL.md) — the master procedure; invokes this skill at step 5
- [regulation-currency-check](../../法規時效性查證/regulation-currency-check/SKILL.md) — verify you are reading the current version before ranking anything
- [boundary-cases-and-escalation](../../邊界案例與函詢時機/boundary-cases-and-escalation/SKILL.md) — where conflicts end and agency discretion begins
- [uncertainty-and-source-control](../../不確定性標示與來源管控/uncertainty-and-source-control/SKILL.md) — how to label conclusions drawn from interpretations vs. statutes
