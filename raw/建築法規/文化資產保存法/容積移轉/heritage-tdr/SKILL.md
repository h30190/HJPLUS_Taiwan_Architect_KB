---
name: heritage-tdr
description: "This skill should be used when assessing and processing the Transfer of Development Rights (TDR) for privately-owned cultural heritage properties to compensate owners for development restrictions according to the Cultural Heritage Preservation Act."
user-invocable: true
---

# Heritage Transfer of Development Rights (容積移轉)

This skill provides guidelines for the calculation and application processes regarding the Transfer of Development Rights (TDR) for privately-owned cultural heritage sites. It aims to compensate owners whose development rights are restricted due to heritage designation.

## 1. Regulatory Basis

The primary legal foundations for heritage TDR are:
- **Cultural Heritage Preservation Act**: Allows for the transfer of restricted building volume to other designated receiving sites.
- **Regulations on the Transfer of Floor Area of Historic Sites**: Detailed rules on the calculation and application procedures.
- Local government urban planning ordinances for TDR.

## 2. Calculation and Taxation Benefits

The transferable volume is typically calculated based on the difference between the statutory maximum floor area ratio (FAR) of the heritage site and the actual existing floor area that must be preserved. The exact equivalent value is adjusted based on the official land value of the sending and receiving sites.

**Tax Exemption Benefit**: According to Ministry of Finance rulings, the income generated from the transfer of development rights of cultural heritage is considered equal to the cost expenditure, effectively rendering the transaction **exempt from Income Tax (免徵所得稅)**.

## 3. Transfer Boundaries and Cross-District TDR (跨區容積移轉)

- **Same Major Plan Area (同一主要計畫區)**: By default, TDR must occur within the same major urban plan area. Taipei City is unique in Taiwan as it operates under a single major urban plan, and its intra-district TDR has been streamlined into a **Documentary Review (書面審查)** process, making it significantly faster.
- **Cross-District Transfer (跨區轉移)**: Transferring volume between different major urban plan areas requires special approval. In counties/cities outside of Taipei, cross-district TDR is the practical norm. Urban planning authorities typically process these through the rigorous **Comprehensive Review of Urban Plan (都市計畫通盤檢討)** procedure, which involves a lengthy **3-tier committee review**:
  1. Township / City Level (鄉鎮市)
  2. County / City Level (縣市)
  3. Ministry of Interior Level (內政部)

## 4. Application Process

The architect assists in preparing the TDR proposal:
1. **Feasibility Assessment & Area Verification**: Evaluating the maximum transferable volume. This heavily relies on the initial "Restoration and Adaptive Reuse Plan". Because heritage buildings usually lack original permit drawings, differentiating between the "legal building area" and "illegal structures (違章建築)" is difficult but critical. If the Urban Planning Authority cannot verify the legal area, they will return the case to the Cultural Heritage Authority for clarification, causing severe delays.
2. **Receiving Site Identification**: Finding suitable sites that comply with local zoning regulations to accept the transferred volume.
3. **Plan Submission**: Submitting the comprehensive plan, including architectural drawings and volume calculations, to both Cultural Affairs and Urban Development departments for joint review.

## 5. Contractual and Transaction Risks (合約與交易風險)

- **Unrestricted Receiving Site Designation**: Current TDR sale contracts often grant the buyer the unilateral right to designate *any* receiving site, leaving the seller with no right to object. Furthermore, the relationship between the buyer and the designated receiving site is often undefined in the contract.
- **Risk of Multiple Sales (一地數賣)**: Due to the above ambiguity, if the transaction involves selling the same TDR volume to multiple parties (double-selling) or other ownership disputes arise, the entire legal transaction relationship will collapse, breaking multiple linked sale contracts. Architects advising owners must highlight these severe contractual risks during the TDR trading phase.

## 6. MCP Integration

Use these tools to search for specific regulations regarding TDR in the applicable local jurisdictions:

```python
# Search for national level regulations regarding heritage TDR
taiwan-building-code_search_building_interpretations(query="古蹟土地容積移轉辦法")

# Note: Local zoning and TDR ordinances (e.g., Taipei City TDR Review Guidelines) 
# may need specialized searches or manual consultation depending on the project location.
```

---
