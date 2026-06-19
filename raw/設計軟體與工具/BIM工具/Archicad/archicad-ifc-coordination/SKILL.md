---
name: archicad-ifc-coordination
description: "This skill should be used when architects need to exchange Archicad models through IFC, coordinate consultant models, map classifications and properties, and troubleshoot BIM interoperability issues."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
metadata:
  audience: architects
  region: taiwan
---

# Archicad IFC Coordination

This skill covers IFC-based coordination workflows in Archicad, including model exchange setup, classification, property mapping, translator settings, consultant model review, and issue tracking.

---

## Section 1: IFC Coordination Purpose

IFC exchange is used to coordinate BIM information across software platforms. In architectural practice, IFC is most often used for structural coordination, MEP coordination, quantity review, clash detection, and model delivery.

### 1.1 What IFC Should Carry

| Information Type | Examples |
|---|---|
| Geometry | Walls, slabs, doors, windows, stairs, spaces |
| Classification | Element type and BIM classification |
| Properties | Fire rating, acoustic rating, material, ID, phase |
| Spatial structure | Site, building, story, space |
| Location | Project origin, elevation, and coordinate reference |

---

## Section 2: Export Preparation

### 2.1 Model Cleanup

- Confirm project origin, story settings, and coordinate agreement.
- Remove temporary design options or clearly exclude them through layers.
- Check element IDs, classifications, and renovation status.
- Confirm zones and spaces if area or room information is required.
- Use a dedicated export view or 3D view for IFC output.

### 2.2 Translator Decisions

| Setting | Decision Question |
|---|---|
| Geometry conversion | Should elements export as extruded, BREP, or precise geometry? |
| Element filtering | Which layers, stories, or element types should be included? |
| Property mapping | Which Archicad properties map to IFC properties? |
| Classification | Which classification system drives IFC type assignment? |
| Coordinate handling | Should the model use project origin or survey coordinates? |

---

## Section 3: Import And Reference Models

### 3.1 Consultant Model Review

- Import or hotlink consultant IFC models into a coordination file when possible.
- Check model alignment in plan, section, and 3D.
- Compare story heights, grids, and major levels.
- Use model filters and graphic overrides to isolate consultant elements.
- Record issues with screenshots, coordinates, element IDs, and responsible party.

### 3.2 Common Problems

| Problem | Likely Cause | Check |
|---|---|---|
| Model is far away | Different origin or survey coordinate handling | Project location and translator coordinate settings |
| Elements are missing | Layer, story, renovation, or element filter excluded them | Export view and translator filters |
| Wrong element type | Missing or incorrect classification | Classification and IFC type mapping |
| Heavy file | Overly precise geometry or unnecessary objects | Geometry conversion and export scope |
| Bad material data | Attribute or property mapping issue | IFC property mapping |

---

## Section 4: Coordination Deliverables

- Dated IFC model.
- PDF or image export showing model scope.
- Model issue list or coordination log.
- Export translator name and version.
- Coordinate basis statement.
- Change summary since previous exchange.

