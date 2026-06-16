#!/usr/bin/env python3
"""Refresh sitemap-enriched.json metadata from the static site build sources."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

import yaml

ROOT = Path(__file__).resolve().parents[1]
ENRICHED = ROOT / "sitemap-enriched.json"
CONTENT_V2 = ROOT / "content" / "v2"
SITEMAP = ROOT / "public" / "sitemap.xml"
SITE = "https://liberating.it"

sys.path.insert(0, str(ROOT / "public" / "scripts"))
from build import (  # noqa: E402
    HUBS_COMPLESSITA,
    HUBS_DIFFICOLTA,
    HUBS_DURATA,
    HUBS_FASE,
    PER_BISOGNO,
    parse_structure,
    resolve_editorial_path,
)


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    return yaml.safe_load(text.split("---", 2)[1]) or {}


def load_sitemap_urls(path: Path) -> list[str]:
    tree = ET.parse(path)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [node.text.strip() for node in tree.findall(".//sm:loc", ns) if node.text]


def taxonomy_term(taxonomy: str, slug: str, name: str) -> dict:
    return {
        "slug": slug,
        "name": name,
        "url": f"{SITE}/{taxonomy}/{slug}/",
    }


def structure_taxonomies(structure: dict) -> dict[str, list[dict]]:
    tax: dict[str, list[dict]] = {}
    if structure.get("complessita_slug"):
        tax["complessita"] = [
            taxonomy_term("complessita", structure["complessita_slug"], structure["complessita"])
        ]
    if structure.get("difficolta_slug"):
        tax["difficolta"] = [
            taxonomy_term("difficolta", structure["difficolta_slug"], structure["difficolta"])
        ]
    if structure.get("durata_slug"):
        durata_labels = {
            "breve": "Breve (max 45 min)",
            "media": "Media (max 90 min)",
            "workshop": "Workshop (oltre 90 min)",
            "variabile": "Durata variabile",
        }
        tax["durata"] = [
            taxonomy_term(
                "durata",
                structure["durata_slug"],
                durata_labels.get(structure["durata_slug"], structure["durata"]),
            )
        ]
    if structure.get("fase_slug"):
        tax["design-thinking"] = [
            taxonomy_term("design-thinking", structure["fase_slug"], structure["fase"])
        ]
    return tax


def build_structures_by_taxonomy(structures: list[dict]) -> dict:
    index: dict[str, dict[str, list[str]]] = {
        "complessita": {},
        "difficolta": {},
        "durata": {},
        "design-thinking": {},
    }
    for structure in structures:
        slug = structure["slug"]
        for taxonomy, slug_key in (
            ("complessita", "complessita_slug"),
            ("difficolta", "difficolta_slug"),
            ("durata", "durata_slug"),
            ("design-thinking", "fase_slug"),
        ):
            term = structure.get(slug_key)
            if term:
                index[taxonomy].setdefault(term, []).append(slug)
    for taxonomy in index:
        for term in index[taxonomy]:
            index[taxonomy][term] = sorted(index[taxonomy][term])
    return index


def editorial_pages(content_root: Path) -> list[dict]:
    pages = []
    for name, slug in (
        ("home.md", ""),
        ("10-principi-fondamentali-liberating-structures.md", "10-principi-fondamentali-liberating-structures"),
        ("privacy-policy.md", "privacy-policy"),
        ("termini-di-servizio.md", "termini-di-servizio"),
    ):
        path = resolve_editorial_path(content_root, name)
        meta = parse_frontmatter(path) if path else {}
        url = f"{SITE}/" if not slug else f"{SITE}/{slug}/"
        lastmod = (
            datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).date().isoformat()
            if path and path.is_file()
            else datetime.now(timezone.utc).date().isoformat()
        )
        pages.append(
            {
                "slug": slug or "home",
                "url": url,
                "lastmod": lastmod,
                "name": meta.get("title") or slug or "Home",
            }
        )
    return pages


def content_type_for_url(url: str) -> str:
    path = url.replace(SITE, "").strip("/")
    if not path:
        return "page"
    parts = path.split("/")
    if parts[0] == "structures" and len(parts) == 2:
        return "structure"
    if parts[0] in ("complessita", "difficolta", "durata", "design-thinking", "per-bisogno"):
        return "taxonomy"
    return "page"


def main() -> int:
    if not ENRICHED.is_file():
        print(f"Missing {ENRICHED}", file=sys.stderr)
        return 1
    if not SITEMAP.is_file():
        print(f"Missing {SITEMAP}. Run build first.", file=sys.stderr)
        return 1

    with ENRICHED.open(encoding="utf-8") as handle:
        data = json.load(handle)

    content_root = CONTENT_V2
    structures = [
        parse_structure(path)
        for path in sorted((content_root / "strutture").glob("*.md"))
    ]
    urls = load_sitemap_urls(SITEMAP)
    generated_at = datetime.now(timezone.utc).isoformat()

    old_structures = {
        item["slug"]: item for item in data.get("indexes", {}).get("structures", []) if item.get("slug")
    }
    refreshed_structures = []
    for structure in structures:
        slug = structure["slug"]
        merged = dict(old_structures.get(slug, {}))
        merged.update(
            {
                "slug": slug,
                "url": structure["url"],
                "lastmod": structure["source_lastmod"],
                "name": structure["h1"],
                "title": structure["title"],
                "meta_description": structure["meta_description"],
                "taxonomies": structure_taxonomies(structure),
            }
        )
        refreshed_structures.append(merged)

    data["source"] = {
        "sitemap": f"{SITE}/sitemap.xml",
        "site": SITE,
        "generator": "liberating.it static build",
        "generated_at": generated_at,
        "data_sources": [
            "public/sitemap.xml",
            "content/v2/strutture/*.md",
            "content/v1/pagine/*.md",
            "public/scripts/build.py hub definitions",
        ],
        "legal_content_note": "Testo vigente pagine legali: content/v1/pagine/.",
        "legacy_note": (
            "Campi informative_summary e metadata.content restano dallo snapshot WordPress "
            "per compatibilita' con scripts/generate_structure_drafts.py."
        ),
    }

    counts: dict[str, int] = {}
    for url in urls:
        ct = content_type_for_url(url)
        counts[ct] = counts.get(ct, 0) + 1

    data["statistics"] = {
        "sitemap_count": 1,
        "url_count": len(urls),
        "by_content_type": counts,
        "taxonomy_term_count": (
            len(HUBS_COMPLESSITA)
            + len(HUBS_DIFFICOLTA)
            + len(HUBS_DURATA)
            + len(HUBS_FASE)
            + len(PER_BISOGNO)
            + 1  # per-bisogno index
        ),
        "structure_count": len(structures),
    }

    indexes = data.setdefault("indexes", {})
    indexes["pages"] = editorial_pages(content_root)
    indexes["structures"] = sorted(refreshed_structures, key=lambda item: item.get("url") or "")
    indexes["structures_by_taxonomy"] = build_structures_by_taxonomy(structures)

    with ENRICHED.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    print(
        f"Updated {ENRICHED.name}: {len(urls)} URLs, "
        f"{len(refreshed_structures)} structures, generated_at={generated_at}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
