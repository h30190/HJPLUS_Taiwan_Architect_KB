---
type: Skill
name: construction-permit-application-documents
description: "This skill should be used when architects or construction professionals need to understand the required application documents for Taiwan construction permits (建造執照)."
user-invocable: true
metadata:
  class: C
  status: unverified
---
# 建造執照申請文件

> 🚧 **TODO: 尚未依執照別分化。** 本檔內容目前在 使用執照 / 建造執照 / 拆除執照 / 雜項執照 四種執照下完全相同，描述的是建築執照的通用規定。請熟悉 建造執照 的專業者將以下內容替換為該執照別特有的規定。

> ⚠️ **UNVERIFIED — DO NOT QUOTE NUMBERS AS FACT.** The numeric values in this file (fees, penalties, deadlines, thresholds) were drafted from general knowledge and have **not** been verified clause-by-clause against current Taiwan regulations. Before citing any figure: (1) verify the current provision via MCP `taiwan-building-code_search_building_code` or the Laws & Regulations Database (law.moj.gov.tw); (2) never output a penalty or threshold amount without its governing article number. Methodology: see `raw/建築顧問方法論/不確定性標示與來源管控/uncertainty-and-source-control/SKILL.md`.

## Overview

This skill provides comprehensive information about the standard building permit application documents required in Taiwan. It covers document types, formatting requirements, submission guidelines, and template specifications.

**Division of labor**: this skill holds the *nationwide, municipality-agnostic* view — what categories of document a 建造執照 application consists of. It deliberately does **not** carry any single city's checklist composition, portal file-naming codes, or guild procedures. For a Taipei City submission, load [taipei-permit-drawing-standards](../圖面要求/臺北市建照圖說繪製與圖冊編排/taipei-permit-drawing-standards/SKILL.md) alongside this skill: it owns the A101–A7 sheet index, the 44-item Taipei checklist, the N-prefix portal names, and the peer-review stamping / 對副本 sequence.

## Technical Specifications

### Document Types
- Site plan and layout drawings
- Architectural drawings (floor plans, elevations, sections)
- Structural calculations and engineering reports
- Mechanical, electrical, and plumbing (MEP) drawings
- Fire safety and life safety system designs
- Accessibility compliance documentation
- Environmental impact assessment reports
- Zoning compliance certificates

### Template Requirements
- All drawings must be in A1 or A0 format (scale 1:50 or 1:100)
- Digital submission in PDF format required
- All documents must be signed and sealed by licensed professionals
- Structural calculations must include soil bearing capacity reports
- Fire safety designs must include evacuation paths and emergency lighting plans

### Submission Guidelines
- Online submission through municipal building permit portal
- Hard copy submission at local building department
- Required number of document sets: 3 sets (1 original, 2 copies)
- Submission deadline: 10 business days before construction start
- Document review and feedback cycle: 15-20 business days

## Integration Points

### Taiwan Building Code Search
```typescript
taiwan-building-code_search_building_code(query="申請文件")
taiwan-building-code_search_building_interpretations(query="文件格式")
```

### PCC Specification Downloads
```typescript
pcc-downloader_download_specification(chapter="09", keyword="申請文件", format="pdf")
pcc-downloader_download_specification(chapter="09", keyword="設計圖說", format="pdf")
```

## Related Skills

- [taipei-permit-drawing-standards](../圖面要求/臺北市建照圖說繪製與圖冊編排/taipei-permit-drawing-standards/SKILL.md) — Taipei City packaging of the same application: A101–A7 sheet index, 44-item checklist, N-prefix portal file names, 對副本 SOP
- [construction-permit-application-process](../../申辦流程/construction-permit-application-process/SKILL.md) — the application workflow these documents move through
- [design-change-filing](../../變更設計報備/design-change-filing/SKILL.md) — post-issuance design-change report-filing (建築法 §39)