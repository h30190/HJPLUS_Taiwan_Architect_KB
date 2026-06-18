---
name: adaptive-reuse-plan
description: "This skill should be used when preparing an Adaptive Reuse Response Plan to obtain exemptions from the Building Act or Fire Services Act for cultural heritage projects, proposing alternative safety and compliance measures."
user-invocable: true
---

# Adaptive Reuse Response Plan (再利用因應計畫)

This skill covers the preparation of an Adaptive Reuse Response Plan. Under the Cultural Heritage Preservation Act, if restoring or reusing a heritage building conflicts with modern building, zoning, or fire safety codes, architects can propose alternative measures through this plan to obtain legal exemptions.

## 1. Regulatory Context

- **Primary Law**: Cultural Heritage Preservation Act (文資法)
- **Target Exemptions**: Building Act (建築法), Fire Services Act (消防法), Urban Planning Law (都市計畫法), and Regional Plan Act (區域計畫法).

## 2. Plan Structure

The plan must explicitly detail the conflicts and the proposed alternatives:

| Section | Content |
|---------|---------|
| Project Description | Proposed new use (e.g., converting an old residence into a restaurant). |
| Code Conflict Analysis | Identifying specific articles in the Building Code or Fire Safety regulations that cannot be met without damaging the heritage value. |
| Alternative Measures | Compensatory safety measures. (e.g., strict occupancy limits, independent smoke detectors, enhanced management protocols). |
| Management Plan | Day-to-day operational safety rules. |

## 3. Common Exemptions and Alternatives

- **Fire Safety**: If water sprinklers cannot be installed (to avoid water damage to timber), alternative measures like early warning systems (smoke detectors) and strict ignition source control are proposed.
- **Accessibility**: If ramps cannot be built without altering the historic facade, service alternatives (e.g., staff assistance, accessible facilities in an adjacent new building) may be proposed.
- **Structural Safety**: Justifying the existing structural capacity based on historical performance rather than modern seismic codes, supported by structural assessment.

## 4. MCP Integration

Use these tools to identify the specific regulations that need to be exempted:

```python
# Search for specific building codes to reference in the exemption analysis
taiwan-building-code_search_building_code(query="防火區劃")

# Search for official interpretations regarding heritage exemptions
taiwan-building-code_search_building_interpretations(query="古蹟 再利用 建築法")
```

---
