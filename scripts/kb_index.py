#!/usr/bin/env python3
"""Scan raw/ and emit a structured index of every knowledge entry.

The website's 知識庫 page (docs/kb/) uses this to power browsing, filtering and
the 資料狀況 dashboard, so the scan records not just what each entry *is* but
what it is *missing* — that gap list doubles as the contribution backlog.

Pairing rule
------------
Each skill is a (domain.md, SKILL.md) pair. Two layouts exist in the repo:

    nested (documented)      中文知識入口/domain.md
                             中文知識入口/english-skill/SKILL.md

    flat   (legacy)          english-skill/domain.md
                             english-skill/SKILL.md

Both are indexed; ``layout`` records which one, so the dashboard can flag the
flat ones as structural debt against README/CONTRIBUTING.

Usage:
    python scripts/kb_index.py [-o docs/kb.json] [--pretty]

Output is deterministic for a given commit (dates come from git, not the wall
clock), so the GitHub Action only redeploys when content actually changed.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"

REPO_URL = "https://github.com/h30190/HJPLUS_Taiwan_Architect_KB"
BLOB = REPO_URL + "/blob/main/"

ADAPTATION_MARKER = "<!-- TODO: Taiwan adaptation needed -->"
PLANNED_RE = re.compile(r"籌備中|規劃中|\(planned\)", re.IGNORECASE)

# Frontmatter keys we report coverage for. `class` lives under `metadata:`.
TOP_KEYS = ["type", "name", "description", "license", "compatibility", "verified"]
META_KEYS = ["class", "region", "audience", "status", "regulation", "data-currency"]

# Keys whose absence is a real gap worth surfacing as a contribution task.
# type/name/description are 100% covered and structurally required, so they
# would only add noise to the backlog.
#
# The verification family (`verified`, `status`, `data-currency`) is still
# scanned and still lands in each entry, but is deliberately left out of the
# gap/coverage reporting the site renders — showing verification coverage is
# on hold. Re-enabling it is a display change: add the keys back here.
GAP_KEYS = [
    "region",
    "audience",
    "license",
    "compatibility",
]

CLASS_LABEL = {
    "A": "通用技能",
    "B": "待台灣適配",
    "C": "台灣法規",
}

# metadata.status as actually used in the repo. Note this differs from
# STATUS_VALUES in validate_okf.py ({draft, stable, deprecated}) — the repo
# settled on a verification vocabulary instead. Entries with no status at all
# fall through to "unknown", which is the largest bucket and the point of the
# 資料狀況 dashboard.
STATE_LABEL = {
    "verified": "已查證",
    "unverified": "未查證",
    "draft": "草稿",
    "unknown": "狀態未標示",
}

# A verified entry looks like:
#   verified:
#     - { by: human:Jen666-Tw, at: 2026-07-21T00:00:00Z }
VERIFIED_BY_RE = re.compile(r"by:\s*([^,}\s]+)")
VERIFIED_AT_RE = re.compile(r"at:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})")


def split_frontmatter(path):
    """Return (frontmatter_lines, body_text). Empty list if no frontmatter."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return [], ""
    if not text.startswith("---"):
        return [], text
    lines = text.split("\n")
    for i in range(1, len(lines)):
        if lines[i].rstrip() == "---":
            return lines[1:i], "\n".join(lines[i + 1 :])
    return [], text


def parse_frontmatter(lines):
    """Minimal YAML reader: flat scalars, one level of nesting, and lists.

    Enough for OKF frontmatter in this repo, which never nests deeper or uses
    block scalars. Values keep their raw string form; quotes are stripped.
    Returns (flat, nested, lists) where ``lists`` maps a parent key to its raw
    ``- ...`` item strings — that is how the `verified` family is written.
    """
    flat, nested, lists, parent = {}, {}, {}, None
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indented = line[:1] in (" ", "\t")
        stripped = line.strip()
        if indented and stripped.startswith("-"):
            if parent:
                lists.setdefault(parent, []).append(stripped[1:].strip())
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip().strip("\"'")
        if indented:
            if parent:
                nested.setdefault(parent, {})[key] = value
        else:
            parent = key if not value else None
            flat[key] = value
    return flat, nested, lists


def first_h1(text):
    for line in text.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    return ""


# Inline markdown to strip out of an extracted paragraph.
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]*\)")
MD_EMPH_RE = re.compile(r"[*_`]{1,3}")
# Lines that are structure rather than prose.
NON_PROSE_PREFIX = ("#", "-", "*", "+", ">", "|", "<!--", "<", "```", ":")
ORDERED_ITEM_RE = re.compile(r"^\d+[.)、]\s*")
BULLET_ITEM_RE = re.compile(r"^[-*+]\s+")


def _clean(text, limit):
    out = MD_EMPH_RE.sub("", MD_LINK_RE.sub(r"\1", text)).strip()
    if len(out) > limit:
        out = out[: limit - 1].rstrip("，、。；：,;: ") + "…"
    return out


def _is_prose(stripped):
    """A line that reads as a sentence, not as list/table/heading structure."""
    if stripped.startswith(NON_PROSE_PREFIX):
        return False
    return not ORDERED_ITEM_RE.match(stripped)


def human_summary(text, limit=220):
    """First prose paragraph after the first H2 of a domain.md.

    That is the human-facing gist of a knowledge entry — every domain.md in
    the repo opens with a 使用情境 / 定義 / 為什麼重要 section whose first
    paragraph says what the entry is for. The site shows this instead of the
    SKILL.md `description`, which is written in English for the AI.
    """
    lines = text.split("\n")
    start = None
    for i, line in enumerate(lines):
        if line.startswith("## "):
            start = i + 1
            break
    if start is None:
        return ""

    body = lines[start:]

    # Take the first prose paragraph anywhere after that heading. Roughly a
    # third of the entries open their first section with a table or a list,
    # so stopping at the next H2 would leave them blank.
    para = []
    for line in body:
        stripped = line.strip()
        if not stripped:
            if para:
                break
            continue
        if not _is_prose(stripped):
            if para:
                break
            continue  # skip headings, lists and tables until prose appears
        para.append(stripped)
    if para:
        return _clean(" ".join(para), limit)

    # Fallback: some entries are pure checklists with no prose at all. Their
    # first few list items still say what the entry covers.
    items = []
    for line in body:
        stripped = line.strip()
        m = ORDERED_ITEM_RE.match(stripped) or BULLET_ITEM_RE.match(stripped)
        if m:
            item = stripped[m.end():].split("：")[0].split("|")[0].strip(" *_`")
            item = item.rstrip("。.；;、,")
            if item:
                items.append(item)
        if len(items) >= 5:
            break
    return _clean("、".join(items), limit) if items else ""


def git_last_modified(paths):
    """Most recent commit date touching any of ``paths`` (YYYY-MM-DD)."""
    newest = ""
    for path in paths:
        try:
            out = subprocess.run(
                ["git", "log", "-1", "--format=%cs", "--", str(path)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            ).stdout.strip()
        except OSError:
            out = ""
        if out > newest:
            newest = out
    return newest


def rel(path):
    """Repo-relative posix path, falling back to the raw path when outside."""
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return Path(path).as_posix()


def find_pairs():
    """Yield (domain_md, skill_md, layout) for every skill in raw/."""
    for skill_md in sorted(RAW.rglob("SKILL.md")):
        sibling = skill_md.parent / "domain.md"
        parent = skill_md.parent.parent / "domain.md"
        if sibling.exists():
            yield sibling, skill_md, "flat"
        elif parent.exists():
            yield parent, skill_md, "nested"
        else:
            yield None, skill_md, "orphan"


def build_entry(domain_md, skill_md, layout):
    s_fm, s_body = split_frontmatter(skill_md)
    s_flat, s_nested, s_lists = parse_frontmatter(s_fm)
    meta = s_nested.get("metadata", {})

    # `verified:` is a list of flow-mappings, so it has no scalar value.
    verified_items = s_lists.get("verified", [])
    verified_by = [m.group(1) for i in verified_items for m in [VERIFIED_BY_RE.search(i)] if m]
    verified_at = [m.group(1) for i in verified_items for m in [VERIFIED_AT_RE.search(i)] if m]

    if domain_md is not None:
        d_fm, d_body = split_frontmatter(domain_md)
        d_flat, _, _ = parse_frontmatter(d_fm)
        title = d_flat.get("title") or first_h1(d_body) or skill_md.parent.name
        domain_rel = rel(domain_md)
        domain_chars = len(d_body)
        summary = human_summary(d_body)
    else:
        title = skill_md.parent.name
        domain_rel = None
        domain_chars = 0
        summary = ""

    # Category path: raw/<分類>/<子分類…>/ up to but excluding the skill folder.
    parts = skill_md.relative_to(RAW).parts[:-1]  # drop "SKILL.md"
    skill_dir = parts[-1] if parts else ""
    breadcrumb = list(parts[:-1]) if layout == "flat" else list(parts[:-2])
    category = breadcrumb[0] if breadcrumb else (parts[0] if parts else "未分類")

    present = {k: bool(s_flat.get(k)) for k in TOP_KEYS}
    present.update({k: bool(meta.get(k)) for k in META_KEYS})
    present["verified"] = bool(verified_items)
    missing = [k for k in GAP_KEYS if not present.get(k)]

    # One field the UI can filter and colour on. An entry that carries a
    # `verified` record outranks whatever metadata.status claims.
    state = meta.get("status", "").strip() or "unknown"
    if verified_items:
        state = "verified"
    elif state not in STATE_LABEL:
        state = "unknown"

    combined = s_body + (d_body if domain_md is not None else "")
    skill_folder = skill_md.parent

    return {
        "title": title,
        "name": s_flat.get("name") or skill_dir,
        # summary  = 給人讀的（domain.md 中文）；description = 給 AI 讀的（SKILL.md 英文）
        "summary": summary,
        "description": s_flat.get("description", ""),
        "category": category,
        "breadcrumb": breadcrumb,
        "klass": meta.get("class", ""),
        "klassLabel": CLASS_LABEL.get(meta.get("class", ""), ""),
        "status": meta.get("status", ""),
        "state": state,
        "stateLabel": STATE_LABEL[state],
        "region": meta.get("region", ""),
        "audience": meta.get("audience", ""),
        "regulation": meta.get("regulation", ""),
        "dataCurrency": meta.get("data-currency", ""),
        "license": s_flat.get("license", ""),
        "verified": bool(verified_items),
        "verifiedBy": verified_by,
        "verifiedAt": verified_at[0] if verified_at else "",
        "layout": layout,
        "hasTodo": ADAPTATION_MARKER in combined,
        "isPlanned": bool(PLANNED_RE.search(combined)),
        "hasReferences": (skill_folder / "references").is_dir(),
        "hasScripts": (skill_folder / "scripts").is_dir(),
        "hasAssets": (skill_folder / "assets").is_dir(),
        "domainChars": domain_chars,
        "skillChars": len(s_body),
        "missing": missing,
        "completeness": round(
            100 * (len(GAP_KEYS) - len(missing)) / len(GAP_KEYS)
        ),
        "updated": git_last_modified(
            [p for p in (domain_md, skill_md) if p is not None]
        ),
        "domainPath": domain_rel,
        "skillPath": rel(skill_md),
        "domainUrl": BLOB + domain_rel if domain_rel else None,
        "skillUrl": BLOB + rel(skill_md),
    }


def summarise(entries):
    total = len(entries)

    def count(pred):
        return sum(1 for e in entries if pred(e))

    coverage = {}
    for key in GAP_KEYS:
        have = count(lambda e, k=key: k not in e["missing"])
        coverage[key] = {
            "have": have,
            "missing": total - have,
            "pct": round(100 * have / total) if total else 0,
        }

    # Seed from the directory listing, not from entries, so a category that is
    # advertised in the README but holds no skill yet still shows up — an empty
    # category is a contribution opening, not something to hide.
    categories = {
        d.name: {"total": 0, "verified": 0, "todo": 0, "planned": 0}
        for d in sorted(RAW.iterdir())
        if d.is_dir()
    }
    for e in entries:
        c = categories.setdefault(
            e["category"], {"total": 0, "verified": 0, "todo": 0, "planned": 0}
        )
        c["total"] += 1
        if e["verified"]:
            c["verified"] += 1
        if e["hasTodo"]:
            c["todo"] += 1
        if e["isPlanned"]:
            c["planned"] += 1

    classes = {}
    for e in entries:
        classes[e["klass"] or "?"] = classes.get(e["klass"] or "?", 0) + 1

    states = {k: count(lambda e, k=k: e["state"] == k) for k in STATE_LABEL}

    return {
        "total": total,
        "coverage": coverage,
        "categories": categories,
        "emptyCategories": sorted(k for k, v in categories.items() if not v["total"]),
        "classes": classes,
        "states": states,
        "verified": count(lambda e: bool(e["verified"])),
        "withTodo": count(lambda e: e["hasTodo"]),
        "planned": count(lambda e: e["isPlanned"]),
        "flatLayout": count(lambda e: e["layout"] == "flat"),
        "orphan": count(lambda e: e["layout"] == "orphan"),
        "withReferences": count(lambda e: e["hasReferences"]),
        "withScripts": count(lambda e: e["hasScripts"]),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-o", "--out", default=str(ROOT / "docs" / "kb.json"))
    ap.add_argument("--pretty", action="store_true")
    ap.add_argument(
        "--stats", action="store_true", help="print a human summary to stderr"
    )
    args = ap.parse_args()

    if not RAW.is_dir():
        print(f"raw/ not found at {RAW}", file=sys.stderr)
        return 1

    entries = [build_entry(d, s, layout) for d, s, layout in find_pairs()]
    entries.sort(key=lambda e: (e["category"], e["title"]))

    payload = {
        "okfVersion": "0.2",
        "repo": REPO_URL,
        "summary": summarise(entries),
        "entries": entries,
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None)
        + "\n",
        encoding="utf-8",
    )

    s = payload["summary"]
    print(f"kb_index: {s['total']} entries -> {rel(out)}", file=sys.stderr)
    if args.stats:
        for key, n in s["states"].items():
            print(f"  {STATE_LABEL[key]:<6} {n:>3}/{s['total']}", file=sys.stderr)
        print(f"  TODO adapt  {s['withTodo']}   planned {s['planned']}", file=sys.stderr)
        print(f"  flat layout {s['flatLayout']}   orphan {s['orphan']}", file=sys.stderr)
        print(f"  empty cats  {','.join(s['emptyCategories']) or '-'}", file=sys.stderr)
        for key, c in s["coverage"].items():
            print(f"  {key:<14} {c['have']:>3}/{s['total']} ({c['pct']}%)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
