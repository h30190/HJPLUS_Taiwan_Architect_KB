---
name: public-works-quality-library
description: "This skill should be used when architects or project teams need to query, organize, compare, or source-check Taiwan public works quality-management references, inspection forms, supervision references, traffic-maintenance references, occupational safety references, PCIC construction specifications, and public works checklist sources."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
metadata:
  audience: architects
  region: taiwan
---

# Public Works Quality Library

Use this skill to query and organize Taiwan public works quality-management source materials. Keep the work source-backed and explicitly distinguish official requirements from sample templates.

## Source Priority

1. Project contract documents, drawings, special provisions, and owner instructions.
2. Current laws, regulations, Public Construction Commission requirements, and local authority review rules.
3. PCC PCIC construction specifications and official plan/checklist outlines.
4. Local government public templates, review tables, inspection forms, and construction check standards.
5. Legacy samples. Use them only as structure references unless verified against current official requirements.

## Query Workflow

1. Identify the requested topic: quality management, supervision, traffic maintenance, occupational safety, material/equipment testing, inspection forms, construction specifications, or technical rules.
2. Locate the local Obsidian vault or shared source folder. Prefer an explicit path from the user or the `PUBLIC_WORKS_VAULT` environment variable.
3. Search the source library by folder, chapter number, file name, or official agency.
4. Return the most relevant source file names, official links, and a short note on how each source should be used.
5. If the output may be used for formal submission, remind the user to verify current official requirements and project-specific contract conditions.

## Common Source Categories

| Category | Use |
| --- | --- |
| Official outlines and SOP | PCC quality/supervision outlines and local quality-management SOPs |
| Quality and supervision references | Quality-management and supervision structures, review points, and sample formats |
| Traffic maintenance | Local authority formats, traffic control examples, and road activity references |
| Occupational safety | OSH management plans, pre-construction checks, hazard operation checklists |
| Forms and review tables | Submittal, testing, daily report, supervision report, and review forms |
| Inspection standards | Quality standards, autonomous inspection forms, random inspection standards, inspection records |
| Specifications and technical rules | PCIC chapters, local construction specifications, road design and technical standards |

## Useful Search Keys

- `01450` quality management
- `01556` traffic maintenance
- `01574` occupational safety and health
- `02469` drilled concrete piles
- `02722` aggregate base course
- `02742` asphalt concrete pavement
- `03050` concrete materials and general construction requirements
- `03110` concrete formwork
- `03210` reinforcing steel
- `03310` structural concrete

## Output Rules

- Write in Traditional Chinese unless the user asks otherwise.
- Do not invent project facts, contract requirements, inspection frequencies, or acceptance criteria.
- Use placeholders such as `【待確認：契約規範】` when a fact is not available.
- Cite source file names or official links when summarizing requirements.
- Flag old templates, local-government-specific formats, and items needing current official verification.

## Optional Tool Examples

```python
# Search official building-code or interpretation tools when available.
taiwan-building-code_search_building_interpretations(query="公共工程 施工品質 管理")
```

```python
# Search or download PCC construction specifications when a PCC downloader is available.
pcc-downloader_download_specification(chapter="01450", keyword="品質管理", format="pdf")
```
