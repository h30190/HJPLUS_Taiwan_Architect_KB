# HJPLUS Taiwan Architect KB - Agent Instructions

## Overview
Knowledge base for Taiwan architects with dual-language skill documentation. All working content lives under `raw/`. Use `知識樣板/` as the template when creating new skills.

## Project Structure
All skill content is in `raw/`. There is no separate published/flat structure.

```
raw/
├── 建築設計與規劃/       (5 skills)
├── 專業複委託/            (4 skills)
├── 建築性能/              (12 skills)
├── 建築法規/              (2 skills)
├── 建築施工與材料/        (5 skills)
├── 建築執照/              (16 skills)
├── 公共工程/              (2 skills)
├── 專案管理/              (skills)
├── 經營管理/              (skills)
├── 室內裝修/              (skills)
└── 設計軟體與工具/        (skills)
```

Template: `知識樣板/` — copy this to create new skills.

## Build / Lint / Test Commands
Documentation-only repository. No build/lint/test commands.

Pre-commit hook (`.pre-commit-config.yaml`): runs `python scripts/run_graphify.py` when `raw/` or `graphify.py` changes. Script may not yet exist.

## Skill Classification
| Class | Description | Requirements |
|-------|-------------|--------------|
| A | International standards | No Taiwan adaptation needed |
| B | International → Taiwan | `<!-- TODO: Taiwan adaptation needed -->` before US/international spec blocks |
| C | Taiwan-specific with MCP | Must include MCP tool call examples |

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
---
```

| Field | Required | Rules |
|-------|----------|-------|
| `name` | Yes | 1-64 chars, lowercase alphanumeric + single hyphens, must match directory name |
| `description` | Yes | 1-1024 chars, must include trigger scenario |
| `license` | Optional | License statement |
| `compatibility` | Optional | Compatibility declaration |
| `metadata` | Optional | Key-value extensions |

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

## C-Class MCP Integration
Include MCP tool call examples:
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
7. Update parent `README.md` if one exists

## Editing Existing Skills
- Never delete `SKILL.md` or `domain.md` without replacement
- If file is lowercase `skill.md`, rename to `SKILL.md`
- Keep frontmatter intact; sync `name` with directory name
- Sync changes between SKILL.md and domain.md
- Preserve `<!-- TODO -->` markers in B-class skills

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
