---
type: Skill
name: miscellaneous-permit-application-process
description: "This skill should be used when architects or construction professionals need to understand the application procedures for Taiwan miscellaneous permits (雜項執照)."
user-invocable: true
metadata:
  class: C
  status: unverified
---
# 雜項執照申辦流程

> 🚧 **TODO: 尚未依執照別分化。** 本檔內容目前在 使用執照 / 建造執照 / 拆除執照 / 雜項執照 四種執照下完全相同，描述的是建築執照的通用規定。請熟悉 雜項執照 的專業者將以下內容替換為該執照別特有的規定。

> ⚠️ **UNVERIFIED — DO NOT QUOTE NUMBERS AS FACT.** The numeric values in this file (fees, penalties, deadlines, thresholds) were drafted from general knowledge and have **not** been verified clause-by-clause against current Taiwan regulations. Before citing any figure: (1) verify the current provision via MCP `taiwan-building-code_search_building_code` or the Laws & Regulations Database (law.moj.gov.tw); (2) never output a penalty or threshold amount without its governing article number. Methodology: see `raw/建築顧問方法論/不確定性標示與來源管控/uncertainty-and-source-control/SKILL.md`.

## Overview

This skill provides comprehensive information about the standard building permit application process in Taiwan. It covers the procedural steps, required documentation, timeline expectations, and fee structures for obtaining building permits across standard municipalities.

## Technical Specifications

### Process Steps
- Initial application submission
- Document review and verification
- Payment processing
- Plan approval
- Permit issuance
- Preliminary inspection

### Required Documentation Types
- Site plan and layout
- Architectural drawings
- Structural calculations
- Mechanical, electrical, and plumbing (MEP) drawings
- Fire safety and life safety systems
- Accessibility compliance forms

### Fee Structure Parameters
- Base fee: 5,000 - 20,000 TWD for small projects
- Additional fees based on project size and complexity
- Annual renewal fees for permits exceeding 1 year
- Penalty fees for late submissions (10-25% of base fee)

### Timeline Expectations
- Standard processing time: 15-30 business days
- Expedited processing available for an additional 50% fee
- Emergency situations may be processed within 5 business days (with appropriate justification)
- Inspection scheduling within 2 business days of permit issuance

## Integration Points

### Taiwan Building Code Search
```typescript
taiwan-building-code_search_building_code(query="建築執照")
taiwan-building-code_search_building_interpretations(query="申請程序")
```

### PCC Specification Downloads
```typescript
pcc-downloader_download_specification(chapter="09", keyword="建築執照", format="pdf")
```