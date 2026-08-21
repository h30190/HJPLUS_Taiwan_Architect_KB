---
type: Skill
name: design-change-filing
description: "This skill should be used when an architect needs to file a design-change report (報備) for an already-issued building permit (建造執照) in Taipei City — determining whether report-filing applies instead of a full design-change re-application, choosing between self-filing (自行報備) and spot-check filing (抽查後報備), preparing the required forms, walking through the submission-review-duplicate-collation-collection workflow, and sequencing seals correctly when the case involves structural external review (結構外審)."
metadata:
  class: C
  status: unverified
  region: taipei-city
  data-currency: "2026-05-05"
---

# Building Permit Design-Change Filing (變更設計報備)

## Overview

This skill covers the report-filing (報備) pathway for design changes made after a building permit (建造執照) has been issued, during construction, in Taipei City. Report-filing is a lighter-weight alternative to a full design-change re-application, available only when the change meets specific statutory thresholds. It should be invoked when:

- Determining whether a mid-construction design change qualifies for report-filing instead of a full re-application
- Choosing between self-filing (自行報備, L-series forms) and spot-check filing (抽查後報備, K-series forms)
- Preparing the document set for submission
- Walking through the submission → review → duplicate-copy production → in-person collation → collection workflow
- Sequencing the electronic/physical seal steps for a filing that involves structural external review (結構外審)
- Checking whether a change to an urban-design-reviewed (都審) project is exempt from re-review

## Section 1: Legal Basis

| Provision | Content | Relevance |
|-----------|---------|-----------|
| Building Act (建築法) §39 | A design change during construction must generally be re-applied for. **Exception**: if the change does not alter the primary structure or position, does not increase height or floor area, and does not change building equipment content or position, the change may be filed by submitting as-built floor/elevation plans in a single report ("一次報驗") after completion, without a full re-application. | Statutory basis for report-filing in general |
| Building Act §101 | Authorizes municipalities to issue local building management regulations. | Basis for Taipei City's local ordinance below |
| Taipei City Building Management Self-Government Ordinance (臺北市建築管理自治條例) §21 | A design change during construction should generally apply under Building Act §39. **Exception**: for basement-level work, if construction is halted and the supervising architect determines there is a risk to public safety, the contractor together with the supervising architect may proceed with construction under report-filing first, and complete the formal design-change procedure before formwork/rebar assembly of the ground-floor columns and walls. | Taipei-specific report-filing trigger, including the basement emergency-continuation exception |
| Taipei City Urban Design and Land Use Development Permit Review Rules (臺北市都市設計及土地使用開發許可審議規則) §8 | An applicant proposing a design change to an urban-design-approved (都審) project must generally re-submit for review — **unless** the change falls within the "items exempt from re-review" list (都審變更得免辦理變更設計項目一覽表), e.g.: adjustments matching the exempt-items list or not affecting the approved scheme; use changes that don't affect the approved scheme or parking layout; ancillary facility changes that don't affect the streetscape; landscaping changes within the same plant category; or open-space changes that don't affect visibility/accessibility. | Governs whether a 都審 project's change also needs re-review, independent of the building-permit report-filing question |

> ⚠️ **Verify before quoting to a client**: these article numbers were extracted from the firm's internal SOP documents (dated between 2021 and 2026) and cross-checked against the article text, but regulations are amended periodically. Re-confirm current wording via MCP `taiwan-building-code_search_building_code` before relying on it for a specific case.

## Section 2: Decision Framework

```typescript
interface DesignChangeAssessment {
  altersPrimaryStructureOrPosition: boolean;
  increasesHeightOrArea: boolean;
  changesEquipmentContentOrPosition: boolean;
  isBasementWithSafetyRisk?: boolean; // supervising architect's determination
  isUrbanDesignReviewedProject?: boolean;
  matchesUrbanDesignExemptList?: boolean;
}

function requiresFullReapplication(a: DesignChangeAssessment): boolean {
  // Building Act §39: any of these true => full design-change re-application required
  return a.altersPrimaryStructureOrPosition || a.increasesHeightOrArea || a.changesEquipmentContentOrPosition;
}
```

| Question | If true | If false |
|----------|---------|----------|
| Does the change alter primary structure/position, increase height/area, or change equipment content/position? | Full design-change re-application required (Building Act §39) | Eligible for report-filing |
| Is it basement work halted mid-construction with a safety risk per the supervising architect? | May proceed under report-filing first, complete formal design-change procedure before ground-floor column/wall formwork (自治條例 §21) | Standard report-filing timeline applies |
| Is the project under an approved urban-design (都審) case? | Check against the exempt-items list (§8); if not listed, urban-design re-review is also required regardless of the building-permit report-filing outcome | Urban-design re-review not applicable |

## Section 3: Self-Filing vs. Spot-Check Filing

| Path | Forms | Description |
|------|-------|-------------|
| **自行報備 (Self-filing)** | L1-1 ~ L1-4 | Owner/architect prepares and submits documents directly for review, without going through the architects' association spot-check mechanism |
| **抽查後報備 (Spot-check filing)** | K1-1 ~ K1-5 | Documents first pass through the Taipei City Architects' Association spot-check process, then forward to the Building Management Office |

If a case involves both document sets, the L-series form governs (per the firm's internal "文件相關注意事項" guidance: "兩者皆有請附 L 表").

## Section 4: Required Documents

- Design-change drawing set (1 copy) — cloud-line-outlined change area with annotated change content; A1, plain-paper print condition; architectural drawings company-sealed directly, structural drawings sealed by the structural engineer; site plan and ground-floor plan in color
- Original approved permit drawing corresponding to the change (final approved version, with approval seal). Older SOP guidance calls for this to be printed and placed in its own drawing folder.
  `[Unverified]`: a reviewing officer verbally indicated on one case that a printed copy is not required — it can instead be merged into the single scanned PDF submitted with the filing (see Section 5, Step 2), consistent with the 2026-05-05 electronic-upload update but not confirmed against any written notice covering this specific item. This is a single verbal data point, not a documented rule, and may vary by officer or case — **confirm with the reviewing officer before submission**; do not omit the printed copy on the strength of this note alone.
- Supporting documents per the L1-2 checklist
- Design-change report and green-building report if applicable (include backup copy if required)
- Review form (L1-2) and self-check form (L1-3) — strike irrelevant items, check off verified items
- Applicant's contact phone, contact person, and extension must be filled in on the application, so review scheduling calls can reach someone

## Section 5: Process Steps

1. **Prepare documents** — see Section 4. Optionally check current permit status via the Taipei City e-permit platform before submitting.
2. **Submit (掛件)** — bundle documents with drawings in the folder, hole-punched and tied together (not in a binder); register at the Building Management Office's central intake, and note the receipt number. Per the 2026-05-05 process update, the filing's non-drawing documents (review checklist, self-check form, etc. — including the original approved drawing with its approval seal) are first scanned and merged into a single PDF and submitted at this intake step to obtain the official document number. See Section 4 for the `[Unverified]` note on whether the original-drawing scan removes the need for a separately printed copy. Follow up with the reviewing officer roughly 1–2 business days later.
3. **Review** — once assigned to review, expect a call for the fee-payment and review appointment. Bring proof of payment, company seals, and original documents on review day. If corrections are needed, a re-review appointment is arranged and a fresh review form is required. On completion, a perforated/straddle seal (騎縫章) is applied from the first form (L1-1/K1-1) through to the drawing folder.
4. **Produce and submit duplicate copies** — after approval, produce 1 original + 1 duplicate set of drawings (more copies if the firm wants retained sets; one folder per copy). The original white-print set must be color-printed; duplicates may be black-and-white except drawings requiring color (e.g., ground-floor plan). Upload the approved drawings to the digital system, matching the receipt number; color drawings must be uploaded as color PDFs; filenames must follow the document-coding standard.
   - **System upload (備查作業維護 → 副本校對檔案上傳)**: at this stage, **drawings are uploaded as separate files — do not merge them into the combined document PDF used at intake** (Step 2). Before uploading, check the "文件編碼參考" (document coding reference) table shown at the top of the upload screen, and rename each file's prefix to the matching classification code; the system identifies the document category from that prefix automatically. All uploaded files require a QR code.
   - The professional applying the seal must hold a valid architect's practice license issued by the Ministry of the Interior; if someone other than the original design architect applies the seal, that architect's certification documentation must be separately attached.
   - **Structural external review (結構外審) cases — seal sequence matters**: `[Secondary]`, from firm operating practice, not itself a published regulation.
     1. Have the structural engineer provide a file with **only the electronic seal** (structural engineer's e-seal) applied — not yet sent to the architects' association.
     2. The firm uploads that file to the online platform's sealing step, which generates the QR code.
     3. The engineer takes the drawing now bearing the QR code + e-seal, sends it to the architects' association for the association's seal, and applies their own physical seal.
     4. Only after that is complete does the engineer return the drawing to the firm for intake (掛件).
     - **Do not reorder these steps** — applying the physical seal before the platform upload, or sending to the association before the platform-generated QR code exists, can invalidate the QR code or e-seal verification and require redoing the sealing from scratch.
     - Beyond the drawings, the **external review approval letter (外審核准函) and the structural calculation report (結構計算書) also require the five seals (五顆章) of the structural engineers' association** — don't omit these two documents when assembling the seal-bearing set.
   - After printing, record the duplicate-collation case sequence number and the approval document number, and schedule the in-person collation appointment. Per the online system, submission must occur before collation; the case status only becomes "duplicate collation under review" once the sealed duplicate is formally submitted online.
5. **In-person collation and collection** — bring the company seals, a pencil, drawing folders (one per duplicate copy), and the signed collation undertaking. The reviewing officer scans the drawings' QR codes, returns the case file for pagination (starting from page 1, pencil, both sides, blank pages skipped), and provides an original-copy seal, duplicate-copy seal, and text-annotation seal plus a drawing list. Seal placement: drawing list gets the original seal + company seal; the color-printed original set gets the original seal + text-annotation seal; other copies get the duplicate seal + text-annotation seal (keep seal placement consistent across drawings; touching a line is acceptable, touching drawn content is not). Afterward choose to collect the official document in person (usually faster) or by mail; in-person collection requires the text-annotation page to also carry the company seals, confirmed via the Building Management Office the following business day.

## Section 6: Form Reference

| Form | Purpose |
|------|---------|
| L1-1 | Self-filing application |
| L1-2 | Review checklist |
| L1-3 | Self-check checklist |
| L1-4 | Duplicate-collation Word file (filename = permit number), submitted the day review is approved |
| K1-1 ~ K1-5 | Spot-check filing equivalents; K1-5 is the duplicate-collation file, same submission timing as L1-4 |
| 建築師簽證表 | Sealing architect's certification form |
| 校對副本切結書 | Signed undertaking required for in-person collation |
| 都審變更得免辦理變更設計項目一覽表 | Reference list for determining whether an urban-design-reviewed project's change is exempt from re-review |

## Section 7: MCP Integration

```typescript
taiwan-building-code_search_building_code(query: "建築法 第三十九條 變更設計 報備")
taiwan-building-code_search_building_code(query: "臺北市建築管理自治條例 第二十一條")
taiwan-building-code_search_building_interpretations(query: "變更設計 一次報驗")
taiwan-building-code_search_building_code(query: "臺北市都市設計及土地使用開發許可審議規則 第八條 免辦理變更設計")
```

## Section 8: References

- Building Act (建築法) §8, §10, §11, §39, §101
- Taipei City Building Management Self-Government Ordinance (臺北市建築管理自治條例) §1, §13, §21
- Taipei City Urban Design and Land Use Development Permit Review Rules (臺北市都市設計及土地使用開發許可審議規則) §8
- Firm-internal procedural documents: 台北市建照報備SOP (2021-11-22); 各項執照報備審查【文件注意事項】(2022-05-01); 【核准注意事項】(2025-04-02); 【掛號前須知】(2026-05-05) — administrative contact details and staff names redacted for publication; verify current procedure with the Taipei City Building Management Office before relying on scheduling/contact specifics.

## To Verify

- [ ] Whether the original approved drawing genuinely no longer requires a printed/sealed physical copy (Section 4), or whether that was specific to one reviewing officer/case — no written notice found covering this point; ask the Building Management Office directly before relying on it.
- [ ] Current fee schedule for report-filing cases — not covered by the source SOP documents; do not assume figures from the general 建造執照/相關法規 skill apply without checking.
- [ ] Whether the 2026-05-05 merged-PDF-at-intake requirement applies uniformly to both self-filing (L-series) and spot-check filing (K-series) cases, or only to one path — source document did not distinguish.

## Related Skills

- [建造執照/申辦流程](../../申辦流程/construction-permit-application-process/SKILL.md) — initial building permit application (distinct from post-issuance report-filing covered here)
- [建造執照/相關法規](../../相關法規/construction-permit-related-regulations/SKILL.md) — general building-permit regulatory framework
