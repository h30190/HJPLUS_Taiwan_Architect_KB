---
name: boundary-cases-and-escalation
description: "This skill should be used when a compliance question falls into a regulatory gray zone — the article uses discretionary wording (認定、核定、必要時、經主管機關認可), interpretations contradict each other, municipalities apply different review standards, or the measurement method is undefined (e.g., net depth of an irregular lobby). It teaches when to stop giving a definitive answer and recommend a formal inquiry (函詢) or pre-review (預審) to the competent authority instead."
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

# Boundary Cases & When to Escalate (邊界案例與函詢時機)

## Overview

The single most important consulting judgment is knowing **where determinable law ends and agency discretion begins**. Under 建築法 §2, the competent building authority for permits is the municipal/county government — meaning that for many gray-zone questions, the legally correct answer is not a number but *"this determination belongs to the local 建管處; inquire before filing."*

An AI that guesses confidently in a gray zone can cause a client to design, file, and get rejected. This skill defines how to recognize a boundary case, the escalation ladder, and the required answer phrasing. It fills what was, before this skill, a complete gap in this knowledge base (zero occurrences of 函詢/建管處 escalation advice).

---

## Section 1: Boundary-Case Recognition Signals

Treat the question as a boundary case when **any** of these appears:

| # | Signal | Example |
|---|---|---|
| 1 | Discretionary wording in the article | 「經主管機關**認定**」「**必要時**」「其他經主管機關**認可**之方式」 |
| 2 | Measurement method undefined | Net depth (淨深) of an irregular / flared lobby; where exactly to measure a projecting eave |
| 3 | Interpretations conflict or are absent | Two 函釋 read differently; MCP interpretation search returns nothing on point |
| 4 | Municipalities diverge | Same article, but Taipei and Taichung review standards differ |
| 5 | Aggregation/edge arithmetic | A design sits exactly at a cap (10% / 15% / 2 m) or combines exempt items in an unregulated way |
| 6 | Transitional/legacy status | 既存違建 treatment, existing lawful building undergoing partial alteration |
| 7 | Classification edge | Building use group (使用類組) assignment where the actual use straddles two groups |

## Section 2: Known Gray Zones (seed list — extend as cases accumulate)

| Gray zone | Why it is gray | Related KB skill |
|---|---|---|
| FAR-exemption item boundaries（建築技術規則 §162） | What counts as 機電設備空間/梯廳; caps interact | [floor-area-exemption-pitfalls](../../../建築法規/容積率與建蔽率計算/容積免計實務陷阱/floor-area-exemption-pitfalls/SKILL.md), [balcony-lobby-far-recalculation](../../../建築法規/容積率與建蔽率計算/陽臺梯廳回計容積計算/balcony-lobby-far-recalculation/SKILL.md) |
| Lobby net-depth measurement on irregular plans | No statutory measurement diagram; local reviewers decide | same as above |
| Rooftop structures（屋突）height/area recognition | Recognition criteria applied variably | — |
| Existing unauthorized construction（既存違建） | Enforcement schedules differ per municipality | — |
| Use-group assignment edges | 建築物使用類組及變更使用辦法 groups have overlapping real-world uses | — |
| Open space / incentive FAR recognition | Discretionary review committees | — |

> Maintenance rule: when a consultation reveals a new gray zone (a question the ladder in Section 3 could not resolve), add it to this table with the outcome.

## Section 3: The Escalation Ladder

Work down the ladder; **each step is cheaper than the next**. Only recommend step 4 when steps 1–3 fail to produce a determinate answer.

1. **Search interpretations** — `taiwan-building-code_search_building_interpretations` with the disputed noun + verbs like 認定/計算/適用. A directly-on-point 函釋 usually resolves the case (cite it with agency + number + date).
2. **Check local self-government rules and review standards** — the municipality may have published exactly the criterion the national code leaves open (審查基準、作業要點). Check the project municipality's 建管處 publications.
3. **Check local 建管處 FAQ / pre-review mechanisms** — many municipalities publish Q&A or offer 建造執照預審 for contested design points.
4. **Recommend formal inquiry (函詢) or pre-review (預審)** — when the determination is genuinely discretionary, the deliverable IS the recommendation to ask, plus a well-framed inquiry letter draft if helpful.

## Section 4: Required Answer Phrasing in a Gray Zone

**Never present a gray-zone guess as a determinate answer.** The professional format is: lean + basis + explicit locus of authority + recommended action.

Template (Chinese, for user-facing output):

```text
依〔條文＋函釋〕，本案傾向〔可／不可／可能〕……（理由：……）。
惟〔爭點，例如：不規則梯廳之淨深量測方式〕之認定權在〔○○市建管處〕，
目前無直接函釋可據。建議送件前以〔函詢／預審〕方式確認，避免退件重繪。
```

Rules:
- State your lean and its legal basis — an escalation recommendation without analysis is lazy; analysis without the escalation caveat is dangerous.
- Name the specific authority (which municipality's 建管處), not a vague "主管機關".
- Quantify the downside of guessing wrong when possible (redesign, refile, schedule slip).
- If drafting the inquiry letter, frame it around the specific article and the specific factual configuration — not "please advise generally".

## Section 5: When NOT to Escalate

Escalation has costs (weeks of waiting). Do **not** recommend 函詢 when:

| Situation | Correct action |
|---|---|
| The article is explicit and the facts fit squarely | Answer with the article; cite it |
| A directly-on-point 函釋 exists | Answer with article + interpretation |
| Pure arithmetic under defined rules | Compute it (show the worked example) |
| The uncertainty is *yours*, not the law's (you haven't searched yet) | Do steps 1–3 of the ladder first — do not outsource your homework to the agency |

## Section 6: AI Check Table

| Check | Condition | AI Action |
|---|---|---|
| Discretion ignored | Answer states a determinate conclusion on a Section 1 signal without escalation caveat | ERROR: Rewrite per Section 4 template |
| Vague authority | Answer says 「建議洽主管機關」 without naming which authority | WARNING: Name the specific municipality's 建管處 |
| Premature escalation | 函詢 recommended before the ladder's steps 1–3 were attempted | WARNING: Search interpretations and local standards first |
| Gray zone not recorded | A new gray zone surfaced but Section 2 table not updated | INFO: Propose adding it to the seed list |

## Section 7: MCP Tool Examples

```python
# Step 1 of the ladder: is there an interpretation on point?
taiwan-building-code_search_building_interpretations(query="梯廳 淨深 不規則 認定")
taiwan-building-code_search_building_interpretations(query="屋突 高度 計算")

# Confirm the article's discretionary wording before classifying as gray zone
taiwan-building-code_search_building_code(query="經主管機關認定 容積", limit=10)
```

## Related Skills

- [consultation-workflow](../../顧問諮詢工作流程/consultation-workflow/SKILL.md) — invokes this skill at step 6 of every consultation
- [regulation-hierarchy-and-conflicts](../../法源位階與衝突處理/regulation-hierarchy-and-conflicts/SKILL.md) — unresolvable conflicts route here
- [uncertainty-and-source-control](../../不確定性標示與來源管控/uncertainty-and-source-control/SKILL.md) — tone rules for stating a lean without overclaiming
