#!/usr/bin/env python3
"""Generate structure markdown drafts from sitemap-enriched.json (v2: 3-zone layout)."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITEMAP = ROOT / "sitemap-enriched.json"
OUT_DIR = ROOT / "content" / "v2" / "strutture"
SKIP_SLUGS = {"1-2-4-all"}

PATH_ORDER = [
    "impromptu-networking",
    "1-2-4-all",
    "w3-what-so-what-now-what",
    "15-solutions",
    "troika-consulting",
]

PURPOSE_OVERRIDES: dict[str, str] = {
    "open-space-technology-ost": "Il gruppo si auto-organizza attorno a un tema, crea l'agenda e lavora in sessioni parallele. Tu tieni lo spazio, non dirigi i contenuti.",
    "troika-consulting": "Tre persone, tre ruoli: uno porta un problema, due consigliano ascoltando. Poi ruotate.",
    "1-2-4-all": "Fai emergere idee da tutti in quattro passaggi: da solo, in coppia, in quattro, in plenaria.",
    "celebrity-interview": "Trasforma una presentazione frontale in una conversazione guidata con il gruppo.",
    "ecocycle-planning": "Mappa le attivita' del team sul ciclo di vita e decide cosa tagliare o potenziare.",
    "critical-uncertainties": "Esplora scenari futuri partendo dalle incertezze che non puoi controllare.",
    "wicked-questions": "Formula domande che tengono insieme due obiettivi in tensione, senza forzare una scelta.",
}

# slug -> (before[(slug, reason)], after[(slug, reason)], similar[(slug, reason)], catalog_extra[(slug, reason)])
NAV: dict[str, tuple[list[tuple[str, str]], list[tuple[str, str]], list[tuple[str, str]], list[tuple[str, str]]]] = {
    "1-2-4-all": (
        [("impromptu-networking", "rompe il ghiaccio prima di raccogliere idee")],
        [("w3-what-so-what-now-what", "capire cosa fare delle idee emerse")],
        [("4-2-1-storming", "stessa difficolta', converge su un impegno"), ("25-10-crowd-sourcing", "prioritizza molte idee in poco tempo")],
        [("15-solutions", "passare dalle idee all'azione")],
    ),
    "impromptu-networking": (
        [],
        [("1-2-4-all", "approfondire i temi emersi dal networking")],
        [("conversation-cafe", "altro formato per far parlare tutti"), ("liquid-courage", "breve, rompe il ghiaccio")],
        [],
    ),
    "w3-what-so-what-now-what": (
        [("1-2-4-all", "raccogliere input prima di riflettere")],
        [("15-solutions", "tradurre le conclusioni in azioni")],
        [("heard-seen-respected-hsr", "debriefing empatico dopo un'esperienza")],
        [],
    ),
    "15-solutions": (
        [("1-2-4-all", "generare idee prima di scegliere cosa fare")],
        [("troika-consulting", "chiedere consiglio su come procedere")],
        [("min-specs", "definire regole minime per agire")],
        [],
    ),
    "troika-consulting": (
        [("15-solutions", "avere un'azione in mente da sottoporre")],
        [],
        [("helping-heuristics", "altro formato di consulenza tra pari"), ("wise-crowds", "feedback da piu' prospettive")],
        [],
    ),
    "9-whys": (
        [("wicked-questions", "esplorare tensioni prima di scavare in profondita'")],
        [("triz", "invertire il problema una volta trovata la causa")],
        [("min-specs", "stessa fase Define, regole minime"), ("discovery-action-dialogue-dad", "analisi problemi sul campo")],
        [],
    ),
    "critical-uncertainties": (
        [("agreement-certainty-matrix", "mappare certezze prima degli scenari")],
        [("design-storyboards", "progettare il workshop che segue")],
        [("open-space-technology-ost", "workshop lungo per strategia"), ("ecocycle-planning", "pianificazione organizzativa")],
        [],
    ),
    "open-space-technology-ost": (
        [("shift-share", "condividere output prima di un Open Space")],
        [("purpose-to-practice-p2p", "allineare scopo e pratica dopo")],
        [("social-network-webbing", "trasformazioni organizzative complesse")],
        [],
    ),
}

DEFAULT_BEFORE = [("1-2-4-all", "formato base per coinvolgere tutti")]
DEFAULT_AFTER = [("w3-what-so-what-now-what", "capire cosa fare dopo")]
DEFAULT_SIMILAR = [("impromptu-networking", "facile e veloce"), ("troika-consulting", "facile, lavoro in piccolo gruppo")]
DEFAULT_CATALOG = [("1-2-4-all", "la struttura piu' semplice per iniziare")]

DISPLAY_NAMES: dict[str, str] = {}


def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"[—–]", ", ", text)
    text = text.replace(""", '"').replace(""", '"').replace("'", "'")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def split_phase_name(name: str) -> tuple[str, str]:
    name = clean_text(name)
    if len(name) > 60 and " " in name[20:]:
        idx = name.find(" ", 15)
        if idx > 0:
            return name[:idx].strip(), name[idx:].strip()
    return name, ""


def rewrite_purpose(raw: str, title: str, slug: str = "") -> str:
    if slug in PURPOSE_OVERRIDES:
        return PURPOSE_OVERRIDES[slug]
    raw = clean_text(raw)
    if not raw:
        return "Formato pratico per far lavorare meglio il gruppo."
    first = raw.split(".")[0].strip().rstrip(".")
    first = re.sub(r"^(Scopo principale di [^:]+:?|L'[^ ]+ e' una potente struttura che permette di)\s*", "", first, flags=re.I)
    first = re.sub(r"^di Open Space Technology\s*", "", first, flags=re.I)
    if first and first[0].islower():
        first = first[0].upper() + first[1:]
    if first and not first.endswith("."):
        first += "."
    return first


def rewrite_situation(item: str) -> str:
    item = clean_text(item)
    if not item.endswith("."):
        item += "."
    return item[0].upper() + item[1:] if item else item


def filter_situations(items: list[str]) -> list[str]:
    out = []
    skip = ("risultat", "crea un legame", "facilita una comprensione", "trasforma una potenziale", "stimola l'azione", "fa emergere aspetti")
    for item in items:
        low = item.lower()
        if any(p in low for p in skip):
            continue
        if item.startswith(("Per ", "Dopo ", "Quando ")) or "quando" in low[:25]:
            out.append(item)
        elif len(out) < 3 and len(item) < 120:
            out.append(item)
    return out[:3]


def extract_questions(dg: dict) -> list[str]:
    qs = dg.get("example_questions", []) if isinstance(dg, dict) else []
    out = []
    for q in qs:
        q = clean_text(q).strip('"').strip("'")
        if q and len(q) > 10 and "?" in q:
            out.append(q)
    if not out and isinstance(dg, dict):
        for item in dg.get("items", []):
            item = clean_text(item)
            if "?" in item and len(item) > 15:
                out.append(item.strip('"').strip("'"))
    return out[:3]


def extract_prep(prep: dict) -> list[str]:
    items = prep.get("space_and_setup", []) if isinstance(prep, dict) else []
    out = []
    for item in items[:5]:
        item = clean_text(item)
        if item and len(item) > 5:
            out.append(item[0].upper() + item[1:] if item[0].islower() else item)
    if not out:
        out = ["Spazio per lavorare in coppie e in piccoli gruppi.", "Timer per rispettare i tempi.", "Domanda preparata in anticipo."]
    return out[:5]


def build_steps(tf: dict) -> list[tuple[str, str]]:
    steps: list[tuple[str, str]] = []
    for phase in tf.get("phases", []) or []:
        dur = clean_text(phase.get("duration", ""))
        name, detail = split_phase_name(phase.get("name", ""))
        label = f"{name}: {detail}" if detail and detail.lower() not in name.lower() else name
        steps.append((label, dur))
        for sub in phase.get("steps", []) or []:
            sub = clean_text(str(sub))
            if sub:
                steps.append((sub, ""))
    if not steps:
        for item in (tf.get("items") or [])[:8]:
            item = clean_text(str(item))
            m = re.match(r"\[\s*([^\]]+)\]\s*(.+)", item)
            if m:
                steps.append((m.group(2).strip(), m.group(1).strip()))
            elif item:
                steps.append((item, ""))
    normalized = []
    for label, dur in steps:
        label = label.strip()
        if label and label[0].islower():
            label = label[0].upper() + label[1:]
        normalized.append((label, dur))
    return normalized[:10]


def load_title_map(data: dict) -> dict[str, str]:
    titles = {}
    for sm in data.get("sitemaps", []):
        if sm.get("sitemap_file") != "structures-sitemap.xml":
            continue
        for url in sm.get("urls", []):
            slug = url.get("slug", "")
            title = url.get("metadata", {}).get("content", {}).get("title")
            if slug and title:
                titles[slug] = title
    return titles


def taxonomy_chips(tax: dict) -> str:
    parts = []
    mapping = [
        ("complessita", "Percorso"),
        ("difficolta", "Difficolta'"),
        ("durata", "Durata"),
        ("design-thinking", "Fase"),
    ]
    for key, _label in mapping:
        terms = tax.get(key, [])
        if terms:
            t = terms[0]
            parts.append(f"[{t['name']}]({t['url']})")
    return " · ".join(parts) if parts else "[Le strutture](/structures/)"


def path_nav(slug: str, in_path: bool) -> str:
    if not in_path or slug not in PATH_ORDER:
        return ""
    idx = PATH_ORDER.index(slug)
    lines = []
    if idx > 0:
        prev = PATH_ORDER[idx - 1]
        lines.append(f"← [{DISPLAY_NAMES.get(prev, prev)}](/structures/{prev}/)")
    if idx < len(PATH_ORDER) - 1:
        nxt = PATH_ORDER[idx + 1]
        lines.append(f"→ [{DISPLAY_NAMES.get(nxt, nxt)}](/structures/{nxt}/)")
    return " · ".join(lines)


def nav_for(slug: str) -> tuple[list[tuple[str, str]], list[tuple[str, str]], list[tuple[str, str]], list[tuple[str, str]]]:
    if slug in NAV:
        return NAV[slug]
    return DEFAULT_BEFORE, DEFAULT_AFTER, DEFAULT_SIMILAR, DEFAULT_CATALOG


def link_with_reason(slug: str, reason: str, prefix: str = "") -> str:
    name = DISPLAY_NAMES.get(slug, slug.replace("-", " ").title())
    p = f"{prefix} " if prefix else ""
    return f"- {p}[{name}](/structures/{slug}/) - {reason}"


def extract_structure(entry: dict, title_map: dict[str, str]) -> dict:
    slug = entry["slug"]
    summ = entry.get("informative_summary", {})
    cf = summ.get("come_funziona", {})
    tf = summ.get("tempi_e_fasi", {})
    consigli = summ.get("consigli_pratici", {})
    tax = entry.get("taxonomies", {})

    consigli_items = consigli.get("items", []) if isinstance(consigli, dict) else []
    consigli_text = ""
    errors = []
    for item in consigli_items:
        low = item.lower()
        if any(x in low for x in ("evita", "errore", "non ", "attenzione", "sbaglio")):
            errors.append(clean_text(item))
        elif not consigli_text and len(item) > 20:
            consigli_text = clean_text(item)

    compl_terms = tax.get("complessita", [])
    in_path = any(t.get("slug") == "iniziare-subito" for t in compl_terms)

    return {
        "slug": slug,
        "title": title_map.get(slug) or slug.replace("-", " ").title(),
        "url": entry.get("url", f"https://liberating.it/structures/{slug}/"),
        "purpose": cf.get("purpose", ""),
        "duration": cf.get("duration", "variabile"),
        "participants": cf.get("participants", "illimitato"),
        "difficulty": cf.get("difficulty", {}).get("label", "Intermedia"),
        "situations": filter_situations(cf.get("ideal_situations", {}).get("items", [])),
        "steps": build_steps(tf),
        "questions": extract_questions(summ.get("domanda_generativa", {})),
        "prep": extract_prep(summ.get("preparazione", {})),
        "consigli": consigli_text or "Adatta tempi e passaggi al tuo gruppo. Non serve perfezione, serve provare.",
        "errors": errors[:3] or [
            "Saltare i tempi: rispetta ogni fase, anche quella silenziosa.",
            "Parlare tu al posto del gruppo: lascia spazio alle persone.",
        ],
        "fase": (tax.get("design-thinking") or [{}])[0].get("name", ""),
        "complessita": (compl_terms or [{}])[0].get("name", ""),
        "tax": tax,
        "in_path": in_path,
    }


def build_meta_title(title: str) -> str:
    short = title.split("(")[0].strip()
    for c in (f"{short}: guida pratica", f"{short}: come usarla"):
        if len(c) <= 60:
            return c
    return short[:57] + "..."


def build_meta_desc(title: str, duration: str, slug: str = "") -> str:
    if slug in PURPOSE_OVERRIDES:
        base = PURPOSE_OVERRIDES[slug].split(".")[0]
        return f"{base}. Passaggi chiari in {duration}."[:155]
    short = title.split("(")[0].strip()
    return f"Come usare {short} in {duration}. Passaggi chiari per manager e facilitatori."[:155]


def render_markdown(s: dict) -> str:
    title = s["title"]
    slug = s["slug"]
    in_breve = rewrite_purpose(s["purpose"], title, slug)
    before, after, similar, catalog_extra = nav_for(slug)

    steps_md = []
    for i, (step, dur) in enumerate(s["steps"], 1):
        dur_part = f" - {dur}" if dur else ""
        steps_md.append(f"{i}. {step}{dur_part}")

    questions_md = "\n".join(f'- "{q}"' for q in s["questions"]) or '- "Qual e\' la sfida piu\' urgente su cui lavorare adesso?"'
    prep_md = "\n".join(f"- {p}" for p in s["prep"])

    before_md = "\n".join(link_with_reason(sl, r, "**Prima:**") for sl, r in before[:2])
    after_md = "\n".join(link_with_reason(sl, r, "**Dopo:**") for sl, r in after[:2])
    prima_dopo = "\n".join(x for x in [before_md, after_md] if x) or link_with_reason("1-2-4-all", "formato base per coinvolgere tutti", "**Prima:**")

    similar_md = "\n".join(link_with_reason(sl, r) for sl, r in similar[:3])
    catalog_md = " · ".join(
        ["[Esplora tutte le strutture](/structures/)"]
        + [f"[{DISPLAY_NAMES.get(sl, sl)}](/structures/{sl}/)" for sl, _ in catalog_extra[:2]]
    )

    path_line = path_nav(slug, s["in_path"])
    path_section = f"\n## Prossimo nel percorso\n\n{path_line}\n" if path_line else ""

    yaml_extra = ""
    if s.get("fase"):
        yaml_extra += f'fase: "{s["fase"]}"\n'
    if s.get("complessita"):
        yaml_extra += f'complessita: "{s["complessita"]}"\n'

    fase_cell = s["fase"] or "Multi fase"

    return f"""---
slug: {slug}
title: "{build_meta_title(title)}"
meta_description: "{build_meta_desc(title, s['duration'], slug)}"
registro: manuale-operativo
durata: "{s['duration']}"
difficolta: "{s['difficulty']}"
partecipanti: "{s['participants']}"
{yaml_extra}url: "{s['url']}"
---

# {title}

[Home](/) > [Le strutture](/structures/) > {title}

**In breve** - {in_breve}

| Durata | Difficolta' | Gruppo | Fase |
|--------|-------------|--------|------|
| {s['duration']} | {s['difficulty']} | {s['participants']} | {fase_cell} |

**Filtri:** {taxonomy_chips(s['tax'])}

## Domanda da portare

{questions_md}

## Cosa ti serve

{prep_md}

## I passaggi

{chr(10).join(steps_md)}

## Quando usarla

{chr(10).join('- ' + rewrite_situation(x) for x in s['situations']) or '- Quando la riunione ha bisogno di struttura e partecipazione attiva.'}

## Il consiglio del facilitatore

{s['consigli']}

## Errori da evitare

{chr(10).join('- ' + clean_text(e) for e in s['errors'])}

## Prima e dopo

{prima_dopo}

## Strutture simili

{similar_md}
{path_section}
## Torna al catalogo

{catalog_md}
"""


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Generate structure markdown drafts from sitemap-enriched.json")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files in content/v2/strutture/",
    )
    args = parser.parse_args()

    with open(SITEMAP, encoding="utf-8") as f:
        data = json.load(f)

    title_map = load_title_map(data)
    structures = data.get("indexes", {}).get("structures", [])

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for entry in structures:
        s = extract_structure(entry, title_map)
        DISPLAY_NAMES[s["slug"]] = s["title"]

    written = 0
    skipped = 0
    for entry in structures:
        slug = entry["slug"]
        if slug in SKIP_SLUGS:
            print(f"Skip {slug} (manual draft)")
            skipped += 1
            continue
        out_path = OUT_DIR / f"{slug}.md"
        if out_path.exists() and not args.force:
            print(f"Skip {slug} (exists; use --force to overwrite)")
            skipped += 1
            continue
        s = extract_structure(entry, title_map)
        md = render_markdown(s)
        out_path.write_text(md, encoding="utf-8")
        print(f"Wrote {out_path.name}")
        written += 1

    print(f"Done: {written} written, {skipped} skipped, {len(structures)} total")


if __name__ == "__main__":
    main()
