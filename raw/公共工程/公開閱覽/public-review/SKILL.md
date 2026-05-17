---
name: public-review
description: "This skill should be used when an architect needs to understand Taiwan's public review (公開閱覽) procedures for government procurement, including how to review tender documents, provide professional feedback, and evaluate project opportunities before formal bidding."
user-invocable: true
---

# Public Review (公開閱覽)

This skill covers Taiwan's public review (公開閱覽) process under the Government Procurement Act, a pre-tender procedure where procurement documents are made available for industry feedback. Invoke this skill when reviewing upcoming procurement opportunities, preparing feedback on tender documents, or evaluating whether to participate in subsequent formal bidding.

---

## Section 1: Legal Framework

### 1.1 Governing Provisions

| Law | Article | Content |
|-----|---------|---------|
| Government Procurement Act (政府採購法) | Art. 34 | Public review requirements for tender documents |
| Enforcement Rules | Art. 43 | Detailed procedures for public review process |
| Public Construction Technical Service Contract Template | Full text | Standard contract clauses reference |

### 1.2 When Public Review is Required

| Condition | Requirement |
|-----------|-------------|
| Above announcement threshold (≧ NTD 1,000,000) | May conduct public review |
| Complex or large-scale projects | Recommended by PCC guidelines |
| Projects with novel technical requirements | Recommended to reduce disputes |
| Above audit threshold (≧ NTD 50,000,000) | Strongly recommended |

---

## Section 2: Public Review Process

### 2.1 Process Flow

```
1. Publication
   └─ Procuring entity posts notice on Government e-Procurement System
   └─ Documents made available for download/inspection

2. Review Period
   └─ Typically 5-7 working days
   └─ Minimum period per PCC guidelines

3. Feedback Submission
   └─ Written comments submitted by interested parties
   └─ Format: per procuring entity requirements (usually written/email)

4. Agency Response
   └─ Procuring entity compiles all feedback
   └─ Public response to each comment (accepted/rejected with rationale)

5. Document Revision
   └─ Tender documents revised based on accepted feedback
   └─ Revision history documented

6. Formal Tender
   └─ Revised documents used for formal bidding process
```

---

## Section 3: Key Review Areas for Architects

### 3.1 Document Review Checklist

| Area | What to Check | Common Issues |
|------|--------------|---------------|
| Scope Definition | Clear work items, deliverables | Ambiguous scope, missing items |
| Fee Calculation | Alignment with official fee standards | Below-standard fees, unclear payment schedule |
| Design Timeline | Reasonable duration per project complexity | Unrealistic deadlines |
| Evaluation Criteria | Weight distribution, objectivity | Over-emphasis on price vs. quality |
| Contract Terms | Risk allocation, liability clauses | Unfair risk transfer to service provider |
| Penalty Clauses | Delay penalties, liquidated damages | Excessive penalty rates |
| Technical Requirements | Specifications clarity | Restrictive specs limiting competition |

### 3.2 Feedback Categories

| Category | Priority | Example |
|----------|----------|---------|
| Legal compliance | High | Contract clause contradicts Procurement Act |
| Fee adequacy | High | Fee below 機關委託技術服務廠商計費標準 minimum |
| Timeline feasibility | High | Design period insufficient for required regulatory reviews |
| Risk allocation | Medium | Unfair force majeure clause |
| Technical clarity | Medium | Ambiguous performance specifications |
| Competition fairness | Medium | Specs written for specific vendor |

---

## Section 4: Strategic Considerations

### 4.1 Benefits of Participation

- Influence tender conditions before they become binding
- Early insight into upcoming project opportunities
- Build relationship with procuring entities
- Demonstrate expertise and market awareness

### 4.2 Best Practices

| Practice | Rationale |
|----------|-----------|
| Submit specific, actionable feedback | Generic complaints are less likely to result in changes |
| Reference official standards and regulations | Strengthens the basis for requested changes |
| Coordinate through professional associations (建築師公會) | Collective feedback carries more weight |
| Maintain written records of all submissions | Documentation for potential future disputes |
| Attend pre-bid meetings if offered | Additional context beyond written documents |

---

## Section 5: MCP Tool Integration

```python
# Search Government Procurement Act provisions on public review
taiwan-building-code_search_building_code(query="政府採購法 公開閱覽")

# Search interpretations on tender document requirements
taiwan-building-code_search_building_interpretations(query="招標文件 公開閱覽")

# Download procurement-related specifications
pcc-downloader_download_specification(chapter="procurement", keyword="公開閱覽", format="pdf")
```
