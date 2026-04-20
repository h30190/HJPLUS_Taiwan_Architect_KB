---
name: building-permit-application-process
description: "This skill should be used when architects or construction professionals need to understand the standard building permit application procedures and requirements in Taiwan."
user-invocable: true
---
# 建築執照申辦流程

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