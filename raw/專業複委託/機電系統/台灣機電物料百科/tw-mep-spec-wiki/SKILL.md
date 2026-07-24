---
name: tw-mep-spec-wiki
description: "This skill should be used to search, query, verify, and recommend commercial MEP (Mechanical, Electrical, and Plumbing) materials and specifications in Taiwan from the local JSON database (which currently contains Kaohsingchang piping specs but will expand to include other manufacturers and equipment in the future)."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
metadata:
  audience: architects
  region: taiwan
  class: C
  status: unverified
  data-currency: "2026-07-23"
---

# Taiwan MEP Specifications Skill

## Overview
This skill should be used to search, query, verify, and recommend commercial MEP (Mechanical, Electrical, and Plumbing) materials and specifications in Taiwan. It allows the AI to act as an assistant for the **TW-MEP-Spec-Wiki** database. While the database currently focuses on Kaohsingchang piping items, it is designed to expand and cover various MEP materials and manufacturers in Taiwan. The AI queries the local JSON database to check available specifications, retrieve descriptions, and recommend suitable items based on user requirements.

## File Roles
- **For AI Reading**: [MEP品項百科.json](MEP品項百科.json) is the master JSON database containing 1,180 records of commercial piping specifications.
- **For Human Editing**: [../MEP品項百科.xlsx](../MEP品項百科.xlsx) is the master spreadsheet for humans to maintain and update the catalog.

## Trigger Scenarios
- When a user asks what items are currently available in the database (e.g., "what CNS 6445 pipes are in the catalog?").
- When a user asks for the description, properties, connection methods, or length of a specific pipe specification (e.g., "what is the specification and description for CNS 6445_blk_32A?").
- When a user wants to filter or search the catalog by size (e.g., `32A`, `2"`), coating (`blk`, `gal`), standard (`CNS 6445`, `BS 1387`), or manufacturer (`高興昌`).
- When a user asks for recommendations of suitable MEP items or specifications for a specific engineering scenario or application.

## Guidelines for AI Execution

### 1. Database Querying
- Always load and read [MEP品項百科.json](MEP品項百科.json) to answer user queries. Do not make up or hallucinate pipe specs.
- Support search queries using substring matching on the `"名稱"` (Name) or `"說明"` (Description) fields.

### 2. Formatting Search Results
When a user asks for available items or filters them, format the output as a clean markdown table containing the following columns:
- **編號** (ID)
- **名稱** (Name)
- **廠商** (Manufacturer)
- **說明** (Description) - Show the exact description from the database to explain its uses and specifications.

### 3. Recommending Items based on Requirements
When a user asks what items are suitable for a specific engineering scenario or technical requirement (e.g., "What pipe should be used for a windowless floor?" or "What piping is suitable for small flow rate?"):
- Read the `"說明"` (Description) field of the items in [MEP品項百科.json](MEP品項百科.json) to match the requirements.
- **If suitable items are found in the database**:
  - List the recommended items showing only their **"名稱"** (Name) information.
  - For each recommended item, explain the rationale for the recommendation by extracting and translating the relevant reasons from its **"說明"** (Description) field.
- **If no suitable items are found in the database**:
  - Respond exactly with: "目前資料庫內沒蒐錄適合情況的品項。" (Currently, the database does not contain items suitable for this scenario.)

### 4. Interpreting Specifications
When asked about a specific pipe or MEP item:
- Present its full `"說明"` (Description) directly, as it contains:
  - **Core Purpose** (e.g., "為流體輸送用碳鋼鋼管")
  - **Spec Decoding** (explaining the Standard, Coating type like `blk`/`gal`, and Diameter)
  - **Engineering Notes** (e.g., standard 6m length, threaded vs. welded connection method)
- If the requested item does not exist in the database, explicitly inform the user that it is not found in the catalog (meaning it might be a "virtual spec" not commonly available in the local market) and suggest the closest available alternatives.
