---
name: archicad-basic-workflow
description: "This skill should be used when architects need to understand Archicad project setup, BIM modeling workflow, view organization, drawing production, and publishing processes."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
metadata:
  audience: architects
  region: taiwan
---

# Archicad Basic Workflow

This skill covers the core Archicad workflow for architectural projects, from project setup and model organization to view creation, layout documentation, coordination, and publishing.

---

## Section 1: Project Startup

### 1.1 Initial Setup Checklist

| Item | Purpose | Typical Decision |
|---|---|---|
| Project origin | Defines the shared reference point | Align with survey or agreed BIM coordination point |
| Stories | Controls vertical building levels | Match architectural levels and structural datums |
| Grid system | Establishes planning and structural references | Coordinate with structural consultant |
| Units | Controls display and documentation precision | Set by office standard and project phase |
| Project location | Supports sun studies and geolocation | Use site location when relevant |
| Attributes | Controls graphic and BIM consistency | Start from office template where possible |

### 1.2 Recommended Early Decisions

- Confirm project phase and expected deliverables before modeling in detail.
- Set story heights before placing major walls, slabs, stairs, and curtain walls.
- Establish layer combinations, model view options, and renovation filters early.
- Use favorites for repeated assemblies, components, and annotation types.
- Define naming conventions for views, layouts, zones, modules, and hotlinks.

---

## Section 2: Modeling Workflow

### 2.1 Model From Big To Small

Start with architectural massing and primary building systems before detailed components.

| Stage | Model Focus | Output |
|---|---|---|
| Concept | Massing, levels, gross zones | Feasibility diagrams and area checks |
| Schematic | Walls, slabs, openings, stairs | Plans, sections, elevations, basic schedules |
| Design development | Assemblies, key details, consultant references | Coordinated drawings and model review |
| Construction documents | Accurate dimensions, annotations, details | Permit or construction drawing package |

### 2.2 Core Elements

- Use walls, slabs, roofs, shells, columns, beams, stairs, railings, doors, and windows as native BIM elements.
- Use Morphs and Objects only when native tools cannot represent the design intent efficiently.
- Keep classification, ID, layer, renovation status, and surface settings consistent.
- Avoid over-modeling details that should be drawn as 2D details or worksheets.

---

## Section 3: Views And Documentation

### 3.1 View Structure

| Archicad Area | Role |
|---|---|
| Project Map | Raw model viewpoints |
| View Map | Saved documentation views with scale and graphic settings |
| Layout Book | Sheet composition and title block management |
| Publisher Sets | Export sets for PDF, DWG, BIMx, or coordination packages |

### 3.2 View Settings To Control

- Scale
- Layer combination
- Model view options
- Graphic overrides
- Pen set
- Renovation filter
- Dimension standard
- Partial structure display

---

## Section 4: Coordination Rhythm

### 4.1 Weekly Coordination Cycle

1. Update linked references, survey files, and consultant models.
2. Review clashes and design changes in 3D and section.
3. Resolve ownership: architectural, structural, MEP, interior, or client decision.
4. Update saved views and affected layouts.
5. Publish a dated coordination set.

### 4.2 Quality Checks

- Model origin and consultant model alignment.
- Story height and level consistency.
- Door and window IDs.
- Zone names, numbers, and areas.
- Layout issue date and revision status.
- PDF output scale and title block information.

