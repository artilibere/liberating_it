#!/usr/bin/env python3
"""Generate enriched JSON from liberating.it sitemap with full metadata."""

from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html import unescape
from urllib.parse import urljoin, urlparse

BASE_URL = "https://liberating.it"
SITEMAP_INDEX = f"{BASE_URL}/sitemap_index.xml"
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
USER_AGENT = "liberating-sitemap-generator/2.0"

TAXONOMIES = ("complessita", "difficolta", "durata", "design-thinking")


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8", errors="replace")


def fetch_json(url: str):
    return json.loads(fetch(url))


def normalize_url(url: str) -> str:
    return url.rstrip("/") + "/"


def strip_html(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    return unescape(re.sub(r"\s+", " ", text)).strip()


def extract_headings(html: str) -> dict[str, list[str]]:
    headings: dict[str, list[str]] = {}
    for level in ("h1", "h2", "h3", "h4"):
        tags = re.findall(rf"<{level}[^>]*>(.*?)</{level}>", html, re.DOTALL | re.IGNORECASE)
        clean = [strip_html(tag) for tag in tags if strip_html(tag)]
        if clean:
            headings[level] = clean
    return headings


def extract_internal_links(html: str, base_url: str = BASE_URL) -> dict[str, list[dict]]:
    links: dict[str, list[dict]] = {
        "pages": [],
        "structures": [],
        "taxonomies": [],
        "external": [],
    }
    seen: set[tuple[str, str]] = set()

    for href, text in re.findall(r'href="([^"]+)"[^>]*>(.*?)</a>', html, re.DOTALL | re.IGNORECASE):
        href = unescape(href.strip())
        label = strip_html(text)
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue

        absolute = urljoin(base_url + "/", href)
        parsed = urlparse(absolute)
        if parsed.netloc and parsed.netloc not in ("liberating.it", "www.liberating.it"):
            key = ("external", absolute)
            if key not in seen:
                seen.add(key)
                links["external"].append({"url": absolute, "label": label or None})
            continue

        path = parsed.path.strip("/")
        parts = path.split("/") if path else []
        if not parts:
            bucket = "pages"
            item = {"url": normalize_url(absolute), "slug": "home", "label": label or None}
        elif parts[0] == "structures" and len(parts) >= 2:
            bucket = "structures"
            item = {"url": normalize_url(absolute), "slug": parts[1], "label": label or None}
        elif parts[0] in TAXONOMIES and len(parts) >= 2:
            bucket = "taxonomies"
            item = {
                "url": normalize_url(absolute),
                "taxonomy": parts[0],
                "term_slug": parts[1],
                "label": label or None,
            }
        else:
            bucket = "pages"
            item = {"url": normalize_url(absolute), "slug": parts[-1], "label": label or None}

        key = (bucket, item["url"])
        if key not in seen:
            seen.add(key)
            links[bucket].append(item)

    return links


def extract_images(html: str) -> list[dict]:
    images = []
    seen = set()
    for match in re.finditer(
        r'https://liberating\.it/wp-content/uploads/[^"\']+\.(?:jpg|jpeg|png|webp|gif)',
        html,
        re.IGNORECASE,
    ):
        url = match.group(0)
        if "favicon" in url.lower() or url in seen:
            continue
        seen.add(url)
        alt_match = re.search(rf'<img[^>]+src="{re.escape(url)}"[^>]*alt="([^"]*)"', html, re.IGNORECASE)
        images.append({"url": url, "alt": unescape(alt_match.group(1)) if alt_match else None})
    return images


def filter_body_classes(classes: list[str]) -> list[str]:
    keep = []
    for cls in classes:
        if any(
            token in cls
            for token in (
                "postid-",
                "single-",
                "type-",
                "status-",
                "page-template",
                "structures-template",
            )
        ):
            keep.append(cls)
    return keep or classes[:8]


def merge_reading_time(yoast: dict, fallback_yoast: dict | None) -> dict:
    if not yoast.get("twitter_misc") and fallback_yoast:
        misc = fallback_yoast.get("twitter_misc")
        if misc:
            yoast = {**yoast, "twitter_misc": misc}
    return yoast


def schema_graph_nodes(yoast: dict | None) -> list[dict]:
    if not yoast:
        return []
    schema = yoast.get("schema", {})
    graph = schema.get("@graph", []) if isinstance(schema, dict) else []
    return graph if isinstance(graph, list) else []


def extract_breadcrumbs(yoast: dict | None) -> list[dict]:
    for node in schema_graph_nodes(yoast):
        if node.get("@type") == "BreadcrumbList":
            return [
                {
                    "position": item.get("position"),
                    "name": item.get("name"),
                    "url": item.get("item"),
                }
                for item in node.get("itemListElement", [])
            ]
    return []


def extract_website_schema(yoast: dict | None) -> dict | None:
    for node in schema_graph_nodes(yoast):
        if node.get("@type") == "WebSite":
            return {
                "name": node.get("name"),
                "alternate_name": node.get("alternateName"),
                "description": node.get("description"),
                "url": node.get("url"),
                "in_language": node.get("inLanguage"),
            }
    return None


def parse_yoast(yoast: dict | None) -> dict:
    if not yoast:
        return {}

    graph = schema_graph_nodes(yoast)
    web_node = next((n for n in graph if n.get("@type") in ("WebPage", "CollectionPage")), {})

    og_image = yoast.get("og_image")
    if isinstance(og_image, list) and og_image:
        og_image = og_image[0].get("url") if isinstance(og_image[0], dict) else og_image[0]

    reading_time = None
    twitter_misc = yoast.get("twitter_misc") or {}
    if isinstance(twitter_misc, dict):
        reading_time = twitter_misc.get("Tempo di lettura stimato")

    return {
        "seo": {
            "title": yoast.get("title"),
            "description": yoast.get("description"),
            "canonical": yoast.get("canonical"),
            "robots": yoast.get("robots"),
            "reading_time": reading_time,
        },
        "open_graph": {
            "locale": yoast.get("og_locale"),
            "type": yoast.get("og_type"),
            "title": yoast.get("og_title"),
            "description": yoast.get("og_description"),
            "url": yoast.get("og_url"),
            "site_name": yoast.get("og_site_name"),
            "image": og_image,
            "article_modified_time": yoast.get("article_modified_time"),
        },
        "twitter": {
            "card": yoast.get("twitter_card"),
            "misc": twitter_misc,
        },
        "schema": {
            "type": web_node.get("@type"),
            "id": web_node.get("@id"),
            "name": web_node.get("name"),
            "description": web_node.get("description"),
            "date_published": web_node.get("datePublished"),
            "date_modified": web_node.get("dateModified"),
            "in_language": web_node.get("inLanguage"),
            "graph_nodes": [
                {
                    "type": node.get("@type"),
                    "id": node.get("@id"),
                    "name": node.get("name"),
                }
                for node in graph
            ],
        },
        "breadcrumbs": extract_breadcrumbs(yoast),
        "website": extract_website_schema(yoast),
    }


def fetch_yoast_head(page_url: str, cache: dict[str, dict]) -> dict:
    key = normalize_url(page_url)
    if key in cache:
        return cache[key]

    api_url = (
        f"{BASE_URL}/wp-json/yoast/v1/get_head?"
        f"url={urllib.parse.quote(key, safe='')}"
    )
    try:
        payload = fetch_json(api_url)
        yoast = payload.get("json") or {}
    except Exception as exc:  # noqa: BLE001
        yoast = {"_error": str(exc)}

    cache[key] = yoast
    return yoast


def parse_sitemap_index() -> list[dict]:
    root = ET.fromstring(fetch(SITEMAP_INDEX))
    sitemaps = []
    for sitemap in root.findall("sm:sitemap", NS):
        loc = sitemap.find("sm:loc", NS)
        lastmod = sitemap.find("sm:lastmod", NS)
        sitemaps.append(
            {
                "loc": loc.text.strip() if loc is not None else None,
                "lastmod": lastmod.text.strip() if lastmod is not None else None,
            }
        )
    return sitemaps


def parse_urlset(url: str) -> list[dict]:
    root = ET.fromstring(fetch(url))
    urls = []
    for entry in root.findall("sm:url", NS):
        loc = entry.find("sm:loc", NS)
        lastmod = entry.find("sm:lastmod", NS)
        urls.append(
            {
                "loc": loc.text.strip() if loc is not None else None,
                "lastmod": lastmod.text.strip() if lastmod is not None else None,
            }
        )
    return urls


def slug_from_url(url: str) -> str:
    path = urlparse(url).path.strip("/")
    return path.split("/")[-1] if path else ""


def classify_url(url: str, sitemap_file: str) -> dict:
    path = urlparse(url).path.strip("/")
    parts = path.split("/") if path else []

    if sitemap_file == "page-sitemap.xml":
        return {"content_type": "page", "slug": slug_from_url(url) or "home"}

    if sitemap_file == "structures-sitemap.xml":
        return {"content_type": "structure", "slug": parts[-1] if parts else ""}

    if sitemap_file.endswith("-sitemap.xml"):
        taxonomy = sitemap_file.replace("-sitemap.xml", "")
        return {
            "content_type": "taxonomy",
            "taxonomy": taxonomy,
            "term_slug": parts[-1] if parts else "",
        }

    return {"content_type": "unknown", "slug": slug_from_url(url)}


def load_pages_index() -> dict[str, dict]:
    pages = fetch_json(
        f"{BASE_URL}/wp-json/wp/v2/pages?per_page=100&context=view&_embed=author,wp:featuredmedia"
    )
    return {normalize_url(p["link"]): p for p in pages}


def load_taxonomy_indexes() -> dict[str, dict[str, dict]]:
    indexes: dict[str, dict[str, dict]] = {}
    for taxonomy in TAXONOMIES:
        terms = fetch_json(f"{BASE_URL}/wp-json/wp/v2/{taxonomy}?per_page=100")
        indexes[taxonomy] = {normalize_url(t["link"]): t for t in terms}
    return indexes


def term_lookup(taxonomy_indexes: dict, taxonomy: str, slug: str) -> dict | None:
    for term in taxonomy_indexes.get(taxonomy, {}).values():
        if term.get("slug") == slug:
            return term
    return None


def extract_taxonomy_refs(html: str, taxonomy_indexes: dict) -> dict[str, list[dict]]:
    refs: dict[str, list[dict]] = {}
    for taxonomy in TAXONOMIES:
        slugs = list(
            dict.fromkeys(
                re.findall(rf'href="https://liberating\.it/{taxonomy}/([^"/]+)/"', html)
            )
        )
        items = []
        for slug in slugs:
            term = term_lookup(taxonomy_indexes, taxonomy, slug)
            items.append(
                {
                    "slug": slug,
                    "name": term.get("name") if term else slug.replace("-", " ").title(),
                    "url": f"{BASE_URL}/{taxonomy}/{slug}/",
                    "term_id": term.get("id") if term else None,
                }
            )
        if items:
            refs[taxonomy] = items
    return refs


def extract_main_content(html: str) -> str:
    for pattern in (
        r'id="content"[^>]*>(.*?)(?:<footer\b|<div[^>]+fusion-footer)',
        r'class="[^"]*fusion-post-content[^"]*"[^>]*>(.*?)(?:<div class="fusion-meta-info|</article>)',
        r'<article[^>]*>(.*?)</article>',
    ):
        match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
        if match and len(match.group(1)) > 200:
            return match.group(1)
    return html


def extract_rich_meta_description(html: str) -> str:
    descriptions = [
        unescape(match.group(1))
        for match in re.finditer(r'<meta name="description" content="(.*?)"', html, re.DOTALL)
    ]
    if not descriptions:
        return ""
    return max(descriptions, key=len)


def extract_structure_attributes(html: str, slug: str) -> dict:
    attrs: dict = {}

    post_id_match = re.search(r"postid-(\d+)", html)
    if post_id_match:
        attrs["post_id"] = int(post_id_match.group(1))

    lang_match = re.search(r'<html[^>]*lang="([^"]+)"', html)
    if lang_match:
        attrs["language"] = lang_match.group(1)

    body_match = re.search(r'<body[^>]*class="([^"]+)"', html)
    if body_match:
        attrs["body_classes"] = filter_body_classes(body_match.group(1).split())

    rich_text = extract_rich_meta_description(html) or strip_html(html)

    difficulty_match = re.search(r"(Facile|Intermedia|Avanzata)\s*(★+☆*)", rich_text)
    if difficulty_match:
        attrs["difficulty"] = {
            "label": difficulty_match.group(1),
            "stars": difficulty_match.group(2),
        }

    duration_match = re.search(r"Durata[:\s]*(\d+\s*minuti)", rich_text, re.IGNORECASE)
    if duration_match:
        attrs["duration"] = duration_match.group(1).strip()

    participants_match = re.search(
        r"Numero di partecipanti[:\s]*(.+?)(?:Scopo principale|Situazioni ideali|$)",
        rich_text,
        re.IGNORECASE,
    )
    if participants_match:
        attrs["participants"] = participants_match.group(1).strip()

    purpose_match = re.search(
        rf"Scopo principale di {re.escape(slug)}(.+?)(?:Situazioni ideali|$)",
        rich_text,
        re.IGNORECASE,
    )
    if purpose_match:
        attrs["purpose"] = purpose_match.group(1).strip()

    return attrs


INFORMATIVE_TEMPLATE = [
    {
        "key": "come_funziona",
        "emoji": "🎯",
        "label": "Come funziona",
        "description": "Panoramica, metadati operativi e situazioni ideali d'uso.",
    },
    {
        "key": "domanda_generativa",
        "emoji": "🙋",
        "label": "Domanda generativa",
        "description": "Linee guida e esempi di domande per avviare la struttura.",
    },
    {
        "key": "preparazione",
        "emoji": "🏖️",
        "label": "Preparazione",
        "description": "Spazi, materiali e adattamenti (anche da remoto).",
    },
    {
        "key": "tempi_e_fasi",
        "emoji": "⏳",
        "label": "Tempi e fasi",
        "description": "Sequenza temporale delle fasi con durate.",
    },
    {
        "key": "consigli_pratici",
        "emoji": "💥",
        "label": "Consigli pratici ed errori da evitare",
        "description": "Best practice ed errori comuni da evitare.",
    },
]


def classify_section_title(title: str) -> str | None:
    if "🎯" in title or title.lower().startswith("come funziona"):
        return "come_funziona"
    if "🙋" in title or "domanda generativa" in title.lower():
        return "domanda_generativa"
    if "🏖️" in title or title.lower().startswith("preparazione"):
        return "preparazione"
    if "⏳" in title or "tempi e fasi" in title.lower():
        return "tempi_e_fasi"
    if "💥" in title or "consigli pratici" in title.lower():
        return "consigli_pratici"
    return None


def extract_list_items(html_chunk: str) -> list[str]:
    return [
        item
        for item in (strip_html(li) for li in re.findall(r"<li[^>]*>(.*?)</li>", html_chunk, re.DOTALL))
        if item
    ]


def split_sections_from_content(content_html: str) -> dict[str, dict]:
    headings: list[tuple[int, str, str | None]] = []
    seen_titles: set[str] = set()

    for match in re.finditer(r"<h[12][^>]*>(.*?)</h[12]>", content_html, re.DOTALL | re.IGNORECASE):
        title = strip_html(match.group(1))
        if not title or title in seen_titles:
            continue
        seen_titles.add(title)
        headings.append((match.start(), title, classify_section_title(title)))

    sections: dict[str, dict] = {}
    for index, (start, title, key) in enumerate(headings):
        if not key:
            continue
        end = headings[index + 1][0] if index + 1 < len(headings) else len(content_html)
        chunk = content_html[start:end]
        sections[key] = {
            "title": title,
            "html": chunk,
            "text": strip_html(chunk),
            "items": extract_list_items(chunk),
        }
    return sections


def parse_come_funziona_section(section: dict, slug: str, name: str) -> dict:
    text = section["text"]
    summary: dict = {}

    difficulty_match = re.search(r"(Facile|Intermedia|Avanzata)\s*(★+☆*)", text)
    if difficulty_match:
        summary["difficulty"] = {
            "label": difficulty_match.group(1),
            "stars": difficulty_match.group(2),
        }

    duration_match = re.search(r"Durata\s*:\s*(\d+\s*minuti)", text, re.IGNORECASE)
    if duration_match:
        summary["duration"] = duration_match.group(1).strip()

    participants_match = re.search(
        r"Numero di partecipanti\s*:\s*(.+?)\s*Scopo principale",
        text,
        re.IGNORECASE,
    )
    if participants_match:
        summary["participants"] = participants_match.group(1).strip()

    purpose_match = re.search(
        rf"Scopo principale(?: di {re.escape(slug)}| di {re.escape(name)})?\s*(.+?)\s*Situazioni ideali",
        text,
        re.IGNORECASE,
    )
    if not purpose_match:
        purpose_match = re.search(
            r"Scopo principale\s*(.+?)\s*Situazioni ideali",
            text,
            re.IGNORECASE,
        )
    if purpose_match:
        summary["purpose"] = purpose_match.group(1).strip()

    ideal_match = re.search(
        rf"Situazioni ideali(?: per {re.escape(slug)}| per {re.escape(name)})?\s*(.+)",
        text,
        re.IGNORECASE,
    )
    if ideal_match:
        intro = ideal_match.group(1).strip()
        summary["ideal_situations"] = {
            "intro": intro,
            "items": [item for item in section["items"] if item != summary.get("purpose")],
        }

    return summary


def parse_domanda_generativa_section(section: dict) -> dict:
    text = section["text"]
    questions = re.findall(r"[“\"']([^”\"']+\?)[”\"']", text)
    if not questions:
        questions = [item for item in section["items"] if "?" in item]

    themes = []
    if "lezioni concrete su:" in text.lower():
        themes = [
            item
            for item in section["items"]
            if item and "?" not in item and "esempi" not in item.lower()
        ]

    return {
        "themes": themes,
        "example_questions": questions,
        "items": section["items"],
    }


def parse_preparazione_section(section: dict) -> dict:
    items = section["items"]
    grouped = {
        "space_and_setup": [],
        "materials": [],
        "remote_adaptations": [],
        "other": [],
    }

    mode = "space_and_setup"
    for item in items:
        lower = item.lower()
        if "materiali necessari" in lower:
            mode = "materials"
            continue
        if "adattamenti" in lower and "remoto" in lower:
            mode = "remote_adaptations"
            continue
        grouped[mode].append(item)

    return {key: value for key, value in grouped.items() if value}


def parse_tempi_e_fasi_section(section: dict) -> dict:
    phases = []
    current_phase = None

    for item in section["items"]:
        phase_match = re.match(r"\[\s*(\d+\s*min(?:uti)?)\s*\]\s*(.+)", item, re.IGNORECASE)
        if phase_match:
            if current_phase:
                phases.append(current_phase)
            current_phase = {
                "duration": phase_match.group(1).strip(),
                "name": phase_match.group(2).strip(),
                "steps": [],
            }
            continue
        if current_phase:
            current_phase["steps"].append(item)

    if current_phase:
        phases.append(current_phase)

    total_match = re.search(r"(\d+)\s*min(?:uti)?(?:\s*totali)?", section["text"], re.IGNORECASE)
    return {
        "phases": phases,
        "total_duration": total_match.group(0) if total_match else None,
        "items": section["items"],
    }


def parse_consigli_pratici_section(section: dict) -> dict:
    best_practices = []
    errors_to_avoid = []
    mode = None

    for item in section["items"]:
        lower = item.lower()
        if "best practice" in lower:
            mode = "best"
            continue
        if "errori da evitare" in lower:
            mode = "errors"
            continue
        if mode == "best":
            best_practices.append(item)
        elif mode == "errors":
            errors_to_avoid.append(item)

    return {
        "best_practices": best_practices,
        "errors_to_avoid": errors_to_avoid,
        "items": section["items"],
    }


def extract_informative_structure(html: str, slug: str, name: str) -> dict:
    content_html = extract_main_content(html)
    raw_sections = split_sections_from_content(content_html)

    parsed_sections: dict[str, dict] = {}
    for template_part in INFORMATIVE_TEMPLATE:
        key = template_part["key"]
        section = raw_sections.get(key)
        if not section:
            parsed_sections[key] = {
                "present": False,
                "title": None,
                "html": None,
                "text": None,
                "items": [],
                "parsed": None,
            }
            continue

        parsed = None
        if key == "come_funziona":
            parsed = parse_come_funziona_section(section, slug, name)
        elif key == "domanda_generativa":
            parsed = parse_domanda_generativa_section(section)
        elif key == "preparazione":
            parsed = parse_preparazione_section(section)
        elif key == "tempi_e_fasi":
            parsed = parse_tempi_e_fasi_section(section)
        elif key == "consigli_pratici":
            parsed = parse_consigli_pratici_section(section)

        parsed_sections[key] = {
            "present": True,
            "title": section["title"],
            "html": section["html"],
            "text": section["text"],
            "items": section["items"],
            "parsed": parsed,
        }

    return {
        "template": INFORMATIVE_TEMPLATE,
        "section_order": [part["key"] for part in INFORMATIVE_TEMPLATE],
        "sections": parsed_sections,
        "sections_present": [key for key, sec in parsed_sections.items() if sec.get("present")],
        "sections_missing": [key for key, sec in parsed_sections.items() if not sec.get("present")],
    }


def page_metadata(page: dict, yoast: dict) -> dict:
    author = (page.get("_embedded") or {}).get("author", [{}])
    author_info = author[0] if author else {}
    featured = (page.get("_embedded") or {}).get("wp:featuredmedia", [])
    featured_info = None
    if featured and isinstance(featured, list) and featured[0]:
        media = featured[0]
        featured_info = {
            "id": media.get("id"),
            "url": media.get("source_url"),
            "alt_text": media.get("alt_text"),
            "mime_type": media.get("mime_type"),
            "width": (media.get("media_details") or {}).get("width"),
            "height": (media.get("media_details") or {}).get("height"),
        }

    content_html = (page.get("content") or {}).get("rendered", "")
    excerpt_html = (page.get("excerpt") or {}).get("rendered", "")

    return {
        "wordpress": {
            "id": page.get("id"),
            "slug": page.get("slug"),
            "status": page.get("status"),
            "type": page.get("type"),
            "template": page.get("template"),
            "parent": page.get("parent"),
            "menu_order": page.get("menu_order"),
            "comment_status": page.get("comment_status"),
            "ping_status": page.get("ping_status"),
            "class_list": page.get("class_list"),
            "date": page.get("date"),
            "date_gmt": page.get("date_gmt"),
            "modified": page.get("modified"),
            "modified_gmt": page.get("modified_gmt"),
            "guid": (page.get("guid") or {}).get("rendered"),
            "author": {
                "id": author_info.get("id"),
                "name": author_info.get("name"),
                "slug": author_info.get("slug"),
                "url": author_info.get("url"),
            },
            "featured_media": featured_info,
            "links": page.get("_links"),
        },
        "content": {
            "title": (page.get("title") or {}).get("rendered"),
            "excerpt_html": excerpt_html or None,
            "excerpt_text": strip_html(excerpt_html) or None,
            "content_html": content_html or None,
            "content_text": strip_html(content_html) or None,
            "word_count": len(strip_html(content_html).split()) if content_html else 0,
            "headings": extract_headings(content_html),
        },
        "links": extract_internal_links(content_html),
        "images": extract_images(content_html),
        **parse_yoast(yoast),
    }


def taxonomy_metadata(term: dict, yoast: dict) -> dict:
    description_html = term.get("description") or ""
    return {
        "wordpress": {
            "id": term.get("id"),
            "slug": term.get("slug"),
            "name": term.get("name"),
            "taxonomy": term.get("taxonomy"),
            "parent": term.get("parent"),
            "count": term.get("count"),
            "meta": term.get("meta"),
            "links": term.get("_links"),
        },
        "content": {
            "description_html": description_html or None,
            "description_text": strip_html(description_html) or None,
            "word_count": len(strip_html(description_html).split()) if description_html else 0,
            "headings": extract_headings(description_html),
        },
        "links": extract_internal_links(description_html),
        "images": extract_images(description_html),
        **parse_yoast(yoast),
    }


def structure_metadata(
    url: str,
    slug: str,
    html: str,
    yoast: dict,
    taxonomy_indexes: dict,
) -> dict:
    attrs = extract_structure_attributes(html, slug)
    post_id = attrs.pop("post_id", None)
    taxonomies = extract_taxonomy_refs(html, taxonomy_indexes)

    title = yoast.get("title") or slug
    name = title.split(" - ")[0].strip()

    content_html = extract_main_content(html)
    informative_structure = extract_informative_structure(html, slug, name)

    return {
        "wordpress": {
            "id": post_id,
            "slug": slug,
            "status": "publish",
            "type": "structures",
            "post_type": "structures",
            **attrs,
        },
        "content": {
            "title": name,
            "headings": extract_headings(content_html),
            "summary": extract_rich_meta_description(html) or None,
        },
        "informative_structure": informative_structure,
        "taxonomies": taxonomies,
        "structure_attributes": {
            "difficulty": attrs.get("difficulty"),
            "duration": attrs.get("duration"),
            "participants": attrs.get("participants"),
            "purpose": attrs.get("purpose"),
        },
        "links": extract_internal_links(content_html),
        "images": extract_images(content_html),
        **parse_yoast(yoast),
    }


def build_reverse_taxonomy_index(structure_entries: list[dict]) -> dict[str, dict[str, list[str]]]:
    reverse: dict[str, dict[str, list[str]]] = {tax: {} for tax in TAXONOMIES}
    for entry in structure_entries:
        slug = entry.get("slug")
        taxonomies = (entry.get("metadata") or {}).get("taxonomies") or {}
        for taxonomy, terms in taxonomies.items():
            for term in terms:
                term_slug = term.get("slug")
                if not term_slug or not slug:
                    continue
                reverse.setdefault(taxonomy, {}).setdefault(term_slug, [])
                if slug not in reverse[taxonomy][term_slug]:
                    reverse[taxonomy][term_slug].append(slug)
    return reverse


def build_structure_taxonomy_signatures(structure_entries: list[dict]) -> dict[str, set[str]]:
    signatures: dict[str, set[str]] = {}
    for entry in structure_entries:
        slug = entry.get("slug")
        if not slug:
            continue
        taxonomies = (entry.get("metadata") or {}).get("taxonomies") or {}
        keys = set()
        for taxonomy, terms in taxonomies.items():
            for term in terms:
                keys.add(f"{taxonomy}:{term.get('slug')}")
        signatures[slug] = keys
    return signatures


def structure_url(slug: str) -> str:
    return f"{BASE_URL}/structures/{slug}/"


def structure_ref(slug: str, structure_catalog: dict[str, dict] | None = None) -> dict:
    ref = {
        "slug": slug,
        "url": structure_url(slug),
    }
    if structure_catalog and slug in structure_catalog:
        ref["name"] = structure_catalog[slug].get("name")
        ref["lastmod"] = structure_catalog[slug].get("lastmod")
    return ref


def build_structure_catalog(structure_entries: list[dict]) -> dict[str, dict]:
    catalog: dict[str, dict] = {}
    for entry in structure_entries:
        slug = entry.get("slug")
        if not slug:
            continue
        metadata = entry.get("metadata") or {}
        informative = metadata.get("informative_structure") or {}
        catalog[slug] = {
            "slug": slug,
            "url": entry.get("loc") or structure_url(slug),
            "lastmod": entry.get("lastmod"),
            "name": (metadata.get("content") or {}).get("title") or slug,
            "post_id": (metadata.get("wordpress") or {}).get("id"),
            "taxonomies": metadata.get("taxonomies"),
            "informative_sections": informative.get("sections_present", []),
            "informative_summary": {
                key: section.get("parsed")
                for key, section in (informative.get("sections") or {}).items()
                if section.get("present") and section.get("parsed")
            },
        }
    return catalog


def build_page_index(page_entries: list[dict]) -> list[dict]:
    pages = []
    for entry in page_entries:
        metadata = entry.get("metadata") or {}
        pages.append(
            {
                "slug": entry.get("slug"),
                "url": entry.get("loc"),
                "lastmod": entry.get("lastmod"),
                "name": (metadata.get("content") or {}).get("title"),
                "post_id": (metadata.get("wordpress") or {}).get("id"),
            }
        )
    return sorted(pages, key=lambda item: item.get("url") or "")


def build_structures_by_taxonomy_index(
    reverse_taxonomy: dict[str, dict[str, list[str]]],
    structure_catalog: dict[str, dict],
) -> dict[str, dict[str, list[dict]]]:
    return {
        taxonomy: {
            term_slug: [structure_ref(slug, structure_catalog) for slug in sorted(slugs)]
            for term_slug, slugs in terms.items()
        }
        for taxonomy, terms in reverse_taxonomy.items()
    }


def related_by_shared_taxonomy(
    slug: str,
    signatures: dict[str, set[str]],
    limit: int = 10,
) -> list[dict]:
    own = signatures.get(slug, set())
    if not own:
        return []

    scored: list[tuple[int, str]] = []
    for other_slug, other_keys in signatures.items():
        if other_slug == slug:
            continue
        overlap = len(own & other_keys)
        if overlap:
            scored.append((overlap, other_slug))

    scored.sort(key=lambda item: (-item[0], item[1]))
    return [
        {
            "slug": other_slug,
            "url": f"{BASE_URL}/structures/{other_slug}/",
            "shared_taxonomies": overlap,
        }
        for overlap, other_slug in scored[:limit]
    ]


def main():
    generated_at = datetime.now(timezone.utc).isoformat()
    sitemap_index = parse_sitemap_index()

    pages_index = load_pages_index()
    taxonomy_indexes = load_taxonomy_indexes()
    yoast_cache: dict[str, dict] = {}
    html_cache: dict[str, str] = {}

    sitemaps = []
    all_urls = []

    for sm in sitemap_index:
        sitemap_url = sm["loc"]
        sitemap_file = sitemap_url.rsplit("/", 1)[-1]
        urls = parse_urlset(sitemap_url)

        enriched_urls = []
        for entry in urls:
            url = entry["loc"]
            classification = classify_url(url, sitemap_file)
            yoast_raw = fetch_yoast_head(url, yoast_cache)

            enriched = {**entry, **classification, "metadata": {}}
            content_type = classification["content_type"]

            if content_type == "page":
                page = pages_index.get(normalize_url(url))
                if page:
                    yoast_raw = merge_reading_time(yoast_raw, page.get("yoast_head_json"))
                    enriched["metadata"] = page_metadata(page, yoast_raw)

            elif content_type == "taxonomy":
                taxonomy = classification["taxonomy"]
                term = taxonomy_indexes.get(taxonomy, {}).get(normalize_url(url))
                if term:
                    yoast_raw = merge_reading_time(yoast_raw, term.get("yoast_head_json"))
                    enriched["metadata"] = taxonomy_metadata(term, yoast_raw)

            elif content_type == "structure":
                if url not in html_cache:
                    html_cache[url] = fetch(url)
                enriched["metadata"] = structure_metadata(
                    url,
                    classification["slug"],
                    html_cache[url],
                    yoast_raw,
                    taxonomy_indexes,
                )

            enriched_urls.append(enriched)
            all_urls.append(enriched)

        sitemaps.append(
            {
                "loc": sitemap_url,
                "lastmod": sm["lastmod"],
                "sitemap_file": sitemap_file,
                "url_count": len(enriched_urls),
                "urls": enriched_urls,
            }
        )

    structure_entries = [u for u in all_urls if u.get("content_type") == "structure"]
    reverse_taxonomy = build_reverse_taxonomy_index(structure_entries)
    structure_catalog = build_structure_catalog(structure_entries)
    taxonomy_signatures = build_structure_taxonomy_signatures(structure_entries)

    for entry in structure_entries:
        slug = entry.get("slug")
        if slug and entry.get("metadata"):
            entry["metadata"]["related_structures"] = related_by_shared_taxonomy(
                slug,
                taxonomy_signatures,
            )

    for entry in all_urls:
        if entry.get("content_type") != "taxonomy":
            continue
        taxonomy = entry.get("taxonomy")
        term_slug = entry.get("term_slug")
        structures = reverse_taxonomy.get(taxonomy, {}).get(term_slug, [])
        entry.setdefault("metadata", {})["structures"] = [
            structure_ref(slug, structure_catalog)
            for slug in sorted(structures)
        ]

    counts: dict[str, int] = {}
    for entry in all_urls:
        ct = entry.get("content_type", "unknown")
        counts[ct] = counts.get(ct, 0) + 1

    taxonomy_catalog = []
    for taxonomy, terms in taxonomy_indexes.items():
        for term in terms.values():
            term_slug = term.get("slug")
            structure_slugs = sorted(
                reverse_taxonomy.get(taxonomy, {}).get(term_slug, [])
            )
            taxonomy_catalog.append(
                {
                    "id": term.get("id"),
                    "taxonomy": taxonomy,
                    "slug": term_slug,
                    "name": term.get("name"),
                    "url": term.get("link"),
                    "count": term.get("count"),
                    "structures": [structure_ref(slug, structure_catalog) for slug in structure_slugs],
                }
            )

    structure_index = sorted(
        structure_catalog.values(),
        key=lambda item: item.get("url") or "",
    )
    page_index = build_page_index([u for u in all_urls if u.get("content_type") == "page"])
    structures_by_taxonomy = build_structures_by_taxonomy_index(
        reverse_taxonomy,
        structure_catalog,
    )

    output = {
        "$schema": "https://liberating.it/sitemap-enriched.schema.json",
        "source": {
            "sitemap_index": SITEMAP_INDEX,
            "site": BASE_URL,
            "generator": "Yoast SEO",
            "generated_at": generated_at,
            "data_sources": [
                "sitemap_index.xml",
                "child sitemaps (urlset)",
                "WordPress REST API (pages, taxonomies)",
                "Yoast SEO REST API (get_head)",
                "HTML parsing (structures CPT)",
            ],
        },
        "statistics": {
            "sitemap_count": len(sitemaps),
            "url_count": len(all_urls),
            "by_content_type": counts,
            "taxonomy_term_count": len(taxonomy_catalog),
            "structure_count": counts.get("structure", 0),
        },
        "indexes": {
            "informative_template": INFORMATIVE_TEMPLATE,
            "pages": page_index,
            "structures": structure_index,
            "taxonomies": taxonomy_catalog,
            "structures_by_taxonomy": structures_by_taxonomy,
        },
        "sitemaps": sitemaps,
    }

    out_path = "/var/www/liberating.it/sitemap-enriched.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Written {out_path} ({len(all_urls)} URLs, {len(taxonomy_catalog)} taxonomy terms)")


if __name__ == "__main__":
    main()
