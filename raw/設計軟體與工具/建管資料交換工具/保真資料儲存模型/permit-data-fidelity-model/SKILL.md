---
type: Skill
name: permit-data-fidelity-model
description: "This skill should be used when designing storage, import/export, or database projections for legacy CPAMI permit-case data without losing its original string semantics."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
sources:
  - id: postgres-plan
    resource: https://github.com/Archwiz-boss/BOOKTIRE/blob/06450a39315f453667db995641b4fdc4d0875ac1/docs/POSTGRES_INTEGRATION_PLAN.md
    title: PostgreSQL integration preparation plan
    last_modified: 2026-07-16
metadata:
  audience: architects
  region: taiwan
  class: C
  status: unverified
  data-currency: "2026-07-16"
---

# Permit Data Fidelity Model

## Scope and trust boundary

[Secondary] This is a persistence-design guide distilled from a pinned implementation plan. It is neither a legal definition of a permit record nor a certified production database design.[^postgres-plan]

## Core invariants

- [Secondary] Preserve every business value as a string, including leading zeros, `""`, dates, and Y/N/blank states.[^postgres-plan]
- [Secondary] Treat the versioned JSONB payload as canonical. Relational tables or views are projections for query use, not the reconstruction source.[^postgres-plan]
- [Secondary] Keep 13 core tables under `tables` and retain non-legacy groups under `extraTables`; do not flatten extensions into the legacy export.[^postgres-plan]
- [Secondary] Use CP950 only at the import/export boundary. Database and exchange JSON operate in UTF-8.[^postgres-plan]
- [Secondary] Keep a schema version and reject or migrate incompatible documents deliberately. Do not assume `INDEX_KEY` is globally unique.[^postgres-plan]
- [Secondary] The normalized 13-table JSON-envelope export path applies only after detecting that the source has no passthrough, unknown, or signed package tables/entries. Route any such case to the byte-preserving [legacy permit data interchange](../../舊式案件交換格式/legacy-permit-data-interchange/SKILL.md) workflow, or reject it until lossless routing exists; never silently drop it.

## Workflow

1. Parse a legacy file through the format engine and create a versioned case envelope.
2. Validate that every core table and field is present with string values; preserve empty strings rather than substituting null, zero, boolean, or numeric types.
3. Store the envelope in canonical JSONB with `schemaVersion`, `formSet`, `tables`, and `extraTables`.
4. Build text-first relational views for reporting; offer numeric/date conversions only as separate projected columns.
5. Before normalized export, detect passthrough, unknown, and signed package tables/entries. Route them to the byte-preserving legacy-package workflow or reject the operation; only then validate CP950 encodability and serialize the fixed core tables in their required order.
6. Round-trip using synthetic fixtures and compare the exported bytes where the input is expected to be unchanged.

## Synthetic worked example

Store a fictional case with `INDEX_KEY: "00123"`, an empty numeric-looking field `""`, and a land-number component `"0007"` as strings in `payload.tables`. A query view may expose `NULLIF(value, '')` as a numeric helper, but it must not overwrite the payload. An added equipment row belongs under `payload.extraTables`, not a fabricated core-table column.[^postgres-plan]

## Pitfalls

- [Unverified] A 3NF-only canonical schema can erase field order, blank-versus-zero semantics, and compatibility fields; do not use it as the sole reconstruction source.
- [Secondary] Do not make `INDEX_KEY` a unique primary key; use a surrogate document identity and treat it as a business index.[^postgres-plan]
- [Secondary] Do not persist extensions by appending unknown groups to the legacy file; legacy export serializes core tables only.[^postgres-plan]
- [Secondary] CP950 failures belong at export validation. Silent replacement characters are data loss.[^postgres-plan]

## Privacy boundary

Payloads may contain identifiers, contact details, and other personal data. Keep fixtures fully synthetic, apply access control and encrypted backups in the receiving system, and do not copy payloads into documentation, issue discussions, or logs.[^postgres-plan]

## Related Skills

- [Permit report data mapping](../../書表與資料群組對照/permit-report-data-mapping/SKILL.md)
- [Legacy permit data interchange](../../舊式案件交換格式/legacy-permit-data-interchange/SKILL.md)
- [Permit codebook snapshot governance](../../代碼字典快照治理/permit-codebook-snapshot-governance/SKILL.md)

## Data Currency

The cited design snapshot is dated 2026-07-16. Revalidate before deployment.

## To Verify

- [ ] Confirm the active schema version and complete allowed `extraTables` list. Already checked: only the pinned planning snapshot. Next: inspect the active deployment schema.
- [ ] Define migration, authorization, retention, backup, and incident-response controls. Already checked: the cited plan identifies these as target-system responsibilities. Next: obtain the receiving system's security design.
- [ ] Run import/export and byte-level round-trip checks using synthetic fixtures on the deployed runtime. Already checked: the pinned plan names round-trip fidelity as its acceptance boundary. Next: execute the target runtime test suite.

[^postgres-plan]: Pinned implementation evidence, not legal authority: [PostgreSQL integration plan](https://github.com/Archwiz-boss/BOOKTIRE/blob/06450a39315f453667db995641b4fdc4d0875ac1/docs/POSTGRES_INTEGRATION_PLAN.md).
