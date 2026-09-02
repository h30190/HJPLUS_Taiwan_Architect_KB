---
type: Reference
title: "Observed CPAMI permit report-to-data-group matrix"
---

# Observed CPAMI Permit Report-to-Data-Group Matrix

## Evidence status

[Secondary] This matrix condenses pinned BOOKTIRE implementation evidence. It is not an official form catalogue and must not be used as legal or submission authority. A slash separates observed storage groups; `extraTables` are outside the core 13-table payload.

| Report family / identifiers | Observed data groups | Notes |
|---|---|---|
| A11, A12, A13, A21, A23, A31, A32 | `BMSBASE` plus report-specific `BMSLAN`, `BMSLANOWNER`, `BMSMEMO`, `BMSP01`–`BMSP04`, `BMSPARK`, `BMSSTAIR`, or `BMSWORK` | Full mapping varies by sub-report; computed labels are not extra source tables. |
| B11 | `BMSBASE/BMSLAN/BMSMEMO/BMSP01/BMSP03/BMSP04` | B11-1 also needs `extraTables.BMSROAD`; B11-3/4 are role-specific. |
| B12 | `BMSBASE` with report-specific `BMSLAN/BMSMEMO/BMSP01` | Link text may be derived from master data. |
| B13 | `BMSBASE/BMSLAN/BMSMEMO/BMSP01/BMSP03/BMSP04` | Includes current/original role data where the form requires it. |
| B21 | `BMSBASE/BMSLAN/BMSMEMO/BMSP01/BMSP03/BMSP04` or `BMSBASE/BMSSC` | B21-2 also uses `extraTables.BMSSCRP`. |
| G-coded B14-1 | `BMSBASE/BMSLAN/BMSP01/BMSP03/BMSP04` | Also `extraTables.BMSCHK` for inspection content. |
| G-coded B14-2 | [Unverified] unresolved | Template is missing; no field mapping may be inferred. |
| G-coded B14-3 | `BMSBASE/BMSP04` | Also `extraTables.BMSCHK`; observed template title/number conflicts with directory. |
| G-coded B14-4 / B14-5 | `BMSBASE` header only | Observed templates behave as photo/attachment forms and use `extraTables.RPTPHOTO`; directory/template mismatch remains unresolved. |
| C11 / C12 | shared core groups including `BMSBASE`, `BMSLAN`, `BMSMEMO`, `BMSP01`, role tables, and `BMSPARK` as applicable | C12 review text may be a derived link query. |
| C21 / C22 | shared core groups plus `BMSSTAIR` or role tables as applicable | C21-3 uses `extraTables.C21_3`; C22-5 uses `extraTables.BMELVTR`. |
| D11 / D13 | `BMSBASE/BMSLAN/BMSMEMO/BMSP01/BMSP03/BMSP04` as applicable | D11-1 additionally uses `extraTables.BMSROAD`; D13 link text is derived. |
| F `BM_TEC` | `BMSBASE/BMSLAN/BMSP01/BM_TEC` | `BM_TEC` is a core table, not an extension. |
| H G01 / G02 | `BMSBASE/BMSLAN/BMSP01`, plus `BMSLANOWNER` for G02 | `G01P01` and owner labels are query aliases, not new persisted tables. |

## Storage interpretation

[Secondary] The core payload has 13 fixed tables. `BMSROAD`, `BMSCHK`, `BMSSCRP`, `RPTPHOTO`, `C21_3`, and `BMELVTR` are observed as case extensions rather than fields to force into the legacy file. Keep raw rows and derive presentation text at the reporting layer.

## Source notes

- [Secondary] A-series observations: pinned specified-report mapping, 2026-07-16.
- [Secondary] B/G observations and B14 gaps: pinned B-series mapping, 2026-07-14.
- [Secondary] C/D/F/H observations: pinned C/D-series mapping, 2026-07-14.

## To Verify

- Verify report templates against the deployed legacy system before implementation.
- Do not treat the matrix as a replacement for an official current form set.
