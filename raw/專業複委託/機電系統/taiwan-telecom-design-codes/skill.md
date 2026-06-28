---
name: taiwan-telecom-design-codes
description: "This skill should be used when checking indoor/outdoor telecommunication equipment setups, including telecom room sizes, lead-in conduits, shafts, and distribution boxes."
user-invocable: true
---

# Taiwan Telecom Equipment Installation Codes

## Context & Purpose
This skill encapsulates the NCC "Indoor and Outdoor Telecommunication Equipment Installation Technical Specifications" (屋內外電信設備設置技術規範) in Taiwan, covering critical space and conduit requirements for telecom infrastructure.

## Parameters & Constraints

### 1. Telecom Room Area Sizing (電信室面積計算)
- Telecom rooms are required for buildings meeting specific thresholds (e.g., based on total floor area or number of households).
- Minimum size limits exist based on building type (e.g., minimum 1.5 m² or 2.0 m² up to much larger areas for commercial complexes).
- The room MUST NOT share space with water tanks, transformer rooms, or any area prone to flooding or strong electromagnetic interference.

### 2. Lead-in Conduits (電信引進管)
- Minimum requirement: At least **2 conduits** must be introduced into the building (1 active, 1 spare).
- For larger buildings, specific diameter and quantity formulas apply (typically 80mm or 100mm PVC/HDPE pipes).

### 3. Telecom Shafts (電信管道間)
- Must be vertically aligned and independent.
- **Prohibited**: Water supply pipes, drainage pipes, and fire sprinkler pipes MUST NOT pass through the telecom shaft.

### 4. Home Distribution Box (宅內配線箱)
- Each household must have a dedicated distribution box.
- Must be equipped with at least one **110V AC power outlet** to power networking equipment (modems, routers).
- Installation height: Usually between 30 cm and 150 cm from the floor finish level, avoiding areas prone to moisture.

## Execution Logic for AI
When reviewing telecom plans:
1. Verify the presence of a dedicated telecom room if the building size dictates it.
2. Check the number of lead-in conduits (must be ≧ 2).
3. Validate that telecom shafts do not contain any plumbing pipes.
4. Ensure home distribution boxes include a 110V power receptacle.
