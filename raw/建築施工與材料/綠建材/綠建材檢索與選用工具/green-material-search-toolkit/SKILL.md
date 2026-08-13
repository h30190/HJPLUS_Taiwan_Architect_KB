---
type: Skill
name: green-material-search-toolkit
description: "This skill should be used when an architect or consultant needs to search Taiwan's TABC (財團法人臺灣建築中心) green building material certification database, assemble a set of qualified materials for a project (a \"Set\"), ask the AI to draft a material-selection advisory document for that Set, or export/import a Set as a project file. It does not write to any BIM software model."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
metadata:
  audience: architects
  region: taiwan
  class: C
  status: draft
  data-currency: "2026-08-07"
---

# Green Material Search & Advisory Toolkit

## Overview

A self-contained local web tool + Python backend for browsing Taiwan's TABC green-material certification database, grouping selected materials into a named "Set", and getting the AI to draft a material-selection advisory document (建材選用說明書) for that Set — CNS testing basis, qualified items, and suggested application location per material. Sets can be saved, edited, and exported/imported as project files so they carry over between projects.

This skill is intentionally scoped to search + Set management + advisory Q&A only. It does **not** perform any BIM-software model write (no Revit, Archicad, or other native-format injection). If a future skill needs to push a Set's materials into a specific BIM tool's model, that belongs in a separate, BIM-tool-specific skill — do not extend this one to do that.

## Data Reality — Read Before Answering Questions About a Material

`assets/tabc_master_database.json` has two tiers of trustworthiness per record:

- **Real, scraped from the TABC list page**: `licno`, `title`, `company`, `period` (validity dates, ROC calendar), `category`, `subCategory`, `img`.
- **Inferred from a keyword-rule template, not scraped per-record from TABC's detail page**: `cnsSpec`, `testItems`, `qualifiedItems`, `productSpecFull`, `specList`, `specs`, `keywords`. These are plausible placeholder values grouped by `subCategory`/title keywords, not authoritative lab data for that specific product.

Always disclose this distinction when the advisory document or a direct answer states a specific CNS standard or test value. Never present the inferred fields as officially verified numbers — tell the user to confirm against the TABC record's `detail_url` (`CaseDataInfo.aspx`) or the manufacturer's certificate before using the figures in a formal submission.

## Trigger Confirmation Rule

Mentioning "綠建材" (or a related term — 綠建材標章, TABC 綠建材, 健康/高性能/再生/生態綠建材, etc.) in conversation is enough to make this skill *relevant*, but it is **not** enough to launch anything on its own. Before running `python scripts/local_server.py` (which opens a local port and a browser tab), ask the user whether they want to open the search tool. Only skip the confirmation when the user's message is already an explicit request to open it (e.g. "open the green material search tool", "打開綠建材檢索工具"). This mirrors the equivalent policy in the origin project's `domain/green-material-keyword-search.md` (`.claude/skills/GMweb/SKILL.md` there) — a passing mention should never silently trigger a running process.

## Setup — Obtaining the Data Assets (First Run Only)

`assets/tabc_master_database.json`, `assets/green-material-toolkit.html`, and `assets/exported_material_sets.json` are **not included in this skill's files**. They contain TABC's (財團法人臺灣建築中心) certification data and/or a specific user's project output, neither of which belongs under this repository's CC BY-SA 4.0 license — see `.gitignore` in this directory. The interface itself (`assets/green-material-toolkit.template.html`) *is* shipped with the skill, empty of TABC data (`const tabcDatabase = [];`), so this step is self-contained — no manual download from anywhere.

Before first use:

1. Run `python scripts/update_tabc_database.py` once with no existing `assets/tabc_master_database.json`; the script bootstraps a fresh database from a live TABC crawl (starts from an empty list, everything found is added — takes longer than a normal incremental update since nothing is cached yet), then fills that data into `assets/green-material-toolkit.template.html` and writes the result to `assets/green-material-toolkit.html`. Both outputs are gitignored, regenerated locally on every run.
2. **`assets/exported_material_sets.json`** — not needed up front; it's created automatically the first time a Set is saved.

After this, normal use (steps 1–4 below) works entirely offline except for step 4's optional refresh crawl.

## Execution Steps

### 1. Open the tool (only after the user confirms — see Trigger Confirmation Rule above)

```bash
python scripts/local_server.py
```

Starts a local server, bound to `127.0.0.1` only, at `http://localhost:8888` serving `assets/green-material-toolkit.html`, and opens it in the browser. A plain `file://` open of the HTML also works for browsing/searching, but the "Set" save/export/import buttons need this server running (they call `POST /api/save-sets` / `GET /api/get-sets`).

If port 8888 is already in use by another process (e.g. a different local tool on the same machine), tell the user to free it or check what's using it before starting a second server.

Sets are the user's project output, not skill content, so they are written outside this repository by default — to `~/.green-material-toolkit/exported_material_sets.json`. Set the `GREEN_MATERIAL_OUTPUT_DIR` environment variable before running either `local_server.py` or `generate_material_advisory.py` to point both at a specific project folder instead (both must use the same value to see the same Set data).

### 2. Search and build a Set

The page lets the user filter by keyword/category, select materials, and save a named "Set" (a group of `licno`s with an optional purpose/use note). This is entirely client-side + the local API — no AI involvement needed for this step.

### 3. Ask the AI to draft a material-selection advisory

Once the user has a Set and clicks "🤖 回傳至 AGENT" (or asks in chat, e.g. "請為材料 Set 【某某 Set】撰寫建材選用說明書"), run:

```bash
python -c "
import sys
sys.path.insert(0, 'scripts')
import generate_material_advisory as g
advisory = g.generate_material_advisory('<set_name>', ['<licno1>', '<licno2>', ...], '<original request text>')
g.write_back_to_set_manager('<set_name>', advisory)
"
```

Run this from the `green-material-search-toolkit/` directory (or adjust the `scripts` path). This:

- Matches each `licno` against `assets/tabc_master_database.json` (exact match first, then suffix-tolerant fallback for `(續)`/`(增)`/`(變)` certificates — see `_normalize_licno` in the script). Never truncate a matched licno's suffix in what you report to the user.
- Writes `Material_Advisory_Report.md` under the Set output directory (`$GREEN_MATERIAL_OUTPUT_DIR`, default `~/.green-material-toolkit/`) — a full Markdown advisory document (material list with category, CNS basis, qualified items, test data, and a suggested application location per material — general building-assembly language, e.g. "牆面或天花板塗裝面材", not any specific software's category system).
- Updates the Set's entry in the same directory's `exported_material_sets.json` (`purpose`, `plannedActions` — now holding suggested-usage lines, not any software-specific execution steps — and `planStatus: "已請 Agent 撰寫說明書"`).

Then report a concise summary to the user (do not paste the full report):
- Set name and matched material count (flag if fewer matched than requested — a licno wasn't found even after suffix-tolerant matching).
- For each matched material: licno (full, with suffix if any), title, category/subCategory, suggested application location.
- Remind the user that `cnsSpec`/`testItems`/`qualifiedItems` are inferred values per the Data Reality note above.
- Point them at the generated `Material_Advisory_Report.md` (in the Set output directory) for the full document.

### 4. Refresh the source database (optional, occasional)

```bash
python scripts/update_tabc_database.py --dry-run   # preview diff, no writes
python scripts/update_tabc_database.py              # actually merge + write
```

Crawls the live TABC site (`https://tabcmgr.hopto.org/mgr/SearchCaseAction.aspx`, GBMTYPE 1–4) and merges new/changed records into `assets/tabc_master_database.json`, then re-generates `assets/green-material-toolkit.html` by filling the same data into `assets/green-material-toolkit.template.html`'s embedded offline cache (`const tabcDatabase = [...]`) — the template itself is never modified. Records not seen in a given crawl are **kept, not deleted** — a partial network failure must never wipe real data; they're only listed as "not seen this run" in the diff output. Always run `--dry-run` first and show the user the diff (added/updated/not-seen counts) before running the real update, since it rewrites two local data files (gitignored, not committed to this repo — see Setup section above).

## Requirements & Constraints

- Shipped with this skill: `scripts/local_server.py`, `scripts/update_tabc_database.py`, `scripts/generate_material_advisory.py`, `assets/green-material-toolkit.template.html` (the UI, empty of TABC data).
- Generated locally on first use (not shipped — see Setup section above): `assets/tabc_master_database.json`, `assets/green-material-toolkit.html`. `assets/exported_material_sets.json` (or the `GREEN_MATERIAL_OUTPUT_DIR` equivalent) is generated automatically.
- Environment: Python 3.8+ (standard library only — no `pip install` needed). Any modern browser for the page itself.
- Network: only `scripts/update_tabc_database.py` needs outbound internet access (to `tabcmgr.hopto.org`); everything else is fully local/offline.

## Worked Example

User has already built a Set named "室內牆" containing `GBM0104204` (a coating) and `GBM0104194` (a composite wood floor), and clicks "🤖 回傳至 AGENT".

1. Run the advisory generator with those two licnos and the Set name.
2. It matches both against `tabc_master_database.json`: `GBM0104204` → 健康綠建材（塗料類）, CNS16082/CNS15200 basis; `GBM0104194` → 健康綠建材（地板類）, CNS1349/CNS16083 basis.
3. `Material_Advisory_Report.md` is written (under `~/.green-material-toolkit/`, or `$GREEN_MATERIAL_OUTPUT_DIR` if set) with one section per material, each showing category, validity period, CNS basis, qualified items, test data, and suggested application location (塗料 → "牆面或天花板塗裝面材"; 地板 → "地坪面材...").
4. Report back: "已為 Set【室內牆】的 2 項建材產生選用說明書：GBM0104204（塗料類，建議用於牆面塗裝）、GBM0104194（地板類，建議用於地坪）。試驗數據為模板推論值，正式送審前請核對 TABC 官方文件。完整說明書見 ~/.green-material-toolkit/Material_Advisory_Report.md。"

## Common Pitfalls

### Pitfall: presenting inferred test data as officially verified
- **Severity**: 🔴 rejection risk (if copied verbatim into a formal submission)
- **When it bites**: user asks "what's the TVOC rate for this material" and the answer comes straight from `testItems` without the Data Reality caveat
- **Wrong**: stating the CNS/test figures as if TABC verified that exact number for that exact product
- **Right**: state the figures, then explicitly flag they're template-inferred and should be confirmed against the TABC detail page or manufacturer's certificate before formal use

### Pitfall: dropping a licno silently when it doesn't match
- **Severity**: 🟡 rework risk
- **When it bites**: a Set references a licno that isn't in the local database (expired, renumbered, or the local cache is stale)
- **Wrong**: silently excluding it from the advisory document
- **Right**: list it under "未能比對之核定字號" in the report and tell the user — it may mean the local database needs `update_tabc_database.py`, or the certificate genuinely expired

### Pitfall: treating this skill as a BIM-injection tool
- **Severity**: 🟡 rework risk
- **When it bites**: user asks to "把這個 Set 寫入我的 XX 軟體模型"
- **Wrong**: trying to extend this skill's scripts to write BIM-software-native data
- **Right**: tell the user this skill only produces the advisory document; a BIM-model write is a separate, tool-specific capability outside this skill's scope

## Data Currency

- Source: TABC 綠建材採購指南檢索系統, `https://tabcmgr.hopto.org/mgr/SearchCaseAction.aspx`
- Verified: 2026-08-07, via `scripts/update_tabc_database.py --dry-run` live crawl against the source site
- Volatility: MEDIUM — TABC adds/renews certificates on an ongoing basis; re-run `update_tabc_database.py` periodically, especially before relying on a Set's validity-period data for a live submission

## To Verify

- [ ] `cnsSpec`/`testItems`/`qualifiedItems` are template-inferred, not scraped per-product from TABC's detail page (`CaseDataInfo.aspx`). A future improvement could scrape the real detail page for authoritative values — not attempted here; flagged as a known limitation inherited from the origin project.

## Additional Resources

- For the TABC four-category certification system (健康/高性能/再生/生態) and common pitfalls, see [domain.md](../domain.md)
- Data source: TABC 綠建材採購指南檢索系統 (`https://tabcmgr.hopto.org/mgr/SearchCaseAction.aspx`), mirrored locally to `assets/tabc_master_database.json` — see Setup section above (not committed to this repo)
