---
type: Skill
name: construction-permit-related-regulations
description: "This skill should be used when architects or construction professionals need to understand the regulatory framework for Taiwan construction permits (建造執照)."
user-invocable: true
metadata:
  class: C
  status: unverified
---
# 建造執照相關法規

> 🚧 **TODO: 尚未依執照別分化。** 本檔內容目前在 使用執照 / 建造執照 / 拆除執照 / 雜項執照 四種執照下完全相同，描述的是建築執照的通用規定。請熟悉 建造執照 的專業者將以下內容替換為該執照別特有的規定。

> ⚠️ **UNVERIFIED — DO NOT QUOTE NUMBERS AS FACT.** The numeric values in this file (fees, penalties, deadlines, thresholds) were drafted from general knowledge and have **not** been verified clause-by-clause against current Taiwan regulations. Before citing any figure: (1) verify the current provision via MCP `taiwan-building-code_search_building_code` or the Laws & Regulations Database (law.moj.gov.tw); (2) never output a penalty or threshold amount without its governing article number. Methodology: see `raw/建築顧問方法論/不確定性標示與來源管控/uncertainty-and-source-control/SKILL.md`.

## Overview

This skill provides comprehensive information about the regulatory framework governing building permit applications in Taiwan. It covers the legal basis, statutory requirements, and enforcement mechanisms applicable to building permit processes.

## Technical Specifications

### Legal Framework
- Taiwan Building Code (建築法)
- Municipal Building Management Ordinances (直轄市建築管理條例)
- Environmental Protection Laws (環境保護法)
- Fire Safety Regulations (消防法)
- Accessibility Standards (無障礙設備設置標準)

### Regulatory Parameters
- Permit validity period: 1-3 years depending on project type
- Renewal requirements: 30 days before expiration
- Amendment procedures: Formal application with supporting documents
- Violation penalties: 10,000 - 500,000 TWD per infraction
- Enforcement authority: Local building department with municipal jurisdiction

### Compliance Requirements
- Building permit issued by municipal authorities
- Annual compliance inspections required
- Construction work restrictions during permit validity
- Post-construction verification and approval
- Penalties for unauthorized construction (up to 100,000 TWD per day)

## Integration Points

### Taiwan Building Code Search
```typescript
taiwan-building-code_search_building_code(query="建築執照")
taiwan-building-code_search_building_interpretations(query="法規")
```

### PCC Specification Downloads
```typescript
pcc-downloader_download_specification(chapter="09", keyword="法規", format="pdf")
pcc-downloader_download_specification(chapter="09", keyword="執行細則", format="pdf")
```