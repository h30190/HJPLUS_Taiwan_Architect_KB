# HJPLUS Taiwan Architect KB - Agent Instructions

## Overview
Knowledge base for Taiwan architects with dual-language skill documentation. All working content lives under `raw/`. Use `知識樣板/` as the template when creating new skills.

## Consulting Protocol — READ THIS FIRST when answering architecture questions

There are two distinct tasks in this repository. Identify yours before doing anything:

1. **Consulting** — answering a Taiwan architecture/regulation/design question using this KB.
2. **Maintenance** — creating or editing skills, indexes, or repo infrastructure.

**If consulting**: before answering, read `raw/建築顧問方法論/index.md` and start from
[consultation-workflow](raw/建築顧問方法論/顧問諮詢工作流程/consultation-workflow/SKILL.md).
The five methodology skills there are **horizontal rules** that override topical habit:

- Route through skill **clusters**, not the first matching skill (a §162 FAR question needs 2+ skills).
- Every normative number you output needs an article number + verification date, or an explicit `Unverified` label.
- Skills marked `metadata.status: unverified` — their numbers are hypotheses; re-verify before quoting.
- Gray-zone questions (discretionary wording, undefined measurements, municipal divergence) get the
  lean + basis + authority + 函詢/預審 recommendation format — never a bare yes/no.
- Dual-track domains (fire, accessibility, local add-ons): cite both tracks or declare the unchecked one.

**If maintaining**: follow the sections below, and apply
[uncertainty-and-source-control](raw/建築顧問方法論/不確定性標示與來源管控/uncertainty-and-source-control/SKILL.md)
to any content you author (no unsourced penalty/threshold figures, label certainty, keep To-Verify sections).

## Project Structure
All skill content is in `raw/`. There is no separate published/flat structure.

```
raw/
├── 建築顧問方法論/        (horizontal methodology — consulting entry point)
├── 建築設計與規劃/
├── 專業複委託/
├── 建築性能/
├── 建築法規/
├── 建築施工與材料/
├── 建築執照/
├── 公共工程/
├── 專案管理/
├── 經營管理/
├── 室內裝修/
└── 設計軟體與工具/
```

Do not hardcode per-category skill counts here — they go stale. Current counts live in `README.md`
(auto-updated by `python scripts/update_readme_counts.py`); the authoritative discovery path is `raw/index.md`.

Template: `知識樣板/` — copy this to create new skills.

## Build / Lint / Test Commands
Documentation-only repository. No build/lint/test commands.

Pre-commit hook (`.pre-commit-config.yaml`): runs `python scripts/run_graphify.py` when `raw/` or `graphify.py` changes. Script may not yet exist.

## Skill Classification & Status Metadata

| Class | Description | Requirements |
|-------|-------------|--------------|
| A | International standards | No Taiwan adaptation needed |
| B | International → Taiwan | `<!-- TODO: Taiwan adaptation needed -->` before US/international spec blocks |
| C | Taiwan-specific | May include MCP tool call examples (optional) |

**`metadata.class` is REQUIRED** in every SKILL.md frontmatter (`A`, `B`, or `C`). All existing skills
carry it; new skills must declare it. The class-assignment reference table is `SECTION_CLASS` in
`scripts/update_readme_counts.py` — keep the two consistent.

**`metadata.status`** (optional, but load-bearing when present):

| Value | Meaning | Reader behavior |
|-------|---------|-----------------|
| `verified` | Normative numbers transcribed clause-by-clause from official text | Quotable with the recorded date |
| `unverified` | Numbers drafted from general knowledge, never clause-verified | Structure usable as orientation; **numbers must be re-verified before quoting** |
| `draft` | Incomplete skeleton | Do not rely on it |

**`metadata.data-currency`** (recommended): `"YYYY-MM-DD"` date of the last source verification. See
[regulation-currency-check](raw/建築顧問方法論/法規時效性查證/regulation-currency-check/SKILL.md) for
when stale data forces re-verification.

## Cross-Referencing Rule

Skills do not exist in isolation — AI answers fail when related skills don't know about each other.

- Before creating a skill, search `raw/` for overlapping topics. If overlap exists, either merge or
  **declare the division of labor** in both skills' Overview (e.g., "this skill covers the pitfalls;
  the calculation algorithm lives in X").
- Every skill should end with a `## Related Skills` section linking (relative paths) to skills a
  consultant would need in the same session. The §162 pair
  (`floor-area-exemption-pitfalls` ↔ `balcony-lobby-far-recalculation`) and the concrete group are
  the reference examples.
- When adding a skill that belongs to a question cluster, also add it to the cluster table in
  [consultation-workflow](raw/建築顧問方法論/顧問諮詢工作流程/consultation-workflow/SKILL.md) Section 1 Step 3.

## File Naming — CRITICAL

### Skill files must be `SKILL.md` (uppercase)
The Agent Skills standard (Claude Code, OpenCode) requires the file to be `SKILL.md` in all caps. **As of writing, many files still use lowercase `skill.md` — rename these to `SKILL.md` when editing.**

### Directory name must match frontmatter `name`
The inner English skill directory name **MUST** exactly match the `name` field in `SKILL.md` frontmatter. This is a hard requirement.

## Three-Layer Directory Structure

```text
Subcategory/                              ← Traditional Chinese (e.g. 消防安全/)
├── README.md                             ← Subcategory index
│
└── Knowledge-Entry/                      ← Traditional Chinese (e.g. 排煙窗法規檢討/)
    ├── domain.md                         ← Human doc (Traditional Chinese)
    └── skill-name-hyphenated/            ← AI Skill dir (lowercase-hyphenated English)
        ├── SKILL.md                      ← AI instructions (English)
        ├── assets/                       ← Optional
        ├── references/                   ← Optional
        └── scripts/                      ← Optional
```

File placement:
- `domain.md` → in the **Chinese** Knowledge Entry directory (one level above SKILL.md)
- `SKILL.md` → in the **English** AI Skill directory

✅ Correct: `消防安全/排煙窗法規檢討/smoke-exhaust-review/SKILL.md`
❌ Wrong: `消防安全/smoke-exhaust-review/domain.md`
❌ Wrong: `消防安全/排煙窗法規檢討/SKILL.md` (no English subdirectory)
❌ Wrong: `pai-yan-chuang/SKILL.md` (pinyin instead of English)

## index.md — OKF Directory Index (v0.1)

This project follows the `index.md` convention from Google's
[Open Knowledge Format (OKF) v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
to support progressive discovery for AI agents.

**When exploring a directory, always read `index.md` first** (not `README.md`).
`index.md` is the agent entry point — it lists available skills and subdirectories
so you can discover content without scanning every file. `README.md` is for human
readers browsing GitHub and may be stale or incomplete.

### When to add index.md

| Condition | index.md? |
|-----------|:---------:|
| Directory contains **2+** subdirectories or skills | ✅ Yes |
| Directory IS a knowledge entry (has `domain.md`) | ❌ No |
| Directory IS a skill directory (has `SKILL.md`) | ❌ No |
| `raw/` (bundle root) | ✅ Yes (with `okf_version: "0.1"`) |

Rule of thumb: **If a directory holds multiple things, it gets an index. If it IS one thing, it doesn't.**

### index.md Format

```markdown
# Category Name (English)

## Skills

* [Skill Name](relative/path/SKILL.md) - Copy from SKILL.md frontmatter `description` field
* [Skill Name](relative/path/SKILL.md) - ...

## Planned

* [Planned directory](path/) - Brief description
```

- No frontmatter on subdirectory index.md (only `raw/index.md` may have `okf_version`)
- Link skills directly to `SKILL.md`
- Link subdirectories with trailing `/`
- Do NOT list `domain.md` or `README.md`

### Maintenance

- OKF is currently **v0.1 draft** (June 2026). Revisit this section if the spec updates.

## SKILL.md Frontmatter
```yaml
---
name: skill-name-hyphenated
description: "This skill should be used when [specific trigger scenario]."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
metadata:
  audience: architects
  region: taiwan
  class: C
  status: verified
  data-currency: "2026-07-10"
---
```

| Field | Required | Rules |
|-------|----------|-------|
| `name` | Yes | 1-64 chars, lowercase alphanumeric + single hyphens, must match directory name |
| `description` | Yes | 1-1024 chars, must include trigger scenario |
| `license` | Optional | License statement |
| `compatibility` | Optional | Compatibility declaration |
| `metadata.class` | **Yes** | `A`/`B`/`C` — see Skill Classification & Status Metadata |
| `metadata.status` | Optional | `verified`/`unverified`/`draft` — see Skill Classification & Status Metadata |
| `metadata.data-currency` | Recommended | `"YYYY-MM-DD"` of last source verification |
| `metadata` (other keys) | Optional | Key-value extensions |

## domain.md
- Traditional Chinese, no frontmatter
- Natural explanatory text: 使用情境、學習目標、實務應用
- References to official Taiwan codes/standards

## Language Rules
| File | Language |
|------|----------|
| SKILL.md | English |
| domain.md | Traditional Chinese |
| Frontmatter | English |
| Directory names (Chinese) | Traditional Chinese only — **no Simplified Chinese** |

## C-Class MCP Integration (Optional)

If applicable, MCP tool call examples may be included:
```
taiwan-building-code_search_building_code(query="防火區劃", limit=10)
taiwan-building-code_search_building_interpretations(query="避難設施")
pcc-downloader_download_specification(chapter="09", keyword="09910", format="pdf")
```

## Creating a New Skill
1. Choose category/subcategory under `raw/`
2. Copy `知識樣板/` to target location, rename outer dir to Traditional Chinese
3. Inside Chinese dir, rename `skill-name-hyphenated/` to lowercase-hyphenated English
4. Write `SKILL.md` with frontmatter (`name` must match dir name)
5. Write `domain.md` in Traditional Chinese
6. Delete unused `assets/`, `references/`, `scripts/` subdirectories
7. **Update parent `index.md`**: If the parent directory has an `index.md`, add a new entry under `## Skills`. If it doesn't have one but qualifies (multiple children), create it.

## Editing Existing Skills
- Never delete `SKILL.md` or `domain.md` without replacement
- If file is lowercase `skill.md`, rename to `SKILL.md`
- Keep frontmatter intact; sync `name` with directory name
- Sync changes between SKILL.md and domain.md
- Preserve `<!-- TODO -->` markers in B-class skills
- When adding or removing a skill, update the parent directory's `index.md` accordingly

## Pre-Merge Verification

Before merging a PR, the maintainer must independently verify any **new or changed `[Verified]` value**
(dimension, factor, cap, fee, penalty) against the official source per
[regulation-currency-check](raw/建築顧問方法論/法規時效性查證/regulation-currency-check/SKILL.md) — do
not trust the tag the contributor attached. If the source cannot be confirmed, require the value be
downgraded to `[Unverified]` or reject it. Adding `[Unverified]` / `[Secondary]` content is not subject
to this check (readers already treat those as non-authoritative). Rationale: `[Verified]` is the only tag
that unlocks 「規定為/必須」 tone, so the maintainer's verification cost is concentrated there.

## Post-Merge Maintenance

After merging a PR, the maintainer must:

1. **Update README `## 📰 最近更新`** — Add a new entry at the top of the list with the format:
   ```
   - **YYYY-MM-DD** {emoji} {brief description} ([#{pr-number}](url) by @author)
   ```
2. **Update parent `index.md`** — If the PR added or removed skills, sync the parent directory's `index.md` `## Skills` list per [OKF v0.1](#indexmd--okf-directory-index-v01).
3. **Run `python scripts/update_readme_counts.py`** to refresh the skill count table (auto-runs via pre-commit hook if configured, but verify the numbers match).

The landing page data (`docs/data.json` — knowledge-graph tree, tag list, 最新更新, stat counters)
is **auto-regenerated at deploy time**: the `Deploy landing page` GitHub Action runs
`scripts/update_landing_page.py` on every push to main and publishes docs/ (with the fresh
data.json) to GitHub Pages. Do NOT edit `docs/data.json` by hand — the committed copy is only a
local-preview fallback; the deployed site always uses the freshly generated one. Its 最新更新 list
is parsed from README `## 📰 最近更新`, so keeping step 1 above accurate is what keeps the landing
page accurate. To preview locally, run `python scripts/update_landing_page.py`.

## Markdown Style
- One `# H1` per file
- `##` for major sections, `###` for subsections
- Tables for structured data
- Bullets use `-`, checkboxes use `- [ ]`
- Internal links: relative paths only

## Prohibited
- No frontmatter in `domain.md`
- No Simplified Chinese in any file
- No Chinese characters in skill directory names
- No absolute paths
- No secrets/credentials
- Don't remove TODO markers without completing adaptation

## License
| Content Type | License |
|--------------|---------|
| Documentation (`.md`) | CC BY-SA 4.0 |
| Code (`.sh`, `.py`, `.js`, `.ts`) | Apache 2.0 |
