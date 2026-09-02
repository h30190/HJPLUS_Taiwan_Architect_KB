---
type: Skill
name: legacy-permit-data-interchange
description: "This skill should be used when preserving or producing a legacy CPAMI permit-package data.txt interchange file without treating reverse-engineering evidence as official procedure."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
sources:
  - id: booktire-data-format
    resource: https://github.com/Archwiz-boss/BOOKTIRE/blob/06450a39315f453667db995641b4fdc4d0875ac1/CPAMI_data_txt_%E6%AC%84%E4%BD%8D%E8%88%87%E4%BB%A3%E7%A2%BC%E5%B0%8D%E6%87%89%E8%A1%A8.md
    title: CPAMI data.txt field and code mapping (implementation evidence)
    last_modified: 2026-07-16
  - id: booktire-extension-format
    resource: https://github.com/Archwiz-boss/BOOKTIRE/blob/fcd075e7def6b5a82351dc6ec679d580a75ec8b4/CPAMI_%E4%BA%8C%E7%B6%AD%E5%B0%81%E5%8C%85%E6%93%B4%E5%85%85%E8%A1%A8_%E6%95%B8%E6%93%9A%E5%B0%8D%E6%87%89%E8%A1%A8.md
    title: CPAMI two-dimensional package extension-table mapping (implementation evidence)
    last_modified: 2026-08-10
metadata:
  audience: architects
  region: taiwan
  class: C
  status: unverified
  data-currency: "2026-08-10"
---

# Legacy Permit `data.txt` Interchange

## Scope and certainty

This is a non-authoritative interoperability guide derived from BOOKTIRE reverse-engineering and implementation documentation. It does not establish an official CPAMI specification, a legal submission procedure, or acceptance criteria. Reconfirm behavior with the receiving system and responsible authority before operational use.

The sources report a text export made of table blocks: `@TableName <name>`, `@RecordBegin`, zero or more `@d <field> "<value>"`, and `@RecordEnd`.[^booktire-data-format] Treat this grammar as [Secondary], not a substitute for an authority-issued interface contract.

## Preservation rules

- [Secondary] Encode output in strict Big5/CP950 with no BOM and CRLF line endings. Reject characters that cannot be encoded; never silently replace them with `?`.[^booktire-data-format]
- [Secondary] Preserve `""` as an empty value and `"0"` as numeric zero; they are not interchangeable. Emit numbers as text without thousands separators or units.[^booktire-data-format]
- [Secondary] Preserve date values in the encountered ROC `yyyMMdd` text form (for example, `1150713`), rather than converting them to ISO dates.[^booktire-data-format]
- [Secondary] The documented core tables include `BMSBASE`, `BM_TEC`, `BMSLAN`, `BMSLANOWNER`, `BMSMEMO`, `BMSP01`–`BMSP04`, `BMSPARK`, `BMSSC`, `BMSSTAIR`, and `BMSWORK`.[^booktire-data-format]
- [Secondary] Do not assume that list is a fixed package schema: the exporter is documented as iterating a table-name collection, and package extensions can add tables.[^booktire-extension-format]
- [Secondary] Pass through unknown tables in their original order and content. Never edit signed or otherwise unknown entries in place; retain them byte-for-byte where the implementation can do so.[^booktire-extension-format]

Use that passthrough rule only on the **direct package-preservation path**: it retains and re-emits every encountered passthrough table or entry. A normalized 13-table JSON-envelope export is a separate path; it must not consume a package that contains passthrough or signed tables unless those tables are safely routed outside that export or preserved by an explicitly tested mechanism.

## Execution workflow

1. Work from an authorized copy of the package and record its source/version; minimize access to personal data.
2. Parse each block without normalizing table names, field names, field order, dates, empty values, or line endings.
3. Map only tables and fields with a documented, tested transformation. Keep unmodeled tables as a passthrough payload.
4. For known rows, retain the common `INDEX_KEY`; retain positive row sequences where present and do not infer missing business meaning.
5. Serialize with strict CP950 and CRLF, then re-parse the result and compare block order, table collection, field names, and all untouched values.
6. Run an import/read test only in an approved test environment. A successful parse is not proof of authority acceptance.

## Worked synthetic example

Use synthetic values only:

```text
@TableName BMSBASE
@RecordBegin
@d INDEX_KEY "1150101000000"
@d BUILDING_NAME "測試案件"
@d BUILDING_AREA ""
@d FLOOR_COUNT "0"
@RecordEnd
```

This illustrates the block grammar and the distinction between `BUILDING_AREA` being empty and `FLOOR_COUNT` being zero. It is not a complete importable case and does not assert that these fields are sufficient for any jurisdiction.

## Pitfalls

- Do not serialize as CSV, JSON, UTF-8, LF-only text, or a guessed escaping convention.
- Do not collapse multiple floor/use rows merely because a floor code repeats.
- Do not turn `_OLD`, `_TEAR`, display text, or auxiliary code fields into defaults; their meaning can be case-specific.
- Do not rename irregular field names or unify different field names just because they appear semantically similar.
- Do not expose package contents, identifiers, addresses, contact details, drawings, or signatures in logs, examples, issue reports, or this repository.

## Data currency

The latest technical evidence used here is dated 2026-08-10. It describes a particular implementation and observed package behavior, not a current official format. Re-check when the target system version, municipality, or package generator changes.

## To Verify

- [ ] [Unverified] Receiver-specific mandatory tables, fields, ordering tolerance, and escaping behavior; compare against an authorized receiver test package and the receiver's current interface documentation.
- [ ] [Unverified] Whether a particular receiver accepts generated AutoNumber-like identifiers or assigns them during import; verify through an approved test-environment import.
- [ ] [Unverified] The allowed workflow for any signed, sealed, or otherwise protected package component; obtain written confirmation from the responsible authority or system owner.

## Privacy boundary

Use only minimized, authorized case data. Store test fixtures with fabricated names, identifiers, addresses, dates, and drawings. Do not commit package exports, `data.txt`, codebooks, certificates, or third-party binaries.

## Related Skills

- [Permit Codebook Snapshot Governance](../../代碼字典快照治理/permit-codebook-snapshot-governance/SKILL.md)
- [Permit Report Data Mapping](../../書表與資料群組對照/permit-report-data-mapping/SKILL.md)
- [Permit Data Fidelity Model](../../保真資料儲存模型/permit-data-fidelity-model/SKILL.md)

[^booktire-data-format]: BOOKTIRE implementation evidence, revision dated 2026-07-16; it is not an official CPAMI publication.
[^booktire-extension-format]: BOOKTIRE implementation evidence, revision dated 2026-08-10; it is not an official CPAMI publication.
