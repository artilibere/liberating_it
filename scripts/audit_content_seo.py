#!/usr/bin/env python3
"""Audit SEO/GEO for content/v2 structure and editorial markdown files."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STRUCTURES = ROOT / "content" / "v2" / "strutture"
TITLE_MAX = 60
META_MAX = 155
FAQ_MIN = 3


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    return yaml.safe_load(parts[1]) or {}, parts[2]


def audit_structure(path: Path) -> list[str]:
    issues: list[str] = []
    meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
    slug = meta.get("slug", path.stem)
    title = meta.get("title", "")
    description = meta.get("meta_description", "")

    if len(title) > TITLE_MAX:
        issues.append(f"title {len(title)}>{TITLE_MAX}")
    if len(description) > META_MAX:
        issues.append(f"meta {len(description)}>{META_MAX}")
    if "faciltazioni" in path.read_text(encoding="utf-8"):
        issues.append("typo faciltazioni")
    if not re.search(r"^#\s+", body, re.M):
        issues.append("missing H1")
    faq_count = len(re.findall(r"^### ", body, re.M))
    if "## Domande frequenti" not in body:
        issues.append("missing FAQ section")
    elif faq_count < FAQ_MIN:
        issues.append(f"faq {faq_count}<{FAQ_MIN}")
    if "\u2014" in body or "\u2013" in body:
        issues.append("em dash in body")
    if "\u2019" in body or "\u201c" in body or "\u201d" in body:
        issues.append("curly quotes")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit content/v2 SEO quality")
    parser.add_argument("--structures", type=Path, default=DEFAULT_STRUCTURES)
    parser.add_argument("--strict", action="store_true", help="Exit 1 if any issue")
    args = parser.parse_args()

    if not args.structures.exists():
        print(f"Not found: {args.structures}", file=sys.stderr)
        return 1

    rows: list[tuple[str, list[str]]] = []
    for path in sorted(args.structures.glob("*.md")):
        issues = audit_structure(path)
        if issues:
            rows.append((path.stem, issues))

    total = len(list(args.structures.glob("*.md")))
    clean = total - len(rows)
    print(f"Audited {total} structures: {clean} ok, {len(rows)} with issues")
    for slug, issues in rows:
        print(f"  {slug}: {', '.join(issues)}")

    return 1 if args.strict and rows else 0


if __name__ == "__main__":
    raise SystemExit(main())
