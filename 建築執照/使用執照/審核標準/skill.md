---
name: building-permit-review-standards
description: "This skill should be used when architects or construction professionals need to understand the standard building permit review criteria and compliance requirements in Taiwan."
user-invocable: true
---
# 建築執照審核標準

## Overview

This skill provides comprehensive information about the standard building permit review criteria and compliance requirements in Taiwan. It covers the technical standards, safety requirements, and regulatory compliance measures applied during building permit approvals.

## Technical Specifications

### Compliance Standards
- Building code compliance (Taiwan Building Code)
- Structural safety standards
- Fire safety and life safety requirements
- Accessibility compliance (ADA standards)
- Environmental protection regulations
- Urban planning and zoning requirements

### Review Categories
- Design compliance verification
- Safety system adequacy assessment
- Environmental impact evaluation
- Zoning and land use conformity
- Structural stability verification
- Fire resistance and evacuation planning

### Standard Parameters
- Structural load capacity requirements (minimum 150 kg/m² for residential)
- Fire resistance rating (minimum 60 minutes for critical areas)
- Accessibility requirements (minimum 1.2m clear width for corridors)
- Environmental impact thresholds (noise level: ≤70 dB(A) during daytime)
- Zoning compliance requirements (floor area ratio limits)

## Integration Points

### Taiwan Building Code Search
```typescript
taiwan-building-code_search_building_code(query="審查標準")
taiwan-building-code_search_building_interpretations(query="安全標準")
```

### PCC Specification Downloads
```typescript
pcc-downloader_download_specification(chapter="09", keyword="審查標準", format="pdf")
pcc-downloader_download_specification(chapter="09", keyword="安全要求", format="pdf")
```