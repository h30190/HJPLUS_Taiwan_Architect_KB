---
name: taichung-land-parcel-query
description: "This skill should be used when an architect receives just an address or lot number (地號) for a site in Taichung City, Taiwan, and needs to quickly understand the land's basic data — zoning, registered land area, land value, building numbers and permits, building overlay/footprint status, urban planning land-use regulations, geological hazard zones, slope-land restrictions, fire-break setback zones, active fault distances, sewer connection announcements, building-line exemption zones, military restricted-building zones, and whether the parcel (or a neighboring parcel) falls within a legally designated cultural heritage asset boundary — while also getting a head start on the official PDF certificates commonly needed as supporting documents for a later building permit application. Trigger scenarios: evaluating site feasibility right after receiving an address/lot number, checking land-use restrictions and pre-gathering supporting documents before a permit application, due diligence before a real-estate transaction, checking whether a development project near a historic site/monument may need to submit a cultural heritage impact statement, or converting a Taichung street address to its lot number. Taichung City only — does not work for other Taiwan counties/cities."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
metadata:
  audience: architects
  region: taiwan
  class: C
---

# Taichung Land Parcel Query

## Overview

> ⚠️ Taichung City only. All district codes, section (地段) code tables, and source websites this skill queries are Taichung City government systems. Inputting a district/section from another county or city will simply return no results.

This skill drives a browser-automation script that queries eleven different Taichung City government GIS/data websites in parallel for a given land parcel (地號), then compiles the results into a single PDF report. It replaces manually opening each government website, selecting district/section/lot, waiting for the map to load, and reading legend colors — a workflow that normally takes 10+ minutes per parcel.

**Core value**: given just an address or a lot number, an architect gets a full picture of a site's basic land data within minutes — and, as a side effect of the query, already has several of the official PDF certificates (geological hazard zone, slope-land, active fault) that are typically required as supporting documents when a building permit application is actually filed later.

Use this skill when the user wants to:
- Quickly understand a Taichung site right after receiving an address or lot number from a client (zoning, floor area ratio, building coverage ratio, and other constraints).
- Check for geological hazard zones, slope-land restrictions, or fire-break setback requirements before a building permit application, while getting a head start on gathering the corresponding supporting-document PDFs needed for the filing.
- Check whether a parcel is exempt from building-line designation requirements, or falls within a military restricted-building zone (e.g. near an airbase, with height limits).
- Check whether a parcel — or a nearby parcel — falls within a legally designated cultural heritage asset boundary (historic site, historic building, settlement cluster, archaeological site, cultural landscape), since even a parcel outside the boundary may still need to submit a cultural heritage impact statement if a designated monument is nearby.
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
3. Read the generated report at `~/Desktop/查詢結果/臺中市{district}{section}{lot}地號/`, which contains the main PDF report plus any supporting PDFs/screenshots that were actually found (building overlay, geological hazard, slope-land, active fault — the active fault report includes an auto-annotated map showing measured distance to the nearest fault lines; the cultural heritage query includes a screenshot of the official map with the parcel's boundary and any nearby monument highlighted).

## Requirements & Constraints

- Required assets: `scripts/taichung-land-parcel-query.py`
- Environment: Python 3.9+, `playwright` (with the Chromium browser installed), `Pillow`
- Taichung City only — the built-in district/section code table (29 districts, 1,625 sections) does not cover any other county or city.
- Pure browser automation against public government websites with no official API; a site redesign can break a query and require updating the corresponding selector in the script.
- A single-parcel query typically takes 1–3 minutes because some sources (geological hazard zone, active fault, cultural heritage screenshot) require polling for dynamically loaded results or a headless-browser interaction; the eleven sources are queried in parallel background subprocesses to keep total time down.
- The cultural heritage query also does a best-effort color scan of its screenshot for a nearby designated monument (古蹟) fill color; it only reliably detects that one category (others blend too closely with the basemap to detect automatically), so the report also always includes a reminder to visually check the screenshot against the map legend for other categories. If the screenshot itself cannot be captured, the report says so explicitly and states that the nearby-monument scan was **not** performed — it never silently drops that check.
- The urban-planning land-use regulation PDF is matched to the parcel's plan case by filename, since the city's Urban Development Bureau site offers no per-plan lookup. The report always states how the PDF was matched (`精確` / `唯一` / `模糊`) and warns when the match is not exact; if no candidate can be matched with confidence, the query reports a failure rather than downloading a plausible-looking but wrong set of regulations.
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
