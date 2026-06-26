---
name: heritage-restoration-phases
description: "This skill should be used to understand and manage the statutory four-phase workflow for cultural heritage restoration and adaptive reuse projects in Taiwan."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
metadata:
  audience: architects
  region: taiwan
---

# Heritage Restoration Phases (Taiwan)

## Overview
This skill outlines the mandatory procedural phases for restoring or adapting cultural heritage (Monuments, Historic Buildings, etc.) in Taiwan. According to the "Regulations for the Restoration and Adaptive Reuse of Monuments," a restoration project MUST proceed through four distinct statutory phases to ensure the historical and cultural value is preserved.

## Execution Steps
1. **Phase 1: Restoration and Adaptive Reuse Plan (Investigation & Research) (修復或再利用計畫 - 調查研究)**
   - Conduct comprehensive historical research, damage assessment, and structural surveys.
   - Establish the guiding principles for restoration and the intended adaptive reuse.
2. **Phase 2: Restoration Design (修復設計)**
   - Develop detailed architectural and engineering drawings based on the approved Plan from Phase 1.
   - Integrate the Adaptive Reuse Response Plan (因應計畫) to address modern building, fire, and accessibility codes.
3. **Phase 3: Construction Supervision (施工監造)**
   - Supervise the construction process to ensure contractors use appropriate traditional techniques, materials, and adhere strictly to the approved design.
4. **Phase 4: Working Report (工作報告書)**
   - Document the entire restoration process, including any newly discovered historical artifacts, structural details uncovered during dismantling, and a complete record of the interventions made.

## Technical Specifications & Requirements

| Phase | Key Deliverables | Regulatory Requirement |
|-------|------------------|------------------------|
| **1. Plan (Research)** | Investigation Report, Restoration Principles | Must be approved by the cultural authority before design begins. |
| **2. Design** | Construction Drawings, Specifications, Budget | Requires specific qualifications for the lead architect. |
| **3. Supervision** | Inspection Records, Material Approvals | Continuous monitoring by qualified personnel. |
| **4. Report** | Final Working Report (工作報告書) | Mandatory for project closure and archival purposes. |

## Requirements & Constraints
- Personnel leading each phase (project directors, architects, supervisors) MUST possess specific qualifications and prior experience in cultural heritage, as defined in the regulations.
- Skipping phases or proceeding to construction without an approved Investigation & Research plan is strictly prohibited.

## MCP Tool Integration Examples
```python
# Search for regulations related to restoration processes
taiwan-building-code_search_building_code(query="古蹟修復及再利用辦法 工作報告書", limit=5)
```
