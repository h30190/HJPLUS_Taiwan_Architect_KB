---
name: regulation-currency-check
description: "This skill should be used when about to quote any normative number (dimension, ratio, monetary threshold, penalty, vendor specification) from memory or from another skill in this knowledge base, when a skill's data is older than one year or carries no date, when the topic is in a high-churn regulatory domain (building code amendments, accessibility standards, green-building versions, procurement thresholds), or when a skill is marked status: unverified."
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

# Regulation Currency Check (法規時效性查證)

## Overview

Regulations amend; vendor catalogs revise; procurement thresholds get re-announced. A knowledge base entry is a **snapshot**, not the law. The systemic failure mode of an AI consultant is quoting a stale snapshot in a confident voice.

This skill defines when re-verification is mandatory, in what order to verify, and how to declare data age. It is a horizontal rule: it applies to every skill in this knowledge base, including this one.

---

## Section 1: The Iron Rule

> **Every normative number you output (dimension, ratio, area cap, monetary threshold, penalty, deadline, vendor spec) must carry (a) its governing article or source, and (b) a verification date. If you cannot provide both, label the number `Unverified` and say so in the answer.**

"I read it in a skill file" is not a source. The skill file's cited article is the source; the skill file's data-currency date is the verification date.

## Section 2: Mandatory Re-Verification Triggers

Re-verify against the current official text (do not answer from the KB alone) when **any** of these holds:

| # | Trigger | Rationale / example |
|---|---|---|
| 1 | Source data older than 1 year, or undated | Most KB skills carry no amendment dates at all |
| 2 | Monetary threshold or penalty involved | Procurement thresholds（公告金額、查核金額）are re-announced by 工程會; penalties change with amendments |
| 3 | Vendor/product specification | e.g., elevator shaft dimension tables are 2023 vendor snapshots — models get discontinued |
| 4 | Versioned standard | 綠建築評估手冊（EEWH）、建築能效評估、耐震設計規範 are published in editions — always identify the edition first |
| 5 | Source skill marked `status: unverified` | Its numbers were never clause-verified; treat every figure as a hypothesis |
| 6 | The answer will be used for permit submission or contract | Highest stakes — verify even recent data |
| 7 | User mentions a specific municipality | Local ordinances and review standards change independently of national code |

## Section 3: Verification Channel Priority

1. **MCP tools** — `taiwan-building-code_search_building_code` for current article text; `taiwan-building-code_search_building_interpretations` for interpretations.
2. **Laws & Regulations Database（全國法規資料庫, https://law.moj.gov.tw/）** — authoritative consolidated text; check the 修正日期 and 沿革 (amendment history) tab, not just the article.
3. **Competent authority website** — 內政部國土管理署（前營建署）for building matters, 工程會 for procurement announcements, local 建管處 for municipal rules.
4. **Ask the user for the governing document** — for vendor specs and project-specific approvals, the current catalog/approval letter outranks any database.

If MCP tools are unavailable in the current environment, say so and downgrade the answer's certainty label accordingly — do not silently skip verification.

## Section 4: Data Currency Declaration Format

Every skill (and every consulting answer) that contains normative numbers should carry a Data Currency block:

```markdown
## Data Currency

- Source: 建築技術規則建築設計施工編 §162（全國法規資料庫）
- Verified: 2026-07-10 via taiwan-building-code MCP
- Volatility: HIGH — this chapter amended repeatedly; re-verify before permit submission
```

How a `[Secondary]` fact must be rendered in an answer — the block below is a **formatting sample only**; its figure may already be outdated by the time you read this, which is exactly the point:

```text
公告金額為新臺幣 150 萬元（工程會公告，2023-01-01 生效）[Secondary, 2026-07-10]
——本數字未逐條查證，引用前請以工程會現行公告確認。
```

Threshold announcements supersede any KB snapshot; never lift the figure out of a sample like this without re-verification.

## Section 5: High-Churn Domains (查證優先名單)

| Domain | Instrument | Why it churns |
|---|---|---|
| Building code | 建築技術規則（各編） | Amended multiple times per year historically |
| Accessibility | 建築物無障礙設施設計規範 | Periodic wholesale revisions; dimension tables change |
| Green building / energy | 綠建築評估手冊、建築能效評估系統 | Edition-based (versioned manuals) |
| Seismic design | 耐震設計規範及解說 | Edition-based; interacts with concrete code editions |
| Procurement thresholds | 工程會公告（公告金額、查核金額、巨額） | Re-announced administratively, not via statute |
| Vendor data | Elevator/equipment catalogs | Commercial, changes without notice |
| Local review standards | 各縣市建管審查基準、自治條例 | Changes independently per municipality |

## Section 6: AI Check Table

| Check | Condition | AI Action |
|---|---|---|
| Undated number | Normative number about to be output without article + date | ERROR: Attach source and verification date, or label Unverified |
| Stale snapshot | Source data > 1 year old and answer is permit/contract-facing | WARNING: Re-verify via Section 3 channels before answering |
| Version blind | Edition-based standard cited without edition | ERROR: Identify the edition (e.g., "EEWH 2023 edition") first |
| Unverified upstream | Number originates from a `status: unverified` skill | ERROR: Do not quote as fact; re-verify or label Unverified |
| Silent tool absence | MCP unavailable but answer written as if verified | ERROR: Declare the verification gap explicitly |

## Section 7: MCP Tool Examples

```python
# Verify current article text before quoting a dimension
taiwan-building-code_search_building_code(query="梯廳 淨深 2公尺", limit=10)

# Check for interpretations that postdate the skill's data
taiwan-building-code_search_building_interpretations(query="容積 免計 修正")

# Procurement chapter spec (for CNS/spec-based questions)
pcc-downloader_download_specification(chapter="09", keyword="09910", format="pdf")
```

## Related Skills

- [consultation-workflow](../../顧問諮詢工作流程/consultation-workflow/SKILL.md) — invokes this skill at step 4 of every consultation
- [uncertainty-and-source-control](../../不確定性標示與來源管控/uncertainty-and-source-control/SKILL.md) — the labeling vocabulary (`Verified/Secondary/Unverified`) used when declaring currency
- [regulation-hierarchy-and-conflicts](../../法源位階與衝突處理/regulation-hierarchy-and-conflicts/SKILL.md) — amendment timing feeds the new-vs-old-law rules there
