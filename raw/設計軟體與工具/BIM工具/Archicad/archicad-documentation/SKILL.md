---
name: archicad-documentation
description: "This skill should be used when architects need to produce plans, sections, elevations, details, schedules, layouts, issue sets, and PDF or DWG publications from an Archicad model."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
metadata:
  audience: architects
  region: taiwan
---

# Archicad Documentation

This skill covers drawing and document production in Archicad, including saved views, annotation strategy, layout management, drawing updates, schedules, details, and publishing.

---

## Section 1: Documentation Model

### 1.1 Documentation Flow

```text
Model Viewpoint -> Saved View -> Layout Drawing -> Publisher Output
```

| Step | Archicad Area | Key Settings |
|---|---|---|
| Model viewpoint | Project Map | Story, section, elevation, detail, 3D, schedule |
| Saved view | View Map | Scale, layer combination, pen set, graphic override |
| Layout drawing | Layout Book | Sheet size, title block, drawing title, crop, numbering |
| Output | Publisher Sets | File format, folder structure, naming, issue package |

---

## Section 2: Drawing Production

### 2.1 View Discipline

- Create formal output only from saved views, not directly from raw project map viewpoints.
- Use separate saved views for different scales or graphic purposes.
- Keep view names readable and stable, because layout drawings depend on them.
- Use graphic overrides intentionally for presentation, permit, and construction sets.

### 2.2 Annotation Strategy

| Annotation Type | Recommended Use |
|---|---|
| Dimensions | Use project standards and avoid manual overrides |
| Labels | Connect to element information when possible |
| Text notes | Use for drawing-specific explanation |
| Zones | Use for room names, numbers, areas, and schedules |
| Markers | Keep section, elevation, detail, and worksheet references coordinated |

---

## Section 3: Layouts And Publishing

### 3.1 Layout Checklist

- Drawing title matches the layout index.
- Drawing scale is visible and correct.
- Crops do not hide relevant tags, dimensions, or markers.
- Title block fields are populated from project info when possible.
- Revision and issue data match the transmittal.

### 3.2 Publisher Sets

| Output | Use |
|---|---|
| PDF | Formal drawing issue and review |
| DWG | Consultant or contractor exchange |
| BIMx | Model review and client communication |
| Image | Presentation and quick review |
| IFC | BIM coordination, not drawing documentation |

---

## Section 4: QA Before Issue

- Update all placed drawings.
- Check missing external references and linked drawings.
- Confirm sheet order and numbering.
- Review line weights in a real PDF export.
- Open exported DWG in a separate viewer when DWG exchange is required.
- Confirm issue date, revision ID, and file naming before transmission.

