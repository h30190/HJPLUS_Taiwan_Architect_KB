---
name: public-bidding
description: "This skill should be used when an architect needs guidance on Taiwan's public open bidding (公開招標) procedures under the Government Procurement Act, including bid preparation, evaluation criteria, threshold amounts, and compliance requirements."
user-invocable: true
---

# Public Bidding (公開招標)

This skill covers Taiwan's open bidding procedures for public works under the Government Procurement Act (政府採購法). Invoke this skill when preparing bid documents, evaluating procurement opportunities, understanding threshold requirements, or navigating the evaluation and selection process for architectural services in government projects.

---

## Section 1: Legal Framework

### 1.1 Governing Legislation

| Law | Scope |
|-----|-------|
| Government Procurement Act (政府採購法) | Primary procurement law, 114 articles |
| Enforcement Rules of the Government Procurement Act | Detailed implementation procedures |
| Regulations for Selection and Fee Calculation of Technical Service Providers (機關委託技術服務廠商評選及計費辦法) | Architect/engineer selection and fee standards |
| Organization Regulations for Procurement Evaluation Committees (採購評選委員會組織準則) | Evaluation committee structure and procedures |

### 1.2 Procurement Methods

| Method | Chinese | Article | When Used |
|--------|---------|---------|-----------|
| Open Bidding | 公開招標 | Art. 19 | Default method; public notice inviting all qualified suppliers |
| Selective Bidding | 選擇性招標 | Art. 20 | Pre-qualified supplier list; invitation from qualified pool |
| Limited Bidding | 限制性招標 | Art. 22 | Specific conditions (sole source, emergency, specialized expertise) |

---

## Section 2: Threshold Amounts

| Threshold | Amount (NTD) | Requirements |
|-----------|-------------|--------------|
| Below Announcement Threshold | < 1,000,000 | Direct contracting or price comparison allowed |
| Announcement Threshold (公告金額) | ≧ 1,000,000 | Must publish on Government e-Procurement System |
| Audit Threshold (查核金額) | ≧ 50,000,000 | Requires superior agency approval and enhanced review |
| Large-Scale Procurement (巨額採購) | ≧ 200,000,000 | International bidding required (WTO/GPA compliance) |

---

## Section 3: Bidding Process for Architectural Services

### 3.1 Process Flow

```
1. Opportunity Identification
   └─ Search Government e-Procurement System (政府電子採購網)
   └─ URL: https://web.pcc.gov.tw/

2. Document Acquisition
   └─ Download or purchase tender documents
   └─ Review scope, schedule, budget, evaluation criteria

3. Team Formation
   └─ Lead: Licensed Architect (建築師)
   └─ Structural Engineer (結構技師)
   └─ MEP Engineer (機電技師)
   └─ Other specialists as required

4. Proposal Preparation
   └─ Technical Proposal (服務建議書)
   └─ Fee Proposal (報價單)
   └─ Qualification Documents (資格文件)

5. Submission
   └─ Before deadline (截止投標日)
   └─ Required documents per tender specifications

6. Evaluation
   └─ Presentation to Evaluation Committee (評選委員會)
   └─ Scoring based on published criteria
   └─ Committee: 5-17 members, ≧ 1/3 external experts

7. Negotiation
   └─ Price negotiation with highest-ranked proposer
   └─ If negotiation fails, proceed to next-ranked

8. Contract Award
   └─ Contract execution
   └─ Performance bond: typically 5-10% of contract value
```

### 3.2 Evaluation Criteria (Typical)

| Criterion | Weight Range | Key Elements |
|-----------|-------------|--------------|
| Technical Approach | 30-40% | Design methodology, innovation, feasibility |
| Team Qualifications | 20-30% | Experience, certifications, track record |
| Project Understanding | 15-20% | Site analysis, regulatory awareness, risk identification |
| Schedule | 10-15% | Milestone plan, resource allocation |
| Fee Proposal | 10-20% | Reasonableness, value for money |

---

## Section 4: Key Compliance Requirements

### 4.1 Joint Venture Bidding (共同投標)

- Permitted for large-scale projects requiring multi-disciplinary teams
- Lead firm (代表廠商) must be clearly designated
- Joint and several liability among all members
- Revenue/responsibility split must be defined in agreement

### 4.2 Subcontracting Restrictions

- Primary services cannot be subcontracted entirely
- Subcontracting limits typically 30-50% of contract value
- Must obtain procuring entity approval for subcontractors
- Architect remains primarily liable regardless of subcontracting

### 4.3 Performance Guarantee

| Item | Typical Requirement |
|------|-------------------|
| Bid Bond (押標金) | 1-5% of budget estimate |
| Performance Bond (履約保證金) | 5-10% of contract value |
| Warranty Bond (保固保證金) | 1-3% of contract value |
| Warranty Period | 1-5 years depending on project type |

---

## Section 5: MCP Tool Integration

```python
# Search Government Procurement Act provisions
taiwan-building-code_search_building_code(query="政府採購法 公開招標")

# Search official interpretations on procurement
taiwan-building-code_search_building_interpretations(query="技術服務 評選")

# Download procurement specifications
pcc-downloader_download_specification(chapter="procurement", keyword="公開招標", format="pdf")
```

---

## Section 6: Common Pitfalls

| Pitfall | Risk | Mitigation |
|---------|------|------------|
| Incomplete qualification documents | Bid rejection | Use checklist per tender requirements |
| Underestimating fee proposal | Financial loss during execution | Reference 機關委託技術服務廠商計費標準 |
| Missing submission deadline | Disqualification | Set internal deadline 2 days before official |
| Non-compliant team composition | Bid rejection | Verify all required licenses before submission |
| Ignoring site visit requirements | Weak proposal | Attend all mandatory site visits |
