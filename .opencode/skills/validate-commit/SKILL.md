---
name: validate-commit
description: "This skill should be used when validating new contributions, checking PR files, or running full repository checks for HJPLUS Taiwan Architect Knowledge Base."
license: "CC BY-NC-SA 4.0"
compatibility: "opencode"
---

# Validate Commit Skill

This skill validates contributions to the HJPLUS Taiwan Architect Knowledge Base, ensuring consistency, format compliance, and proper licensing before merging.

## When to Use

This skill can be invoked in these scenarios:

1. **Validate a Pull Request** — When reviewing incoming changes from contributors
2. **Pre-commit Check** — Before you commit your own changes locally
3. **Full Repository Audit** — When running periodic checks across all content
4. **New Skill Creation** — When adding new skill.md and domain.md pairs

## Validation Dimensions

### 1. Skill Structure (skill.md + domain.md Pair)

| Check | Expected | File |
|-------|----------|------|
| skill.md exists | Must exist | `[skillname]/skill.md` |
| domain.md exists | Must exist | `[skillname]/domain.md` |
| skill.md frontmatter | Valid YAML frontmatter with `name`, `description`, `user-invocable` | skill.md |
| domain.md no frontmatter | No frontmatter block | domain.md |

### 2. Licensing

| Check | Expected | File |
|-------|----------|------|
| Content (.md) includes CC BY-NC-SA 4.0 | License reference present | *.md files |
| Script (.py/.sh/.js/.ts) includes PolyForm | License reference present | *.py, *.sh, *.js, *.ts |
| LICENSE file exists | Present in root | LICENSE |
| LICENSE-CODE file exists | Present in root (if scripts exist) | LICENSE-CODE |

### 3. Format Standards

| Check | Requirement |
|-------|------------|
| H1 header (#) | One per file at top |
| No Simplified Chinese | zh-CN characters forbidden |
| Relative links only | No absolute paths |
| Tables aligned | Columns properly aligned |
| Code blocks with language hint | \`\`\`yaml, \`\`\`typescript |

### 4. Classification Requirements

| Class | Requirement |
|-------|------------|
| A-class | No Taiwan adaptation markers |
| B-class | Contains `<!-- TODO: Taiwan adaptation needed -->` |
| C-class | Contains MCP tool call examples |

### 5. Naming Conventions

| Item | Format | Example |
|------|--------|---------|
| Category folder | Traditional Chinese | `建築設計與規劃/` |
| Subcategory folder | Traditional Chinese | `設計理論/` |
| Skill folder | lowercase-hyphenated | `concept-design/` |
| Skill files | snake_case | `skill.md`, `domain.md` |
| Frontmatter name | lowercase-hyphenated | `name: building-envelope` |

## Script Usage

Run the validation script:

```bash
bash .opencode/skills/validate-commit/scripts/validate.sh
```

### Interactive Mode

The script will prompt you to select:

1. **Check PR / New Files** — Validate a specific set of new files
2. **Check Single File** — Validate one specific file
3. **Full Repository** — Run all checks across entire repo

### Output

The script outputs:

- **Markdown table** with ✅/❌ status for each check
- **JSON summary** for further processing

## Integration

### Pre-commit Hook (Optional)

To set up automatic validation before commits:

```bash
# Add to .git/hooks/pre-commit
bash .opencode/skills/validate-commit/scripts/validate.sh
```

---

## Validation Checklist

Before merging any PR, ensure:

- [ ] skill.md has valid frontmatter
- [ ] domain.md has no frontmatter
- [ ] All .md files include license reference
- [ ] No Simplified Chinese characters
- [ ] skill.md + domain.md pairs are complete
- [ ] All internal links are relative
- [ ] B-class skills have TODO markers
- [ ] C-class skills have MCP examples

## See Also

- [CONTRIBUTING.md](../CONTRIBUTING.md)
- [LICENSE](../LICENSE)
- [LICENSE-CODE](../LICENSE-CODE)