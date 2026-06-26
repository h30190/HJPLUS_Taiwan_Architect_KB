---
name: archicad-template-setup
description: "This skill should be used when architects need to create, audit, or maintain an Archicad office template with consistent layers, pens, attributes, favorites, composites, layouts, and publishing standards."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
metadata:
  audience: architects
  region: taiwan
---

# Archicad Template Setup

This skill defines the structure and maintenance logic for an Archicad office template. A good template reduces repeated setup work, improves drawing consistency, and supports predictable BIM coordination.

---

## Section 1: Template Scope

### 1.1 Template Contents

| Component | Purpose |
|---|---|
| Stories | Typical level structure and naming logic |
| Layers and layer combinations | Model visibility and documentation control |
| Pen sets | Drawing hierarchy, line weights, and plotting consistency |
| Building materials | Physical, graphic, and priority settings |
| Composites | Standard walls, slabs, roofs, and assemblies |
| Surfaces | Rendering and material identification |
| Fills and lines | Documentation graphics |
| Favorites | Reusable element settings |
| View Map | Standard plan, section, elevation, detail, and schedule views |
| Layout Book | Title blocks, sheet sizes, master layouts, and numbering |
| Publisher Sets | PDF, DWG, BIMx, and coordination outputs |

---

## Section 2: Attribute Management

### 2.1 Attribute Governance

- Use a naming convention that groups attributes by type, discipline, and purpose.
- Keep layer combinations limited and meaningful.
- Avoid duplicate materials with slightly different names.
- Assign building material priorities deliberately to support clean junctions.
- Keep pen sets stable after production drawings begin.

### 2.2 Naming Pattern Examples

| Item | Pattern | Example |
|---|---|---|
| Layer | Discipline - Element - Status | A-Wall-New |
| Composite | Element - Assembly - Thickness | Wall-RC-200 |
| Surface | Material - Finish | Concrete-Exposed |
| Favorite | Tool - Assembly - Use | Wall-RC-Exterior |
| View | Phase - Type - Scale | DD-Plan-1-100 |

---

## Section 3: Template QA

### 3.1 Audit Checklist

- Remove unused or duplicated attributes before releasing a template update.
- Test default wall, slab, door, window, stair, railing, object, and zone favorites.
- Publish a sample PDF set and inspect line weight, fonts, fills, and title block data.
- Export a sample DWG and check layer mapping.
- Export a sample IFC and check classification, properties, and model alignment.

### 3.2 Update Rules

- Version the template and record changes in a short changelog.
- Avoid changing production standards in the middle of a live project unless necessary.
- Keep project-specific fixes out of the office template until they are reviewed.
- Archive old templates so past projects can still be opened with their original standards.

