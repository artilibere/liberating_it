#!/usr/bin/env python3
"""Download Liberating Structures icons from liberatingstructures.com/ls-menu-1."""

from __future__ import annotations

import argparse
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MENU_URL = "https://www.liberatingstructures.com/ls-menu-1"
ICON_DIR = ROOT / "assets" / "images" / "structures"
MANIFEST_PATH = ICON_DIR / "manifest.json"

# liberating.it slug -> slug on liberatingstructures.com (ls-menu-1)
SITE_TO_LS_SLUG: dict[str, str | None] = {
    "1-2-4-all": "1-2-4-all",
    "impromptu-networking": "impromptu-networking",
    "w3-what-so-what-now-what": "what-so-what-now-what",
    "15-solutions": "15-percent-solutions",
    "troika-consulting": "troika-consulting",
    "appreciative-interviews-ai": "appreciative-interviews",
    "heard-seen-respected-hsr": "heard-seen-respected",
    "9-whys": "nine-whys",
    "agreement-certainty-matrix": "agreement-and-certainty",
    "what-i-need-from-you-winfy": "what-i-need-from-you",
    "discovery-action-dialogue-dad": "discovery-and-action-dialogue",
    "purpose-to-practice-p2p": "purpose-to-practice",
    "generative-relationship-star": "generative-relationships-star",
    "25-10-crowd-sourcing": "25-10-crowdsourcing",
    "mad-tea": "mad-tea-calm-tea",
    "shift-share": "shift-and-share",
    "integrated-autonomy": "integrated-autonomy",
    "improv-prototyping": "improv-prototyping",
    "user-experience-fishbowl": "user-experience-fishbowl",
    "wicked-questions": "wicked-questions",
    "spiral-journal": "spiral-journal",
    "helping-heuristics": "helping-heuristics",
    "talking-with-pixies": "talking-with-pixies",
    "drawing-together": "drawing-together",
    "social-network-webbing": "social-network-webbing",
    "simple-ethnography": "simple-ethnography",
    "critical-uncertainties": "critical-uncertainties",
    "celebrity-interview": "celebrity-interview",
    "ecocycle-planning": "ecocycle-planning",
    "min-specs": "min-specs",
    "conversation-cafe": "conversation-cafe",
    "wise-crowds": "wise-crowds",
    "design-storyboards": "design-storyboards",
    "panarchy": "panarchy",
    # Adattamenti / assenti dal menu ufficiale
    "4-2-1-storming": None,
    "mad-love": None,
    "triz": None,
    "open-space-technology-ost": None,
    "tiny-demons": None,
    "liquid-courage": None,
    "pixies-reflection": None,
}


def fetch_menu_html() -> str:
    request = urllib.request.Request(
        MENU_URL,
        headers={"User-Agent": "liberating.it-build/1.0 (+https://liberating.it)"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_menu_icons(html: str) -> dict[str, str]:
    pattern = re.compile(
        r'data-sqsp-image-block-link\s+href="(/[^"#?]+)"[\s\S]*?data-image="(https://images\.squarespace-cdn\.com/[^"]+\.png)"',
        re.I,
    )
    icons: dict[str, str] = {}
    for match in pattern.finditer(html):
        slug = match.group(1).strip("/")
        icons.setdefault(slug, match.group(2))
    return icons


def download_icon(url: str, dest: Path) -> None:
    fetch_url = url if "format=" in url else f"{url}?format=300w"
    request = urllib.request.Request(
        fetch_url,
        headers={"User-Agent": "liberating.it-build/1.0 (+https://liberating.it)"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        dest.write_bytes(response.read())


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch LS structure icons")
    parser.add_argument("--dry-run", action="store_true", help="Show mapping without downloading")
    args = parser.parse_args()

    html = fetch_menu_html()
    menu_icons = parse_menu_icons(html)
    ICON_DIR.mkdir(parents=True, exist_ok=True)

    manifest: dict[str, str] = {}
    missing: list[str] = []

    for site_slug, ls_slug in sorted(SITE_TO_LS_SLUG.items()):
        if not ls_slug:
            missing.append(site_slug)
            continue
        source_url = menu_icons.get(ls_slug)
        if not source_url:
            missing.append(site_slug)
            continue
        rel_path = f"assets/images/structures/{site_slug}.png"
        dest = ROOT / rel_path
        if args.dry_run:
            print(f"{site_slug} <- {ls_slug} ({source_url.split('/')[-1]})")
            manifest[site_slug] = rel_path
            continue
        download_icon(source_url, dest)
        manifest[site_slug] = rel_path
        print(f"saved {site_slug}")

    if not args.dry_run:
        existing: dict[str, str] = {}
        if MANIFEST_PATH.exists():
            existing = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        merged = {**existing, **manifest}
        MANIFEST_PATH.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        manifest = merged

    print(f"\nIcons: {len(manifest)} downloaded, {len(missing)} without official icon")
    if missing:
        print("No icon:", ", ".join(missing))


if __name__ == "__main__":
    main()
