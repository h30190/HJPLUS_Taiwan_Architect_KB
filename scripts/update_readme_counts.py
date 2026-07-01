#!/usr/bin/env python3
"""Update skill counts in README.md by counting actual SKILL.md files under raw/.

Insert `<!-- COUNT -->` before any auto-managed count line in README.md.
For the bottom classification table, insert `<!-- COUNT:summary -->`.

Usage:
    python scripts/update_readme_counts.py
"""

import os
import re
from pathlib import Path

RAW = Path(__file__).resolve().parent.parent / "raw"
README = Path(__file__).resolve().parent.parent / "README.md"

# Section → (default_class, individual overrides)
# Overrides key = relative path WITHOUT the /SKILL.md suffix
SECTION_CLASS = {
    "建築設計與規劃": {"default": "A", "overrides": {
        "建築設計與規劃/設計理論/spatial-planning": "B",
    }},
    "專業複委託":      {"default": "B", "overrides": {
        "專業複委託/材料設備/material-selection": "A",
    }},
    "建築性能":        {"default": "B"},
    "建築法規":        {"default": "C"},
    "專案管理":        {"default": "C"},
    "經營管理":        {"default": "B", "overrides": {
        "經營管理/專業服務費": "C",
        "經營管理/專業財務管理": "C",
        "經營管理/業務承接": "C",
        "經營管理/事務所營運": "C",
        "經營管理/創業指南": "C",
        "經營管理/專業執照": "C",
        "經營管理/繼續教育": "C",
    }},
    "建築施工與材料":  {"default": "C"},
    "建築執照":        {"default": "C"},
    "公共工程":        {"default": "C"},
    "設計軟體與工具":  {"default": "A"},
    "室內裝修":        {"default": "C"},
}


def get_class(section: str, rel_stem: str) -> str:
    """Return 'A', 'B', or 'C' for a skill given its section and relative path."""
    cfg = SECTION_CLASS.get(section, {"default": "C"})
    override = cfg.get("overrides", {}).get(rel_stem)
    return override or cfg["default"]


def fmt_count(total: int, a: int, b: int, c: int) -> str:
    """Format like '5 個技能模組（4A+1B）' or '17 個技能模組（17C）'."""
    if total == 0:
        return "**0 個技能模組（尚無 SKILL.md 檔案）**"
    parts = []
    if a:
        parts.append(f"{a}A")
    if b:
        parts.append(f"{b}B")
    if c:
        parts.append(f"{c}C")
    label = "+".join(parts)
    return f"**{total} 個技能模組（{label}）**"


def main():
    # ── 1. Count SKILL.md files ──────────────────────────────
    counts = {}  # section → {"total": int, "A": int, "B": int, "C": int}

    for sk_path in sorted(RAW.rglob("SKILL.md")):
        rel = sk_path.relative_to(RAW)
        section = rel.parts[0]
        # relative path without /SKILL.md
        stem = str(rel.parent).replace("\\", "/")

        if section not in counts:
            counts[section] = {"total": 0, "A": 0, "B": 0, "C": 0}
        cls = get_class(section, stem)
        counts[section]["total"] += 1
        counts[section][cls] += 1

    # ── 2. Read README and update ────────────────────────────
    content = README.read_text(encoding="utf-8")
    lines = content.split("\n")
    out = []
    i = 0

    while i < len(lines):
        line = lines[i]

        if line.strip() == "<!-- COUNT -->":
            out.append(line)  # keep marker
            i += 1

            # Scan backwards to find the section link: [名稱](dir/)
            section_name = None
            for j in range(len(out) - 1, max(len(out) - 6, -1), -1):
                m = re.search(r'\[([^\]]+)\]\(([^)]+)/\)', out[j])
                if m:
                    section_name = m.group(1)
                    break

            if section_name:
                cnt = counts.get(section_name, {"total": 0, "A": 0, "B": 0, "C": 0})
                new_line = fmt_count(cnt["total"], cnt["A"], cnt["B"], cnt["C"])
            else:
                new_line = lines[i] if i < len(lines) else ""

            # Skip old count lines
            while i < len(lines) and (
                lines[i].strip().startswith("**") and "個" in lines[i]
            ):
                i += 1
            out.append(new_line)
            continue

        if line.strip() == "<!-- COUNT:summary -->":
            out.append(line)
            i += 1

            # Recompute totals from all sections
            total_a = sum(c["A"] for c in counts.values())
            total_b = sum(c["B"] for c in counts.values())
            total_c = sum(c["C"] for c in counts.values())

            # Find the next 3 table rows and replace them
            summary_rows = i
            rows_found = 0
            while i < len(lines) and rows_found < 3:
                if lines[i].strip().startswith("| **"):
                    rows_found += 1
                i += 1

            new_summary = [
                f"| **A 類通用技能** | {total_a} 個 | 國際通用標準，無需台灣適配 | AI + 人類直接使用 |",
                f"| **B 類適配技能** | {total_b} 個 | 國際規範→台灣適配，保留 TODO 注記 | 國際→台灣雙向支援 |",
                f"| **C 類台灣法規技能** | {total_c} 個 | 完全台灣法規，MCP 工具對接 | 台灣法規本位，官方對接 |",
            ]
            out.extend(new_summary)
            continue

        out.append(line)
        i += 1

    # ── 3. Write back ────────────────────────────────────────
    README.write_text("\n".join(out), encoding="utf-8")
    total_all = sum(c["total"] for c in counts.values())
    print(f"[OK] Updated README.md - {total_all} skills across {len(counts)} sections")


if __name__ == "__main__":
    main()
