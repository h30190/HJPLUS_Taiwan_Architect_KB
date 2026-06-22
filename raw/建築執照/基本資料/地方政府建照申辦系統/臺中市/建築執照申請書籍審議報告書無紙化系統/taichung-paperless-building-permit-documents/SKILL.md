---
name: taichung-paperless-building-permit-documents
description: "This skill should be used when working with Taichung City's web-based paperless building permit booklet and review report system, including login identity, personnel authorization, application case management, online case import, and legacy standalone case import."
user-invocable: true
---

# Taichung Paperless Building Permit Documents

## Overview

This skill covers the Taichung City web-based paperless system for building permit application booklets and review reports. In local practice this system is often called the "2D system" (二維系統). Use it when preparing Taichung permit workflows, explaining login and authorization rules, managing application cases, importing cases, or distinguishing Taichung's local web system from the 2016 Building Permit Application Form System used by many other Taiwan jurisdictions.

---

## Section 1: Official Entry Points

| Resource | URL |
|----------|-----|
| Login page | https://mcgbm.taichung.gov.tw/arch/loginpage |
| E-Government account registration | https://www.cp.gov.tw/portal/cpinit/RegisterM.aspx?ReturnUrl=https%3a%2f%2fmcgbm.taichung.gov.tw%2fegov%2farch%2floginok |
| Full operation training manual | https://mcgbm.taichung.gov.tw/arch/pdf/useword_I80.pdf |
| Web case import manual | https://mcgbm.taichung.gov.tw/arch/pdf/case_import_web.pdf |
| Standalone case import manual | https://mcgbm.taichung.gov.tw/arch/pdf/case_import_single.pdf |

Do not attempt to parse the PDF manuals unless explicitly requested. They are primarily linked for direct user viewing or download.

---

## Section 2: System Context

| Item | Current Scope |
|------|---------------|
| Jurisdiction | Taichung City |
| Common local name | 2D system / 二維系統 |
| Platform type | Web-based paperless local government system |
| Primary document group | Application booklets, written application documents, and review reports |
| Common user groups | Architects, architecture office staff, contractors, contractor staff, permit runners |
| Key distinction | Do not assume the 2016 Building Permit Application Form System workflow applies to Taichung City |

---

## Section 3: Login Identity Rules

| User identity | Login method | Rule |
|---------------|--------------|------|
| Practicing architect | Citizen digital certificate | The architect must log in with a natural person certificate; organization certificates are not accepted for this identity. |
| Contractor company | Business certificate | Contractor-side access uses the business certificate. |
| Architecture office staff | E-Government account | Staff must first register an E-Government account, then receive authorization under the architect account. |
| Contractor staff | E-Government account | Staff must first register an E-Government account, then receive authorization under the contractor account. |
| Permit runner or external collaborator | E-Government account | The same person may be authorized by multiple offices or contractors and switch the active organization after login. |

---

## Section 4: Personnel Authorization Model

First-time staff login status is unauthorized. The architect account or contractor account must open the personnel authorization management page and authorize the staff member.

Authorization requires:

| Field | Notes |
|-------|-------|
| Account | Staff E-Government account |
| Name | Staff name |

Permission behavior:

| Permission type | Capability |
|-----------------|------------|
| Management permission enabled | Can authorize other users and manage all cases under the organization. |
| Management permission disabled | Can only see cases specifically authorized to that user. |
| Multiple organization authorization | User can switch the active architecture office or contractor on the home page after login. |

---

## Section 5: Functional Modules

| Module | Scope | Repository folder |
|--------|-------|-------------------|
| E-Government account registration | Staff account preparation before authorization | `功能模組/申請E政府帳號流程/` |
| Personnel authorization management | Staff authorization and management permission control | `功能模組/人員授權管理/` |
| Application case management | Main daily workflow for building professionals | `功能模組/申請案件管理/` |
| Import application cases | Web case import and standalone V8/V88 case import | `功能模組/匯入申請案件/` |
| Rare character code upload | Placeholder for rare character code handling | `功能模組/罕見字代碼上傳/` |
| System code update report | Placeholder for code update reporting | `功能模組/系統代碼更新回報/` |

---

## Section 6: Application Case Management

Application case management is the most commonly used function for building professionals. After login, users authorized by multiple offices or contractors should switch to the intended organization on the home page. Then use the hamburger menu at the upper left to open application case management.

Current case-management substructure:

| Subfunction | Scope |
|-------------|-------|
| New case | Start a new application case |
| Construction permit | Web-based construction permit cases |
| Occupancy permit | Web-based occupancy permit cases |
| Demolition permit | Web-based demolition permit cases |
| Design change | Web-based design change cases |
| Preliminary review | Web-based preliminary review applications |
| Interior renovation | Web-based interior renovation applications |

---

## Section 7: Case Import Rules

### Web Case Import

To import a web-version case, enter the 32-character code generated when the case was exported and submit it.

Manual: https://mcgbm.taichung.gov.tw/arch/pdf/case_import_web.pdf

### Standalone Case Import

Use this path for standalone system cases, including V8 and V88 workflows where applicable.

Steps:

1. Select the case category.
2. Select the issuing authority.
3. If the case is under review, enter the one-code pass value to convert the legacy case.
4. If the one-code pass value is omitted, the output is treated as a new case.
5. Attach the `data.txt` file generated by the standalone system.

Manual: https://mcgbm.taichung.gov.tw/arch/pdf/case_import_single.pdf

---

## Section 8: Recommended Answering Workflow

Use the following structure as the starting point for future integration:

1. Confirm the project is under Taichung City jurisdiction.
2. Identify the user role: architect, contractor, staff, or external permit runner.
3. Confirm login method and whether authorization has already been granted.
4. If the task concerns staff access, explain the personnel authorization management flow.
5. If the task concerns daily permit work, route to application case management.
6. If the task concerns legacy or transferred cases, route to web or standalone case import.
7. Preserve unresolved details as pending field-level or screen-level notes rather than inventing system behavior.

---

## Section 9: Data Model Placeholder

```typescript
interface TaichungPaperlessPermitSystemUser {
  jurisdiction: "Taichung City";
  systemName: "paperless-building-permit-booklet-review-report-system";
  commonName: "2d-system";
  userRole: "architect" | "contractor" | "office-staff" | "contractor-staff" | "permit-runner";
  loginMethod: "citizen-digital-certificate" | "business-certificate" | "egov-account";
  authorizedOrganizations: string[];
  hasManagementPermission: boolean;
}

interface TaichungApplicationCaseManagement {
  activeOrganization: string;
  caseType:
    | "new-case"
    | "construction-permit"
    | "occupancy-permit"
    | "demolition-permit"
    | "design-change"
    | "preliminary-review"
    | "interior-renovation";
  visibleBecauseOf: "management-permission" | "case-specific-authorization";
}

interface TaichungCaseImport {
  importType: "web-version" | "standalone-version";
  webExportCode32?: string;
  standaloneVersion?: "V8" | "V88" | "other";
  issuingAuthority?: string;
  oneCodePass?: string;
  dataTxtAttached?: boolean;
}
```

---

## Section 10: Taiwan-Specific Notes

This is a Taiwan municipal workflow skill. Do not assume that workflows from the national 2016 Building Permit Application Form System apply to Taichung City without verification.

Pending information to collect:

- Exact screen path for personnel authorization management
- Application case management field lists by case type
- Construction permit booklet field mapping
- Review report data-entry rules
- Attachment upload constraints
- Web case import failure handling
- Standalone V8/V88 import differences
- Rare character code upload flow
- System code update report flow
- Common correction comments from Taichung reviewers

---

## Section 11: Integration Points

Future versions should connect this skill with:

- Taichung City building permit application document checklists
- Construction permit application process guidance
- Local building code and municipal autonomy rules
- Office-level permit submission QA checklists
- Legacy 2016 Building Permit Application Form System comparison notes
