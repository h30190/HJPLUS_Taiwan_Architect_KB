---
name: contributor-pr-workflow
description: "This skill should be used when a contributor wants to submit a new skill, edit an existing skill, or make any change to the Taiwan Architect KB repository. It guides the full lifecycle: clone/fetch, branch, create/edit, self-validate, and submit PR."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
metadata:
  audience: contributors
  region: taiwan
  class: A
  status: verified
  data-currency: "2026-07-14"
---

# Contributor PR Workflow

Guide a contributor through the end-to-end process of submitting a change to this KB.

## Overview

This skill covers the full lifecycle from first clone to PR submission, with automated validation gates at each step. It prevents common mistakes: wrong directory structure, mismatched frontmatter, dirty files, broken links, and Simplified Chinese content.

## How It Works

### Phase 0: Environment Setup

1. **Clone the repo** (if first time):
   ```bash
   git clone https://github.com/h30190/HJPLUS_Taiwan_Architect_KB.git
   cd HJPLUS_Taiwan_Architect_KB
   ```

2. **Sync with latest main**:
   ```bash
   git checkout main
   git pull origin main
   ```

3. **Create a feature branch**:
   ```bash
   git checkout -b feat/your-feature-description
   ```

4. **Ask the contributor**: "What are you contributing?"
   - New skill → Phase 1
   - Edit existing skill → Phase 2
   - Rename / restructure → Phase 3
   - Other (fix typo, add reference, translate) → Phase 4

### Phase 1: Creating a New Skill

1. **Choose the category**: Look at `raw/` subdirectories to find the right home (建築設計與規劃, 建築法規, 公共工程, etc.).

2. **Copy the template**:
   ```bash
   cp -r 知識樣板/ raw/<category>/<chinese-entry-name>/
   ```

3. **Name the entry directory** (Traditional Chinese, intuitive name like `排煙窗法規檢討/`).

4. **Rename the skill directory** (inside the Chinese entry, from `skill-name-hyphenated/` to lowercase English hyphenated).

5. **Clean up optional subdirectories**: Delete `assets/`, `references/`, `scripts/` if not needed.

6. **Write `SKILL.md`**:
   - Frontmatter: `name` MUST match the skill directory name
   - `metadata.class` is REQUIRED (A/B/C)
   - `metadata.status` is RECOMMENDED (verified/unverified/draft)
   - `license` and `compatibility` are RECOMMENDED
   - Body in English, keep under 500 lines
   - C-class skills MUST include MCP tool examples

7. **Write `domain.md`**:
   - Traditional Chinese, NO frontmatter
   - 使用情境、學習目標、實務應用

8. **Update parent `index.md`**:
   - Open the parent directory's `index.md`
   - Add a new `* [Skill Name](path/SKILL.md) - description` entry under `## Skills`
   - If no `index.md` exists and the directory has 2+ children, create one per OKF v0.1

### Phase 2: Editing an Existing Skill

1. **Never delete `SKILL.md` or `domain.md` without a replacement**.

2. **Sync SKILL.md and domain.md**: If you change one, update the other.

3. **Preserve frontmatter**: `name` must stay in sync with directory name.

4. **If file is lowercase `skill.md`**, rename to `SKILL.md`:
   ```bash
   git mv <path>/skill.md <path>/SKILL.md
   ```

5. **B-class skills**: Keep `<!-- TODO: Taiwan adaptation needed -->` markers until adaptation is complete.

6. **When adding or removing a skill**, update the parent directory's `index.md` accordingly.

### Phase 3: Renaming / Restructuring

1. **Use `git mv`**, not OS-level rename:
   ```bash
   git mv <old-path> <new-path>
   ```

2. **Scan the entire repo** for stale references:
   ```bash
   # Search for old directory name in all markdown files
   grep -r "<old-name>" raw/ --include="*.md"
   ```
   Every reference must be updated.

3. **Update all `index.md` entries** that point to the old path.

4. **Update frontmatter `name`** if the skill directory name changed.

### Phase 4: Other Changes (Typo, Reference, Translation)

1. Make the change directly on your branch.
2. If touching a skill AND its domain, keep both in sync.
3. No special structure requirements.

### Phase 5: Self-Validation (RUN BEFORE SUBMITTING)

Run ALL checks below. If any fails, fix it before proceeding.

#### Structure Checks

- [ ] `SKILL.md` is uppercase (❌ `skill.md` is wrong)
- [ ] Three-layer structure correct:
      `category/chinese-entry/english-skill-name/SKILL.md`
      `category/chinese-entry/domain.md`
- [ ] `domain.md` has NO frontmatter (no `---` at top)
- [ ] No `.history/`, `.vscode/`, `node_modules/`, `__pycache__/` files in the diff
- [ ] Skill directory name is lowercase English hyphenated (❌ pinyin like `pai-yan-chuang`)
- [ ] Skill directory name matches `name` in SKILL.md frontmatter

#### Frontmatter Checks

- [ ] `name` is 1-64 chars, lowercase + hyphens only
- [ ] `description` is 1-1024 chars, includes trigger scenario
- [ ] `metadata.class` is present: A / B / C
- [ ] No undefined frontmatter fields (❌ `user-invocable`, `language`, `category` without AGENTS.md approval)

#### Content Checks

- [ ] **No Simplified Chinese characters** anywhere in new/modified files

  Common simplified characters to catch:
  `质`(→質) `体`(→體) `设`(→設) `门`(→門) `气`(→氣) `车`(→車)
  `机`(→機) `发`(→發/發展) `层`(→層) `组`(→組) `备`(→備)
  `标`(→標) `规`(→規) `场`(→場) `试`(→試) `复`(→複/復)
  `认`(→認) `适`(→適) `整`(→整) `审`(→審) `图`(→圖)
  `电`(→電) `专`(→專) `阀`(→閥) `预`(→預) `签`(→簽)
  `标`(→標) `记`(→記) `证`(→證) `准`(→準) `验`(→驗)

- [ ] In `REFERENCES.md` or body text: no broken relative paths
- [ ] C-class skills have MCP tool call examples

#### Index & Cross-Reference Checks

- [ ] Parent directory's `index.md` lists this skill (or is created if needed)
- [ ] If the skill belongs to an existing question cluster, it's added to `consultation-workflow/SKILL.md` Section 1 Step 3
- [ ] `## Related Skills` section exists (if overlapping skills exist in `raw/`)

### Phase 6: Submit

1. **Stage and commit**:
   ```bash
   git add -A
   git commit -m "type(scope): brief description"
   ```
   Use Conventional Commits:
   - `feat` = new skill
   - `fix` = bug/correction
   - `docs` = documentation
   - `refactor` = restructure

2. **Push**:
   ```bash
   git push origin feat/your-feature-description
   ```

3. **Create PR via GitHub CLI**:
   ```bash
   gh pr create --title "<title>" --body "<description>"
   ```

4. **Tell the contributor**: "Your PR is submitted! A maintainer will review it. If changes are requested, the review comments will tell you exactly what to fix."

## Troubleshooting

**"I don't have gh (GitHub CLI)"**
→ Push your branch, then open the PR manually at https://github.com/h30190/HJPLUS_Taiwan_Architect_KB/pulls

**"I can't push (permission denied)"**
→ You need to fork the repo first, then push to your fork and create a PR from there.

**"I don't know what class my skill is"**
→ A = International standard (no Taiwan adaptation). B = International → Taiwan (add TODO). C = Taiwan-specific code/regulation.

## Related Skills

* [consultation-workflow](../raw/建築顧問方法論/顧問諮詢工作流程/consultation-workflow/SKILL.md) - For consultants using the KB to answer questions
