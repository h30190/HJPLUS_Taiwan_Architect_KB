---
name: taichung-land-parcel-query
description: "This skill should be used when an architect receives just an address or lot number (地號) for a site in Taichung City, Taiwan, and needs to quickly understand the land's basic data — zoning, registered land area, land value, building numbers and permits, building overlay/footprint status, urban planning land-use regulations, geological hazard zones, slope-land restrictions, fire-break setback zones, active fault distances, and sewer connection announcements — while also getting a head start on the official PDF certificates commonly needed as supporting documents for a later building permit application. Trigger scenarios: evaluating site feasibility right after receiving an address/lot number, checking land-use restrictions and pre-gathering supporting documents before a permit application, due diligence before a real-estate transaction, or converting a Taichung street address to its lot number. Taichung City only — does not work for other Taiwan counties/cities."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
metadata:
  audience: architects
  region: taiwan
---

# Taichung Land Parcel Query

## Overview

> ⚠️ Taichung City only. All district codes, section (地段) code tables, and source websites this skill queries are Taichung City government systems. Inputting a district/section from another county or city will simply return no results.

This skill drives a browser-automation script that queries nine different Taichung City government GIS/data websites in parallel for a given land parcel (地號), then compiles the results into a single PDF report. It replaces manually opening each government website, selecting district/section/lot, waiting for the map to load, and reading legend colors — a workflow that normally takes 10+ minutes per parcel.

**Core value**: given just an address or a lot number, an architect gets a full picture of a site's basic land data within minutes — and, as a side effect of the query, already has several of the official PDF certificates (geological hazard zone, slope-land, active fault) that are typically required as supporting documents when a building permit application is actually filed later.

Use this skill when the user wants to:
- Quickly understand a Taichung site right after receiving an address or lot number from a client (zoning, floor area ratio, building coverage ratio, and other constraints).
- Check for geological hazard zones, slope-land restrictions, or fire-break setback requirements before a building permit application, while getting a head start on gathering the corresponding supporting-document PDFs needed for the filing.
- Look up a parcel's building permit history, existing building footprint (套繪), or registered land area for due diligence.
- Convert a Taichung street address into its cadastral district/section/lot number, or the reverse.

## Execution Steps

1. Install dependencies: `pip install playwright pillow` then `playwright install chromium`.
2. Run the script with one of:
   - A street address (auto-converted to a lot number): `python3 scripts/taichung-land-parcel-query.py <district><road><number>號`
   - District + section + lot: `python3 scripts/taichung-land-parcel-query.py <district> <section> <lot>`
   - Multiple lots in the same section: `python3 scripts/taichung-land-parcel-query.py <district> <section> <lot1> <lot2> <lot3>`
   - A batch file (one query per line: `district section lot`): `python3 scripts/taichung-land-parcel-query.py queries.txt`
   - `python3 scripts/taichung-land-parcel-query.py list` to print all valid district/section codes.
3. Read the generated report at `~/Desktop/查詢結果/臺中市{district}{section}{lot}地號/`, which contains the main PDF report plus any supporting PDFs/screenshots that were actually found (building overlay, geological hazard, slope-land, active fault — the active fault report includes an auto-annotated map showing measured distance to the nearest fault lines).

## Requirements & Constraints

- Required assets: `scripts/taichung-land-parcel-query.py`
- Environment: Python 3.9+, `playwright` (with the Chromium browser installed), `Pillow`
- Taichung City only — the built-in district/section code table (29 districts, 1,625 sections) does not cover any other county or city.
- Pure browser automation against public government websites with no official API; a site redesign can break a query and require updating the corresponding selector in the script.
- A single-parcel query typically takes 1–3 minutes because some sources (geological hazard zone, active fault) require polling for dynamically loaded results; the nine sources are queried in parallel background subprocesses to keep total time down.
- Output paths are hardcoded to the local user's `~/Desktop/查詢結果/` folder — results stay on the machine running the script, nothing is uploaded anywhere.

## Examples

```bash
# Street address (auto-converts to lot number)
python3 scripts/taichung-land-parcel-query.py <district><road><number>號

# District + section + lot
python3 scripts/taichung-land-parcel-query.py <district> <section> <lot>

# Multiple lots in the same section
python3 scripts/taichung-land-parcel-query.py <district> <section> <lot1> <lot2> <lot3>

# Batch file (queries.txt, one "district section lot" per line)
python3 scripts/taichung-land-parcel-query.py queries.txt

# List all valid district/section codes
python3 scripts/taichung-land-parcel-query.py list
```

## Additional Resources
- For the human-readable overview, use case, and legal references, see [domain.md](../domain.md)
- For the implementation, see [scripts/taichung-land-parcel-query.py](scripts/taichung-land-parcel-query.py)
