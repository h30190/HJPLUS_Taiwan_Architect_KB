---
type: Skill
name: permit-codebook-snapshot-governance
description: "This skill should be used when governing a legacy CPAMI permit-codebook snapshot so historical mappings are not represented as current official codes."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
sources:
  - id: booktire-data-format
    resource: https://github.com/Archwiz-boss/BOOKTIRE/blob/06450a39315f453667db995641b4fdc4d0875ac1/CPAMI_data_txt_%E6%AC%84%E4%BD%8D%E8%88%87%E4%BB%A3%E7%A2%BC%E5%B0%8D%E6%87%89%E8%A1%A8.md
    title: CPAMI data.txt field and code mapping (implementation evidence)
    last_modified: 2026-07-16
metadata:
  audience: architects
  region: taiwan
  class: C
  status: unverified
  data-currency: "2026-07-16"
---

# Permit Codebook Snapshot Governance

## Scope and certainty

This skill governs a historical codebook snapshot used for legacy permit-package interoperability. BOOKTIRE documents reverse-engineering evidence; it is neither an official current codebook nor proof that a code remains accepted by any authority.

The documented `bldcode.mdb` snapshot contains [Secondary snapshot] 22,383 rows across [Secondary snapshot] 43 observed `CODE_TYPE` values; `ALLRPT` contains [Secondary snapshot] 109 rows.[^booktire-data-format] These counts identify that snapshot only and must never be presented as current or official totals.

## Governance workflow

1. Assign every lookup result a source identifier, source revision/date, extraction method, and the exact snapshot version.
2. Label output from this snapshot `[Secondary snapshot]`; do not label it “official”, “current”, “verified”, or “latest”.
3. Keep the raw code, lookup dimensions, and display text together. A lookup can depend on a code type plus county/city or subcode fields, rather than one code alone.[^booktire-data-format]
4. Preserve unknown codes as received. Do not invent a replacement, silently map to a nearest value, or overwrite the incoming display text.
5. For a live filing, legal interpretation, or current code confirmation, obtain and record the relevant authority's current source separately; this skill cannot validate it.
6. Version any derived mapping and rerun comparison tests before changing the snapshot or its transformation rules.

## Worked synthetic example

Record a lookup as provenance, not as a current assertion:

```text
input: { code_type: "STC", code_seq: "U", sub_seq: "0010" }
snapshot: BOOKTIRE / 2026-07-16 / bldcode.mdb evidence
result: [Secondary snapshot] "地上 1 層"
decision: preserve code and display text; current applicability not evaluated
```

The example is fabricated for workflow illustration. Its displayed meaning is not an official current-code confirmation.

## Pitfalls

- A historic snapshot may omit types or values present in another system release; absence is not proof that a code is invalid.
- Do not merge municipal or later data into a snapshot and still call the result the original snapshot.
- Do not reduce multi-part keys: documented patterns use county/city context for administrative areas, land-use zones, structures, and remarks.[^booktire-data-format]
- Do not use a building-code search or an unrelated regulatory source as proof of this file format or snapshot contents.
- Do not publish codebook files, package content, or personal case values. Ship only reproducible instructions and synthetic fixtures.

## Data currency

The source revision used for this snapshot description is dated 2026-07-16. The date is evidence currency, not an assertion of the codebook's legal or operational currency. Re-verify against a responsible authority whenever present-day use matters.

## To Verify

- [ ] [Unverified] Whether a target legacy system uses the same codebook revision; compare its documented version or exported values against the identified snapshot.
- [ ] [Unverified] The recipient's current code source, update cadence, and municipality-specific additions; obtain the current source from the responsible authority.
- [ ] [Unverified] Any mapping not accompanied by the original snapshot version and lookup dimensions; recover those provenance fields before relying on the mapping.

## Privacy boundary

Codebook governance must not become a channel for retaining case data. Store only source/version metadata and fabricated regression fixtures in source control; keep authorized case data and any third-party database outside the repository.

## Related Skills

- [Legacy Permit data.txt Interchange](../../舊式案件交換格式/legacy-permit-data-interchange/SKILL.md)
- [Permit Report Data Mapping](../../書表與資料群組對照/permit-report-data-mapping/SKILL.md)
- [Permit Data Fidelity Model](../../保真資料儲存模型/permit-data-fidelity-model/SKILL.md)

[^booktire-data-format]: BOOKTIRE implementation evidence, revision dated 2026-07-16; it is not an official CPAMI publication.
