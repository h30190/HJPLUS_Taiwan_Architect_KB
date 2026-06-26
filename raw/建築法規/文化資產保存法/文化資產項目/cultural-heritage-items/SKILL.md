---
name: cultural-heritage-items
description: "This skill should be used when assessing the categories of cultural heritage defined by the Cultural Heritage Preservation Act in Taiwan, especially during site analysis and architectural planning."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
metadata:
  audience: architects
  region: taiwan
---

# Cultural Heritage Items (Taiwan)

## Overview
This skill provides the classification of cultural heritage according to Taiwan's Cultural Heritage Preservation Act (Article 3). It should be invoked when evaluating site constraints, historical preservation projects, or when a project site involves potential cultural heritage elements.

## Execution Steps
1. Identify if the project site contains or is adjacent to any registered cultural heritage.
2. Categorize the heritage based on the statutory definitions (Tangible, Intangible, or Preservation Technology).
3. Determine the specific type (e.g., Monument, Historic Building, Archaeological Site) to apply the correct regulatory procedures.

## Technical Specifications (Cultural Heritage Categories)

### 1. Tangible Cultural Heritage (有形文化資產)
| Category | Definition / Architectural Relevance |
|----------|--------------------------------------|
| **Monuments** (古蹟) | Historic works, buildings, or places with immense historical, artistic, or scientific value. Strict preservation rules apply. |
| **Historic Buildings** (歷史建築) | Historic structures or places with historical or cultural value, subject to preservation and adaptive reuse guidelines. |
| **Commemorative Buildings** (紀念建築) | Buildings and ancillary facilities associated with significant historical figures. |
| **Groups of Buildings** (聚落建築群) | Architecturally and environmentally integral groups of traditional or historic buildings. |
| **Archaeological Sites** (考古遺址) | Areas containing ancient human remains and associated artifacts. Requires preliminary surveys before development. |
| **Historic Sites** (史蹟) | Places of historic events with historical or cultural value. |
| **Cultural Landscapes** (文化景觀) | Environments reflecting the interaction between humans and nature. |
| **Antiquities** (古物) | Works of art, daily utensils, etc., of historical or artistic value. |
| **Natural Landscapes & Monuments** (自然地景、自然紀念物) | Natural environments with preservation value. |

### 2. Intangible Cultural Heritage (無形文化資產)
Includes Traditional Performing Arts (傳統表演藝術), Traditional Crafts (傳統工藝), Oral Traditions (口述傳統), Folklore (民俗), and Traditional Knowledge and Practices (傳統知識與實踐).

### 3. Preservation Technology & Preservers (保存技術及保存者)
Specialized techniques required for preserving, restoring, or maintaining cultural heritage.

## Requirements & Constraints
- Information provided must align with the latest version of the Cultural Heritage Preservation Act (文化資產保存法).
- Any adaptive reuse (再利用) or restoration of tangible architectural heritage requires approval from the relevant cultural affairs authority.

## MCP Tool Integration Examples
```python
# Query relevant building codes or interpretations for cultural heritage
taiwan-building-code_search_building_code(query="文化資產", limit=5)
taiwan-building-code_search_building_interpretations(query="古蹟")
```
