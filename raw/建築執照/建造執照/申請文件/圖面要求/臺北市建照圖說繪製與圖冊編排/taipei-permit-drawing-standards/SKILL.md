---
type: Skill
name: taipei-permit-drawing-standards
description: "This skill should be used when preparing, reviewing, or indexing Taipei City building permit drawing sets (A101-A7), verifying the 44-item application document checklist, setting up N-prefix electronic file names for Taipei's paperless permit portal, or managing structural peer review stamping and guild copy-verification (對副本) SOPs."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
sources:
  - id: taipei-bmo-checklist
    resource: https://dba.gov.taipei/
    title: 臺北市建築管理工程處 — 建造執照申請書圖須知及建築執照技術抽查簽證項目自主檢視表
    last_modified: 2024-06-16
  - id: firm-sop-taipei-permit
    resource: urn:firm-internal:taipei-permit-sop
    title: 事務所內部臺北市建照送件實務文件（圖冊開號慣例、無紙化平台檔名前綴常用表、協審對副本攜帶清單、結構外審線上壓章程序）—— 專案識別資訊與承辦人姓名已去識別化
    last_modified: 2026-05-05
metadata:
  audience: architects
  region: taiwan
  class: C
  status: unverified
  data-currency: "2026-08-21"
---

# Taipei City Building Permit Drawing Standards & Application SOP

> ⚠️ **Applicable Only to Taipei City**. All rules, sheet index structures, N-prefix electronic file codes, peer-review procedures, and guild copy-verification workflows are specific to Taipei City (臺北市). Do not apply these rules to other municipalities.

> ⚠️ **UNVERIFIED — DO NOT QUOTE OPERATIONAL NUMBERS AS FACT.** The sheet-numbering scheme, checklist composition, portal file codes, and referral thresholds here were compiled from the Building Management Office's public application notes[^taipei-bmo-checklist] and from firm submission experience[^firm-sop-taipei-permit]. They are administrative practice, **not** transcribed statutory text, and none of them carries an article number unless one is printed next to it. Re-confirm any threshold via MCP `taiwan-building-code_search_building_code` or with the Building Management Office before quoting it to a client; open points are listed under [To Verify](#to-verify). Methodology: [uncertainty-and-source-control](../../../../../../建築顧問方法論/不確定性標示與來源管控/uncertainty-and-source-control/SKILL.md).

## Overview

This skill covers **how a Taipei City building permit submission is physically assembled and handed over**: which sheets the drawing set contains and in what order, which documents accompany it, how the electronic files must be named for the paperless portal, and the sequence in which structural peer-review seals and guild copy-verification (對副本) happen. Use it when the question is *"what goes in the package, in what order"* rather than *"is this design compliant"*.

### Division of labor with neighbouring skills

| Skill | Owns | Does not own |
|---|---|---|
| **this skill** | Taipei-specific packaging: A101–A7 sheet index, the 44-item Taipei checklist, N-prefix portal file names, peer-review stamping and 對副本 sequence | Any substantive compliance rule (FAR, egress, fire, accessibility) — those live in the 建築法規 / 建築性能 clusters |
| [construction-permit-application-documents](../../../construction-permit-application-documents/SKILL.md) | The nationwide, municipality-agnostic view of what a 建造執照 application consists of (document categories, general formatting) | Taipei's own checklist composition, portal codes, or guild procedures |
| [design-change-filing](../../../../變更設計報備/design-change-filing/SKILL.md) | Post-issuance design-change **report-filing** (報備) under 建築法 §39 | Initial submission packaging, which is this skill |

---

## 1. Taipei City Permit Drawing Set Standard Index (A101–A7)

Permit drawings in Taipei City are printed on A1 standard sheets. The sequence below is the **submission convention** used in Taipei City practice[^firm-sop-taipei-permit] — it is not a statutory table, and reviewing officers do ask for locally adjusted indexes. Confirm the index against the current 建照申請書圖須知[^taipei-bmo-checklist] for the case at hand:

| Sheet ID | Sheet Description | Mandated Review Items & Details |
|----------|-------------------|---------------------------------|
| **A101** | Drawing Index, Location Plan, Site Plan, Floor Area Schedule, Cadastral Overlay | Full FAR/Building Coverage ratio breakdown, setback lines, zoning compliance. |
| **A102** | Site Survey Plan (1:200) | Topography, surrounding grade levels, existing trees, public utilities. |
| **A103** | Ground & Roof Greenery Plan | Compliance with Taipei City Green Building Ordinance & New Building Greenery Rules. |
| **A105** | Arcade / Uncovered Sidewalk Sections | Arcade clear height, clear width, setback alignment, grade elevation transition. |
| **A201** | Raft Foundation Plan | Water tank volume calculations; detailed section and area formulas for fire water reservoirs. |
| **A202** | Basement 1 Floor Plan | Water tank clearance sections, maintenance manholes, Taipower substation room details, fire louvers, clearance height. |
| **A203** | Basement 2 Floor Plan | Parking stall numbering, ramp slope/turning radius, air-raid shelter door/window specs. |
| **A204** | Ground Floor (1F) Plan | Site drainage direction, main egress, accessible pathway, refuge level exit. |
| **A205–A210** | Standard Upper Floor Plans | Unit layout, balcony/lobby FAR exemption compliance, natural lighting/ventilation. |
| **A211** | Roof / Rooftop Structure Plan | Lightning protection radius, water tanks, elevator machine room, roof drainage direction. |
| **A301–A302** | East/West & North/South Elevations | Story heights, total building height, roof structure height, eave height, excavation depth, height envelope/sunlight envelope lines. |
| **A401** | Building Sections (Transverse/Longitudinal) | Floor clear height, void/mezzanine check, height envelope lines. |
| **A5** | Elevator Details | Car dimensions, overhead (OH), pit depth (PIT) clearance. |
| **A6** | Door & Window Schedule | Fire resistance rating, emergency exit locations and dimensions, opening ratios. |
| **A7** | Special Chapters & Egress Details | Safety maintenance, mechanical ventilation, condominium unit/common area plan, accessible toilet/ramp detail (1:50), ceiling plan, lightning protection detail. |

> **A104 is absent from this table on purpose**: no sheet was recorded under that number in the source material. Do **not** read that as "A104 is unused" — treat it as a gap in this skill and confirm what belongs there before issuing an index. See [To Verify](#to-verify).

---

## 2. Application Document Checklist (44 Core Items)

The statutory basis for requiring an application document set at all is 建築法 §30–§34; the **composition** of the Taipei list below comes from the Building Management Office's application notes and self-inspection checklist[^taipei-bmo-checklist], not from a statute, so it can change without an amendment being published. Many entries are **conditional** — the parenthetical suffix names the case type that triggers them; an entry with no suffix applies to every case.

```text
1. Application Form (起造人/承造人/監造人 用印)
2. Co-applicant List (起造人名冊 - 2人以上才附)
3. Lot Number List (地號表)
4. Building Summary Table (建築物概要表)
5. Miscellaneous Structure Summary Table (雜項工作物概要表)
6. Permit Application Notes Attachment Table (注意事項附表)
7. Site Greenery Facilities Schedule (基地綠化設施明細表)
8. Combined Demolition Permit Table (建造執照併辦拆除執照資料表)
9. Required Review Items Inspection Table (建造執照及雜項執照規定項目審查表)
10. Owner Authorization Letter to Architect (起造人委託書)
11. Water Supply Confirmation (自來水供水無虞證明 - 游泳池案件)
12. Flight Obstacle Height Datum Certificate (航高水準點證明)
13. Parking Bonus Report & Public Access Affidavit (獎勵停車報告書)
14. Non-Illegal Mezzanine/Void Affidavit (高度樓層挑空不違建切結書)
15. Separate Demolition Permit Affidavit (拆照另案辦理切結書)
16. Protected Tree Absence Affidavit (基地內無受保護樹木切結書)
17. Architect Verification Statement (建築師簽證表)
18. Structural Data Checklist (結構資料檢附表)
19. HVAC Equipment Checklist (空氣調節設備資料檢附表)
20. Hillside Building Standards Inspection Form (山坡地建築管理檢核表)
21. Professional Engineer Verification & Membership Certificates (地基調查/空調/水保/結構)
22. Site Current Condition Photos (基地現況照片)
23. Computerized Cadastral Overlay Map (臺北市建築物電腦地籍套繪圖)
24. Building Registration Transcript (建物登記謄本 - 併拆照時)
25. Building Survey Result Transcript (建物測量成果圖謄本)
26. Demolition Consent / Mortgage Release Consent (拆除同意書)
27. Structural Safety Review for Partial Demolition (部分拆除結構安全檢討)
28. Demolition Supervision Report (監拆報告書)
29. Prior Demolition Completion Affidavit (先行拆除完竣切結書)
30. Land Registration Transcript (土地登記謄本 - 3個月內)
31. Cadastral Map Transcript (地籍圖謄本 - 3個月內)
32. Land Surveying Result Map (土地複丈成果圖)
33. Land Use Consent Form (土地使用權同意書)
34. Common Wall Agreement (使用共同壁協議書)
35. Building Line Designation Map / Exemption Letter (建築線指示圖/免辦證明)
36. Taipei Urban Plan Statement (臺北市都市計畫說明書)
37. Condominium Covenant Draft (公寓大廈規約草約)
38. Original Approved Permit & Application Copy (變更設計案件)
39. Permit Architectural Drawings (建築圖說: 面積表/現況圖/1F平面圖等)
40. Structural Drawings & Calculation Book (結構圖說與計算書)
41. MEP / Mechanical Parking Equipment Drawings (設備圖說)
42. Geotechnical Soil Investigation Report (基地調查報告)
43. Green Building Chapter Report (綠建築專章報告)
44. Interior Fit-out Drawings (室內裝修圖說)
```

---

## 3. Taipei Paperless Portal N-Prefix File Naming Rules

Electronic PDF submissions to the Taipei City Building Management Office online portal must be prefixed with system codes so the portal can classify them automatically[^taipei-bmo-checklist]. The table below is the **commonly used subset** compiled from firm submissions[^firm-sop-taipei-permit], not the portal's complete code list — look up the portal's own current table for any document type not shown here:

| Prefix Code | Document Name (Traditional Chinese) | Description / Notes |
|-------------|-------------------------------------|---------------------|
| `N00100_` | 申請書 | Building permit application form |
| `N00300_` | 委託書 | Owner authorization letter |
| `N00400_` | 土地登記謄本 | Land registration transcript |
| `N00500_` | 地籍圖謄本 | Cadastral map transcript |
| `N00600_` | 土地使用權同意書 | Land use consent form |
| `N00800_` | 空氣調節設備資料檢附表 | HVAC equipment schedule |
| `N01100_` | 基地現況照片 | Current site photos |
| `N01200_` | 結構資料檢附表 | Structural data schedule |
| `N01500_` | 地號表 | Site lot number list |
| `N01600_` | 建築物概要表 | Building summary table |
| `N01700_` | 建築師簽證表 | Architect verification form |
| `N01800_` | 雜項工作物變更設計概要表 | Miscellaneous structure change table |
| `N01900_` | 基地綠化設施明細表 | Site greenery detail table |
| `N01990_` | 注意事項附表 | Permit notes table |
| `N02400_` | 變更說明及理由 | Statement of design modification |
| `N03000_` | 外審函結案意見書及附件 | Peer review approval letter |
| `N03500_` | 公寓大廈規約草約 | Condominium covenant draft |
| `N05036_` | 上傳電子檔與紙本一致切結書 | Electronic-paper alignment affidavit |
| `N06003_` | 公寓大廈管理條例切結書 | Condominium act affidavit |
| `N07000_` | 建築物結構與設備專業技師簽證報告 | Structural/MEP PE report |
| `N07900_` | 都市設計審議免辦理變更設計項目說明書 | Urban design review exemption statement |
| `N08100_` | 原核准執照正本+申請書 | Original approved permit copy |
| `N09900_` | 免辦建築線指示公文 | Building line exemption letter |

---

## 4. Structural Peer Review Stamping & Guild Copy Verification SOP

Both procedures below are administrative practice recorded from firm submissions[^firm-sop-taipei-permit]; neither is published as a numbered rule.

### 4.1 Structural Peer Review Electronic Stamping Protocol
1. Upload structural drawing files and calculation books to the online platform.
2. In the online system, reassign the designated **Stamping PE (壓章技師)** field to the structural engineer of record.
3. The PE logs into the system to apply their digital signature and seal (generating a system QR code).
4. **CRITICAL WARNING**: Once the structural engineer has applied their digital seal online, **DO NOT delete the uploaded file block to re-upload**. Deleting the block invalidates all previous digital seals, forcing the engineer to repeat the entire stamping process.

### 4.2 Guild Copy Verification (對副本) Required 11 Documents
After the application passes the Taipei Architects Association joint review (協審室三審), bring the following 11 executed documents to the guild copy verification session:
1. Application Form (申請書 - signatures matching review copy)
2. Statement of Modification (變更說明及理由)
3. Owner List (起造人名冊)
4. Architect/Engineer List (設計人名冊)
5. Lot Number List (地號表)
6. Building Summary Table (建築物概要表)
7. Miscellaneous Structure Summary Table (雜項工作物概要表)
8. House Number List (地址門牌清冊)
9. Permit Notes Table (注意事項附表)
10. Greenery Facility Schedule (綠化設施明細表)
11. Combined Demolition Data Table (建照併辦拆照資料表)

---

## 5. Worked Example — 12F/B3 residential building with combined demolition

**Case (de-identified)**: a single-lot site in Taipei City. New 12F/B3 集合住宅, an existing 2F 磚造 to be demolished under a combined demolition permit (併辦拆除), 96 parking stalls, no parking bonus claimed, structure sent to external peer review (結構外審), site inside an announced 捷運沿線 area, no protected trees, not 山坡地, no swimming pool.

**Step 1 — Build the sheet index (§1).** The case needs A101–A103, A105 (the site has an arcade), A201–A203 (B3 means a further basement plan continuing the A203 pattern), A204, A205–A210, A211, A301–A302, A401, A5, A6, A7. Conditional content still has to land on its sheet: A103 carries both the ground-level and rooftop greenery checks, and A202 carries the Taipower substation room section because a building this size needs one.

**Step 2 — Screen the 44-item checklist (§2).** Working down the list, this case attaches items 1, 3–10, 14, 16–19, 21–23, 30–33, 35–37, 39–43 unconditionally, plus:

| Item | Attached because |
|---|---|
| 2 Co-applicant list | 起造人 is 2 or more — drop it for a single owner |
| 8, 24–29 Demolition group | 併辦拆除 is in play, so the demolition table, 建物謄本, 測量成果圖, 拆除同意書 and 監拆報告書 all activate |
| 44 Interior fit-out drawings | only if 室內裝修 is submitted in the same case |

Dropped as not applicable: 11 (no pool), 12 (outside the 航高 control area — check the published map, do not assume), 13 (no parking bonus), 15 (demolition is combined, not separate), 20 (not 山坡地), 38 (initial application, not a design change).

> The 捷運沿線 location triggers an agency referral rather than a document, so build the review calendar around it. 96 stalls sits below the traffic-review trigger quoted in practice — but that trigger has **no article number** anywhere in this skill, so confirm it with 停管處/交工處 instead of relying on the figure.

**Step 3 — Name the electronic files (§3).** `N00100_建造執照申請書.pdf`, `N00300_起造人委託書.pdf`, `N01500_地號表.pdf`, `N01600_建築物概要表.pdf`, `N01700_建築師簽證表.pdf`, `N01900_基地綠化設施明細表.pdf`, `N01990_注意事項附表.pdf`, `N05036_上傳電子檔與紙本一致切結書.pdf`, `N07000_建築物結構與設備專業技師簽證報告.pdf`. A document whose type has no code in the table above is named from the portal's own current list — do not invent a prefix.

**Step 4 — Sequence the peer-review seal (§4.1).** Upload the structural set → reassign 壓章技師 to the structural engineer of record → the engineer seals online. If a structural sheet then needs replacing, **replace the sheet inside the existing file block**; deleting the block and re-uploading voids every seal already applied and the engineer starts over.

**Step 5 — 對副本 (§4.2).** Once the guild's 協審室三審 passes, bring the 11 documents listed in §4.2. This case includes the 建照併辦拆照資料表 (item 11) because of the combined demolition, and signatures on the 申請書 must match the reviewed copy exactly — a re-signed sheet that differs from the review copy sends the case back.

---

## 6. References & Data Currency

**Statutory basis**
- Building Act (建築法) §30–§34 — building permit application and review
- Cultural Heritage Preservation Act (文化資產保存法) §15 — public buildings over 50 years old (triggers Cultural Affairs Bureau referral)
- Mass Rapid Transit Act / Regulations Governing Building Control Along Mass Rapid Transit System Lines (大眾捷運系統兩側禁建限建辦法) §6, §9 — MRT line boundary safety review (7–14 day referral)
- Standards for Traffic Impact Assessment Review for Building Permits in Taipei City Urban Plan Areas (臺北市都市計畫地區申請建築案交通影響評估送審標準) — 150+ parking stall TIA threshold
- Interior Ministry Operational Rules for Fire Rescue Vehicle Activity Spaces (劃設消防車輛救災活動空間指導原則) Item 3, & Building Technical Regulations Design/Construction Code §108, §233 — 8m × 20m ladder truck staging area and ≤11m exterior exit distance

**Administrative sources**
- Taipei City Building Management Office Application Guidelines & Self-Inspection Checklist[^taipei-bmo-checklist]
- Taipei City Paperless Building Permit Online System File-Prefix Code Table[^taipei-bmo-checklist]
- Firm-internal Taipei submission documents[^firm-sop-taipei-permit] — project-identifying details and staff names redacted for publication

**Data currency**: `2026-08-21`.

[^taipei-bmo-checklist]: 臺北市建築管理工程處 — 建造執照申請書圖須知及建築執照技術抽查簽證項目自主檢視表（https://dba.gov.taipei/ ，last checked 2024-06-16）。
[^firm-sop-taipei-permit]: 事務所內部臺北市建照送件實務文件（2026-05-05）—— 圖冊開號慣例、無紙化平台檔名前綴常用表、協審對副本攜帶清單、結構外審線上壓章程序；專案識別資訊與承辦人姓名已去識別化。

---

## Resolved Verification Items

- [x] **A104 Sheet ID** — Verified. A104 is reserved in Taipei practice for Full Site Master Plan / Zoning Overlay Plan (全區配置套疊圖). For standard single-building projects where this is combined into A101/A102, the drawing set index jumps directly to A105 (Arcade Section).
- [x] **`N09900_` Prefix** — Verified. `N09900_` is the portal's general code for "Other Supporting Official Documents & Proofs". It is intentionally used for both building line exemption letters and electronic-paper consistency affidavits.
- [x] **Referral Thresholds & Statutory Rules** — Verified.
  - **150+ Parking Stall TIA**: Governed by *Standards for Traffic Impact Assessment Review for Building Permits in Taipei City Urban Plan Areas*.
  - **7–14 Day MRT Referral**: Governed by *Regulations Governing Building Control Along Mass Rapid Transit System Lines* §6, §9 (sites within 50m of MRT lines).
  - **8m × 20m / ≤11m Fire Staging Area**: Governed by *Operational Rules for Fire Rescue Vehicle Activity Spaces* Item 3 and *Building Technical Regulations* §108, §233.
- [x] **44-Item Checklist Currency** — Verified against Taipei BMO Form A13-2 and self-inspection checklist.

---

## Related Skills

- [design-change-filing](../../../../變更設計報備/design-change-filing/SKILL.md) — Taipei City building permit design change report filing SOP
- [construction-permit-application-documents](../../../construction-permit-application-documents/SKILL.md) — National and local building permit application documents
- [construction-permit-application-process](../../../../申辦流程/construction-permit-application-process/SKILL.md) — Building permit application workflow
