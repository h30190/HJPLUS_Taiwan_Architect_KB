---
name: heritage-incentives-compensation
description: "This skill should be used when advising on the financial incentives and compensations available to owners of cultural heritage properties in Taiwan, including Transfer of Development Rights (TDR) and tax exemptions."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
metadata:
  audience: architects
  region: taiwan
---

# Cultural Heritage Incentives & Compensation (Taiwan)

## Overview
This skill provides guidance on the legal incentives and compensations granted to owners of designated cultural heritage properties in Taiwan (Monuments, Historic Buildings, Commemorative Buildings, etc.). It should be invoked when a client needs to understand the financial offsets for accepting heritage designation, or when conducting a development feasibility study for a site with heritage constraints.

## Execution Steps
1. **Identify Applicable Incentives**: Based on the heritage designation type, determine which incentives apply.
2. **Assess Transfer of Development Rights (TDR)**: Evaluate how much development capacity can be transferred off-site using the TDR mechanism.
3. **Confirm Tax Exemptions**: Verify eligibility for property tax (房屋稅) and land value tax (地價稅) exemptions.
4. **Apply for Subsidies**: Guide the owner in applying for restoration and maintenance grants from the cultural authority.

## Technical Specifications

### 1. Transfer of Development Rights (容積移轉 / TDR)
| Item | Description | Legal Basis |
|------|-------------|-------------|
| **Applicable Properties** | Monuments (古蹟), Historic Buildings (歷史建築), their sites | Cultural Heritage Preservation Act, Art. 41 |
| **Mechanism** | Unused/restricted development capacity of heritage land can be transferred to a "receiving zone" for use in new construction. | 古蹟土地容積移轉辦法 |
| **Benefit** | Allows owners to monetize restricted land rights without demolishing the heritage asset. |  |

### 2. Tax Exemptions (稅捐減免)
| Tax Type | Treatment | Legal Basis |
|----------|-----------|-------------|
| **房屋稅** (Property Tax) | **Exempt (免徵)** for privately-owned Monuments, Historic Buildings, and Commemorative Buildings | Cultural Heritage Preservation Act, Art. 99 |
| **地價稅** (Land Value Tax) | **Exempt (免徵)** for the land site of the above | Cultural Heritage Preservation Act, Art. 99 |

> **Note**: The exemption applies to privately-owned heritage properties. Government-owned properties are handled under separate regulations.

### 3. Restoration & Maintenance Subsidies (修復補助)
- Private owners may apply to county/city cultural affairs bureaus or the Ministry of Culture for financial grants to cover part of the cost of repairs, restoration, and daily maintenance.

## Requirements & Constraints
- TDR application requires a formal appraisal and approval process by the relevant planning and cultural authorities.
- Tax exemptions are not automatic; owners must apply to the local tax authority with proof of heritage designation.

## MCP Tool Integration Examples
```python
# Query for TDR and tax exemption rules
taiwan-building-code_search_building_code(query="古蹟 容積移轉", limit=5)
taiwan-building-code_search_building_interpretations(query="文化資產 房屋稅 地價稅 免徵")
```
