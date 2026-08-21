---
type: Skill
name: taipei-permit-drawing-standards
description: "This skill should be used when preparing, reviewing, or indexing Taipei City building permit drawing sets (A101-A7), verifying the 44-item application document checklist, setting up N-prefix electronic file names for Taipei's paperless permit portal, or managing structural peer review stamping and guild copy-verification (對副本) SOPs."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
sources:
  - id: taipei-bmo-checklist
    resource: https://dba.gov.taipei/
    title: 臺北市建造執照申請及技術抽查簽證項目自主檢視表
    last_modified: 2024-06-16
  - id: firm-sop-taipei-permit
    resource: https://dba.gov.taipei/
    title: 臺北市建造執照圖說與協審對副本實務作業指引
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

Comprehensive guide for preparing Taipei City building permit drawing sets, verifying application document checklists, configuring file prefix naming for the Taipei City paperless online submission portal, and executing structural peer review stamping and copy verification (對副本) procedures.

---

## 1. Taipei City Permit Drawing Set Standard Index (A101–A7)

Permit drawings in Taipei City are formatted on A1 standard sheets. The drawing sheet sequence must strictly adhere to the standard indexing scheme:

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

---

## 2. Application Document Checklist (44 Core Items)

When submitting a building permit application in Taipei City, review the following 44 core document items:

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

Electronic PDF submissions to the Taipei City Building Management Office online portal must be prefixed with standardized system codes:

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

## Related Skills

- [design-change-filing](../../變更設計報備/design-change-filing/SKILL.md) — Taipei City building permit design change report filing SOP
- [construction-permit-application-documents](../construction-permit-application-documents/SKILL.md) — National and local building permit application documents
- [construction-permit-application-process](../../申辦流程/construction-permit-application-process/SKILL.md) — Building permit application workflow
