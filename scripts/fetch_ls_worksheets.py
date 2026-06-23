#!/usr/bin/env python3
"""Download official LS worksheet/collateral images into public/assets/worksheets/."""

from __future__ import annotations

import argparse
import json
import re
import urllib.request
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
OUT_ROOT = ROOT / "public" / "assets" / "worksheets"
MANIFEST_PATH = OUT_ROOT / "manifest.json"
UA = {"User-Agent": "liberating.it-build/1.0 (+https://liberating.it)"}

# site slug -> (ls page path slug, list of (local_filename, source_filename_substring))
PRIORITY_ASSETS: dict[str, tuple[str, list[tuple[str, str]]]] = {
    "ecocycle-planning": (
        "ecocycle-planning",
        [("ecocycle-template.png", "Ecocycle+Template")],
    ),
    "panarchy": (
        "panarchy",
        [
            ("panarchy-worksheet.png", "Panarchy+Worksheet"),
            ("panarchy-example.png", "Panarchy+example"),
        ],
    ),
    "critical-uncertainties": (
        "critical-uncertainties",
        [
            ("critical-uncertainties-template.png", "CU+Template"),
            ("critical-uncertainties-example.png", "CU+Example"),
        ],
    ),
    "agreement-certainty-matrix": (
        "agreement-and-certainty",
        [
            ("agreement-certainty-template.png", "Agreement+Certainty+Template"),
            ("agreement-certainty-display.png", "Agreement+and+Certainty+Display"),
        ],
    ),
    "drawing-together": (
        "drawing-together",
        [("drawing-together-symbols.png", "DrawingTogetherSymbols")],
    ),
    "integrated-autonomy": (
        "integrated-autonomy",
        [("integrated-autonomy-template.png", "IA+Template")],
    ),
    "generative-relationship-star": (
        "generative-relationships-star",
        [("generative-star-template.png", "Gen+STAR+Template")],
    ),
    "purpose-to-practice-p2p": (
        "purpose-to-practice",
        [("purpose-to-practice-template.png", "P2P+Template")],
    ),
    "design-storyboards": (
        "design-storyboards",
        [
            ("design-storyboard-example.png", "Design+Storyboard+Example"),
            ("ls-selection-matchmaker-excerpt.png", "LS+Selection+Matchmaker+Excerpt"),
        ],
    ),
    "what-i-need-from-you-winfy": (
        "what-i-need-from-you",
        [
            ("winfy-room-layout.png", "WINFY+Room+Layout"),
            ("winfy-responses.png", "WINFY+Responses"),
        ],
    ),
    "social-network-webbing": (
        "social-network-webbing",
        [("social-network-webbing-example.png", "Social+Network+Web+in+Progress")],
    ),
    "spiral-journal": (
        "spiral-journal",
        [("spiral-journal-example.png", "Spiral+Journal+Example")],
    ),
}

OPTIONAL_ASSETS: dict[str, tuple[str, list[tuple[str, str]]]] = {
    "wicked-questions": ("wicked-questions", []),
    "min-specs": (
        "min-specs",
        [("min-specs-example.png", "Max+Specs+to+Min+Specs")],
    ),
}

SKIP_IMG = re.compile(r"(LS\+icon|Principle|Color\.png|ccheart|Screenshot|constellation)", re.I)


def fetch_html(slug: str) -> str:
    url = f"https://www.liberatingstructures.com/{slug}/"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as response:
        return response.read().decode("utf-8", errors="replace")


def page_images(html: str) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    seen: set[str] = set()
    for match in re.finditer(r'<img[^>]+>', html, re.I):
        tag = match.group(0)
        src_m = re.search(r'data-src="([^"]+)"', tag) or re.search(r'src="([^"]+)"', tag)
        if not src_m:
            continue
        src = src_m.group(1).split("?")[0]
        if src.startswith("//"):
            src = "https:" + src
        if src in seen:
            continue
        seen.add(src)
        fname = unquote(src.split("/")[-1])
        if SKIP_IMG.search(fname):
            continue
        alt_m = re.search(r'alt="([^"]*)"', tag)
        alt = alt_m.group(1).strip() if alt_m else ""
        found.append((fname, src))
    return found


def download(url: str, dest: Path) -> None:
    fetch_url = url if "format=" in url else f"{url}?format=2500w"
    req = urllib.request.Request(fetch_url, headers=UA)
    with urllib.request.urlopen(req, timeout=90) as response:
        dest.write_bytes(response.read())


def resolve_assets(site_slug: str, spec: tuple[str, list[tuple[str, str]]], html: str) -> list[dict]:
    images = page_images(html)
    ls_slug, wanted = spec
    resolved = []
    for local_name, needle in wanted:
        hit = next((src for fname, src in images if needle in fname), None)
        if not hit:
            raise SystemExit(f"Missing asset '{needle}' on {ls_slug} for {site_slug}")
        resolved.append(
            {
                "site_slug": site_slug,
                "ls_slug": ls_slug,
                "local": local_name,
                "source_url": hit,
                "rel_path": f"assets/worksheets/{site_slug}/{local_name}",
            }
        )
    return resolved


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch LS worksheet images")
    parser.add_argument("--optional", action="store_true", help="Also fetch optional assets")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    groups = dict(PRIORITY_ASSETS)
    if args.optional:
        groups.update(OPTIONAL_ASSETS)

    manifest: dict[str, list[dict]] = {}
    for site_slug, spec in groups.items():
        if not spec[1]:
            continue
        html = fetch_html(spec[0])
        items = resolve_assets(site_slug, spec, html)
        manifest[site_slug] = items
        for item in items:
            dest = ROOT / "public" / item["rel_path"]
            if args.dry_run:
                print(f"{item['rel_path']} <- {item['source_url']}")
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            download(item["source_url"], dest)
            print(f"saved {item['rel_path']}")

    if not args.dry_run:
        OUT_ROOT.mkdir(parents=True, exist_ok=True)
        MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"\nManifest: {MANIFEST_PATH.relative_to(ROOT)} ({sum(len(v) for v in manifest.values())} files)")


if __name__ == "__main__":
    main()
