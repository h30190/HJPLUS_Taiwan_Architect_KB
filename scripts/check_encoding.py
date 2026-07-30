#!/usr/bin/env python3
"""Encoding guard — reject text files mangled by a non-UTF-8 pipeline.

Windows tooling defaults to the ANSI codepage (cp950 on zh-TW). Round-tripping
a UTF-8 file through it destroys Chinese irrecoverably: characters cp950 cannot
represent become '?', and the survivors land in the Unicode private-use area.
PR #13's cultural-heritage skills were lost this way — this hook stops a repeat.

Checks each file for:
    - invalid UTF-8            → wrong encoding on write
    - UTF-8 BOM                → breaks the leading `---` of SKILL.md frontmatter
    - private-use characters   → UTF-8 → cp950 → UTF-8 round-trip damage
    - U+FFFD replacement char  → lossy decode
    - no newline at all        → line endings flattened in transit

Usage:
    python scripts/check_encoding.py [files...]

With no arguments, scans every text file tracked by git. Exits 1 on any finding.
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TEXT_SUFFIXES = {".md", ".html", ".json", ".py", ".yml", ".yaml", ".txt", ".csv"}

# A single-line file is only suspicious once it is long enough to have wanted a break.
FLATTENED_MIN_CHARS = 200


def tracked_text_files():
    out = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True
    ).stdout
    return [Path(p.decode("utf-8")) for p in out.split(b"\0") if p]


def check(path):
    """Return a list of problem descriptions for one file (empty when clean)."""
    try:
        raw = path.read_bytes()
    except OSError as e:
        return [f"cannot read: {e}"]

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        return [f"not valid UTF-8 at byte {e.start} - saved with the wrong encoding?"]

    problems = []

    if raw.startswith(b"\xef\xbb\xbf"):
        problems.append("UTF-8 BOM at start of file - save as UTF-8 without BOM")

    pua = sum(1 for c in text if 0xE000 <= ord(c) <= 0xF8FF)
    if pua:
        problems.append(
            f"{pua} private-use character(s) - text was round-tripped through "
            "cp950/Big5 and the original characters are gone"
        )

    # Escape, not the literal character - otherwise this file fails its own check.
    fffd = text.count("\ufffd")
    if fffd:
        problems.append(f"{fffd} U+FFFD replacement character(s) - lossy decode")

    if "\n" not in text and len(text) >= FLATTENED_MIN_CHARS:
        problems.append(
            f"{len(text)} characters on a single line - line endings were flattened"
        )

    return problems


def main():
    args = [Path(a) for a in sys.argv[1:]]
    files = args or tracked_text_files()
    files = [f for f in files if f.suffix.lower() in TEXT_SUFFIXES]

    failed = 0
    checked = 0
    for path in files:
        full = path if path.is_absolute() else ROOT / path
        if not full.is_file():
            continue
        checked += 1
        for problem in check(full):
            print(f"{path.as_posix()}: {problem}")
            failed += 1

    if failed:
        print(
            f"\n[FAIL] {failed} encoding problem(s) in {checked} file(s) checked.\n"
            "       On Windows, write files with an explicit UTF-8 encoding:\n"
            "         PowerShell : Set-Content -Encoding utf8NoBOM  (5.1: use "
            "[IO.File]::WriteAllText)\n"
            "         Python     : open(path, 'w', encoding='utf-8')\n"
            "       Damage from a cp950 round-trip is NOT reversible - restore the "
            "file from git instead of hand-editing it.",
            file=sys.stderr,
        )
        return 1

    print(f"[OK] {checked} file(s) checked, no encoding problems.")
    return 0


if __name__ == "__main__":
    # Keep the console's own encoding so Chinese paths stay readable in a cp950
    # terminal, but never let an unencodable character crash the hook.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except AttributeError:
            pass
    sys.exit(main())
