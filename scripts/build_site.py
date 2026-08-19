#!/usr/bin/env python3
"""Assemble docs/ (the GitHub Pages deploy target) from site/.

The repo's contributors are architects, not web developers, so the site keeps a
zero-JavaScript-toolchain build: this script is plain stdlib string templating.
`git clone && python scripts/build_site.py` gives a working local preview.

Source layout
-------------
    site/templates/base.html   page shell; {{placeholders}} filled per page
    site/partials/*.html       header / footer, shared by every page
    site/pages/*.html          one file per page, with a `<!--meta ... -->` head
    site/assets/*              css / js, copied verbatim to docs/assets/

Every page is written to docs/<slug>/index.html (docs/index.html for `index`),
and links between pages spell out `index.html` so the output works both on a
web server and when opened straight off disk with file://.

Usage:
    python scripts/build_site.py [--clean]
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
DOCS = ROOT / "docs"

NL = chr(10)

META_RE = re.compile(r"^<!--meta\s*(.*?)-->\s*", re.DOTALL)
PLACEHOLDER_RE = re.compile(r"\{\{(\w+)\}\}")

REPO_URL = "https://github.com/h30190/HJPLUS_Taiwan_Architect_KB"
SITE_URL = "https://h30190.github.io/HJPLUS_Taiwan_Architect_KB"

# Order defines the header nav. `slug` doubles as the output directory name and
# as the `nav:` value a page declares to light up its own tab.
NAV = [
    {"slug": "index", "label": "首頁"},
    {"slug": "why", "label": "為什麼"},
    {"slug": "kb", "label": "知識庫"},
    {"slug": "contribute", "label": "參與"},
    {"slug": "quality", "label": "品質"},
    {"slug": "community", "label": "社群"},
]

# Assets that are already in docs/ and are not build output.
KEEP_IN_DOCS = {"images", "CNAME", ".nojekyll"}


def parse_meta(text):
    """Pull the leading `<!--meta key: value -->` block off a page source."""
    m = META_RE.match(text)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).split("\n"):
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    return meta, text[m.end() :]


def render(template, values):
    """Replace {{key}} with values[key]; unknown keys collapse to empty."""
    return PLACEHOLDER_RE.sub(lambda m: str(values.get(m.group(1), "")), template)


def build_nav(active, root):
    items = []
    for item in NAV:
        href = f"{root}index.html" if item["slug"] == "index" else f"{root}{item['slug']}/index.html"
        cls = ' class="active"' if item["slug"] == active else ""
        items.append(f'<a href="{href}"{cls}>{item["label"]}</a>')
    return "\n      ".join(items)


def out_path(slug):
    return DOCS / "index.html" if slug == "index" else DOCS / slug / "index.html"


def page_url(slug):
    return f"{SITE_URL}/" if slug == "index" else f"{SITE_URL}/{slug}/"


def last_modified(path):
    """Date of the last commit touching `path`, as YYYY-MM-DD.

    Returns None outside a git checkout, or for a file that has never been
    committed — the sitemap entry then omits <lastmod> rather than claiming a
    date we cannot back up.
    """
    result = subprocess.run(
        ["git", "log", "-1", "--format=%cs", "--", str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() or None


def write_sitemap(entries):
    """docs/sitemap.xml — the file to submit to Search Console.

    `entries` is [(url, lastmod)], collected by the same loop that writes the
    pages, so a newly added page cannot be forgotten here.
    """
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, lastmod in entries:
        lines.append("  <url>")
        lines.append("    <loc>" + url + "</loc>")
        if lastmod:
            lines.append("    <lastmod>" + lastmod + "</lastmod>")
        lines.append("  </url>")
    lines.append("</urlset>")
    (DOCS / "sitemap.xml").write_text(NL.join(lines) + NL, encoding="utf-8")


def write_robots():
    """docs/robots.txt.

    Caveat worth knowing: this deploys to a *project* Pages site
    (h30190.github.io/HJPLUS_Taiwan_Architect_KB/), and crawlers only read
    robots.txt from the domain root — which belongs to the user Pages repo,
    not this one. So the file is inert today; it starts working the day the
    site moves to a custom domain. The sitemap gets submitted to Search
    Console directly either way.
    """
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        "Sitemap: " + SITE_URL + "/sitemap.xml",
    ]
    (DOCS / "robots.txt").write_text(NL.join(lines) + NL, encoding="utf-8")


def clean_docs():
    """Remove previous build output, leaving hand-managed assets in place."""
    if not DOCS.is_dir():
        return
    for child in DOCS.iterdir():
        if child.name in KEEP_IN_DOCS:
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def run_generator(script, *extra):
    """Run one of the sibling data generators, failing loudly if it errors."""
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script)] + list(extra),
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        sys.stderr.write(result.stdout + result.stderr)
        raise SystemExit(f"{script} failed")
    sys.stderr.write(result.stderr)


def run_data():
    """Regenerate the two JSON files every page reads at load time.

    kb.json   — 知識庫 index and 資料狀況 dashboard
    data.json — hero counters, contributor list, 最近更新
    """
    run_generator("kb_index.py", "-o", str(DOCS / "kb.json"))
    run_generator("update_landing_page.py")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--clean", action="store_true", help="wipe build output first")
    ap.add_argument("--skip-index", action="store_true", help="don't regenerate kb.json")
    args = ap.parse_args()

    if not SITE.is_dir():
        raise SystemExit(f"site/ not found at {SITE}")

    if args.clean:
        clean_docs()
    DOCS.mkdir(parents=True, exist_ok=True)

    base = (SITE / "templates" / "base.html").read_text(encoding="utf-8")
    header = (SITE / "partials" / "header.html").read_text(encoding="utf-8")
    footer = (SITE / "partials" / "footer.html").read_text(encoding="utf-8")

    # Assets are shared, so every page links them through {{root}}.
    assets_src = SITE / "assets"
    assets_dst = DOCS / "assets"
    if assets_dst.exists():
        shutil.rmtree(assets_dst)
    shutil.copytree(assets_src, assets_dst)

    known = {item["slug"] for item in NAV}
    built = []
    sitemap_entries = []
    for src in sorted((SITE / "pages").glob("*.html")):
        slug = src.stem
        meta, body = parse_meta(src.read_text(encoding="utf-8"))
        root = "" if slug == "index" else "../"
        values = {
            "root": root,
            "title": meta.get("title", slug),
            "description": meta.get("description", ""),
            "bodyclass": meta.get("bodyclass", "doc"),
            "url": page_url(slug),
            "repo": REPO_URL,
            "site": SITE_URL,
            "nav": build_nav(meta.get("nav", slug), root),
            "extrahead": meta.get("extrahead", ""),
            "extrajs": meta.get("extrajs", ""),
        }
        values["header"] = render(header, values)
        values["footer"] = render(footer, values)
        values["content"] = render(body, values)

        dst = out_path(slug)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(render(base, values), encoding="utf-8")
        built.append((slug, dst))
        sitemap_entries.append((page_url(slug), last_modified(src)))
        if slug not in known:
            print(f"  note: {slug} is not in NAV, so no header tab links to it", file=sys.stderr)

    write_sitemap(sitemap_entries)
    write_robots()

    if not args.skip_index:
        run_data()

    print(f"build_site: {len(built)} pages + sitemap.xml + robots.txt", file=sys.stderr)
    for slug, dst in built:
        print(f"  {slug:<12} {dst.relative_to(ROOT).as_posix()}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
