#!/usr/bin/env python3
"""知識庫內容品質檢查：相對連結、去識別化、README 計數同步。

貢獻者可在送出 PR 前自行執行：

    python scripts/check_content.py

CI 於 PR 階段執行同一支腳本。預設只檢查有變動的檔案；加 --all 檢查全庫。

檢查項目
--------
1. links  相對連結是否可解析。指向尚未建立的目錄、且該行標示「籌備中」或
          「規劃」者視為刻意佔位，不算錯誤。
2. pii    是否夾帶個資或專案識別資訊（電話、email、身分證字號、統一編號、
          建照號碼、地號、與專案關聯的事務所名、本機絕對路徑、憑證樣式）。
          知識庫以 CC BY-SA 4.0 對外散布且實務上無法收回，這類資訊一旦
          併入即難以移除，因此在 PR 階段就要擋下。
3. counts README 的技能分類計數是否與 raw/ 實際內容相符（僅提示，不失敗；
          計數由維護者在合併後執行 scripts/update_readme_counts.py 更新，
          貢獻者無須自行修改 README）。
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"

# ── 1. 相對連結 ──────────────────────────────────────────────────────────
LINK = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
# 指向 GitHub 功能頁的相對路徑（../../issues/new 之類）在網站上有效，本地會誤判
GH_RELATIVE = re.compile(r"^\.\./\.\./(issues|pulls|discussions|wiki)/")
PLACEHOLDER_HINT = ("籌備", "規劃中", "TODO")


def check_links(files):
    problems = []
    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for lineno, line in enumerate(text.split("\n"), 1):
            for m in LINK.finditer(line):
                url = m.group(2).split("#")[0].strip()
                if not url or url.startswith(("http://", "https://", "mailto:")):
                    continue
                if GH_RELATIVE.match(url):
                    continue
                target = (f.parent / url).resolve()
                if target.exists():
                    continue
                # 尚未建立的目錄 + 該行標明籌備中 → 刻意佔位
                if url.endswith("/") and any(h in line for h in PLACEHOLDER_HINT):
                    continue
                problems.append((f, lineno, "連結無法解析：[%s](%s)" % (m.group(1)[:30], url)))
    return problems


# ── 2. 去識別化 ──────────────────────────────────────────────────────────
# 反斜線一律以 chr(92) 組出，避免經由 shell / heredoc 傳遞時被吞掉。
BS = chr(92)
DQ = chr(34)
SQ = chr(39)

PII = [
    ("身分證字號", re.compile(r"\b[A-Z][12]\d{8}\b")),
    ("統一編號", re.compile(r"(?:統一編號|統編)\s*[:：]?\s*\d{8}")),
    ("行動電話", re.compile(r"\b09\d{2}[-\s]?\d{3}[-\s]?\d{3}\b")),
    ("email", re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")),
    ("建照號碼", re.compile(r"\d{2,3}\s*[建使拆雜]字第\s*\d+\s*號")),
    ("地號", re.compile(r"[一-鿿]{2,6}段\s*\d+(?:-\d+)?\s*地號")),
    # 事務所名稱單獨出現多為公開案例引用（如認證名單、代表作品），不視為個資；
    # 只有與「本案／承辦／委託／業主／設計人／監造」等專案關聯詞同行時才報。
    ("專案關聯的事務所名", re.compile(
        r"(?:本案|承辦|委託|業主|設計人|監造)[^\n]{0,12}[一-鿿]{2,6}建築師事務所"
        r"|[一-鿿]{2,6}建築師事務所[^\n]{0,8}(?:承辦|監造|設計本案)")),
    ("承辦人姓名", re.compile(r"(?:承辦[人員]|經辦|聯絡人)\s*[:：]\s*[一-鿿]{2,4}")),
    ("本機絕對路徑", re.compile(
        "(?:[A-Z]:[" + BS + BS + "/]Users[" + BS + BS + "/]|/Users/|/home/)"
        "[^" + BS + "s" + DQ + SQ + "`)" + BS + "]]+")),
    ("憑證樣式", re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*['\"]?\S{8,}")),
]

PII_ALLOW = [
    # 政府公文函號（內授消字第 0920093655 號、台內營字第 … 號等）。
    # 民國年 + 流水號恰好長得像手機號碼，必須先排除，否則整庫函號都會誤報。
    #
    # 機關代碼限定 2 字以上：建照號碼是「112 建字第 0456 號」這種單字前綴
    # （建／使／拆／雜），若這裡寫成 {1,8} 會把建照號碼一起豁免掉，
    # 那正是我們要擋的專案識別資訊。
    re.compile(r"[一-鿿]{2,8}字第\s*\d+\s*號"),
    # 同一個函號在英文段落的寫法：Interpretation Letter No. 0920093655
    re.compile(r"(?i)\b(?:letter|order|ruling|decree|interpretation)\s+No\.?\s*\d+"),
    re.compile(r"example\.(com|org|net)"),
]


# 指南與範本本身會刻意示範「不該長這樣」的反例（例如 CONTRIBUTING 用
# C:\Users\王大明\… 說明路徑會洩漏案名），掃了必然誤報，故排除。
# 這些檔案不是知識內容，不對外散布實務資料。
PII_SKIP_FILES = {"CONTRIBUTING.md", "AGENTS.md"}
PII_SKIP_DIRS = {".github", "scripts"}


def check_pii(files):
    problems = []
    for f in files:
        if f.suffix.lower() not in (".md", ".json", ".yaml", ".yml", ".py", ".html"):
            continue
        if f.name in PII_SKIP_FILES:
            continue
        try:
            rel_parts = f.relative_to(ROOT).parts
        except ValueError:
            rel_parts = f.parts
        if rel_parts and rel_parts[0] in PII_SKIP_DIRS:
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for lineno, line in enumerate(text.split("\n"), 1):
            if any(a.search(line) for a in PII_ALLOW):
                continue
            for label, pat in PII:
                m = pat.search(line)
                if m:
                    problems.append((f, lineno, "疑似%s：%s" % (label, m.group(0)[:40])))
    return problems


# ── 3. README 計數（僅提示）──────────────────────────────────────────────
def check_counts():
    script = ROOT / "scripts" / "update_readme_counts.py"
    readme = ROOT / "README.md"
    if not script.exists() or not readme.exists():
        return []
    before = readme.read_bytes()
    subprocess.run([sys.executable, str(script)], capture_output=True, text=True, cwd=ROOT)
    after = readme.read_bytes()
    if after != before:
        readme.write_bytes(before)  # 還原，檢查腳本不應改動工作區
        return [(readme, 0,
                 "技能計數與 raw/ 實際內容不同步"
                 "（維護者合併後執行 scripts/update_readme_counts.py 即可；"
                 "貢獻者無須自行修改 README）")]
    return []


# ── 執行 ─────────────────────────────────────────────────────────────────
def changed_files(base):
    r = subprocess.run(["git", "diff", "--name-only", "--diff-filter=ACMR", base + "...HEAD"],
                       capture_output=True, text=True, cwd=ROOT)
    if r.returncode != 0:
        return None
    out = []
    for line in r.stdout.split("\n"):
        line = line.strip()
        if line:
            p = ROOT / line
            if p.exists():
                out.append(p)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="檢查全庫，而非只檢查變動檔案")
    ap.add_argument("--base", default="origin/main", help="比較基準（預設 origin/main）")
    args = ap.parse_args()

    if args.all:
        files = sorted(RAW.rglob("*.md")) + [ROOT / "README.md"]
        scope = "全庫"
    else:
        files = changed_files(args.base)
        if files is None:
            files = sorted(RAW.rglob("*.md")) + [ROOT / "README.md"]
            scope = "全庫（取不到 diff，改為全庫檢查）"
        else:
            scope = "%s...HEAD 的 %d 個變動檔案" % (args.base, len(files))

    print("檢查範圍：%s" % scope)
    print()

    link_problems = check_links(files)
    pii_problems = check_pii(files)
    count_notes = check_counts()

    for title, problems, fatal in (
        ("相對連結", link_problems, True),
        ("去識別化", pii_problems, True),
        ("README 計數", count_notes, False),
    ):
        mark = "OK" if not problems else ("FAIL" if fatal else "NOTE")
        print("[%s] %s：%d 項" % (mark, title, len(problems)))
        for f, lineno, msg in problems:
            loc = f.relative_to(ROOT).as_posix()
            print("       %s%s — %s" % (loc, (":%d" % lineno) if lineno else "", msg))
        print()

    if link_problems or pii_problems:
        print("有必須修正的項目。")
        print("去識別化若為誤判（例如政府函號、公開案例引用），請於 PR 說明，"
              "維護者會調整 scripts/check_content.py 的規則。")
        return 1
    print("通過。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
