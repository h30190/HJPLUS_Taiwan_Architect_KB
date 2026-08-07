#!/usr/bin/env python3
"""Validate the raw/ bundle against Open Knowledge Format (OKF) v0.2.

Checks the subset of OKF §8/§9/§11/§12 this repo commits to, plus the
repo-local conventions layered on top (see AGENTS.md "index.md — OKF
Directory Index").

Deliberate deviation: README.md files are human-facing navigation and are
exempt from the §11 `type` requirement. §11 forbids consumers from rejecting
a bundle over missing optional fields, so this stays conformant in practice.

Usage:
    python scripts/validate_okf.py          # report and exit 1 on error
    python scripts/validate_okf.py --quiet  # errors only
"""

import re
import sys
from pathlib import Path

# Paths and headings are Traditional Chinese; the Windows console defaults to
# cp950 and would mangle them.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"

OKF_VERSION = "0.2"
RESERVED = {"index.md", "log.md"}
EXEMPT = {"README.md"}

# Concept type vocabulary used by this bundle. OKF has no central registry;
# producers choose descriptive values and consumers tolerate unknown ones.
TYPES = {
    "domain.md": "Knowledge Entry",
    "SKILL.md": "Skill",
}

STATUS_VALUES = {"draft", "stable", "deprecated"}
ADAPTATION_MARKER = "<!-- TODO: Taiwan adaptation needed -->"
# Planned entries are marked either by a "## Planned" heading or, more often
# in this repo, inline with （籌備中） in the description.
PLANNED_INLINE = re.compile(r"籌備中|規劃中|\(planned\)", re.IGNORECASE)
ACTOR_RE = re.compile(r"^(human:|process:)\S+|^\S+/\S+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

errors = []
warnings = []
skill_names = {}  # name -> first path that claimed it


def err(path, msg):
    errors.append(f"{path.relative_to(ROOT)}: {msg}")


def warn(path, msg):
    warnings.append(f"{path.relative_to(ROOT)}: {msg}")


def split_frontmatter(path):
    """Return (frontmatter_lines, ok). ok=False when no frontmatter block."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return [], False
    lines = text.splitlines()
    try:
        end = lines.index("---", 1)
    except ValueError:
        err(path, "frontmatter block is never closed")
        return [], False
    return lines[1:end], True


def top_level_keys(fm_lines):
    """Flat key -> raw value for top-level (unindented) keys only."""
    out = {}
    for line in fm_lines:
        m = re.match(r"^([A-Za-z_][\w.-]*)\s*:\s*(.*)$", line)
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


def nested_keys(fm_lines, parent):
    """Flat key -> value for keys indented one level under `parent`."""
    out = {}
    inside = False
    for line in fm_lines:
        if re.match(rf"^{parent}\s*:\s*$", line):
            inside = True
            continue
        if inside:
            m = re.match(r"^\s+([\w.-]+)\s*:\s*(.*)$", line)
            if m:
                out[m.group(1)] = m.group(2).strip()
            elif line.strip() and not line.startswith((" ", "\t", "-")):
                inside = False
    return out


def check_concept(path, expected_type):
    fm, ok = split_frontmatter(path)
    if not ok:
        err(path, "§11.1 missing YAML frontmatter block")
        return
    keys = top_level_keys(fm)
    got = keys.get("type", "").strip("\"'")
    if not got:
        err(path, "§11.2 missing non-empty `type`")
    elif got != expected_type:
        err(path, f"§11.2 type is {got!r}, expected {expected_type!r}")

    if "status" in keys:
        v = keys["status"].strip("\"'")
        if v not in STATUS_VALUES:
            err(path, f"§5 status {v!r} not one of {sorted(STATUS_VALUES)}")
    if "stale_after" in keys:
        v = keys["stale_after"].strip("\"'")
        if not DATE_RE.match(v):
            err(path, f"§5 stale_after {v!r} is not YYYY-MM-DD")
    for line in fm:
        m = re.search(r"\bby\s*:\s*([^,}\s]+)", line)
        if m and not ACTOR_RE.match(m.group(1).strip("\"'")):
            warn(path, f"§7 actor {m.group(1)!r} is not human:/process:/<producer>/<version>")

    if path.name == "SKILL.md":
        name = keys.get("name", "").strip("\"'")
        if not name:
            err(path, "missing `name`")
        else:
            # Agent Skills resolve by `name`; two skills sharing one collide.
            first = skill_names.setdefault(name, path)
            if first != path:
                err(path, f"duplicate skill `name` {name!r}, already used by "
                          f"{first.relative_to(ROOT)}")
        if name and name != path.parent.name:
            # Pre-existing layout debt: a few skills sit directly in their
            # Chinese knowledge-entry directory instead of an English skill
            # directory. Renaming would break inbound links, so warn only.
            warn(path, f"`name` {name!r} != directory {path.parent.name!r}")
        if not keys.get("description"):
            err(path, "missing `description`")
        cls = nested_keys(fm, "metadata").get("class", "").strip("\"'")
        if cls not in {"A", "B", "C"}:
            err(path, f"metadata.class {cls!r} must be A, B or C")
        elif cls == "B" and ADAPTATION_MARKER not in path.read_text(encoding="utf-8"):
            # AGENTS.md requires B-class skills to flag the international spec
            # blocks that still need Taiwan adaptation. Warn rather than fail:
            # some skills on this list may simply be misclassified (a
            # Taiwan-only skill tagged B belongs in C, with no marker needed).
            warn(path, f"metadata.class B but no `{ADAPTATION_MARKER}` marker — "
                       "add markers, or reclassify if the content is not international")


def check_index(path, is_root):
    text = path.read_text(encoding="utf-8")
    has_fm = text.startswith("---")
    if is_root:
        if not has_fm:
            err(path, f"§12 bundle root must declare okf_version: \"{OKF_VERSION}\"")
        else:
            v = top_level_keys(split_frontmatter(path)[0]).get("okf_version", "").strip("\"'")
            if v != OKF_VERSION:
                err(path, f"§12 okf_version {v!r}, expected {OKF_VERSION!r}")
    elif has_fm:
        err(path, "§8 only the bundle-root index.md may carry frontmatter")

    planned = False
    for line in text.splitlines():
        if line.startswith("#"):
            # Entries under "## Planned" point at directories that do not
            # exist yet — that is the point of the section.
            planned = "Planned" in line or "籌備" in line
            continue
        m = re.match(r"^\s*\*\s*\[[^\]]+\]\(([^)]+)\)", line)
        if not m or planned or PLANNED_INLINE.search(line):
            continue
        target = m.group(1)
        if target.startswith(("http://", "https://", "#")):
            continue
        if not (path.parent / target).exists():
            err(path, f"§8 broken link: {target}")


def check_log(path):
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            d = line[3:].strip()
            if not DATE_RE.match(d):
                err(path, f"§9 date heading {d!r} must be ISO 8601 YYYY-MM-DD")


def main():
    quiet = "--quiet" in sys.argv
    if not RAW.is_dir():
        print(f"error: {RAW} not found")
        return 1

    concepts = 0
    for path in sorted(RAW.rglob("*.md")):
        name = path.name
        if name in EXEMPT:
            continue
        if name == "index.md":
            check_index(path, is_root=path.parent == RAW)
        elif name == "log.md":
            check_log(path)
        elif name in TYPES:
            check_concept(path, TYPES[name])
            concepts += 1
        else:
            # references/, assets/ and other loose .md are concept documents
            # too under §11; flag rather than fail so contributors can triage.
            fm, ok = split_frontmatter(path)
            if not ok or not top_level_keys(fm).get("type"):
                warn(path, "§11 non-reserved .md without `type`")

    if warnings and not quiet:
        print(f"warnings ({len(warnings)}):")
        for w in warnings:
            print(f"  ~ {w}")
    if errors:
        print(f"errors ({len(errors)}):")
        for e in errors:
            print(f"  x {e}")
        return 1
    if not quiet:
        print(f"OKF v{OKF_VERSION}: {concepts} concepts valid, 0 errors.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
