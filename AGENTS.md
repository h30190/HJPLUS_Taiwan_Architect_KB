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

### Tool-Backed Skills — Confirm Before Launching Anything

A handful of skills under `raw/` ship their own `scripts/` that open a local port, start a server, or otherwise run a live process — not just static reference reading. Mentioning the topic in conversation is not, by itself, permission to launch one. Check the matching skill's own confirmation rule before running its scripts.

- **綠建材 / TABC 綠建材 / green building material** topics → read [green-material-search-toolkit](raw/建築施工與材料/綠建材/綠建材檢索與選用工具/green-material-search-toolkit/SKILL.md) first. Its "Trigger Confirmation Rule" section applies: do **not** run `scripts/local_server.py` (it opens port 8888 and a browser tab) until the user has explicitly confirmed they want the search tool opened — a passing mention of the topic is not confirmation.

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

`scripts/validate_okf.py` warns when a `B` skill carries no `<!-- TODO: Taiwan adaptation needed -->`
marker. When that warning fires, first ask whether the skill is international at all: a skill built on
Taiwan's own regulations or labels (台電/自來水/電信規範, EEWH, 低碳建築標示, 室內空氣品質管理法) is
`C`, and reclassifying it is the fix — do not insert a marker to silence the warning. Only genuinely
international content (ASHRAE, AISC/ACI, ISO/ASTM, IBC/NFPA, LEED, WELL) is `B`, and there the marker
goes immediately before the block whose specs are not yet localized, naming the standards it follows.

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

## OKF v0.2 — Bundle Conventions

`raw/` is an [Open Knowledge Format (OKF) v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
bundle. OKF is Google's open format for agent-readable knowledge; this project
adopts its concept/index/log structure so agents can discover content
progressively instead of scanning every file.

Run `python scripts/validate_okf.py` after any structural change. It checks
everything in this section and exits non-zero on error.

### Concept documents and `type`

OKF §11 requires every non-reserved `.md` to carry frontmatter with a non-empty
`type`. `index.md` and `log.md` are reserved filenames and carry none.

| File | `type` value | Notes |
|------|-------------|-------|
| `SKILL.md` | `Skill` | Matches the value used in OKF's own reference bundles |
| `domain.md` | `Knowledge Entry` | Plus `title` copied from the document's `# H1` |
| `index.md` | — | Reserved (§8) |
| `log.md` | — | Reserved (§9) |
| Other loose `.md` (e.g. under `references/`) | `Reference` | Supporting material that is not itself a skill |
| `README.md` | — | **Deliberate deviation**, see below |

**`README.md` is exempt.** READMEs are human-facing GitHub navigation; adding
frontmatter would render a metadata table above every page for no agent benefit.
§11 forbids consumers from rejecting a bundle over missing fields, so the bundle
stays usable.

There is no central OKF type registry: producers pick descriptive values and
consumers must tolerate unknown ones. Do not invent new types without adding
them to the table above and to `TYPES` in `scripts/validate_okf.py`.

### Trust and freshness families

OKF v0.2 added optional frontmatter for provenance. This project uses them as
follows, alongside the pre-existing `metadata.*` fields (both are kept; the OKF
families are the machine-readable ones):

```yaml
verified:
  - { by: human:Jacky820507, at: 2026-07-10T00:00:00Z }
```

| Our field | OKF equivalent | Rule |
|-----------|----------------|------|
| `metadata.status: verified` | `verified:` list entry | `by` = the contributor who verified, as `human:<github-handle>`; `at` = the `metadata.data-currency` date normalized to `T00:00:00Z` |
| `metadata.status: unverified` | *absence of* `verified:` | OKF derives the **unverified** trust tier from a missing key — nothing to write |
| `metadata.status: draft` | `status: draft` | Top-level `status` is lifecycle, not trust; valid values are `draft`/`stable`/`deprecated` only |
| `metadata.data-currency` | `verified[].at` | Kept as the human-facing date |

Do NOT put `verified`/`unverified` in the top-level `status` field — those are
not valid OKF lifecycle values and a consumer will reject them.

`stale_after: YYYY-MM-DD` is available for content with a known expiry (a
regulation with an announced amendment date). Leave it off when there is no
real expiry date — an invented one is worse than none.

### sources

v0.2 moves provenance from a body `# Citations` list into `sources:` frontmatter
with credibility signals. **New skills MUST declare `sources`**; existing skills
are being backfilled gradually, so absence is not an error yet.

```yaml
sources:
  - id: btr-33
    resource: https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=D0070115
    title: 建築技術規則建築設計施工編 §33
    last_modified: 2024-03-14
```

Cite a specific claim in the body with a markdown footnote keyed to the `id`:
`... 淨寬不得小於 75 公分。[^btr-33]`

### log.md — bundle history

`raw/log.md` is the machine-readable history of the bundle (OKF §9). Date
headings MUST be ISO 8601 `YYYY-MM-DD`, newest first, with `**Update**` /
`**Creation**` / `**Deprecation**` prefixes. README's 「最近更新」 block is the
human-facing view of the same history — update both when merging a PR.

### index.md — directory index

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
| `raw/` (bundle root) | ✅ Yes (with `okf_version: "0.2"`) |

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
- A not-yet-created directory may instead be listed inline under `## Skills`
  with a `（籌備中）` suffix; the validator skips link-checking those

### Maintenance

- OKF is currently **v0.2** (released 2026-07-24). Revisit this section if the spec updates.
- v0.2's two breaking changes (`timestamp` → `generated.at`, body `# Citations` →
  `sources`) never applied here: this bundle never used either legacy field.

## SKILL.md Frontmatter
```yaml
---
type: Skill
name: skill-name-hyphenated
description: "This skill should be used when [specific trigger scenario]."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
verified:
  - { by: human:github-handle, at: 2026-07-10T00:00:00Z }
sources:
  - id: btr-33
    resource: https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=D0070115
    title: 建築技術規則建築設計施工編 §33
    last_modified: 2024-03-14
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
| `type` | **Yes** | Always `Skill` — OKF §11.2, see [OKF v0.2 — Bundle Conventions](#okf-v02--bundle-conventions) |
| `name` | Yes | 1-64 chars, lowercase alphanumeric + single hyphens, must match directory name |
| `description` | Yes | 1-1024 chars, must include trigger scenario |
| `license` | Optional | License statement |
| `compatibility` | Optional | Compatibility declaration |
| `verified` | Recommended | List of `{ by: human:<handle>, at: <ISO 8601> }` — write one when `metadata.status: verified`; omit entirely for unverified |
| `sources` | **Yes (new skills)** | Provenance with `id`/`resource`/`title`/`last_modified`; cite in body via `[^id]` footnotes |
| `status` | Optional | OKF lifecycle: `draft`/`stable`/`deprecated` **only**. Defaults to `stable`. Never `verified`/`unverified` |
| `stale_after` | Optional | `YYYY-MM-DD` — only when a real expiry date exists |
| `metadata.class` | **Yes** | `A`/`B`/`C` — see Skill Classification & Status Metadata |
| `metadata.status` | Optional | `verified`/`unverified`/`draft` — see Skill Classification & Status Metadata |
| `metadata.data-currency` | Recommended | `"YYYY-MM-DD"` of last source verification |
| `metadata` (other keys) | Optional | Key-value extensions |

## domain.md
- Traditional Chinese body
- OKF frontmatter only: `type: Knowledge Entry` and `title` (matching the `# H1`).
  Do not add skill fields (`name`, `description`, `metadata.*`) here — those live in `SKILL.md`
- Natural explanatory text: 使用情境、學習目標、實務應用
- References to official Taiwan codes/standards

```yaml
---
type: Knowledge Entry
title: "排煙窗法規檢討"
---
```

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
4. Write `SKILL.md` with frontmatter (`type: Skill`, `name` must match dir name, `sources` declared)
5. Write `domain.md` in Traditional Chinese with `type: Knowledge Entry` + `title` frontmatter
6. Delete unused `assets/`, `references/`, `scripts/` subdirectories
7. **Update parent `index.md`**: If the parent directory has an `index.md`, add a new entry under `## Skills`. If it doesn't have one but qualifies (multiple children), create it.
8. **Run `python scripts/validate_okf.py`** and fix any error it reports.

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

### Run what the PR ships — do not review from the commit message

When a PR contains a script, or when a previous review asked for a fix, **execute it** rather than
reading the diff and trusting the commit title. Two failures found this way that a diff read would
have missed:

- A contributor's commit said the catalog PDF was replaced by an official URL. The `.xlsx` was
  indeed fixed — but the generated `.json` that `SKILL.md` actually feeds to the AI was never
  regenerated, so all 1,180 records still pointed at a file that had just been deleted from the repo.
  Running the contributor's own converter and diffing its output against the committed file exposed it.
- A `pre-commit` hook declared `language: system` and silently required an unlisted `openpyxl`.
  It exited 1 on any machine without that package — meaning the hook meant to keep those two files
  in sync had never actually run for anyone.

Use a throwaway venv when a script needs packages this repo does not depend on; never install into
the maintainer's environment to test someone's PR.

### Frontmatter must agree with in-body certainty tags

`metadata.status: verified` claims every normative number was transcribed clause-by-clause. If the
body carries `[Unverified]` or `[Secondary]` tags and no `[Verified]` ones, the frontmatter is
overclaiming even when each individual tag is honest — ask for `status: unverified` instead.

### Locality must be visible at the index, not only in the body

A skill covering one municipality's procedure (建照報備, 地籍查詢, 都審) must say so where a reader
meets it first: a `⚠️ 僅適用於OO市` line under `domain.md`'s H1, **and** the municipality in the
parent `index.md` entry. 建築執照 and 地籍 procedures diverge sharply between counties, and someone
browsing `建造執照/index.md` will not read the frontmatter's `region:` key.
[臺中地號查詢](raw/建築執照/基本資料/地方政府地籍查詢系統/臺中市/臺中地號查詢/domain.md) is the
reference example.

### A new rule does not block a PR that predates it

When this repo adopts a convention (OKF v0.2's `type`, a new required field), PRs opened before that
date are **not** sent back for it. Merge on the PR's own merits and backfill in a separate
maintainer commit — see the OKF backfill PRs #50, #52, #53. Tell the contributor explicitly that
they do not need to act on it, so the message does not read as one more round of homework.

Conversely, when a defect class shows up in a real PR, add a check to
`scripts/validate_okf.py` so it cannot recur silently — the duplicate-`name` and B-class-marker
checks both exist because a merged PR had already tripped them.

## Post-Merge Maintenance

After merging a PR, the maintainer must:

1. **Update README `## 📰 最近更新`** — Add a new entry at the top of the list with the format:
   ```
   - **YYYY-MM-DD** {emoji} {brief description} ([#{pr-number}](url) by @author)
   ```
2. **Update `raw/log.md`** — Add the same change under an ISO 8601 `## YYYY-MM-DD` heading
   (newest first) with an `**Update**` / `**Creation**` / `**Deprecation**` prefix. This is the
   machine-readable twin of step 1 (OKF §9).
3. **Update parent `index.md`** — If the PR added or removed skills, sync the parent directory's `index.md` `## Skills` list per [OKF v0.2](#indexmd--directory-index).
4. **Run `python scripts/update_readme_counts.py`** to refresh the skill count table (auto-runs via pre-commit hook if configured, but verify the numbers match).
5. **Run `python scripts/validate_okf.py`** — must report 0 errors. A PR that predates a convention
   will fail here; backfill it in a separate commit rather than reopening the PR (see
   [Pre-Merge Verification](#a-new-rule-does-not-block-a-pr-that-predates-it)).
6. **Sync `SECTION_CLASS`** in `scripts/update_readme_counts.py` when the new skill's
   `metadata.class` differs from its section default — otherwise the README count table and the
   frontmatter disagree.

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
- No frontmatter in `index.md` (except `okf_version` at the bundle root) or `log.md`
- No skill fields (`name`, `description`, `metadata.*`) in `domain.md`
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
