---
type: Skill
name: permit-report-data-mapping
description: "This skill should be used when mapping a legacy CPAMI permit report identifier to its actual BMS data groups, computed display fields, or unresolved template dependencies."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
sources:
  - id: specified-mapping
    resource: https://github.com/Archwiz-boss/BOOKTIRE/blob/06450a39315f453667db995641b4fdc4d0875ac1/CPAMI_%E6%8C%87%E5%AE%9A%E6%9B%B8%E8%A1%A8_%E5%AF%A6%E7%94%A8%E6%95%B8%E6%93%9A%E5%B0%8D%E6%87%89%E8%A1%A8.md
    title: CPAMI specified-report practical data mapping
    last_modified: 2026-07-16
  - id: b-mapping
    resource: https://github.com/Archwiz-boss/BOOKTIRE/blob/6130a8a667477d4db1c771d95e288932059ff963/CPAMI_B%E7%B3%BB%E5%88%97%E6%9B%B8%E8%A1%A8_%E6%95%B8%E6%93%9A%E5%B0%8D%E6%87%89%E8%A1%A8.md
    title: CPAMI B-series report data mapping
    last_modified: 2026-07-14
  - id: cd-mapping
    resource: https://github.com/Archwiz-boss/BOOKTIRE/blob/f3c8639ea9821bf9a32c1b7e6c6b8589092d58a3/CPAMI_CD%E7%B3%BB%E5%88%97%E6%9B%B8%E8%A1%A8_%E6%95%B8%E6%93%9A%E5%B0%8D%E6%87%89%E8%A1%A8.md
    title: CPAMI C/D-series report data mapping
    last_modified: 2026-07-14
metadata:
  audience: architects
  region: taiwan
  class: C
  status: unverified
  data-currency: "2026-07-16"
---

# Permit Report Data Mapping

## Scope and trust boundary

[Secondary] This is an implementation-facing routing aid derived from pinned upstream reverse-engineering documents, not an official CPAMI form specification. It maps report IDs to observed storage groups; it does not establish filing requirements or legal validity.[^specified-mapping]

Use the detailed [report matrix](references/report-matrix.md) before changing an importer, report adapter, or payload schema.

## Workflow

1. Identify the exact report ID and its template/version; do not infer from a family letter alone.
2. Look up its 13-table groups and any `extraTables` dependency in the matrix.
3. Populate raw `BMS*` fields, preserving code plus display companions where listed; treat query aliases and composed labels as derived output.
4. Record any missing template or title mismatch as unresolved, then request the actual template or a product decision.
5. Test only with synthetic or de-identified records; keep personal data out of examples and this repository.

## Observed routing summary

- [Secondary] A reports in the supplied set use shared groups such as `BMSBASE`, `BMSLAN`, `BMSP01`–`BMSP04`, `BMSPARK`, `BMSSTAIR`, and `BMSWORK` according to the individual report.[^specified-mapping]
- [Secondary] B11/B12/B13/B21 reports add operational groupings; observed extra dependencies include `BMSROAD`, `BMSCHK`, `BMSSCRP`, and `RPTPHOTO`.[^b-mapping]
- [Secondary] C11/C12/C21/C22 and D11/D13 route through the shared tables, while `C21_3` and `BMELVTR` are observed extensions. `BM_TEC` is a core table used by the F-coded technical report; G01/G02 reuse core groups.[^cd-mapping]

## Pitfalls

- [Unverified] `B14-2` has no observed template: do not invent its mapping.
- [Unverified] Observed B14-3/4/5 templates conflict with their directory labels; do not call those reports fully supported without a resolved template decision.[^b-mapping]
- [Secondary] A composed address, land number, certificate number, or aggregate is often a report calculation, not a new storage field.[^specified-mapping]
- [Secondary] `*_DESC`, `*_T`, and `MEMO_SEQ_NAME` may be display inputs and should not be discarded merely because a code exists.[^specified-mapping]

## Synthetic worked example

A synthetic `A12-2` land-number report can begin with one `BMSBASE` row and one or more `BMSLAN` rows. Preserve district, section, and the two land-number parts separately; the printed full land number is derived. This example does not establish a filing form or validate any real case.[^specified-mapping]

## Related Skills

- [Legacy permit data interchange](../../舊式案件交換格式/legacy-permit-data-interchange/SKILL.md)
- [Permit codebook snapshot governance](../../代碼字典快照治理/permit-codebook-snapshot-governance/SKILL.md)
- [Data fidelity model](../../保真資料儲存模型/permit-data-fidelity-model/SKILL.md)

## Data Currency

The newest cited mapping snapshot is dated 2026-07-16. Re-check upstream evidence and the target template before relying on any mapping.

## To Verify

- [ ] Obtain a correct B14-2 template; the pinned B-series mapping found no matching local template. Next: obtain the template from the target legacy deployment or its maintainer.
- [ ] Resolve whether B14-3 through B14-5 follow directory labels or the observed attachment/photo templates. Next: compare the target deployment's templates and obtain a product decision.
- [ ] Confirm the target deployment's report-template version and extension schema before mapping data. Next: inspect the deployed schema and template inventory.

[^specified-mapping]: Pinned implementation evidence, not legal authority: [specified report mapping](https://github.com/Archwiz-boss/BOOKTIRE/blob/06450a39315f453667db995641b4fdc4d0875ac1/CPAMI_%E6%8C%87%E5%AE%9A%E6%9B%B8%E8%A1%A8_%E5%AF%A6%E7%94%A8%E6%95%B8%E6%93%9A%E5%B0%8D%E6%87%89%E8%A1%A8.md).
[^b-mapping]: Pinned implementation evidence, not legal authority: [B-series mapping](https://github.com/Archwiz-boss/BOOKTIRE/blob/6130a8a667477d4db1c771d95e288932059ff963/CPAMI_B%E7%B3%BB%E5%88%97%E6%9B%B8%E8%A1%A8_%E6%95%B8%E6%93%9A%E5%B0%8D%E6%87%89%E8%A1%A8.md).
[^cd-mapping]: Pinned implementation evidence, not legal authority: [C/D-series mapping](https://github.com/Archwiz-boss/BOOKTIRE/blob/f3c8639ea9821bf9a32c1b7e6c6b8589092d58a3/CPAMI_CD%E7%B3%BB%E5%88%97%E6%9B%B8%E8%A1%A8_%E6%95%B8%E6%93%9A%E5%B0%8D%E6%87%89%E8%A1%A8.md).
