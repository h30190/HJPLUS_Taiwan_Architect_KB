# HJPLUS Taiwan Architect KB - Agent Instructions

## Overview

This is a knowledge base for architects working in Taiwan, containing architectural skills organized into 8 main categories. Each skill has dual-language documentation: **skill.md** (English for AI) and **domain.md** (Traditional Chinese for humans).

## Project Structure

```
├── Design & Planning/           (5 skills: 4A+1B)
├── Technical Knowledge/         (4 skills: 1A+3B)
├── 性能/                       (4 skills: 4B)
├── Building Codes & Regulations/ (5 skills: 5C)
├── Project Management/          (0 skills - future)
├── Professional Practice/       (0 skills - future)
├── Construction Materials/      (0 skills - future)
└── Specialized Fields/          (0 skills - future)
```

### Skill Classification

| Class | Count | Description |
|-------|-------|-------------|
| A | 5 | General international standards |
| B | 8 | International → Taiwan adaptation (with TODOs) |
| C | 5 | Taiwan-specific regulations with MCP tools |

## File Format Guidelines

### skill.md (AI Documentation)
- **Language**: English
- **Frontmatter**: Required (name, description, user-invocable)
- **Style**: Technical, precise, actionable
- **Content**: Core capabilities, AI operation guide, technical specifications
- **Example frontmatter**:
```yaml
---
name: concept-design
description: Parti development, massing studies, spatial organization strategies
user-invocable: true
---
```

### domain.md (Human Documentation)
- **Language**: Traditional Chinese (繁體中文)
- **Style**: Natural, explanatory, learnable
- **Content**: Usage context, learning objectives, practical applications
- **No frontmatter required**

### Naming Conventions
- **Directories**: Chinese for categories (設計理論，材料設備), English for skills (concept-design, structural-systems)
- **Files**: snake_case (skill.md, domain.md, concept-design.md)
- **Skills**: Lowercase with hyphens (building-envelope, taiwan-building-codes)
- **References**: Use relative links with proper space encoding

## Code Style Guidelines

### Markdown Formatting
- Use `#` for H1 (once per file), `##` for H2 sections, `###` for H3 subsections
- Use tables for structured data with proper alignment
- Use code blocks for technical specifications: \`\`\`yaml
- Use bullet points with `-` for lists
- Use checkboxes `- [ ]` for task lists
- Use horizontal rules `---` to separate major sections

### Language & Localization
- **skill.md**: International English, technical terminology
- **domain.md**: Traditional Chinese, natural language
- **B-class skills**: Add `<!-- TODO: Taiwan adaptation needed -->` where norms differ
- **C-class skills**: Use Taiwan Building Code official terminology

### Link Format
```markdown
[Link Name](Design%20&%20Planning/設計理論/concept-design/)
```
- Always encode spaces as `%20`
- Use relative paths from the same directory level

### Error Handling Documentation
- Include fallback procedures in `skill.md`
- Use `<thinking>` blocks for AI chain-of-thought
- Document Taiwan code references with official URLs for C-class skills

## Development Workflow

### Creating a New Skill
1. Determine skill classification (A/B/C)
2. Create directory: `Category/Subcategory/skill-name/`
3. Write `skill.md` with frontmatter and English content
4. Write `domain.md` with Traditional Chinese content
5. Add to category `README.md` table
6. Update ROOT `README.md` if adding new category

### Updating Existing Content
- Maintain backward compatibility in skill names
- Preserve TODO markers for B-class adaptations
- Reference Taiwan Building Code for C-class skills
- Keep both `skill.md` and `domain.md` in sync

### MCP Tool Usage
- **taiwan-building-code_search_building_code**: Search Taiwan Building Code articles
- **taiwan-building-code_search_building_interpretations**: Search official interpretations
- **pcc-downloader_***: Download construction specifications
- Always provide official URLs for verification

## Quality Standards

### skill.md Requirements
- ✅ Frontmatter with name, description, user-invocable
- ✅ Comprehensive technical content
- ✅ Clear AI operation guidelines
- ✅ Structured sections with H2/H3 headers
- ✅ Tables for specifications/parameters

### domain.md Requirements
- ✅ Traditional Chinese language
- ✅ Usage context explanation
- ✅ Learning objectives
- ✅ References and resources

### Documentation Checklist
- [ ] skill.md has proper frontmatter
- [ ] skill.md is in English with technical terms
- [ ] domain.md is in Traditional Chinese
- [ ] Files are linked in parent README.md
- [ ] B-class skills have TODO markers
- [ ] C-class skills reference official sources
- [ ] No secrets or credentials in files

## Common Tasks

### Add a New Skill
```bash
# 1. Create directory structure
mkdir -p "Category/Subcategory/new-skill/"

# 2. Create skill.md with frontmatter
# 3. Create domain.md with Chinese content
# 4. Update Category/Subcategory/README.md
# 5. Update ROOT README.md if adding new category
```

### Search Taiwan Building Code
```python
# Use taiwan-building-code_search_building_code MCP tool
query = "活載重"  # Live load
# Returns official law articles
```

### Download Construction Specifications
```python
# Use pcc-downloader tools
chapter = "09"  # Chapter code
keyword = "09910"  # Specification code
```

## Contribution Rules

1. **Follow existing structure**: Match the pattern of existing skills in same category
2. **Maintain dual language**: Always update both skill.md and domain.md
3. **Classify correctly**: A (general), B (adapted), C (Taiwan-specific)
4. **Use TODO markers**: Document adaptation gaps in B-class skills
5. **Reference sources**: Link to Taiwan Building Code for C-class skills
6. **Test links**: Verify all relative links work
7. **Keep it clean**: No secrets, credentials, or personal data

## License

MIT License - see LICENSE file for details.
