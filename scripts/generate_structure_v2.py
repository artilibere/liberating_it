#!/usr/bin/env python3
"""Generate v2 structure markdown in content/v2/strutture/ with FAQ, SEO and enriched content."""

from __future__ import annotations

import csv
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITEMAP = ROOT / "sitemap-enriched.json"
SINTESI = ROOT / ".cursor/skills/ls-content-specialist/strutture-sintesi.md"
SEO_DIR = ROOT / "seo"
OUT_DIR = ROOT / "content/v2/strutture"

PATH_ORDER = [
    "impromptu-networking",
    "1-2-4-all",
    "w3-what-so-what-now-what",
    "15-solutions",
    "troika-consulting",
]

# slug -> benefit for title (keyword: beneficio, max 60 char total)
TITLE_BENEFIT: dict[str, str] = {
    "1-2-4-all": "far parlare tutti in 15 minuti",
    "15-solutions": "agire subito senza permessi",
    "25-10-crowd-sourcing": "prioritizzare le idee del gruppo",
    "4-2-1-storming": "idee profonde in 10 minuti",
    "9-whys": "scoprire il vero scopo del team",
    "agreement-certainty-matrix": "scegliere il metodo giusto",
    "appreciative-interviews-ai": "costruire sulle storie di successo",
    "celebrity-interview": "interviste che coinvolgono tutti",
    "conversation-cafe": "dialoghi profondi senza dibattito",
    "critical-uncertainties": "pianificare scenari futuri",
    "design-storyboards": "progettare workshop efficaci",
    "discovery-action-dialogue-dad": "imparare sul campo insieme",
    "drawing-together": "pensare insieme disegnando",
    "ecocycle-planning": "decidere cosa tagliare o potenziare",
    "generative-relationship-star": "mappare le relazioni che contano",
    "heard-seen-respected-hsr": "debriefing empatico dopo un evento",
    "helping-heuristics": "imparare ad aiutarsi a vicenda",
    "impromptu-networking": "rompere il ghiaccio in 20 minuti",
    "improv-prototyping": "testare idee con improvvisazione",
    "integrated-autonomy": "autonomia e coordinamento insieme",
    "liquid-courage": "coraggio liquido per il cambiamento",
    "mad-love": "celebrare cio' che funziona",
    "mad-tea": "domande rapide a tutto il gruppo",
    "min-specs": "regole minime per agire",
    "open-space-technology-ost": "workshop auto-organizzati",
    "panarchy": "capire sistemi complessi a piu' livelli",
    "pixies-reflection": "riflettere con metafore visive",
    "purpose-to-practice-p2p": "allineare scopo e pratica",
    "shift-share": "condividere output in plenaria",
    "simple-ethnography": "osservare utenti sul campo",
    "social-network-webbing": "mappare reti e relazioni",
    "spiral-journal": "riflessione personale a spirale",
    "talking-with-pixies": "dialogo con prospettive immaginarie",
    "tiny-demons": "affrontare le resistenze nascoste",
    "troika-consulting": "consiglio tra pari in tre",
    "triz": "superare i compromessi nel team",
    "user-experience-fishbowl": "feedback UX in fishbowl",
    "w3-what-so-what-now-what": "capire cosa fare dopo",
    "what-i-need-from-you-winfy": "chiedere supporto con chiarezza",
    "wicked-questions": "tenere insieme obiettivi in tensione",
    "wise-crowds": "feedback da molte prospettive",
}

PURPOSE_OVERRIDES: dict[str, str] = {
    "open-space-technology-ost": "Il gruppo si auto-organizza attorno a un tema, crea l'agenda e lavora in sessioni parallele. Tu tieni lo spazio, non dirigi i contenuti.",
    "troika-consulting": "Tre persone, tre ruoli: uno porta un problema, due consigliano ascoltando. Poi ruotate.",
    "1-2-4-all": "1-2-4-All e' una struttura di facilitazione in quattro passaggi: riflessione individuale, scambio in coppia, discussione in gruppi da quattro, condivisione in plenaria. Fai emergere idee da tutti in 15 minuti.",
    "celebrity-interview": "Trasforma una presentazione frontale in una conversazione guidata con il gruppo.",
    "ecocycle-planning": "Mappa le attivita' del team sul ciclo di vita e decide cosa tagliare o potenziare.",
    "critical-uncertainties": "Esplora scenari futuri partendo dalle incertezze che non puoi controllare.",
    "wicked-questions": "Formula domande che tengono insieme due obiettivi in tensione, senza forzare una scelta.",
    "triz": "TRIZ (Teoria della Risoluzione Inventiva dei Problemi) inverte l'obiettivo: chiedi al gruppo come peggiorare la situazione. Da li' emergono le abitudini da interrompere.",
    "w3-what-so-what-now-what": "W³ (What, So What, Now What) guida il gruppo in tre domande: cosa e' successo, cosa significa, cosa fare adesso.",
    "15-solutions": "15% Solutions chiede a ognuno: cosa puoi fare subito con le risorse e l'autonomia che hai gia', senza chiedere permessi?",
    "impromptu-networking": "Impromptu Networking fa muovere le persone in coppie con domande brevi. Rompe il ghiaccio e crea connessioni in pochi minuti.",
    "9-whys": "9 Whys scava nel perche' profondo con domande a cascata. Aiuta a scoprire il vero scopo del lavoro del gruppo.",
    "drawing-together": "Drawing Together usa il disegno per far emergere idee che le parole non riescono a esprimere. Nessuna abilita' artistica richiesta.",
    "min-specs": "Min Specs definisce le regole minime indispensabili per agire. Tutto il resto e' libertà.",
    "social-network-webbing": "Social Network Webbing mappa le relazioni informali e le reti di influenza dentro e fuori l'organizzazione.",
}

CONSIGLIO_OVERRIDES: dict[str, str] = {
    "1-2-4-all": "Proteggi il silenzio del primo minuto. E' la fase piu' importante: chi di solito non parla in plenaria ha bisogno di quel tempo per pensare. Se qualcuno rompe il silenzio, riporta gentilmente l'attenzione alla domanda.",
    "triz": "Mantieni un tono leggero ma serio. L'obiettivo e' far emergere tabu' e abitudini nascoste, non ridicolizzare nessuno. Se qualcuno propone nuove iniziative, riportalo al tema: cosa smettere di fare?",
    "9-whys": "Non trasformarlo in un interrogatorio. Usa tono curioso, non giudicante. In Italia puo' aiutare chiarire che non cerchi colpevoli, ma chiarezza sul perche'.",
    "open-space-technology-ost": "La regola d'oro: chi viene e' la persona giusta, quello che succede e' l'unica cosa che poteva succedere, quando finisce finisce. Tu prepari lo spazio e poi ti metti da parte.",
    "impromptu-networking": "Dai un segnale chiaro per cambiare partner (campanello o countdown). In remoto usa breakout room con timer automatico.",
}

ERRORS_OVERRIDES: dict[str, list[str]] = {
    "1-2-4-all": [
        "Saltare la fase individuale e passare subito alla discussione di gruppo.",
        "Lasciare che in plenaria si creino due conversazioni parallele.",
        "Porre una domanda troppo generica (\"Cosa ne pensate?\") invece di una domanda operativa.",
    ],
    "triz": [
        "Accettare suggerimenti su nuove attivita' da avviare: TRIZ serve a identificare cosa smettere.",
        "Saltare il confronto tra comportamenti nefasti e pratiche attuali del team.",
        "Trattare l'esercizio come una battuta senza passare alle azioni concrete.",
    ],
}

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
        [("heard-seen-respected-hsr", "debriefing empatico dopo un'esperienza"), ("discovery-action-dialogue-dad", "analisi concreta sul campo")],
        [],
    ),
    "15-solutions": (
        [("1-2-4-all", "generare idee prima di scegliere cosa fare")],
        [("troika-consulting", "chiedere consiglio su come procedere")],
        [("min-specs", "definire regole minime per agire"), ("4-2-1-storming", "impegno personale concreto")],
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
    "triz": (
        [("9-whys", "aver chiarito il perche' profondo del problema")],
        [("15-solutions", "tradurre le abitudini da cambiare in azioni")],
        [("wicked-questions", "stessa fase Define, tensioni strategiche"), ("25-10-crowd-sourcing", "prioritizza le soluzioni emerse")],
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
        [("social-network-webbing", "trasformazioni organizzative complesse"), ("critical-uncertainties", "preparare scenari futuri")],
        [],
    ),
    "ecocycle-planning": (
        [("agreement-certainty-matrix", "capire la natura della sfida")],
        [("min-specs", "definire regole minime per il rinnovamento")],
        [("panarchy", "sistemi complessi a piu' livelli"), ("critical-uncertainties", "pianificazione strategica")],
        [],
    ),
    "drawing-together": (
        [("1-2-4-all", "raccogliere idee prima di disegnare")],
        [("improv-prototyping", "testare le metafore emerse")],
        [("design-storyboards", "visualizzare scenari"), ("spiral-journal", "riflessione visiva personale")],
        [],
    ),
    "wicked-questions": (
        [("1-2-4-all", "generare tensioni da esplorare")],
        [("9-whys", "scavare nel perche' delle tensioni")],
        [("critical-uncertainties", "incertezze strategiche"), ("triz", "invertire il problema")],
        [],
    ),
}

DEFAULT_BEFORE = [("1-2-4-all", "formato base per coinvolgere tutti")]
DEFAULT_AFTER = [("w3-what-so-what-now-what", "capire cosa fare dopo")]
DEFAULT_SIMILAR = [("impromptu-networking", "facile e veloce"), ("troika-consulting", "facile, lavoro in piccolo gruppo")]
DEFAULT_CATALOG = [("1-2-4-all", "la struttura piu' semplice per iniziare")]

H1_OVERRIDES: dict[str, str] = {
    "1-2-4-all": "1-2-4-All",
    "15-solutions": "15% Solutions",
    "25-10-crowd-sourcing": "25/10 Crowd Sourcing",
    "4-2-1-storming": "4-2-1-Storming",
    "9-whys": "9 Whys",
    "w3-what-so-what-now-what": "What, So What, Now What? (W³)",
    "what-i-need-from-you-winfy": "What I Need From You (WINFY)",
    "open-space-technology-ost": "Open Space Technology (OST)",
    "discovery-action-dialogue-dad": "Discovery & Action Dialogue (DAD)",
    "purpose-to-practice-p2p": "Purpose to Practice (P2P)",
    "appreciative-interviews-ai": "Appreciative Interviews (AI)",
    "agreement-certainty-matrix": "Agreement & Certainty Matrix",
    "heard-seen-respected-hsr": "Heard, Seen, Respected (HSR)",
    "generative-relationship-star": "Generative Relationship STAR",
    "user-experience-fishbowl": "User Experience Fishbowl",
}

STEPS_OVERRIDES: dict[str, list[tuple[str, str]]] = {
    "triz": [
        ("Presenta TRIZ: l'obiettivo e' ottenere il peggior risultato possibile, non il migliore", "5 min"),
        ("Identifica il risultato indesiderato principale rispetto al vostro obiettivo", "2 min"),
        ("Con 1-2-4-All, elenca i comportamenti che porterebbero al peggior risultato", "10 min"),
        ("Confronta la lista con le pratiche attuali del team: cosa assomiglia?", "10 min"),
        ("Definisci i primi passi concreti per interrompere le attivita' controproducenti", "10 min"),
    ],
}

WHEN_OVERRIDES: dict[str, list[str]] = {
    "triz": [
        "Il team e' bloccato su abitudini che non funzionano ma nessuno le nomina.",
        "Devi affrontare un tema tabu' senza creare conflitto frontale.",
        "Vuoi spazio per innovare tagliando cio' che ostacola, non aggiungendo progetti.",
    ],
}

DISPLAY_NAMES: dict[str, str] = {}
SINTESI_DATA: dict[str, dict] = {}


def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"[—–]", ", ", text)
    text = text.replace(""", '"').replace(""", '"').replace("'", "'")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_sintesi(path: Path) -> dict[str, dict]:
    text = path.read_text(encoding="utf-8")
    blocks = re.split(r"\n## ", text)
    data: dict[str, dict] = {}
    for block in blocks[1:]:
        slug_m = re.search(r"\*\*Slug:\*\* `([^`]+)`", block)
        if not slug_m:
            continue
        slug = slug_m.group(1)
        entry: dict = {"slug": slug}

        for field in ("Scopo", "Domanda esempio", "Nota mercato IT", "Hub Per bisogno"):
            m = re.search(rf"- \*\*{re.escape(field)}:\*\* (.+)", block)
            if m:
                entry[field.lower().replace(" ", "_")] = clean_text(m.group(1))

        quando = re.findall(r"(?:Quando usarla:\*\*\n(?:  - .+\n)+)", block)
        if quando:
            items = re.findall(r"  - (.+)", quando[0])
            entry["quando"] = [clean_text(i) for i in items[:3]]

        passaggi = re.findall(r"^\s+\d+\. .+", block, re.M)
        if passaggi:
            steps = []
            for p in passaggi:
                p = clean_text(p.lstrip())
                p = re.sub(r"^\d+\.\s*", "", p)
                m = re.search(r" - (\d+ min(?:uti)?|\d+/\d+ min|\[\s*[^\]]+\])$", p)
                if m:
                    steps.append((p[: m.start()].strip(), m.group(1).strip("[] ")))
                else:
                    steps.append((p, ""))
            entry["passaggi"] = steps[:8]

        string_m = re.search(r"\*\*String:\*\* (.+)", block)
        if string_m:
            entry["string_raw"] = string_m.group(1)

        data[slug] = entry
    return data


def slug_from_name(name: str) -> str | None:
    name = clean_text(name).lower()
    name = name.split("(")[0].strip()
    aliases = {
        "1-2-4-all": "1-2-4-all",
        "124 all": "1-2-4-all",
        "what, so what, now what?": "w3-what-so-what-now-what",
        "w³": "w3-what-so-what-now-what",
        "w3": "w3-what-so-what-now-what",
        "15% solutions": "15-solutions",
        "troika consulting": "troika-consulting",
        "wicked questions": "wicked-questions",
        "open space technology (ost)": "open-space-technology-ost",
        "open space technology": "open-space-technology-ost",
        "min specs": "min-specs",
        "conversation café": "conversation-cafe",
        "conversation cafe": "conversation-cafe",
        "agreement / certainty matrix": "agreement-certainty-matrix",
        "agreement certainty matrix": "agreement-certainty-matrix",
        "design storyboards": "design-storyboards",
        "discovery & action dialogue": "discovery-action-dialogue-dad",
        "what i need from you (winfy)": "what-i-need-from-you-winfy",
        "25/10 crowd sourcing": "25-10-crowd-sourcing",
        "4-2-1-storming": "4-2-1-storming",
        "9 whys": "9-whys",
        "heard, seen, respected (hsr)": "heard-seen-respected-hsr",
        "purpose to practice (p2p)": "purpose-to-practice-p2p",
        "appreciative interviews": "appreciative-interviews-ai",
    }
    if name in aliases:
        return aliases[name]
    for slug, title in DISPLAY_NAMES.items():
        if title.lower().startswith(name) or name in title.lower():
            return slug
    guess = name.replace(" ", "-").replace("/", "-")
    if guess in DISPLAY_NAMES:
        return guess
    return None


def parse_string_nav(raw: str) -> tuple[list[tuple[str, str]], list[tuple[str, str]], list[tuple[str, str]]]:
    before, after, similar = [], [], []
    for part in raw.split("|"):
        part = part.strip()
        for label, dest in (("Prima:", before), ("Dopo:", after), ("Simili:", similar)):
            if part.startswith(label):
                body = part[len(label) :].strip()
                m = re.match(r"(.+?)\s*\((.+)\)$", body)
                if m:
                    name, reason = m.group(1).strip(), m.group(2).strip()
                    sl = slug_from_name(name)
                    if sl:
                        dest.append((sl, reason))
    return before, after, similar


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
    sint = SINTESI_DATA.get(slug, {})
    if sint.get("scopo"):
        scopo = clean_text(sint["scopo"])
        scopo = re.sub(r"^Di [^ ]+ ", "", scopo)
        if scopo and scopo[0].islower():
            scopo = scopo[0].upper() + scopo[1:]
        return scopo
    raw = clean_text(raw)
    if not raw:
        return "Formato pratico per far lavorare meglio il gruppo."
    first = raw.split(".")[0].strip().rstrip(".")
    first = re.sub(r"^(Scopo principale di [^:]+:?|L'[^ ]+ e' una potente struttura che permette di)\s*", "", first, flags=re.I)
    if first and first[0].islower():
        first = first[0].upper() + first[1:]
    if first and not first.endswith("."):
        first += "."
    return first


def rewrite_situation(item: str) -> str:
    item = clean_text(item)
    low = item.lower()
    if low.startswith(("per ", "quando ", "dopo ", "durante ", "all'inizio", "il ", "la ", "lo ", "i ", "gli ", "le ", "deve", "vuoi", "devi")):
        return item[0].upper() + item[1:] if item else item
    if low.startswith(("creare ", "affrontare ", "identificare ", "risolvere ", "generare ")):
        return f"Devi {item[0].lower() + item[1:]}" if item else item
    return f"Quando {item[0].lower() + item[1:]}" if item else item


def filter_situations(items: list[str], slug: str) -> list[str]:
    if slug in WHEN_OVERRIDES:
        return WHEN_OVERRIDES[slug]
    sint = SINTESI_DATA.get(slug, {})
    if sint.get("quando"):
        return [rewrite_situation(x) for x in sint["quando"][:3]]
    out = []
    skip = ("risultat", "crea un legame", "facilita una comprensione", "trasforma una potenziale", "stimola l'azione")
    for item in items:
        low = item.lower()
        if any(p in low for p in skip):
            continue
        out.append(rewrite_situation(item))
        if len(out) >= 3:
            break
    return out or ["Quando la riunione ha bisogno di struttura e partecipazione attiva."]


def normalize_question(q: str) -> str:
    q = unicodedata.normalize("NFD", q)
    q = "".join(c for c in q if unicodedata.category(c) != "Mn")
    q = re.sub(r"[^\w\s?]", " ", q.lower())
    return re.sub(r"\s+", " ", q).strip()


def extract_questions(dg: dict, slug: str) -> list[str]:
    qs = dg.get("example_questions", []) if isinstance(dg, dict) else []
    out = []
    seen = set()
    sint = SINTESI_DATA.get(slug, {})
    if sint.get("domanda_esempio"):
        dom = sint["domanda_esempio"].strip('"')
        out.append(dom)
        seen.add(normalize_question(dom))
    for q in qs:
        q = clean_text(q).strip('"').strip("'")
        key = normalize_question(q)
        if q and len(q) > 10 and "?" in q and key not in seen:
            out.append(q)
            seen.add(key)
    return out[:3]


def extract_prep(prep: dict) -> list[str]:
    items = prep.get("space_and_setup", []) if isinstance(prep, dict) else []
    out = []
    for item in items[:5]:
        item = clean_text(item)
        if item and len(item) > 5:
            out.append(item[0].upper() + item[1:] if item[0].islower() else item)
    if not out:
        out = [
            "Spazio per lavorare in coppie e in piccoli gruppi.",
            "Timer per rispettare i tempi.",
            "Una domanda chiara, preparata prima della riunione.",
        ]
    return out[:5]


def build_steps(tf: dict, slug: str) -> list[tuple[str, str]]:
    if slug in STEPS_OVERRIDES:
        return STEPS_OVERRIDES[slug]
    sint = SINTESI_DATA.get(slug, {})
    if sint.get("passaggi"):
        cleaned = []
        for label, dur in sint["passaggi"]:
            label = re.sub(r"^[^:]+:\s*", "", label) if label.count(":") == 1 and len(label.split(":")[0]) < 25 else label
            label = re.sub(r"\s+\.", ".", label)
            cleaned.append((label.strip(), dur))
        return cleaned
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
        label = re.sub(r"\s+\.", ".", label)
        label = re.sub(r"\s{2,}", " ", label)
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


def taxonomy_url(url: str) -> str:
    if not url:
        return "/structures/"
    m = re.search(r"liberating\.it(/[^?#]+)", url)
    if m:
        return m.group(1).rstrip("/") + "/"
    if url.startswith("/"):
        return url if url.endswith("/") else url + "/"
    return url


def taxonomy_chips(tax: dict) -> str:
    parts = []
    for key in ("complessita", "difficolta", "durata", "design-thinking"):
        terms = tax.get(key, [])
        if terms:
            t = terms[0]
            parts.append(f"[{t['name']}]({taxonomy_url(t['url'])})")
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
    sint = SINTESI_DATA.get(slug, {})
    if sint.get("string_raw"):
        b, a, sim = parse_string_nav(sint["string_raw"])
        if b or a or sim:
            catalog = DEFAULT_CATALOG
            return b or DEFAULT_BEFORE, a or DEFAULT_AFTER, sim or DEFAULT_SIMILAR, catalog
    return DEFAULT_BEFORE, DEFAULT_AFTER, DEFAULT_SIMILAR, DEFAULT_CATALOG


def link_with_reason(slug: str, reason: str, prefix: str = "") -> str:
    name = DISPLAY_NAMES.get(slug, slug.replace("-", " ").title())
    p = f"{prefix} " if prefix else ""
    return f"- {p}[{name}](/structures/{slug}/) - {reason}"


def short_title(title: str) -> str:
    return title.split("(")[0].strip()


def build_meta_title(title: str, slug: str) -> str:
    st = H1_OVERRIDES.get(slug) or short_title(title)
    benefit = TITLE_BENEFIT.get(slug, "")
    if benefit:
        candidate = f"{st}: {benefit}"
        if len(candidate) <= 60:
            return candidate
    for c in (f"{st}: {benefit[:30]}", f"{st}: come usarla", st):
        if len(c) <= 60:
            return c
    return st[:57] + "..."


def build_meta_desc(slug: str, title: str, duration: str, in_breve: str) -> str:
    custom = {
        "1-2-4-all": "Fai emergere idee da tutti in quattro passaggi. Passaggi chiari in 15 minuti per manager e facilitatori.",
        "triz": "Inverti il problema con TRIZ: emergono le abitudini da interrompere. Passaggi chiari in 35 minuti.",
        "w3-what-so-what-now-what": "Debriefing in tre domande: cosa e' successo, cosa significa, cosa fare. Passaggi chiari in 30 minuti.",
        "open-space-technology-ost": "Workshop auto-organizzato: il gruppo crea l'agenda. Passaggi chiari per facilitatori.",
    }
    if slug in custom:
        return custom[slug][:155]
    if slug in PURPOSE_OVERRIDES:
        base = PURPOSE_OVERRIDES[slug].split(".")[0]
        desc = f"{base}. Passaggi chiari in {duration}."
    else:
        base = in_breve.split(".")[0]
        desc = f"{base}. Passaggi chiari in {duration} per manager e facilitatori."
    return desc[:155]


def load_seo_keywords(slug: str) -> list[str]:
    url_key = f"https___liberating.it_structures_{slug}__all_keywords.csv"
    path = SEO_DIR / url_key
    if not path.exists():
        return []
    keywords = []
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            kw = row.get("Keyword", "").strip()
            try:
                opp = float(row.get("Keyword Opportunity", 0) or 0)
            except ValueError:
                opp = 0
            if kw and opp >= 70:
                keywords.append(kw)
    return keywords[:4]


def build_faq(s: dict, in_breve: str) -> list[tuple[str, str]]:
    slug = s["slug"]
    title = short_title(s["title"])
    duration = s["duration"]
    steps = s["steps"]
    faqs: list[tuple[str, str]] = []

    faqs.append((
        f"Cos'e' {title}?",
        in_breve if in_breve.endswith(".") else in_breve + ".",
    ))

    if duration and duration != "variabile":
        step_summary = ""
        if steps:
            times = [d for _, d in steps if d]
            if times:
                step_summary = f" I passaggi prevedono tempi fissi ({', '.join(times[:4])})."
        faqs.append((
            f"Quanto dura {title}?",
            f"Di solito {duration}.{step_summary} Adatta i tempi al tuo gruppo, ma rispetta le transizioni.",
        ))

    when = s.get("situations") or []
    if when:
        faqs.append((
            f"Quando conviene usare {title}?",
            when[0] if when[0].endswith(".") else when[0] + ".",
        ))

    extra_map: dict[str, list[tuple[str, str]]] = {
        "1-2-4-all": [
            ("Cos'e' il metodo 1-2-4-All?", "1-2-4-All e' una struttura di facilitazione in quattro fasi: 1 minuto da solo, 2 in coppia, 4 in gruppo da quattro, 5 in plenaria. Serve a far emergere idee da tutti senza che dominino le voci piu' forti."),
            ("1-2-4-All funziona anche in remoto?", "Si. Usa breakout room per coppie e gruppi da quattro, e un documento condiviso per annotare. Il timer e' ancora piu' importante online, dove e' facile perdere i passaggi."),
        ],
        "triz": [
            ("Cos'e' TRIZ nelle Liberating Structures?", "TRIZ (Teoria della Risoluzione Inventiva dei Problemi) chiede al gruppo come ottenere il peggior risultato possibile. L'inversione fa emergere abitudini controproducenti da interrompere."),
            ("TRIZ e brainstorming: qual e' la differenza?", "Nel brainstorming cerchi idee nuove. In TRIZ elenchi prima comportamenti che peggiorerebbero la situazione, poi li confronti con cio' che il team fa gia'. Il focus e' smettere, non aggiungere."),
        ],
        "15-solutions": [
            ("Cosa sono le 15% Solutions?", "Sono azioni che ogni persona puo' fare subito con le risorse e l'autonomia che ha gia', senza chiedere permessi o budget aggiuntivo. Il nome indica la parte del problema che puoi influenzare direttamente."),
        ],
        "w3-what-so-what-now-what": [
            ("Cos'e' What So What Now What (W³)?", "W³ e' una struttura di debriefing in tre domande: What (cosa e' successo), So What (cosa significa per noi), Now What (cosa fare adesso). Evita di passare troppo presto all'azione senza capire."),
        ],
        "impromptu-networking": [
            ("Cos'e' Impromptu Networking?", "Impromptu Networking fa muovere le persone in coppie con domande brevi e rotazioni rapide. In 20 minuti crea connessioni e rompe il ghiaccio senza presentazioni formali."),
        ],
        "9-whys": [
            ("Cos'e' la tecnica dei 9 Whys?", "9 Whys e' una sequenza di domande \"perche' e' importante per te?\" a coppie. Scava oltre le risposte superficiali fino al vero scopo del lavoro del gruppo."),
        ],
        "open-space-technology-ost": [
            ("Cos'e' Open Space Technology?", "Open Space Technology e' un formato di workshop in cui i partecipanti creano l'agenda, scelgono i temi e si auto-organizzano in sessioni parallele. Il facilitatore prepara lo spazio e le regole, non i contenuti."),
        ],
        "ecocycle-planning": [
            ("Cos'e' Ecocycle Planning?", "Ecocycle Planning mappa le attivita' del team sulle fasi di un ciclo di vita (nascita, maturita', rigenerazione o morte). Aiuta a decidere cosa investire, cosa mantenere e cosa abbandonare."),
        ],
    }
    if slug in extra_map:
        for q, a in extra_map[slug]:
            if not any(q.lower() == x[0].lower() for x in faqs):
                faqs.append((q, a))

    return faqs[:4]


def render_faq(faqs: list[tuple[str, str]]) -> str:
    lines = ["## Domande frequenti", ""]
    for q, a in faqs:
        lines.append(f"### {q}")
        lines.append(a)
        lines.append("")
    return "\n".join(lines).rstrip()


def render_json_ld(faqs: list[tuple[str, str]]) -> str:
    entities = []
    for q, a in faqs:
        entities.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        })
    schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities}
    return (
        "\n<!--\n<script type=\"application/ld+json\">\n"
        + json.dumps(schema, ensure_ascii=False, indent=2)
        + "\n</script>\n-->"
    )


def extract_structure(entry: dict, title_map: dict[str, str]) -> dict:
    slug = entry["slug"]
    summ = entry.get("informative_summary", {})
    cf = summ.get("come_funziona", {})
    tf = summ.get("tempi_e_fasi", {})
    consigli = summ.get("consigli_pratici", {})
    tax = entry.get("taxonomies", {})

    consigli_items = consigli.get("items", []) if isinstance(consigli, dict) else []
    consigli_text = CONSIGLIO_OVERRIDES.get(slug, "")
    errors = ERRORS_OVERRIDES.get(slug, [])
    for item in consigli_items:
        low = item.lower()
        if any(x in low for x in ("evita", "errore", "non ", "attenzione", "sbaglio")):
            if len(errors) < 3:
                errors.append(clean_text(item))
        elif not consigli_text and len(item) > 20:
            consigli_text = clean_text(item)

    sint = SINTESI_DATA.get(slug, {})
    if not consigli_text:
        nota = sint.get("nota_mercato_it", "")
        if nota and "Applica regole generali" not in nota:
            consigli_text = nota
        else:
            consigli_text = "Adatta tempi e passaggi al tuo gruppo. Non serve perfezione, serve provare."

    compl_terms = tax.get("complessita", [])
    in_path = any(t.get("slug") == "iniziare-subito" for t in compl_terms)

    display = H1_OVERRIDES.get(slug) or title_map.get(slug) or slug.replace("-", " ").title()

    return {
        "slug": slug,
        "title": display,
        "url": entry.get("url", f"https://liberating.it/structures/{slug}/"),
        "purpose": cf.get("purpose", ""),
        "duration": cf.get("duration", "variabile"),
        "participants": cf.get("participants", "illimitato"),
        "difficulty": cf.get("difficulty", {}).get("label", "Intermedia"),
        "situations": filter_situations(cf.get("ideal_situations", {}).get("items", []), slug),
        "steps": build_steps(tf, slug),
        "questions": extract_questions(summ.get("domanda_generativa", {}), slug),
        "prep": extract_prep(summ.get("preparazione", {})),
        "consigli": consigli_text,
        "errors": errors[:3] or [
            "Saltare i tempi: rispetta ogni fase, anche quella silenziosa.",
            "Parlare tu al posto del gruppo: lascia spazio alle persone.",
            "Porre una domanda troppo generica invece di una domanda operativa.",
        ],
        "fase": (tax.get("design-thinking") or [{}])[0].get("name", ""),
        "complessita": (compl_terms or [{}])[0].get("name", ""),
        "tax": tax,
        "in_path": in_path,
        "hub_bisogno": sint.get("hub_per_bisogno", ""),
    }


def render_markdown(s: dict) -> str:
    title = s["title"]
    slug = s["slug"]
    in_breve = rewrite_purpose(s["purpose"], title, slug)
    before, after, similar, catalog_extra = nav_for(slug)

    steps_md = []
    for i, (step, dur) in enumerate(s["steps"], 1):
        dur_part = f" - {dur}" if dur else ""
        steps_md.append(f"{i}. {step}{dur_part}")

    questions = s["questions"]
    if len(questions) < 2:
        defaults = [
            "Qual e' la sfida piu' urgente su cui lavorare adesso?",
            "Cosa cambieresti se avessi piu' autonomia in questo tema?",
        ]
        for d in defaults:
            if len(questions) >= 3:
                break
            if d not in questions:
                questions.append(d)
    questions_md = "\n".join(f'- "{q}"' for q in questions[:3])
    prep_md = "\n".join(f"- {p}" for p in s["prep"])

    before_md = "\n".join(link_with_reason(sl, r, "**Prima:**") for sl, r in before[:2])
    after_md = "\n".join(link_with_reason(sl, r, "**Dopo:**") for sl, r in after[:2])
    prima_dopo_parts = [x for x in [before_md, after_md] if x]
    prima_dopo = "\n".join(prima_dopo_parts) if prima_dopo_parts else link_with_reason("1-2-4-all", "formato base per coinvolgere tutti", "**Prima:**")

    similar_md = "\n".join(link_with_reason(sl, r) for sl, r in similar[:3])
    catalog_links = ["[Esplora tutte le strutture](/structures/)"]
    for sl, reason in catalog_extra[:2]:
        name = DISPLAY_NAMES.get(sl, sl)
        catalog_links.append(f"[{name}](/structures/{sl}/) - {reason}")
    catalog_md = " · ".join(catalog_links)

    path_line = path_nav(slug, s["in_path"])
    path_section = f"\n## Prossimo nel percorso\n\n{path_line}\n" if path_line else ""

    faqs = build_faq(s, in_breve)
    faq_md = render_faq(faqs)
    json_ld = render_json_ld(faqs)

    yaml_extra = ""
    if s.get("fase"):
        yaml_extra += f'fase: "{s["fase"]}"\n'
    if s.get("complessita"):
        yaml_extra += f'complessita: "{s["complessita"]}"\n'

    fase_cell = s["fase"] or "Multi fase"
    meta_title = build_meta_title(title, slug)
    meta_desc = build_meta_desc(slug, title, s["duration"], in_breve)

    return f"""---
slug: {slug}
title: "{meta_title}"
meta_description: "{meta_desc}"
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

{chr(10).join('- ' + x for x in s['situations'])}

## Il consiglio del facilitatore

{s['consigli']}

## Errori da evitare

{chr(10).join('- ' + clean_text(e) for e in s['errors'])}

{faq_md}

## Prima e dopo

{prima_dopo}

## Strutture simili

{similar_md}
{path_section}
## Torna al catalogo

{catalog_md}
{json_ld}
"""


def main() -> None:
    import argparse

    global SINTESI_DATA
    parser = argparse.ArgumentParser(description="Generate v2 structure markdown with FAQ and SEO")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files in content/v2/strutture/",
    )
    args = parser.parse_args()

    SINTESI_DATA = parse_sintesi(SINTESI)

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

    print(f"Done: {written} written, {skipped} skipped -> {OUT_DIR}")


if __name__ == "__main__":
    main()
