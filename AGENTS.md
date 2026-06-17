# HJPLUS Taiwan Architect KB - Agent Instructions

## Overview
Knowledge base for Taiwan architects with dual-language skill documentation (SKILL.md for AI in English, domain.md for humans in Traditional Chinese).

## Project Structure
```
建築設計與規劃/     (5 skills: concept-design, design-theory, building-typology, spatial-planning, architect-foundations)
專業複委託/          (4 skills: material-selection, building-envelope, structural-systems, building-services)
建築性能/            (4 skills: daylighting-design, acoustic-design, building-sustainability, architect-calculator)
建築法規/            (5 C-class skills with MCP tool integration)
專案管理/            (18 skills: project management subcategories)
經營管理/            (14 skills: professional practice subcategories)
建築施工與材料/      (future)
建築執照/            (future)
.opencode/skills/     (maintenance skills: validate-commit - OpenCode compatible)
```

## Build / Lint / Test Commands
This is a documentation-only repository. No build/lint/test commands apply.

## Skill Classification
| Class | Description | Files |
|-------|-------------|-------|
| A | International standards (no Taiwan adaptation) | skill.md, domain.md |
| B | International → Taiwan adaptation | skill.md with `<!-- TODO: Taiwan adaptation -->`, domain.md |
| C | Taiwan-specific with MCP tools | skill.md, domain.md, MCP tool calls |

## File Format Requirements

### SKILL.md (AI-facing, English)
**Required frontmatter:**
```yaml
---
name: skill-id-hyphenated
description: "Functional summary starting with 'This skill should be used when...'"
user-invocable: true
---
```
**Content sections:**
- H1 `# Skill Title`
- Overview paragraph (trigger scenarios + invocation context)
- `## Section X:` headers with technical specifications
- Tables for parameters/thresholds/classifications
- Code blocks for TypeScript interfaces or formulas
- Horizontal rules `---` between major sections

### domain.md (Human-facing, Traditional Chinese)
**No frontmatter.**
- H1 `# 技能標題`
- Natural explanatory text
- 使用情境、學習目標、實務應用
- References to official Taiwan codes/standards

## Naming Conventions
| Item | Format | Example |
|------|--------|---------|
| Top-level category | Traditional Chinese | `建築設計與規劃/` |
| Subcategory | Traditional Chinese | `設計理論/` |
| **Knowledge Entry** (outer) | **Traditional Chinese** | **`排煙窗法規檢討/`** |
| **AI Skill Directory** (inner) | **lowercase-hyphenated** | **`smoke-exhaust-review/`** |
| Files placement | domain.md in Knowledge Entry dir, SKILL.md in AI Skill dir | see tree below |
| Frontmatter name | lowercase-hyphenated | `name: building-envelope` |

**CRITICAL**: The AI Skill directory name **MUST** exactly match the `name` field in SKILL.md frontmatter. This is a hard requirement of the Agent Skills standard (Claude Code, OpenCode).

### Three-Layer Directory Structure

The actual hierarchy has **three layers** (not two):

```text
子類別/                              ← e.g. 消防安全/
├── README.md                        ← 子類別索引（列出旗下 Knowledge Entries）
│
└── 知識條目中文/                     ← Knowledge Entry (outer, Chinese)
    ├── domain.md                    ← 人類閱讀文件 (Traditional Chinese)
    └── skill-english-hyphenated/    ← AI Skill Directory (inner, lowercase-hyphenated)
        ├── SKILL.md                 ← AI 指令 (English, `name` MUST match this dir name)
        ├── assets/                  ← AI 用附件（可選）
        ├── references/              ← AI 用參考（可選）
        └── scripts/                 ← AI 用腳本（可選）
```

**Key placement rules:**
- `domain.md` lives in the **Chinese** Knowledge Entry directory (one level up from SKILL.md)
- `SKILL.md` lives in the **English** AI Skill directory (inside the Chinese dir)

✅ Correct:
```
消防安全/排煙窗法規檢討/smoke-exhaust-review/SKILL.md
消防安全/排煙窗法規檢討/domain.md
```

❌ Wrong — domain.md in English dir:
```
消防安全/smoke-exhaust-review/domain.md  ← must be in a Chinese parent dir
```

❌ Wrong — SKILL.md in Chinese dir without English subdirectory:
```
消防安全/排煙窗法規檢討/SKILL.md  ← must be in an English-named subdirectory
```

**English translation, NOT pinyin**: The inner AI Skill directory names must be English translations of the concept, never Chinese pinyin.

- ✅ `排煙窗法規檢討/smoke-exhaust-review/SKILL.md`
- ❌ `排煙窗法規檢討/pai-yan-chuang/SKILL.md`
- ❌ `排煙窗法規檢討/assets/skill.md` (SKILL.md must be in the root of the English directory)

## Code Style Guidelines

### Markdown Structure
- One `# H1` per file (skill title)
- Use `##` for major sections, `###` for subsections
- Tables for all structured data (align columns)
- Code blocks with language hint: \`\`\`yaml, \`\`\`typescript
- Bullets use `-`, checkboxes use `- [ ]`
- Horizontal rule `---` between major sections only

### Language Rules
| File | Language | Terminology |
|------|----------|-------------|
| skill.md | English | International technical terms |
| domain.md | Traditional Chinese | 台灣專業術語 |
| Frontmatter | English | Required in skill.md only |

### B-Class Adaptation Marker
Add `<!-- TODO: Taiwan adaptation needed -->` before US/international spec blocks that differ from Taiwan codes.

### C-Class MCP Integration
Include MCP tool call examples with official Taiwan Building Code URLs:
- `taiwan-building-code_search_building_code(query: "活載重")`
- `taiwan-building-code_search_building_interpretations(query: "採光")`
- `pcc-downloader_download_specification(chapter, keyword, format)`

### Internal Links
```markdown
[Parent Category](建築設計與規劃/)
[Sibling Skill](../design-theory/)
```
- Always use relative paths
- Encode spaces as `%20` for paths with spaces (rare in current structure)

## Creating a New Skill
1. Choose category/subcategory directory
2. Copy `知識樣板/` to the target location and rename the outer directory to Traditional Chinese.
3. Inside the Chinese directory, create an inner directory named in **lowercase-hyphenated English only**.
4. Write `SKILL.md` in the English directory with frontmatter + English technical content (the `name` field MUST match the English directory name).
5. Write `domain.md` in the Chinese directory with Traditional Chinese content.
6. Update `Category/Subcategory/README.md` table
7. Update root `README.md` skill count

### Important: Understand the Three Layers

When step 2 says "rename the outer directory", this outer directory becomes the **Knowledge Entry** (Chinese). Inside it, step 3 creates the **AI Skill Directory** (English). These two live **inside** a subcategory:

```text
Category/Subcategory/          ← already exists or chosen in step 1
  Chinese-Knowledge-Entry/     ← renamed from 知識樣板/ (step 2)
    domain.md                  ← human doc here (step 5)
    english-skill-name/        ← created inside (step 3)
      SKILL.md                 ← AI skill here (step 4)
```

## Editing Existing Skills
- Never delete existing `SKILL.md` or `domain.md` without replacement
- Keep frontmatter intact in `SKILL.md`
- Sync changes between skill.md and domain.md
- Preserve `<!-- TODO -->` markers in B-class skills

## MCP Tool Usage for C-Class Skills
```python
# Taiwan Building Code search
taiwan-building-code_search_building_code(query="防火區劃", limit=10)

# Official interpretations
taiwan-building-code_search_building_interpretations(query="避難設施")

# Construction specs
pcc-downloader_download_specification(chapter="09", keyword="09910", format="pdf")
```

## Validation Checklist
Before committing:
- [ ] SKILL.md has valid frontmatter (name, description, user-invocable)
- [ ] SKILL.md is in English with technical precision
- [ ] SKILL.md name matches the directory name exactly
- [ ] domain.md is in Traditional Chinese
- [ ] B-class skills have `<!-- TODO -->` markers
- [ ] C-class skills have MCP tool examples
- [ ] Internal links are relative and work
- [ ] No secrets/credentials in files

## Common Patterns

### Parameter Interface (skill.md)
```typescript
interface SkillParams {
  buildingType: string;
  floorCount: number;
  area: number;
}
```

### Table Format (technical specs)
```markdown
| Condition | Threshold | Reference |
|-----------|-----------|-----------|
| 樓地板面積 | ≧100 m² | 建築技術規則第 97 條 |
```

### Code Example (calculation)
\`\`\`
防火區劃面積 = 樓地板面積 / 防火牆數量
最大面積 ≦ 2000 m² (設置火灑水時)
\`\`\`

## Prohibited
- Do not add frontmatter to domain.md
- Do not use Simplified Chinese in any file
- Do not use Chinese characters in skill directory names (use lowercase-hyphenated English instead)
- Do not hardcode absolute paths
- Do not commit secrets, credentials, or personal data
- Do not remove TODO markers without completing the adaptation

## License

| Content Type | License |
|--|--|
| **Documentation** (`.md` files) | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.en) |
| **Code** (`.sh`, `.py`, `.js`, `.ts`, etc.) | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) |

See [LICENSE](LICENSE) and [LICENSE-CODE](LICENSE-CODE) for full text.
