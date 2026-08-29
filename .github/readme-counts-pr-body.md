由 `update-readme-counts` workflow 自動產生。

上一次合併變動了 `raw/**/SKILL.md`，技能分類計數因此需要重算。由於 main 的分支保護要求 review，workflow 無法直接推送到 main，改以 PR 形式提出。

**這個 PR 只動 README 的計數表**，可直接合併。

若希望日後由 workflow 直接推送、不再產生這類 PR，可在 Settings → Branches → main 的保護規則中，將 `github-actions[bot]` 加入 *Allow specified actors to bypass required pull requests*。
