---
name: taiwan-mep-specifications
description: "This skill should be used to search, query, and verify available commercial MEP piping materials and specifications in Taiwan from the local JSON database (such as checking available sizes, coatings, connection methods, and descriptions in the catalog)."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
metadata:
  audience: architects
  region: taiwan
---

# Taiwan MEP Specifications Skill

## Overview
This skill allows the AI to act as an assistant for the **TW-MEP-Spec-Wiki** database. It guides the AI to query the local JSON specification database to tell users what piping items exist in the catalog, filter items by specifications, and retrieve or explain their descriptions.

## File Roles
- **For AI Reading**: [references/MEP品項百科.json](references/MEP品項百科.json) is the master JSON database containing 1,180 records of commercial piping specifications.
- **For Human Editing**: `參考資料/MEP品項百科.xlsx` is the master spreadsheet for humans to maintain and update the catalog.

## Trigger Scenarios
- When a user asks what items are currently available in the database (e.g., "what CNS 6445 pipes are in the catalog?").
- When a user asks for the description, properties, connection methods, or length of a specific pipe specification (e.g., "what is the specification and description for CNS 6445_blk_32A?").
- When a user wants to filter or search the catalog by size (e.g., `32A`, `2"`), coating (`blk`, `gal`), standard (`CNS 6445`, `BS 1387`), or manufacturer (`高興昌`).

## Guidelines for AI Execution

### 1. Database Querying
- Always load and read [references/MEP品項百科.json](references/MEP品項百科.json) to answer user queries. Do not make up or hallucinate pipe specs.
- Support search queries using substring matching on the `"名稱"` (Name) or `"說明"` (Description) fields.

### 2. Formatting Search Results
When a user asks for available items or filters them, format the output as a clean markdown table containing the following columns:
- **編號** (ID)
- **名稱** (Name)
- **廠商** (Manufacturer)
- **說明** (Description) - Show the exact description from the database to explain its uses and specifications.

### 3. Interpreting Specifications
When asked about a specific pipe item:
- Present its full `"說明"` (Description) directly, as it contains:
  - **Core Purpose** (e.g., "為流體輸送用碳鋼鋼管")
  - **Spec Decoding** (explaining the Standard, Coating type like `blk`/`gal`, and Diameter)
  - **Engineering Notes** (e.g., standard 6m length, threaded vs. welded connection method)
- If the requested item does not exist in the database, explicitly inform the user that it is not found in the catalog (meaning it might be a "virtual spec" not commonly available in the local market) and suggest the closest available alternatives.
