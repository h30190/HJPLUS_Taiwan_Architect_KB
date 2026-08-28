---
type: Skill
name: revit-ai-targeting-and-safe-execution
description: "This skill should be used when an AI agent, MCP tool, Revit add-in, or automation must inspect or change a live Revit model and needs to prove its target set, choose bounded read-only context, preview risk, execute in a supported Revit API context, read the result back independently, and report evidence without overstating success."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
sources:
  - id: autodesk-revit-2024-transactions
    resource: https://help.autodesk.com/cloudhelp/2024/ENU/Revit-API/files/Revit_API_Developers_Guide/Basic_Interaction_with_Revit_Elements/Revit_API_Revit_API_Developers_Guide_Basic_Interaction_with_Revit_Elements_Transactions_html.html
    title: "Autodesk Revit 2024 API Developers Guide: Transactions"
    last_modified: 2023-10-26
  - id: autodesk-revit-2024-transaction-classes
    resource: https://help.autodesk.com/cloudhelp/2024/ENU/Revit-API/files/Revit_API_Developers_Guide/Basic_Interaction_with_Revit_Elements/Transactions/Revit_API_Revit_API_Developers_Guide_Basic_Interaction_with_Revit_Elements_Transactions_Transaction_Classes_html.html
    title: "Autodesk Revit 2024 API Developers Guide: Transaction Classes"
    last_modified: 2023-10-26
  - id: autodesk-revit-2024-external-events
    resource: https://help.autodesk.com/cloudhelp/2024/ENU/Revit-API/files/Revit_API_Developers_Guide/Advanced_Topics/Revit_API_Revit_API_Developers_Guide_Advanced_Topics_External_Events_html.html
    title: "Autodesk Revit 2024 API Developers Guide: External Events"
    last_modified: 2023-10-26
  - id: bim-personal-agent-v081
    resource: https://github.com/NicheSam/BIM-personal-agent/releases/tag/v0.8.1
    title: "BIM Personal Agent v0.8.1"
    last_modified: 2026-08-28
metadata:
  audience: architects
  region: taiwan
  class: A
  data-currency: "2026-08-28"
---

# Revit AI Targeting and Safe Execution

## Overview

Use this skill for any live Revit task where an AI-controlled workflow may inspect, create, modify, or delete model data. The workflow is:

> read current state → prove targets → inspect only what is needed → preview risk and scope → execute through Revit → read back independently → report evidence and recovery

This is a workflow skill, not an installation guide, product API, or claim that one tool makes arbitrary Revit automation safe. Autodesk documentation is authoritative for Revit API context and transaction behavior. BIM Personal Agent is the contributor's personal research project; v0.8.1 is cited only as a public implementation example of read-only element inspection, explicit target sources, and conservative single-target auto-follow.[^bim-personal-agent-v081]

No existing Revit skill in this knowledge base covers this workflow. The cross-linked uncertainty skill governs source confidence; this skill governs live-model targeting, execution, and readback.

## Non-Negotiable Distinctions

Keep these claims separate:

1. **Target resolved**: the exact element set is known.
2. **Execution returned**: Revit or a bridge returned a result.
3. **Model impact observed**: created, modified, or deleted IDs are known.
4. **Outcome verified**: required claims were independently read from the model.
5. **Deployment verified**: the intended manifest, DLL, runtime, and configuration are installed.

None of these proves the others.

## Execution Steps

### 1. Read Current Revit State

Before planning a mutation, capture only the state needed to bind the task:

- exact Revit version;
- connection or bridge identity, when one exists;
- active document identity or a privacy-safe fingerprint;
- active view ID and type when view context matters;
- current selection IDs;
- whether the document changed during inspection.

If the active document changes between planning and execution, invalidate the plan and re-read state.

### 2. Prove the Target Set

Classify the target source before using it:

| Target source | May execute automatically? | Required check |
|---|---|---|
| Explicit ElementId supplied by the user | Yes | Confirm it exists in the bound document and matches the requested kind |
| Current selection | Yes, when selection and intent match | Preserve the complete selected ID set; do not silently take only the first item |
| Reviewed candidate set | Yes | Record the reviewed IDs and the distinguishing evidence |
| IDs returned by an earlier tool in the same trace | Yes | Preserve lineage to the producing request |
| IDs created by the current operation | Yes for follow-up/readback | Preserve creation lineage and transaction state |
| Name, category, family, type, proximity, or heuristic match | No | Treat as candidates and request review or add a deterministic filter |

An empty target or ambiguous candidate set is a stop condition, not permission to guess.

Single-target auto-follow is a conservative convenience: automatically deepen inspection only when exactly one target is proven. It is not a ban on multi-target work. A multi-target mutation is allowed when the full set is explicit, previewable, and verifiable.

### 3. Inspect Read-Only Context Progressively

Start with the smallest useful level:

1. **Summary**: identity, category/type, document/view relevance, location summary.
2. **Parameters**: requested instance and type parameters, including writable/read-only state.
3. **Full**: geometry summary, relationships, owner/view/sheet context, or other bounded detail required by the task.

Do not begin with a project-wide scan when one exact element answers the question. Read-only inspection must not open a mutation Transaction or trigger another inspection recursively.

### 4. Classify Risk and Preview Scope

| Risk class | Minimum preview | Execution rule |
|---|---|---|
| Read-only | Query purpose and target set | No model mutation |
| Reversible write | Target IDs, before/after fields, expected count, Undo label | Execute in a named Transaction and verify Commit status |
| Multi-step reversible write | All steps, shared document, failure behavior | Use an atomic boundary when supported; rollback the group if a required step fails |
| Destructive or hard-to-recover | Actual affected scope and recovery limits | Require explicit human confirmation; refuse if actual scope cannot be shown |
| Uncertain after dispatch | Last confirmed state and unresolved operation | Do not retry automatically; read current state first |

Any Revit model change requires an active Transaction.[^autodesk-revit-2024-transactions] A committed named Transaction appears in Revit's Undo menu. TransactionGroup can rollback committed inner transactions or assimilate them into one Undo item when the API workflow supports it.[^autodesk-revit-2024-transaction-classes]

### 5. Execute Through a Supported Revit API Context

For a modeless UI or asynchronous agent, marshal work through ExternalEvent or another supported Revit API entry point. Raising an ExternalEvent requests execution; Revit calls the handler when it can process the event.[^autodesk-revit-2024-external-events]

During execution:

- bind again to the expected document;
- restrict inputs to the proven target set;
- give the Transaction a task-specific name;
- record Start, Commit, Rollback, or Pending status;
- collect actual created, modified, and deleted ElementIds;
- never treat queue acceptance as completed execution.

### 6. Read Back Required Claims Independently

Define the claims before execution. Examples:

- parameter X on ElementId Y equals the requested value;
- every created ID exists and has the expected type/level/location;
- every deleted ID is absent;
- the active view override exists for exactly the intended elements.

After execution, query Revit again. Do not call an echoed input, an execution summary, or the mutating function's own assertion independent readback.

Use these outcome terms consistently:

| Status | Meaning |
|---|---|
| `verified` | Every required claim has independent evidence and passed |
| `partially_verified` | Execution completed, but one or more required claims lack evidence |
| `verification_failed` | At least one required claim was read back and failed |
| `not_verified` | Execution completed without requested readback |
| `uncertain` | Dispatch or timeout makes it unsafe to assert whether execution happened |

Counts are not enough. Compare the actual ElementId sets and claim coverage. If applied count, verified count, and unique IDs disagree, preserve partial, failed, or unknown status.

### 7. Report Evidence and Recovery

Return a compact engineering summary containing:

- active document/view binding without exposing sensitive paths;
- target source and exact or redacted target set;
- operation and risk class;
- actual created/modified/deleted counts and IDs when safe to disclose;
- Transaction name and final state;
- verification status, covered claims, failed claims, and missing evidence;
- Undo or rollback instructions;
- any timeout, document change, or unresolved ambiguity.

Use [references/evidence-contract.md](references/evidence-contract.md) as the reusable output checklist.

## Worked Example

**Request:** Change the Comments value of the currently selected wall to `待協調`.

1. Read the active document, view, and selection.
2. Stop if selection is empty, has multiple elements for this singular request, or the selected element is not a wall.
3. Inspect the selected wall's identity, current Comments value, and parameter writability.
4. Preview one target ID, old value, requested value, named Transaction, and Undo availability.
5. Execute the parameter write in the supported Revit API context and commit the Transaction.
6. Re-query Comments for the same ElementId.
7. Report `verified` only when the readback equals `待協調`; otherwise report the observed value and `verification_failed` or `uncertain`.

If the call times out after dispatch, do not send the same write again. Re-read the wall first, because the original operation may already have reached the Revit UI thread.

## Common Pitfalls

### Pitfall: First match becomes the target
- **Severity**: 🔴 model-impact risk
- **Wrong**: Mutate the first element returned by a name or category search.
- **Right**: Present candidates or add deterministic constraints until the exact set is proven.

### Pitfall: Success response becomes verification
- **Severity**: 🔴 false-completion risk
- **Wrong**: Report the requested value from the execution response as actual model state.
- **Right**: Perform an independent Revit query and map each required claim to an observation.

### Pitfall: Automatic retry after timeout
- **Severity**: 🔴 duplicate-change risk
- **Wrong**: Reissue a mutation when completion is unknown.
- **Right**: Mark the state uncertain, read back the model, then decide whether correction is needed.

### Pitfall: Matching counts hide mismatched IDs
- **Severity**: 🟡 evidence risk
- **Wrong**: Treat five applied and five verified elements as the same set without comparing IDs.
- **Right**: Compare unique ID sets and per-claim coverage.

### Pitfall: One-target auto-follow becomes a batch prohibition
- **Severity**: 🟡 workflow risk
- **Wrong**: Reject every multi-element task.
- **Right**: Restrict automatic inference; allow explicit, reviewed, bounded multi-target sets.

## Evidence Boundaries

| Evidence layer | What it proves | What it does not prove |
|---|---|---|
| Source and policy review | Intended behavior and documented constraints | Compiled or deployed behavior |
| Automated tests | Covered policy branches and data contracts | Live Revit API behavior in the current model |
| Build and deployment checks | Intended artifacts and configuration are present | Correct task result |
| Live smoke | One bounded scenario worked in a named environment | General correctness for other models or versions |
| Independent model readback | Required claims for the current target set | Unchecked adjacent effects |
| Public release/tag | Reproducible version identity and distributable artifact | User-specific installation or live-model state |

## Data Currency

- Autodesk Revit API version checked: Revit 2024 documentation.
- Autodesk pages last modified: 2023-10-26; checked 2026-08-28.
- Implementation example: BIM Personal Agent v0.8.1; checked 2026-08-28.
- Volatility: **HIGH across Revit versions and agent implementations**. Re-check the exact Revit version documentation and the currently loaded add-in/runtime before execution.

## To Verify

- [ ] Re-check transaction, failure-processing, and ExternalEvent behavior against the exact documentation for any Revit version other than 2024; this entry only checked the 2024 guide.
- [ ] Define separate recovery and evidence rules before applying this workflow to linked documents, cross-document plans, or operations that cannot be undone.

## Related Skills

- [uncertainty-and-source-control](../../../../../建築顧問方法論/不確定性標示與來源管控/uncertainty-and-source-control/SKILL.md) — controls certainty labels and source trust; use it when describing unresolved or version-dependent claims.

[^autodesk-revit-2024-transactions]: Autodesk, [Revit 2024 API Developers Guide — Transactions](https://help.autodesk.com/cloudhelp/2024/ENU/Revit-API/files/Revit_API_Developers_Guide/Basic_Interaction_with_Revit_Elements/Revit_API_Revit_API_Developers_Guide_Basic_Interaction_with_Revit_Elements_Transactions_html.html).
[^autodesk-revit-2024-transaction-classes]: Autodesk, [Revit 2024 API Developers Guide — Transaction Classes](https://help.autodesk.com/cloudhelp/2024/ENU/Revit-API/files/Revit_API_Developers_Guide/Basic_Interaction_with_Revit_Elements/Transactions/Revit_API_Revit_API_Developers_Guide_Basic_Interaction_with_Revit_Elements_Transactions_Transaction_Classes_html.html).
[^autodesk-revit-2024-external-events]: Autodesk, [Revit 2024 API Developers Guide — External Events](https://help.autodesk.com/cloudhelp/2024/ENU/Revit-API/files/Revit_API_Developers_Guide/Advanced_Topics/Revit_API_Revit_API_Developers_Guide_Advanced_Topics_External_Events_html.html).
[^bim-personal-agent-v081]: [BIM Personal Agent v0.8.1 release](https://github.com/NicheSam/BIM-personal-agent/releases/tag/v0.8.1), a public personal research project developed by the contributor and used here only as an implementation example; its project-specific policies are not Autodesk requirements.
