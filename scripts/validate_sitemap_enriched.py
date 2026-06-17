#!/usr/bin/env python3
"""Validate sitemap-enriched.json against the static sitemap.xml."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENRICHED = ROOT / "sitemap-enriched.json"
DEFAULT_SITEMAP = ROOT / "public" / "sitemap.xml"


def count_sitemap_urls(path: Path) -> int:
    tree = ET.parse(path)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return len(tree.findall(".//sm:loc", ns))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate sitemap-enriched.json metadata")
    parser.add_argument("--enriched", type=Path, default=DEFAULT_ENRICHED)
    parser.add_argument("--sitemap", type=Path, default=DEFAULT_SITEMAP)
    args = parser.parse_args()

    issues: list[str] = []
    if not args.enriched.is_file():
        issues.append(f"missing enriched file: {args.enriched}")
    if not args.sitemap.is_file():
        issues.append(f"missing sitemap: {args.sitemap}")
    if issues:
        for item in issues:
            print(item, file=sys.stderr)
        return 1

    data = json.loads(args.enriched.read_text(encoding="utf-8"))
    stats = data.get("statistics", {})
    url_count = stats.get("url_count")
    structure_count = stats.get("structure_count")
    live_urls = count_sitemap_urls(args.sitemap)

    if url_count != live_urls:
        issues.append(f"url_count mismatch: enriched={url_count} sitemap={live_urls}")
    if structure_count != 41:
        issues.append(f"structure_count expected 41, got {structure_count}")
    generator = data.get("source", {}).get("generator", "")
    if "static" not in generator.lower():
        issues.append(f"source.generator not static: {generator!r}")

    if issues:
        for item in issues:
            print(item, file=sys.stderr)
        return 1

    print(
        f"OK: {url_count} URLs, {structure_count} structures, generator={generator}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
