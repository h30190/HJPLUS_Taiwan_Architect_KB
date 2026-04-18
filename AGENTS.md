# HJPLUS Taiwan Architect KB - Agent Instructions

## Overview
Knowledge base for Taiwan architects with dual-language skill documentation (skill.md for AI in English, domain.md for humans in Traditional Chinese).

## Project Structure
```
建築設計與規劃/     (5 skills: concept-design, design-theory, building-typology, spatial-planning, architect-foundations)
專業複委託/          (4 skills: material-selection, building-envelope, structural-systems, building-services)
建築性能/            (4 skills: daylighting-design, acoustic-design, building-sustainability, architect-calculator)
建築法規/            (5 C-class skills with MCP tool integration)
專案管理/            (future)
經營管理/            (future)
建築施工與材料/      (future)
建築執照/            (future)
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

### skill.md (AI-facing, English)
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
| Skill directory | lowercase-hyphenated | `concept-design/` |
| Files inside skill | snake_case | `skill.md`, `domain.md` |
| Frontmatter name | lowercase-hyphenated | `name: building-envelope` |

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
2. Create `Category/Subcategory/skill-name/`
3. Write `skill.md` with frontmatter + English technical content
4. Write `domain.md` with Traditional Chinese content
5. Update `Category/Subcategory/README.md` table
6. Update root `README.md` skill count

## Editing Existing Skills
- Never delete existing `skill.md` or `domain.md` without replacement
- Keep frontmatter intact in `skill.md`
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
- [ ] skill.md has valid frontmatter (name, description, user-invocable)
- [ ] skill.md is in English with technical precision
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
- Do not hardcode absolute paths
- Do not commit secrets, credentials, or personal data
- Do not remove TODO markers without completing the adaptation

## License
MIT License — see LICENSE file.
