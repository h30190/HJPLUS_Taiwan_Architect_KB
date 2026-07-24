---
name: skill-name-hyphenated
description: "This skill should be used when [specific trigger scenarios]. [1-1024 chars]"
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
metadata:
  audience: architects
  region: taiwan
  class: C            # REQUIRED: A (international) / B (adapted) / C (Taiwan-specific)
  status: draft       # verified (clause-checked) / unverified (numbers not checked) / draft
  data-currency: "YYYY-MM-DD"   # date you last verified the sources
---

# Skill Display Title

## Overview
[What this skill does and when to invoke it. Include trigger scenarios. If an overlapping skill
exists, declare the division of labor here (e.g., "pitfalls live here; the calculation algorithm
lives in X") and cross-link it under Related Skills.]

## Execution Steps
1. Step one...
2. Step two...

## Requirements & Constraints
- Required assets: scripts/main.py
- Environment: Python 3.10+

## Worked Example
[At least one complete calculation or judgment walk-through: inputs → rule applied (with article
number) → result. A skill that states rules but shows no worked application is a lookup table,
not a skill.]

## Common Pitfalls
[Real failure modes, one card each:]

### Pitfall: [one-line description]
- **Severity**: 🔴 rejection risk / 🟡 rework risk / 🟢 minor
- **When it bites**: [design stage / permit review / construction]
- **Wrong**: [the mistaken approach]
- **Right**: [the correct approach, with article number]

## AI Design Check Table
[Only for skills that perform compliance checks. ERROR = determinate violation of a verified rule
(cite article); WARNING = source unresolved, resolve before judging; INFO = advisory.
Never emit ERROR from an unverified value.]

| Check | Condition | AI Action |
|---|---|---|
| ... | ... | ERROR/WARNING/INFO: ... |

## Data Currency
- Source: [instrument + article, e.g., 建築技術規則建築設計施工編 §XX]
- Verified: [YYYY-MM-DD, via which channel — MCP / law.moj.gov.tw / agency site]
- Volatility: [HIGH/MEDIUM/LOW — how often this domain amends; when to force re-verification]

## To Verify
- [ ] [Unresolved point — what was tried, where to look next. Do not silently drop open questions.]

## MCP Tool Examples
[C-class skills: show the queries that verify this skill's key numbers.]

```python
taiwan-building-code_search_building_code(query="...", limit=10)
taiwan-building-code_search_building_interpretations(query="...")
```

## Related Skills
- [skill-name](../../相對路徑/skill-name/SKILL.md) — [why a consultant needs it in the same session]

## Additional Resources
- For detailed reference material, see [references/](references/)
- For templates and images, see [assets/](assets/)
