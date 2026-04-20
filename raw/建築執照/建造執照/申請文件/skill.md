---
name: building-permit-application-documents
description: "This skill should be used when architects or construction professionals need to understand the standard building permit application documents and requirements in Taiwan."
user-invocable: true
---
# 建築執照申請文件

## Overview

This skill provides comprehensive information about the standard building permit application documents required in Taiwan. It covers document types, formatting requirements, submission guidelines, and template specifications.

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