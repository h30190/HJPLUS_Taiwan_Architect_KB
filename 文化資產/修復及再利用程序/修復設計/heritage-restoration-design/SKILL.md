---
name: heritage-restoration-design
description: "This skill should be used when undertaking the architectural restoration design for cultural heritage buildings, detailing preservation methods and compliance with the Regulations for the Restoration and Adaptive Reuse of Historic Monuments."
user-invocable: true
---

# Heritage Restoration Design

This skill defines the procedures and technical requirements for the restoration design of cultural heritage structures, ensuring authenticity and material conservation according to Taiwan's regulations.

## 1. Principles of Restoration

Restoration design must adhere to the core principles established by the cultural heritage authority:
- Minimal intervention.
- Reversibility of applied treatments.
- Distinguishability of new additions from original historical fabric.

## 2. Design Document Requirements

The restoration design submission must include:
1. **Restoration Drawings**: Detailed plans, elevations, sections, and joinery details.
2. **Technical Specifications**: Describing the traditional methods and materials to be used.
3. **Budget Estimation**: Cost analysis for specialized heritage restoration tasks.

## 3. Structural and Material Considerations

| Element | Preservation Strategy |
|---------|-----------------------|
| Timber Structures | Focus on splicing or partial replacement; anti-termite treatment is required. |
| Masonry | Use compatible mortars; avoid high-strength cement that may trap moisture. |
| Roofing | Retain original tile forms and installation methods; improve waterproofing underneath if reversible. |

## 4. Taiwan Building Code / MCP Integration

For integrating modern utility requirements without violating preservation principles:

```python
# Search for official specs related to traditional materials or construction
pcc-downloader_download_specification(chapter="04", keyword="磚石", format="pdf")
```

---
