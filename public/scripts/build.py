#!/usr/bin/env python3
"""Build static HTML site from liberating.it content/v2."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, pass_context, select_autoescape

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTENT = ROOT.parent / "content" / "v2"
OUT_ROOT = ROOT
TRACKING_CONFIG_PATH = ROOT / "tracking.json"
SITE_ORIGIN = "https://liberating.it"
ORGANIZATION_ID = f"{SITE_ORIGIN}/#organization"
WEBSITE_ID = f"{SITE_ORIGIN}/#website"

OFFICIAL_LS_COUNT = 33
LEGACY_STRUCTURE_COUNT = 35

LLMS_POPULAR_SLUGS = (
    "1-2-4-all",
    "impromptu-networking",
    "w3-what-so-what-now-what",
    "15-solutions",
    "troika-consulting",
)

LLMS_HIGH_TRAFFIC_SLUGS = (
    "drawing-together",
    "triz",
    "ecocycle-planning",
    "social-network-webbing",
    "open-space-technology-ost",
    "w3-what-so-what-now-what",
)

PER_BISOGNO_INDEX_META = (
    "Scegli la Liberating Structure giusta per il tuo obiettivo: idee, decisioni, "
    "analisi o strategia. Percorsi guidati in italiano."
)

PER_BISOGNO_INDEX_FAQ = [
    {
        "question": "Cos'e' il percorso Per bisogno?",
        "answer": (
            "Raggruppa le Liberating Structures per obiettivo concreto: generare idee, "
            "prendere decisioni, analizzare problemi o fare strategia. "
            "Ogni percorso elenca le strutture piu' adatte con passaggi e tempi."
        ),
    },
    {
        "question": "Come scelgo la struttura giusta per la mia riunione?",
        "answer": (
            "Parti dall'obiettivo: se devi far emergere idee usa Generare idee, "
            "se la riunione non conclude usa Prendere decisioni. "
            "Apri la scheda della struttura scelta per i passaggi pronti da usare."
        ),
    },
]

GENERATED_DIRS = (
    "structures",
    "complessita",
    "difficolta",
    "durata",
    "design-thinking",
    "per-bisogno",
    "10-principi-fondamentali-liberating-structures",
    "privacy-policy",
    "termini-di-servizio",
)
GENERATED_FILES = ("index.html",)

LEGAL_PAGES = ("privacy-policy", "termini-di-servizio")

CSS_BUNDLE_SOURCES = (
    "tokens.css",
    "base.css",
    "components.css",
)
CSS_BUNDLE_VIRTUAL = "css/site.css"
MANIFEST_NAME = "build-manifest.json"
JS_SOURCES = ("filters-panel.js", "nav.js", "filters.js", "scroll-spy.js", "share.js", "consent.js")
ICON_MANIFEST_PATH = "assets/images/structures/manifest.json"
ICON_THUMB_MAX_WIDTH = 160
ICON_THUMB_DIR = "assets/images/structures/thumbs"
OG_IMAGE_REL = "assets/images/og.png"
OG_IMAGE_WIDTH = 1200
OG_IMAGE_HEIGHT = 630
OG_DEFAULT_ALT = "Liberating.it — formati pratici per riunioni e workshop"
FAVICON_ICO = "favicon.ico"
FAVICON_PNG = "favicon-32x32.png"
FAVICON_APPLE = "apple-touch-icon.png"
FAVICON_SIZES = (16, 32, 48, 180)
ORGANIZATION_SAME_AS = ("https://www.linkedin.com/in/carlogandolfo/",)
READING_WPM = 200
TITLE_SUFFIX = " | Liberating.it"
TITLE_MAX_LEN = 60
META_MAX_LEN = 155


def format_page_title(title: str, suffix: str = TITLE_SUFFIX, max_len: int = TITLE_MAX_LEN) -> str:
    """Keep the document title within SERP-friendly length."""
    title = (title or "").strip()
    if not title:
        return "Liberating.it"[:max_len]
    full = f"{title}{suffix}"
    if len(full) <= max_len:
        return full
    budget = max_len - len(suffix)
    if budget < 8:
        return full[:max_len]
    if len(title) <= budget:
        return full
    trimmed = title[: budget - 1].rstrip(" -–—:|,")
    return f"{trimmed}…{suffix}"


def format_meta_description(text: str, max_len: int = META_MAX_LEN) -> str:
    """Keep meta description within SERP-friendly length after HTML escaping."""
    from html import escape

    text = (text or "").strip()
    if len(escape(text)) <= max_len:
        return text
    trimmed = text
    while len(trimmed) > 10:
        trimmed = trimmed[: len(trimmed) - 1].rstrip(" -–—:,.")
        candidate = f"{trimmed}…"
        if len(escape(candidate)) <= max_len:
            return candidate
    return trimmed


def hub_page_title(hub: dict) -> str:
    return format_page_title(hub.get("page_title") or hub["title"])


PATH_ORDER = [
    "impromptu-networking",
    "1-2-4-all",
    "w3-what-so-what-now-what",
    "15-solutions",
    "troika-consulting",
]

DISPLAY_NAMES: dict[str, str] = {}

COMPLESSITA_MAP = {
    "Per iniziare subito": "iniziare-subito",
    "Per team gia' rodati": "team-rodati",
    "Per team già rodati": "team-rodati",
    "Per facilitazioni complesse": "facilitazioni-complesse",
    "Per faciltazioni complesse": "facilitazioni-complesse",
    "Per trasformazioni organizzative": "trasformazioni-organizzative",
}

DIFFICOLTA_MAP = {
    "Facile": "facile",
    "Intermedia": "intermedia",
    "Avanzata": "avanzata",
}

FASE_MAP = {
    "Empathize": "empathize",
    "Define": "define",
    "Ideate": "ideate",
    "Prototype": "prototype",
    "Test": "test",
    "Multi fase": "multi-fase",
}

FASE_SLUG_LABELS_IT = {
    "empathize": "Empatizzare",
    "define": "Definire",
    "ideate": "Ideare",
    "prototype": "Prototipare",
    "test": "Testare",
    "multi-fase": "Multi fase",
}

FASE_FILTER_OPTIONS = tuple(FASE_SLUG_LABELS_IT.items())

LLMS_INCLUSION_SLUGS = (
    "1-2-4-all",
    "heard-seen-respected-hsr",
    "impromptu-networking",
    "conversation-cafe",
)

HUBS_COMPLESSITA = {
    "iniziare-subito": {
        "title": "Per iniziare subito",
        "page_title": "Liberating Structures per iniziare subito",
        "intro": "Strutture facili per provare le Liberating Structures senza esperienza precedente.",
        "meta_description": (
            "Percorso Liberating Structures per iniziare subito: Impromptu Networking, 1-2-4-All, "
            "W³, 15% Solutions e Troika. Passaggi pronti per la prima riunione."
        ),
        "filter": ("complessita", "iniziare-subito"),
        "path_list": True,
        "faq": [
            {
                "question": "Cosa sono le Liberating Structures?",
                "answer": (
                    "Sono formati di facilitazione con passaggi e tempi definiti per coinvolgere tutti "
                    "in riunioni e workshop. Il percorso Per iniziare subito raccoglie le cinque "
                    "piu' semplici da provare senza esperienza da facilitatore."
                ),
            },
            {
                "question": "Come iniziare con le Liberating Structures?",
                "answer": (
                    "Parti dal percorso guidato in cinque tappe: Impromptu Networking, 1-2-4-All, "
                    "What So What Now What?, 15% Solutions e Troika Consulting. "
                    "Ogni struttura ha passaggi e tempi pronti da usare."
                ),
            },
            {
                "question": "Serve esperienza da facilitatore?",
                "answer": (
                    "No. Le strutture di questo percorso sono pensate per chi prova per la prima volta. "
                    "Segui i passaggi indicati nella scheda e adatta i tempi al tuo gruppo."
                ),
            },
            {
                "question": "Quanto dura il percorso per iniziare subito?",
                "answer": (
                    "Le cinque strutture del percorso richiedono da 10 a 30 minuti ciascuna. "
                    "Puoi usarne una sola in una riunione o concatenarle in un workshop breve."
                ),
            },
        ],
    },
    "team-rodati": {
        "title": "Per team gia' rodati",
        "page_title": "Liberating Structures per team rodati",
        "intro": (
            "Liberating Structures per team gia' rodati: formati intermedi quando il gruppo "
            "conosce turni e plenaria e vuole andare piu' in profondita'."
        ),
        "meta_description": (
            "Liberating Structures per team rodati: 25/10 Crowd Sourcing, TRIZ, Drawing Together "
            "e Mad Tea per gruppi con esperienza di facilitazione partecipativa."
        ),
        "filter": ("complessita", "team-rodati"),
        "faq": [
            {
                "question": "Quando passare alle strutture per team rodati?",
                "answer": (
                    "Quando il gruppo ha gia' provato formati semplici come 1-2-4-All "
                    "e rispetta tempi e turni. Servono strutture con piu' passaggi o conversazioni piu' profonde."
                ),
            },
            {
                "question": "Cosa distingue queste strutture da quelle per iniziare?",
                "answer": (
                    "Richiedono piu' attenzione al timing e alla gestione del plenario. "
                    "Il facilitatore deve essere pronto a intervenire se il gruppo perde il filo."
                ),
            },
            {
                "question": "Quali strutture provare per un team rodato?",
                "answer": (
                    "25/10 Crowd Sourcing per prioritizzare idee in gruppi numerosi, "
                    "TRIZ per smettere abitudini controproducenti, Drawing Together "
                    "quando le parole non bastano. Ogni scheda ha passaggi e tempi pronti."
                ),
            },
            {
                "question": "Quanto tempo serve per le strutture da team rodato?",
                "answer": (
                    "La maggior parte richiede da 30 a 90 minuti. Mad Tea e Spiral Journal "
                    "partono da 15 minuti; Ecocycle Planning e workshop piu' lunghi arrivano a 2 ore."
                ),
            },
        ],
    },
    "facilitazioni-complesse": {
        "title": "Per facilitazioni complesse",
        "intro": (
            "Le Liberating Structures per facilitazioni complesse sono formati da 90 minuti a 4 ore "
            "per workshop articolati: molti stakeholder, tensioni da tenere insieme o prototipi da testare in scena."
        ),
        "meta_description": (
            "Liberating Structures per facilitazioni complesse: Wicked Questions, Improv Prototyping "
            "e altri formati multi-ora per situazioni articolate."
        ),
        "filter": ("complessita", "facilitazioni-complesse"),
        "faq": [
            {
                "question": "Quando serve una facilitazione complessa?",
                "answer": (
                    "Quando il tema e' articolato, ci sono molti stakeholder "
                    "o serve lavorare su piu' livelli in una sola sessione. "
                    "Prevedi almeno mezza giornata."
                ),
            },
            {
                "question": "Quanto tempo prevedere?",
                "answer": (
                    "La maggior parte delle strutture in questo elenco richiede da 90 minuti a 4 ore. "
                    "Controlla la durata nella scheda e lascia margine per pausa e debrief."
                ),
            },
            {
                "question": "Quali strutture provare per un workshop complesso?",
                "answer": (
                    "Wicked Questions per tensioni strategiche, Improv Prototyping per testare "
                    "comportamenti in scena, Conversation Cafe per dialoghi profondi su temi delicati. "
                    "Ogni scheda ha passaggi e tempi pronti."
                ),
            },
        ],
    },
    "trasformazioni-organizzative": {
        "title": "Per trasformazioni organizzative",
        "intro": "Strutture per cambiamenti profondi e workshop di piu' giorni.",
        "meta_description": (
            "Liberating Structures per trasformazioni organizzative: Open Space, Panarchy, "
            "P2P e altre per cambiamenti profondi."
        ),
        "filter": ("complessita", "trasformazioni-organizzative"),
        "faq": [
            {
                "question": "Per quali contesti servono le strutture per trasformazioni?",
                "answer": (
                    "Cambiamenti organizzativi, riorganizzazioni, nuove strategie "
                    "o workshop multi-giorno con molte persone. "
                    "Servono facilitatori esperti e sponsor interno."
                ),
            },
            {
                "question": "Open Space o Purpose to Practice?",
                "answer": (
                    "Open Space conviene quando non sai in anticipo quali temi emergeranno "
                    "e hai un gruppo numeroso. Purpose to Practice aiuta a tradurre "
                    "valori e scopo in pratiche quotidiane del team."
                ),
            },
        ],
    },
}

HUBS_DIFFICOLTA = {
    "facile": {
        "title": "Strutture facili",
        "page_title": "Liberating Structures facili",
        "intro": "Facili da condurre, ideali per iniziare.",
        "meta_description": (
            "Liberating Structures facili da condurre: 1-2-4-All, Impromptu Networking e altre. "
            "Ideali per la prima riunione o workshop."
        ),
        "faq": [
            {
                "question": "Quali Liberating Structures sono piu' facili da condurre?",
                "answer": (
                    "1-2-4-All, Impromptu Networking, What So What Now What? e 15% Solutions "
                    "sono tra le piu' semplici: pochi passaggi, tempi chiari, funzionano anche con chi non le conosce."
                ),
            },
            {
                "question": "Posso usarle alla prima riunione?",
                "answer": (
                    "Si. Scegli una struttura breve, spiega i passaggi e rispetta i tempi. "
                    "Il percorso Per iniziare subito ordina le cinque piu' adatte per chi parte da zero."
                ),
            },
        ],
    },
    "intermedia": {
        "title": "Strutture intermedie",
        "page_title": "Liberating Structures intermedie",
        "intro": "Richiedono un po' di pratica come facilitatore.",
        "meta_description": (
            "Liberating Structures di difficolta' intermedia: TRIZ, Ecocycle Planning, Wicked Questions. "
            "Passaggi, tempi e consigli pratici in italiano."
        ),
        "faq": [
            {
                "question": "Cosa sono le Liberating Structures intermedie?",
                "answer": (
                    "Sono formati di facilitazione con piu' passaggi delle versioni facili: "
                    "servono a generare idee, analizzare problemi o prendere decisioni "
                    "con gruppi gia' abituati a lavorare insieme."
                ),
            },
            {
                "question": "Quando usare Liberating Structures intermedie?",
                "answer": (
                    "Quando il team ha gia' provato formati semplici come 1-2-4-All e rispetta tempi e turni. "
                    "Servono per andare piu' in profondita' su idee, decisioni o analisi di problemi."
                ),
            },
            {
                "question": "Quale struttura intermedia usare per prima?",
                "answer": (
                    "TRIZ e What So What Now What? sono un buon punto di partenza: "
                    "la prima sblocca discussioni polarizzate, la seconda aiuta a capire cosa fare dopo una riunione."
                ),
            },
            {
                "question": "TRIZ ed Ecocycle Planning: qual e' la differenza?",
                "answer": (
                    "TRIZ serve a superare compromessi e abitudini controproducenti in 35 minuti. "
                    "Ecocycle Planning mappa attivita' e progetti sul ciclo di vita del team per decidere cosa potenziare o tagliare."
                ),
            },
        ],
    },
    "avanzata": {
        "title": "Strutture avanzate",
        "intro": "Per facilitatori esperti e contesti complessi.",
        "meta_description": (
            "Liberating Structures avanzate per facilitatori esperti e contesti complessi. "
            "Quando usarle e cosa ti serve."
        ),
        "faq": [
            {
                "question": "Quando usare strutture avanzate?",
                "answer": (
                    "Con gruppi grandi, temi sensibili o workshop multi-giorno "
                    "dove serve tenere insieme molte conversazioni parallele. "
                    "Non sono il primo passo se il team e' alle prime armi."
                ),
            },
            {
                "question": "Cosa serve per facilitare strutture avanzate?",
                "answer": (
                    "Esperienza con formati intermedi, capacita' di gestire tempi lunghi "
                    "e un piano B se il gruppo si blocca. "
                    "Leggi la scheda completa prima della sessione."
                ),
            },
        ],
    },
}

HUBS_DURATA = {
    "breve": {
        "title": "Breve (max 45 min)",
        "intro": "Strutture rapide da inserire in una riunione.",
        "meta_description": (
            "Liberating Structures brevi (max 45 minuti): formati rapidi da inserire "
            "in una riunione senza stravolgere l'agenda."
        ),
        "faq": [
            {
                "question": "Quali Liberating Structures durano meno di 45 minuti?",
                "answer": (
                    "1-2-4-All (15 min), Impromptu Networking (20 min), 15% Solutions (10 min) "
                    "e altre in questo elenco. "
                    "Controlla sempre la durata indicata nella scheda."
                ),
            },
            {
                "question": "Come inserirle in una riunione gia' piena?",
                "answer": (
                    "Annuncia la struttura all'inizio, rispetta i tempi al minuto "
                    "e chiudi con un passaggio concreto (es. una decisione o un prossimo passo). "
                    "Meglio una struttura breve fatta bene che una lunga tagliata."
                ),
            },
        ],
    },
    "media": {
        "title": "Media (max 90 min)",
        "intro": "Sessioni fino a un'ora e mezza.",
        "meta_description": (
            "Liberating Structures di durata media (fino a 90 minuti): sessioni strutturate "
            "per workshop e riunioni di mezza giornata."
        ),
        "faq": [
            {
                "question": "Quando serve una sessione di durata media?",
                "answer": (
                    "Quando devi andare piu' in profondita' di un icebreaker "
                    "ma non hai mezza giornata. "
                    "Ideale per riunioni di team o workshop con un obiettivo chiaro."
                ),
            },
            {
                "question": "Differenza tra struttura breve e media?",
                "answer": (
                    "Le brevi entrano in un'agenda gia' piena. "
                    "Le medie richiedono un blocco dedicato e spesso includono "
                    "piu' passaggi o un debrief piu' lungo."
                ),
            },
        ],
    },
    "estesa": {
        "title": "Estesa (max 4 h)",
        "intro": "Half-day o sessioni lunghe.",
        "meta_description": (
            "Liberating Structures estese (fino a 4 ore): formati per half-day "
            "e sessioni di lavoro lunghe."
        ),
        "faq": [
            {
                "question": "Quali strutture richiedono mezza giornata?",
                "answer": (
                    "Ecocycle Planning, Open Space parziale, Conversation Cafe esteso "
                    "e altre in questo catalogo durano fino a 4 ore. "
                    "Pianifica pause e materiali in anticipo."
                ),
            },
            {
                "question": "Come combinarle in un half-day?",
                "answer": (
                    "Apri con una struttura breve per scaldare il gruppo, "
                    "poi la struttura estesa principale, chiudi con What So What Now What? "
                    "o 15% Solutions per i prossimi passi."
                ),
            },
        ],
    },
    "workshop": {
        "title": "Workshop (+1g)",
        "intro": "Formati per workshop e eventi multi-giorno.",
        "meta_description": (
            "Liberating Structures per workshop multi-giorno: Open Space, Ecocycle "
            "e altri formati per eventi lunghi."
        ),
        "faq": [
            {
                "question": "Quali Liberating Structures servono per workshop multi-giorno?",
                "answer": (
                    "Open Space Technology, Panarchy, Purpose to Practice "
                    "e altre in questo elenco sono pensate per eventi lunghi "
                    "con decine o centinaia di partecipanti."
                ),
            },
            {
                "question": "Open Space Technology: quando conviene?",
                "answer": (
                    "Quando hai un tema ampio, partecipanti motivati "
                    "e almeno mezza giornata. "
                    "Il gruppo crea l'agenda sul momento attorno a domande che contano."
                ),
            },
        ],
    },
}

HUBS_FASE = {
    "empathize": {
        "title": "Empatizzare",
        "intro": "Strutture per la fase di empatia nel design thinking.",
        "meta_description": (
            "Liberating Structures per empatizzare nel design thinking: "
            "ascolto, osservazione e comprensione degli utenti."
        ),
        "faq": [
            {
                "question": "Come empatizzare con le Liberating Structures?",
                "answer": (
                    "Usa strutture che danno voce a chi vive il problema: "
                    "Appreciative Interviews, Heard Seen Respected, Simple Ethnography. "
                    "L'obiettivo e' capire bisogni prima di proporre soluzioni."
                ),
            },
            {
                "question": "Quali strutture per ascoltare utenti e stakeholder?",
                "answer": (
                    "User Experience Fishbowl mette al centro chi ha vissuto il servizio. "
                    "Conversation Cafe crea spazio per storie condivise. "
                    "Scegli in base a quante persone coinvolgi."
                ),
            },
        ],
    },
    "define": {
        "title": "Definire",
        "intro": "Strutture per definire il problema.",
        "meta_description": (
            "Liberating Structures per definire il problema: TRIZ, 9 Whys, Wicked Questions "
            "e altre per trovare il problema giusto."
        ),
        "faq": [
            {
                "question": "Come definire il problema giusto prima di ideare?",
                "answer": (
                    "9 Whys scava nelle cause profonde in 20 minuti. "
                    "Wicked Questions mette in tensione due verita' che sembrano opposte. "
                    "Evita di saltare alla soluzione troppo presto."
                ),
            },
            {
                "question": "TRIZ o 9 Whys per definire il problema?",
                "answer": (
                    "9 Whys quando devi capire perche' succede qualcosa. "
                    "TRIZ quando il gruppo e' gia' polarizzato su due posizioni "
                    "e devi trovare una terza via."
                ),
            },
        ],
    },
    "ideate": {
        "title": "Ideare",
        "intro": "Strutture per generare idee.",
        "meta_description": (
            "Liberating Structures per ideare: 1-2-4-All, 25/10 e altre "
            "per generare idee in team."
        ),
        "faq": [
            {
                "question": "Quali Liberating Structures usare in fase di ideazione?",
                "answer": (
                    "1-2-4-All per far emergere idee da tutti, "
                    "25/10 Crowd Sourcing per prioritizzare molte proposte, "
                    "Drawing Together quando le idee passano dal disegno."
                ),
            },
            {
                "question": "1-2-4-All basta per ideare?",
                "answer": (
                    "Spesso si, soprattutto in 15 minuti. "
                    "Se emergono troppe idee simili, aggiungi 25/10 per votare. "
                    "Se il gruppo e' bloccato, passa a TRIZ."
                ),
            },
        ],
    },
    "prototype": {
        "title": "Prototipare",
        "intro": "Strutture per prototipare soluzioni.",
        "meta_description": (
            "Liberating Structures per prototipare: Improv Prototyping, "
            "Drawing Together e altre per testare soluzioni."
        ),
        "faq": [
            {
                "question": "Come prototipare con le Liberating Structures?",
                "answer": (
                    "Improv Prototyping fa recitare scenari in pochi minuti. "
                    "Drawing Together produce metafore visive condivise. "
                    "Entrambe rendono tangibile un'idea senza slide."
                ),
            },
            {
                "question": "Drawing Together o Improv Prototyping?",
                "answer": (
                    "Drawing Together se il gruppo e' a suo agio con carta e pennarelli. "
                    "Improv Prototyping se vuoi testare comportamenti e interazioni "
                    "in modo teatrale e leggero."
                ),
            },
        ],
    },
    "test": {
        "title": "Testare",
        "intro": "Strutture per testare e validare.",
        "meta_description": (
            "Liberating Structures per testare: formati per validare ipotesi "
            "e raccogliere feedback dal gruppo."
        ),
        "faq": [
            {
                "question": "Come testare ipotesi con un gruppo?",
                "answer": (
                    "What So What Now What? aiuta a capire cosa e' emerso da un test "
                    "e cosa fare dopo. "
                    "Troika Consulting raccoglie feedback da consulenti pari in tempi brevi."
                ),
            },
            {
                "question": "Strutture per raccogliere feedback onesto?",
                "answer": (
                    "Troika Consulting crea turni strutturati di consulenza tra pari. "
                    "WINFY chiede esplicitamente cosa serve da ogni persona per andare avanti."
                ),
            },
        ],
    },
    "multi-fase": {
        "title": "Multi fase",
        "intro": "Strutture utilizzabili in piu' fasi.",
        "meta_description": (
            "Liberating Structures multi-fase: formati utilizzabili in piu' fasi "
            "del design thinking o di un percorso di lavoro."
        ),
        "faq": [
            {
                "question": "Cosa significa multi-fase?",
                "answer": (
                    "Sono strutture flessibili: le puoi usare per empatizzare, ideare "
                    "o decidere a seconda del contesto. "
                    "What So What Now What? e Conversation Cafe sono esempi tipici."
                ),
            },
            {
                "question": "Quale struttura multi-fase usare per prima?",
                "answer": (
                    "What So What Now What? e' la piu' versatile: "
                    "funziona dopo un'esperienza condivisa, un test o una riunione difficile. "
                    "Aiuta a tradurre osservazioni in azioni."
                ),
            },
        ],
    },
}

PER_BISOGNO = {
    "generare-idee": {
        "title": "Generare idee",
        "page_title": "Liberating Structures per generare idee",
        "intro": "Per team bloccati e workshop creativi.",
        "meta_description": (
            "Liberating Structures per generare idee: 1-2-4-All, TRIZ, 25/10 e altre. "
            "Format passo passo per workshop e riunioni."
        ),
        "slugs": ["1-2-4-all", "25-10-crowd-sourcing", "triz", "4-2-1-storming"],
        "examples": ["1-2-4-All", "25/10", "TRIZ"],
        "faq": [
            {
                "question": "Quale Liberating Structure usare per generare idee?",
                "answer": (
                    "1-2-4-All e' la piu' rapida (15 minuti) per far emergere idee da tutti. "
                    "TRIZ aiuta quando il gruppo e' bloccato su un compromesso. "
                    "25/10 Crowd Sourcing prioritizza molte proposte in mezz'ora."
                ),
            },
            {
                "question": "1-2-4-All o TRIZ per un workshop creativo?",
                "answer": (
                    "Usa 1-2-4-All all'inizio per raccogliere molte idee in poco tempo. "
                    "Passa a TRIZ se emergono posizioni rigide o il gruppo ripete le stesse soluzioni."
                ),
            },
        ],
    },
    "prendere-decisioni": {
        "title": "Prendere decisioni",
        "page_title": "Liberating Structures per prendere decisioni",
        "intro": "Per riunioni che non concludono.",
        "meta_description": (
            "Liberating Structures per prendere decisioni: Min Specs, WINFY e altre. "
            "Per riunioni che devono concludere con un impegno chiaro."
        ),
        "slugs": ["min-specs", "agreement-certainty-matrix", "what-i-need-from-you-winfy"],
        "examples": ["Min Specs", "Agreement/Certainty Matrix", "WINFY"],
        "faq": [
            {
                "question": "Quali Liberating Structures aiutano a prendere decisioni?",
                "answer": (
                    "Min Specs definisce il minimo indispensabile per agire. "
                    "Agreement/Certainty Matrix ordina le decisioni per urgenza e chiarezza. "
                    "WINFY chiude con impegni espliciti tra le persone."
                ),
            },
            {
                "question": "Min Specs o WINFY per chiudere una riunione?",
                "answer": (
                    "Min Specs quando devi stabilire regole minime condivise. "
                    "WINFY quando servono richieste chiare tra ruoli diversi "
                    "per sbloccare il lavoro."
                ),
            },
        ],
    },
    "analizzare-problemi": {
        "title": "Analizzare problemi",
        "page_title": "Liberating Structures per analizzare problemi",
        "intro": "Per situazioni complesse e cause profonde.",
        "meta_description": (
            "Liberating Structures per analizzare problemi: 9 Whys, Ecocycle, DAD e altre. "
            "Cause profonde e azioni concrete."
        ),
        "slugs": ["9-whys", "discovery-action-dialogue-dad", "ecocycle-planning"],
        "examples": ["9 Whys", "Discovery & Action Dialogue", "Ecocycle"],
        "faq": [
            {
                "question": "Come analizzare un problema complesso con le Liberating Structures?",
                "answer": (
                    "9 Whys va dritto alle cause profonde. "
                    "Discovery & Action Dialogue coinvolge chi vive il problema sul campo. "
                    "Ecocycle Planning mappa attivita' sul ciclo di vita del team."
                ),
            },
            {
                "question": "9 Whys o Ecocycle Planning?",
                "answer": (
                    "9 Whys per un problema specifico e recente. "
                    "Ecocycle quando devi decidere cosa potenziare, cosa tagliare "
                    "o lasciare in incubazione nel portfolio di attivita'."
                ),
            },
        ],
    },
    "fare-strategia": {
        "title": "Fare strategia",
        "page_title": "Liberating Structures per fare strategia",
        "intro": "Per trasformazioni e pianificazione.",
        "meta_description": (
            "Liberating Structures per fare strategia: Open Space, Critical Uncertainties, "
            "P2P e altre per trasformazioni e pianificazione."
        ),
        "slugs": ["critical-uncertainties", "open-space-technology-ost", "purpose-to-practice-p2p"],
        "examples": ["Critical Uncertainties", "Open Space", "Purpose to Practice"],
        "faq": [
            {
                "question": "Quali Liberating Structures servono per la strategia?",
                "answer": (
                    "Critical Uncertainties esplora scenari futuri. "
                    "Open Space coinvolge molte persone su temi strategici. "
                    "Purpose to Practice allinea scopo, valori e pratiche quotidiane."
                ),
            },
            {
                "question": "Open Space per la strategia di organizzazione?",
                "answer": (
                    "Si, quando hai un tema strategico ampio e persone motivate "
                    "a lavorarci insieme. "
                    "Serve almeno mezza giornata e un facilitatore esperto."
                ),
            },
        ],
    },
}


def slugify_fase(fase: str) -> str:
    return FASE_MAP.get(fase, fase.lower().replace(" ", "-"))


def fase_label_it(fase: str, fase_slug: str) -> str:
    return FASE_SLUG_LABELS_IT.get(fase_slug, fase)


def truncate_text(text: str, max_len: int) -> str:
    """Truncate at a word boundary with ellipsis."""
    text = text.strip()
    if len(text) <= max_len:
        return text
    prefix = text[: max_len - 3]
    parts = prefix.rsplit(maxsplit=1)
    cut = parts[0] if len(parts) > 1 and parts[0] else prefix
    return cut.rstrip(".,;:") + "..."


def hub_meta_description(hub: dict) -> str:
    return hub.get("meta_description") or hub["intro"]


def durata_bucket(durata: str) -> str:
    d = durata.lower()
    if "workshop" in d or "+1" in d or "giorn" in d or "variabile" in d and "g" in d:
        return "workshop"
    m = re.search(r"(\d+)", d)
    if not m:
        return "media"
    mins = int(m.group(1))
    if "h" in d and mins < 10:
        mins *= 60
    if mins <= 45:
        return "breve"
    if mins <= 90:
        return "media"
    if mins <= 240:
        return "estesa"
    return "workshop"


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta = yaml.safe_load(parts[1]) or {}
    return meta, parts[2].strip()


def split_sections(body: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current = "_preamble"
    buf: list[str] = []
    for line in body.splitlines():
        if line.startswith("## "):
            sections[current] = "\n".join(buf).strip()
            current = line[3:].strip()
            buf = []
        else:
            buf.append(line)
    sections[current] = "\n".join(buf).strip()
    return sections


def parse_bullet_list(text: str) -> list[str]:
    items = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("- "):
            items.append(line[2:].strip())
    return items


def parse_steps(text: str) -> list[dict[str, str]]:
    steps = []
    for line in text.splitlines():
        m = re.match(r"^\d+\.\s+(.+?)\s+-\s+(.+)$", line.strip())
        if m:
            steps.append({"action": m.group(1).strip(), "time": m.group(2).strip()})
        elif re.match(r"^\d+\.", line.strip()):
            rest = re.sub(r"^\d+\.\s*", "", line.strip())
            steps.append({"action": rest, "time": ""})
    return steps


def parse_faq(text: str) -> list[dict[str, str]]:
    items = []
    text = text.strip()
    if text.startswith("###"):
        text = re.sub(r"^#+\s*", "", text, count=1)
    blocks = re.split(r"\n### ", text)
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        lines = block.split("\n", 1)
        q = re.sub(r"^#+\s*", "", lines[0].strip())
        a = lines[1].strip() if len(lines) > 1 else ""
        if q:
            items.append({"question": q, "answer": a})
    return items


def parse_nav_links(text: str) -> list[dict[str, str]]:
    links = []
    for line in text.splitlines():
        m = re.search(r"\[([^\]]+)\]\((/structures/[^/)]+)/?\)\s*-\s*(.+)", line)
        if m:
            slug = m.group(2).rstrip("/").split("/")[-1]
            links.append({"name": m.group(1), "url": m.group(2).rstrip("/") + "/", "slug": slug, "reason": m.group(3).strip()})
    return links


def parse_prima_dopo(text: str) -> tuple[list[dict], list[dict]]:
    prima, dopo = [], []
    for line in text.splitlines():
        m = re.search(r"\*\*(Prima|Dopo):\*\*\s*\[([^\]]+)\]\((/structures/[^/)]+)/?\)\s*-\s*(.+)", line)
        if m:
            item = {"name": m.group(2), "url": m.group(3).rstrip("/") + "/", "reason": m.group(4).strip()}
            (prima if m.group(1) == "Prima" else dopo).append(item)
    return prima, dopo


def parse_path_nav(text: str) -> tuple[dict | None, dict | None]:
    prev = next_ = None
    m_prev = re.search(r"←\s*\[([^\]]+)\]\((/structures/[^/)]+)/?\)", text)
    m_next = re.search(r"→\s*\[([^\]]+)\]\((/structures/[^/)]+)/?\)", text)
    if m_prev:
        prev = {"name": m_prev.group(1), "url": m_prev.group(2).rstrip("/") + "/"}
    if m_next:
        next_ = {"name": m_next.group(1), "url": m_next.group(2).rstrip("/") + "/"}
    return prev, next_


def parse_chips_line(text: str) -> list[dict[str, str]]:
    chips = []
    for m in re.finditer(r"\[([^\]]+)\]\((/[^)]+)/?\)", text):
        chips.append({"label": m.group(1), "url": m.group(2).rstrip("/") + "/"})
    return chips


def parse_catalogo_extra(text: str) -> list[dict[str, str]]:
    extras = []
    for m in re.finditer(r"\[([^\]]+)\]\((/structures/[^/)]+)/?\)\s*-\s*([^·\n]+)", text):
        if "Esplora" not in m.group(1):
            extras.append({"name": m.group(1), "url": m.group(2).rstrip("/") + "/", "reason": m.group(3).strip()})
    return extras


def parse_breadcrumb_from_preamble(preamble: str) -> list[dict[str, str]]:
    crumbs: list[dict[str, str]] = []
    bc_line = None
    for line in preamble.splitlines():
        if ">" in line and "[" in line and not line.strip().startswith("**"):
            bc_line = line.strip()
            break

    if bc_line:
        crumbs.append({"name": "Home", "url": "/"})
        for m in re.finditer(r"\[([^\]]+)\]\((/[^)]+)/?\)", bc_line):
            name = m.group(1)
            if name != "Home":
                crumbs.append({"name": name, "url": m.group(2).rstrip("/") + "/"})
        tail = re.sub(r"\[[^\]]+\]\([^)]+\)", "", bc_line)
        tail = tail.replace(">", " ").strip()
        if tail:
            crumbs.append({"name": tail, "url": None})
    else:
        h1_m = re.search(r"^#\s+(.+)$", preamble, re.M)
        crumbs = [{"name": "Home", "url": "/"}]
        if h1_m:
            crumbs.append({"name": h1_m.group(1).strip(), "url": None})
    return crumbs


def extract_brief(preamble: str) -> str:
    m = re.search(r"\*\*In breve\*\*\s*-\s*(.+)$", preamble, re.M)
    if m:
        return f"<strong>In breve</strong> - {m.group(1).strip()}"
    return ""


def absolute_url(path: str | None) -> str:
    if not path:
        return ""
    path = path if path.startswith("/") else f"/{path}"
    return f"{SITE_ORIGIN}{path.rstrip('/')}/"


def parse_duration_iso(durata: str) -> str | None:
    if not durata or durata.strip().lower() == "variabile":
        return None
    text = durata.lower()
    hours = 0
    minutes = 0
    hm = re.search(r"(\d+)\s*h(?:ou)?", text)
    mm = re.search(r"(\d+)\s*min", text)
    if hm:
        hours = int(hm.group(1))
    if mm:
        minutes = int(mm.group(1))
    if not hours and not minutes:
        return None
    iso = "PT"
    if hours:
        iso += f"{hours}H"
    if minutes:
        iso += f"{minutes}M"
    return iso


def build_organization_jsonld() -> dict:
    org = {
        "@type": "Organization",
        "@id": ORGANIZATION_ID,
        "name": "Liberating.it",
        "url": f"{SITE_ORIGIN}/",
        "description": (
            "Guida pratica in italiano alle Liberating Structures per riunioni, workshop e facilitazione."
        ),
        "knowsAbout": [
            "Liberating Structures",
            "Facilitazione",
            "Design thinking",
            "Workshop",
            "Metodi partecipativi",
        ],
        "inLanguage": "it-IT",
    }
    if ORGANIZATION_SAME_AS:
        org["sameAs"] = list(ORGANIZATION_SAME_AS)
    return org


def structure_reading_minutes(structure: dict, *, wpm: int = READING_WPM) -> int:
    """Estimate reading time for structure pages (Yoast-style Twitter card)."""
    chunks: list[str] = [
        structure.get("brief_plain", ""),
        structure.get("consiglio", ""),
        structure.get("meta_description", ""),
    ]
    for key in ("domanda_items", "prep_items", "quando_items", "errori_items"):
        chunks.extend(structure.get(key) or [])
    for step in structure.get("steps") or []:
        chunks.append(step.get("action", ""))
    for item in structure.get("faq") or []:
        chunks.extend([item.get("question", ""), item.get("answer", "")])
    words = len(re.findall(r"\w+", " ".join(chunks), re.UNICODE))
    return max(1, round(words / wpm))


def format_reading_time_label(minutes: int) -> str:
    if minutes == 1:
        return "1 minuto"
    return f"{minutes} minuti"


def build_share_links(canonical: str, title: str) -> dict[str, str]:
    from urllib.parse import quote

    encoded_url = quote(canonical, safe="")
    encoded_title = quote(title, safe="")
    return {
        "url": canonical,
        "title": title,
        "linkedin": (
            "https://www.linkedin.com/shareArticle?mini=true"
            f"&url={encoded_url}&title={encoded_title}"
        ),
        "facebook": f"https://www.facebook.com/sharer.php?u={encoded_url}",
        "x": f"https://x.com/intent/post?url={encoded_url}&text={encoded_title}",
    }


def build_website_jsonld(description: str) -> dict:
    return {
        "@type": "WebSite",
        "@id": WEBSITE_ID,
        "name": "Liberating.it",
        "url": f"{SITE_ORIGIN}/",
        "description": description,
        "inLanguage": "it-IT",
        "publisher": {"@id": ORGANIZATION_ID},
    }


def build_faq_jsonld(faq: list[dict[str, str]]) -> dict | None:
    if not faq:
        return None
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["question"],
                "acceptedAnswer": {"@type": "Answer", "text": item["answer"]},
            }
            for item in faq
        ],
    }


def build_howto_jsonld(structure: dict) -> dict | None:
    steps = structure.get("steps") or []
    if not steps:
        return None
    page_url = structure.get("url", "")
    howto: dict = {
        "@type": "HowTo",
        "@id": f"{page_url}#howto" if page_url else None,
        "name": structure["h1"],
        "description": structure.get("brief_plain") or structure.get("meta_description", ""),
        "inLanguage": "it-IT",
        "step": [],
    }
    if page_url:
        howto["url"] = page_url
    total_time = parse_duration_iso(structure.get("durata", ""))
    if total_time:
        howto["totalTime"] = total_time
    prep = structure.get("prep_items") or []
    if prep:
        howto["supply"] = [{"@type": "HowToSupply", "name": item} for item in prep]
    for index, step in enumerate(steps, start=1):
        entry: dict = {
            "@type": "HowToStep",
            "position": index,
            "name": step["action"],
            "text": step["action"],
        }
        if step.get("time"):
            step_time = parse_duration_iso(step["time"])
            if step_time:
                entry["performTime"] = step_time
        howto["step"].append(entry)
    if howto.get("@id") is None:
        howto.pop("@id", None)
    return howto


def build_defined_term_jsonld(structure: dict) -> dict | None:
    description = structure.get("brief_plain") or structure.get("meta_description")
    if not description:
        return None
    page_url = structure.get("url", "")
    term: dict = {
        "@type": "DefinedTerm",
        "name": structure["h1"],
        "description": description,
        "inDefinedTermSet": {
            "@type": "DefinedTermSet",
            "name": "Liberating Structures",
            "url": f"{SITE_ORIGIN}/structures/",
        },
    }
    if page_url:
        term["url"] = page_url
    return term


def build_collection_jsonld(name: str, description: str, url: str, count: int) -> dict:
    return {
        "@type": "CollectionPage",
        "name": name,
        "description": description,
        "url": url,
        "inLanguage": "it-IT",
        "numberOfItems": count,
    }


def build_item_list_jsonld(name: str, items: list[dict], page_url: str) -> dict | None:
    if not items:
        return None
    return {
        "@type": "ItemList",
        "name": name,
        "url": page_url,
        "numberOfItems": len(items),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index,
                "name": item["title"],
                "url": f"{SITE_ORIGIN}/structures/{item['slug']}/",
            }
            for index, item in enumerate(items, start=1)
        ],
    }


def build_breadcrumb_jsonld(breadcrumbs: list[dict], page_url: str) -> dict:
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index,
                "name": crumb["name"],
                "item": absolute_url(crumb["url"]) if crumb.get("url") else page_url,
            }
            for index, crumb in enumerate(breadcrumbs, start=1)
        ],
    }


# Italian display typography: sources may use ASCII apostrophe instead of accents.
# Applied in render() via italian_typography_ctx; JSON-LD via _typography_json_obj;
# llms.txt at write time. Slugs and URLs are never transformed.
# Patterns: *ita'/*ta' -> *ità/*tà; e'/E' -> è/È; piu'/gia'/perche'/cio'/si' -> più/già/perché/ciò/sì;
# cos'e'/com'e'/qual e'/c'e' -> cos'è/com'è/qual è/c'è. Preserves l', d', un', po', etc.
_SKIP_ITALIAN_TYPOGRAPHY_KEYS = frozenset({
    "slug", "icon", "icon_full", "og_image", "og_type", "page_type", "active_nav",
    "active_per_bisogno", "sort_order", "stem", "bundle", "css", "js", "jsonld",
    "page_path", "out_root", "canonical", "url", "og_image_width", "og_image_height",
    "og_image_type", "has_path_nav", "source_lastmod", "fase", "difficolta", "durata",
    "complessita", "partecipanti", "llms_url",
})


def _should_skip_typography_key(key: str) -> bool:
    if key in _SKIP_ITALIAN_TYPOGRAPHY_KEYS:
        return True
    if key.endswith("_slug") or key.endswith("_url"):
        return True
    return False


def italian_typography(text: str) -> str:
    """Convert ASCII apostrophe-for-accent to proper Italian typography in display text."""
    if not text or "'" not in text:
        return text

    text = re.sub(r"(\w+)ita'", lambda m: m.group(1) + "ità", text)
    text = re.sub(r"(\w+)Ita'", lambda m: m.group(1) + "Ità", text)
    text = re.sub(r"(\w+)ta'", lambda m: m.group(1) + "tà", text)
    text = re.sub(r"(\w+)Ta'", lambda m: m.group(1) + "Tà", text)

    for old, new in (
        ("cos'e'", "cos'è"),
        ("Cos'e'", "Cos'è"),
        ("com'e'", "com'è"),
        ("Com'e'", "Com'è"),
        ("qual e'", "qual è"),
        ("Qual e'", "Qual è"),
    ):
        text = text.replace(old, new)

    text = re.sub(r"(?<![a-zA-Z'])([cnmsl])'e'", lambda m: f"{m.group(1)}'è", text)
    text = re.sub(r"(?<![a-zA-Z'])C'e'", "C'è", text)

    for pattern, repl in (
        (r"perche'(?![a-zA-Z])", "perché"),
        (r"Perche'(?![a-zA-Z])", "Perché"),
        (r"piu'(?![a-zA-Z])", "più"),
        (r"Piu'(?![a-zA-Z])", "Più"),
        (r"gia'(?![a-zA-Z])", "già"),
        (r"Gia'(?![a-zA-Z])", "Già"),
        (r"cio'(?![a-zA-Z])", "ciò"),
        (r"Cio'(?![a-zA-Z])", "Ciò"),
        (r"Si'(?![a-zA-Z])", "Sì"),
        (r"si'(?![a-zA-Z])", "sì"),
        (r"(?<![a-zA-Z'])e'(?![a-zA-Z])", "è"),
        (r"(?<![a-zA-Z'])E'(?![a-zA-Z])", "È"),
    ):
        text = re.sub(pattern, repl, text)

    return text


def _typography_json_obj(obj):
    if isinstance(obj, str):
        return italian_typography(obj)
    if isinstance(obj, dict):
        return {k: _typography_json_obj(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_typography_json_obj(v) for v in obj]
    return obj


def italian_typography_value(key: str, value):
    if _should_skip_typography_key(key):
        return value
    if isinstance(value, str):
        return italian_typography(value)
    if isinstance(value, dict):
        return {k: italian_typography_value(k, v) for k, v in value.items()}
    if isinstance(value, list):
        return [italian_typography_value(key, item) for item in value]
    return value


def italian_typography_ctx(ctx: dict) -> dict:
    return {k: italian_typography_value(k, v) for k, v in ctx.items()}


def merge_jsonld(*nodes: dict | None) -> str | None:
    items = [_typography_json_obj(node) for node in nodes if node]
    if not items:
        return None
    if len(items) == 1:
        return json.dumps({"@context": "https://schema.org", **items[0]}, ensure_ascii=False)
    return json.dumps({"@context": "https://schema.org", "@graph": items}, ensure_ascii=False)


def page_jsonld(
    breadcrumbs: list[dict] | None,
    canonical: str,
    *extra: dict | None,
) -> str | None:
    nodes: list[dict | None] = list(extra)
    if breadcrumbs:
        nodes.append(build_breadcrumb_jsonld(breadcrumbs, canonical))
    return merge_jsonld(*nodes)


def md_inline(text: str) -> str:
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(
        r"\[([^\]]+)\]\((https?://[^)]+)\)",
        r'<a href="\2" rel="noopener noreferrer">\1</a>',
        text,
    )
    text = re.sub(r"\[([^\]]+)\]\((/[^)]+)/?\)", r'<a href="\2/">\1</a>', text)
    text = re.sub(
        r"\[([^\]]+)\]\((mailto:[^)]+)\)",
        r'<a href="\2">\1</a>',
        text,
    )
    text = re.sub(r"\[([^\]]+)\]\([^/)][^)]*\)", r"\1", text)
    text = re.sub(
        r"(?<!\w)(https?://[^\s<]+)",
        r'<a href="\1" rel="noopener noreferrer">\1</a>',
        text,
    )
    return text


def md_block_to_html(text: str) -> str:
    """Lightweight markdown blocks for legal/editorial sections."""
    blocks = re.split(r"\n\n+", text.strip())
    parts: list[str] = []
    for block in blocks:
        lines = block.splitlines()
        if not lines:
            continue
        first = lines[0].strip()
        if first.startswith("#### "):
            parts.append(f"<h4>{md_inline(first[5:].strip())}</h4>")
            rest = "\n".join(lines[1:]).strip()
            if rest:
                parts.append(md_block_to_html(rest))
            continue
        if first.startswith("### "):
            parts.append(f"<h3>{md_inline(first[4:].strip())}</h3>")
            rest = "\n".join(lines[1:]).strip()
            if rest:
                parts.append(md_block_to_html(rest))
            continue
        bullet_lines = [line.strip() for line in lines if line.strip()]
        if bullet_lines and all(line.startswith("- ") for line in bullet_lines):
            items = "".join(f"<li>{md_inline(line[2:].strip())}</li>" for line in bullet_lines)
            parts.append(f"<ul>{items}</ul>")
            continue
        para = md_inline(" ".join(line.strip() for line in lines))
        parts.append(f"<p>{para}</p>")
    return "\n".join(parts)


def parse_legal_page(path: Path) -> dict:
    meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
    sections_map = split_sections(body)
    preamble = sections_map.pop("_preamble", "")
    h1_m = re.search(r"^#\s+(.+)$", preamble, re.M)
    h1 = h1_m.group(1).strip() if h1_m else meta.get("title", "")
    lead_m = re.search(r"^>\s*(.+)$", preamble, re.M)
    lead = lead_m.group(1).strip() if lead_m else ""
    legal_sections = []
    for key, content in sections_map.items():
        m = re.match(r"(\d+)\.\s+(.+)", key)
        if not m:
            continue
        legal_sections.append(
            {
                "number": int(m.group(1)),
                "title": m.group(2),
                "html": md_block_to_html(content.strip()),
            }
        )
    legal_sections.sort(key=lambda item: item["number"])
    return {
        "h1": h1,
        "lead": lead,
        "sections": [{"title": s["title"], "html": s["html"]} for s in legal_sections],
    }


def parse_editorial_links(text: str) -> list[dict[str, str]]:
    links = []
    for line in text.splitlines():
        m = re.search(r"-\s*\[([^\]]+)\]\((/[^)]+)/?\)(?:\s*-\s*(.+))?", line)
        if m:
            links.append(
                {
                    "name": m.group(1),
                    "url": m.group(2).rstrip("/") + "/",
                    "reason": (m.group(3) or "").strip(),
                }
            )
    return links


def build_principles_faq(structure_count: int) -> list[dict[str, str]]:
    return [
        {
            "question": "Cosa sono le Liberating Structures?",
            "answer": (
                f"Le Liberating Structures sono {OFFICIAL_LS_COUNT} formati ufficiali di facilitazione "
                "con passaggi e tempi definiti. "
                f"Su liberating.it trovi {structure_count} schede in italiano con passaggi, tempi e consigli pratici."
            ),
        },
        {
            "question": "Quali sono i principi delle Liberating Structures?",
            "answer": (
                "I principi includono includere chi resta fuori, distribuire la partecipazione, "
                "combinare attivazione e liberazione, e rendere semplice cio' che e' complesso. "
                "Ogni struttura li applica in modo concreto."
            ),
        },
        {
            "question": "Le Liberating Structures funzionano in agile e Scrum?",
            "answer": (
                "Si'. Si usano in retrospective, sprint planning e workshop di team per far emergere idee "
                "da tutti senza discussioni dominate dalle voci piu' forti."
            ),
        },
        {
            "question": "Come faccio partecipare chi di solito resta in silenzio?",
            "answer": (
                "Parti da strutture con tempo individuale prima del plenario, come 1-2-4-All "
                "o Impromptu Networking. Il silenzio iniziale non e' vuoto: e' tempo per pensare. "
                "Per ricostruire fiducia nel gruppo, prova Heard, Seen, Respected (HSR)."
            ),
        },
    ]


def normalize_structure_count_text(text: str, structure_count: int) -> str:
    """Replace legacy hardcoded catalog size (35) with the live structure count."""
    if not text:
        return text
    legacy = str(LEGACY_STRUCTURE_COUNT)
    n = str(structure_count)
    text = re.sub(
        rf"\b{legacy}\s+Liberating Structures\b",
        f"{n} Liberating Structures",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        rf"\b{legacy}\s+(strutture|schede|formati|strumenti)\b",
        rf"{n} \1",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(rf"\btutte le {legacy}\b", f"tutte le {n}", text, flags=re.IGNORECASE)
    text = re.sub(rf"\bsono {legacy}\b", f"sono {n}", text, flags=re.IGNORECASE)
    text = re.sub(rf"\bHai {legacy} strutture\b", f"Hai {n} strutture", text, flags=re.IGNORECASE)
    text = re.sub(rf"\bsui {legacy} strumenti\b", f"sui {n} strumenti", text, flags=re.IGNORECASE)
    return text


def build_home_faq(structure_count: int) -> list[dict[str, str]]:
    return [
        {
            "question": "Cosa sono le Liberating Structures?",
            "answer": (
                "Sono formati di facilitazione con passaggi e tempi definiti "
                "per far partecipare tutti in riunioni e workshop. "
                "Non servono anni di formazione: la piu' usata, 1-2-4-All, si fa in 15 minuti."
            ),
        },
        {
            "question": "Da dove inizio se non ho mai facilitato?",
            "answer": (
                "Apri il percorso Per iniziare subito: cinque strutture facili in ordine, "
                "con passaggi pronti. In alternativa prova 1-2-4-All nella prossima riunione "
                "con una domanda concreta per il team."
            ),
        },
        {
            "question": "Quante Liberating Structures ci sono su liberating.it?",
            "answer": (
                f"Il menu ufficiale ne conta {OFFICIAL_LS_COUNT}; su liberating.it trovi {structure_count} schede "
                "in italiano, inclusi adattamenti e varianti documentate con passaggi e tempi."
            ),
        },
        {
            "question": "Quando conviene usare le Liberating Structures?",
            "answer": (
                "Quando una riunione ha bisogno di piu' partecipazione, idee da tutti o una decisione condivisa. "
                "Funzionano in presenza e online. Parti da 1-2-4-All (15 min) o dal percorso Per iniziare subito."
            ),
        },
    ]


def apply_structure_counts(editorial: dict, structure_count: int) -> dict:
    def replace_counts(text: str) -> str:
        return normalize_structure_count_text(text, structure_count)

    if editorial.get("lead"):
        editorial["lead"] = replace_counts(editorial["lead"])
    if editorial.get("cta_text"):
        editorial["cta_text"] = replace_counts(editorial["cta_text"])
    if editorial.get("h1"):
        editorial["h1"] = replace_counts(editorial["h1"])
    for section in editorial.get("sections", []):
        if section.get("title"):
            section["title"] = replace_counts(section["title"])
        if section.get("body"):
            section["body"] = replace_counts(section["body"])
    for link in editorial.get("leggi_anche", []):
        if link.get("reason"):
            link["reason"] = replace_counts(link["reason"])
    for item in editorial.get("faq", []):
        if item.get("question"):
            item["question"] = replace_counts(item["question"])
        if item.get("answer"):
            item["answer"] = replace_counts(item["answer"])
    return editorial


def parse_editorial_page(path: Path, faq: list[dict[str, str]] | None = None) -> dict:
    meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
    sections_map = split_sections(body)
    preamble = sections_map.get("_preamble", "")

    h1_m = re.search(r"^#\s+(.+)$", preamble, re.M)
    h1 = h1_m.group(1).strip() if h1_m else meta.get("title", "")

    lead_lines: list[str] = []
    for line in preamble.splitlines():
        if line.startswith("# "):
            continue
        if line.startswith("**Cosa trovi"):
            break
        stripped = line.strip()
        if stripped and not stripped.startswith("-"):
            lead_lines.append(stripped)
    lead = " ".join(lead_lines)

    editorial_sections = []
    for key, content in sections_map.items():
        m = re.match(r"(\d+)\.\s+(.+)", key)
        if not m:
            continue
        editorial_sections.append(
            {
                "number": int(m.group(1)),
                "title": m.group(2),
                "body": md_inline(content.strip().replace("\n", " ")),
            }
        )
    editorial_sections.sort(key=lambda item: item["number"])

    return {
        "h1": h1,
        "lead": lead,
        "sections": [{"title": s["title"], "body": s["body"]} for s in editorial_sections],
        "leggi_anche": parse_editorial_links(sections_map.get("Leggi anche", "")),
        "faq": faq or [],
        "cta_text": sections_map.get("E adesso?", "").strip(),
        "cta_url": "/structures/1-2-4-all/",
        "cta_label": "Prova 1-2-4-All domani",
    }


def parse_structure(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(raw)
    sections = split_sections(body)
    preamble = sections.get("_preamble", "")

    h1_m = re.search(r"^#\s+(.+)$", preamble, re.M)
    h1 = h1_m.group(1).strip() if h1_m else meta.get("slug", "")

    slug = meta["slug"]
    DISPLAY_NAMES[slug] = h1

    brief_raw = extract_brief(preamble)
    complessita = meta.get("complessita", "")
    difficolta = meta.get("difficolta", "")
    fase = meta.get("fase", "")
    durata = meta.get("durata", "")

    prima, dopo = parse_prima_dopo(sections.get("Prima e dopo", ""))
    path_prev, path_next = parse_path_nav(sections.get("Prossimo nel percorso", ""))

    chips_text = ""
    for line in preamble.splitlines():
        if line.startswith("**Filtri:**"):
            chips_text = line
            break

    faq = parse_faq(sections.get("Domande frequenti", ""))

    return {
        "slug": slug,
        "title": meta.get("title", h1),
        "meta_description": meta.get("meta_description", ""),
        "url": meta.get("url", f"https://liberating.it/structures/{slug}/"),
        "h1": h1,
        "brief": brief_raw,
        "brief_plain": re.sub(r"<[^>]+>", "", brief_raw).replace("In breve - ", ""),
        "durata": durata,
        "durata_slug": durata_bucket(durata),
        "difficolta": difficolta,
        "difficolta_slug": DIFFICOLTA_MAP.get(difficolta, difficolta.lower()),
        "partecipanti": meta.get("partecipanti", ""),
        "fase": fase,
        "fase_slug": slugify_fase(fase),
        "fase_label": fase_label_it(fase, slugify_fase(fase)),
        "complessita": complessita,
        "complessita_slug": COMPLESSITA_MAP.get(complessita, complessita.lower().replace(" ", "-")),
        "chips": parse_chips_line(chips_text),
        "domanda_items": parse_bullet_list(sections.get("Domanda da portare", "")),
        "prep_items": parse_bullet_list(sections.get("Cosa ti serve", "")),
        "steps": parse_steps(sections.get("I passaggi", "")),
        "quando_items": parse_bullet_list(sections.get("Quando usarla", "")),
        "consiglio": sections.get("Il consiglio del facilitatore", "").strip(),
        "errori_items": parse_bullet_list(sections.get("Errori da evitare", "")),
        "faq": faq,
        "prima_items": prima,
        "dopo_items": dopo,
        "simili_items": parse_nav_links(sections.get("Strutture simili", "")),
        "path_prev": path_prev,
        "path_next": path_next,
        "catalogo_extra": parse_catalogo_extra(sections.get("Torna al catalogo", "")),
        "breadcrumbs": parse_breadcrumb_from_preamble(preamble),
        "sort_order": PATH_ORDER.index(slug) if slug in PATH_ORDER else 999,
        "source_lastmod": datetime.fromtimestamp(path.stat().st_mtime).date().isoformat(),
    }


def sort_structures(structures: list[dict]) -> list[dict]:
    def key(s: dict) -> tuple:
        compl_order = ["iniziare-subito", "team-rodati", "facilitazioni-complesse", "trasformazioni-organizzative"]
        try:
            ci = compl_order.index(s["complessita_slug"])
        except ValueError:
            ci = 99
        return (ci, s["sort_order"], s["title"])

    return sorted(structures, key=key)


def load_tracking_config(path: Path | None = None) -> dict:
    """Load analytics / tag manager IDs from public/tracking.json."""
    cfg_path = path or TRACKING_CONFIG_PATH
    data = {
        "enabled": False,
        "gtm_id": "",
        "consent_default_denied": True,
    }
    if cfg_path.exists():
        try:
            raw = json.loads(cfg_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"warning: invalid {cfg_path.name}, tracking disabled: {exc}", file=sys.stderr)
            raw = None
        if isinstance(raw, dict):
            data.update(raw)
    data["enabled"] = bool(data.get("enabled"))
    data["consent_default_denied"] = bool(data.get("consent_default_denied", True))
    return data


def resolve_url(target: str, from_file: Path, out_root: Path) -> str:
    """Absolute site path -> relative directory URL (trailing slash, no index.html)."""
    target = (target or "/").strip()
    if target in ("/", ""):
        dest = out_root / "index.html"
    elif target.startswith("assets/") or target.lstrip("/").startswith("assets/"):
        dest = out_root / target.lstrip("/")
    elif target.endswith((".css", ".js", ".json", ".htm", ".html", ".ico", ".png", ".svg", ".webp")):
        dest = out_root / target.lstrip("/")
    else:
        dest = out_root / target.strip("/") / "index.html"

    if dest.name in ("index.html", "index.htm"):
        link_dest = dest.parent
        rel = Path(os.path.relpath(link_dest, from_file.parent))
        if rel == Path("."):
            return "./"
        return rel.as_posix() + "/"

    rel = Path(os.path.relpath(dest, from_file.parent))
    return rel.as_posix()


def load_icon_manifest(out_root: Path) -> dict[str, str]:
    path = out_root / ICON_MANIFEST_PATH
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def minify_html(html: str) -> str:
    return re.sub(r">\s+<", "><", html.strip())


def minify_css(css: str) -> str:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{}:;,>+~])\s*", r"\1", css)
    return css.strip()


def ensure_icon_thumbs(out_root: Path, icons: dict[str, str]) -> dict[str, str]:
    """Display-sized PNG thumbs (max 160px wide) for cards and scheda hero."""
    from PIL import Image

    thumb_dir = out_root / ICON_THUMB_DIR
    thumb_dir.mkdir(parents=True, exist_ok=True)
    thumbs: dict[str, str] = {}
    for slug, icon_rel in icons.items():
        thumb_rel = _ensure_icon_thumb(out_root, slug, icon_rel)
        if thumb_rel:
            thumbs[slug] = thumb_rel
    return thumbs


def _ensure_icon_thumb(out_root: Path, slug: str, icon_rel: str) -> str | None:
    from icon_mono import MONO_PIPELINE_VERSION, monochrome_structure_icon, resize_monochrome_icon
    from PIL import Image

    icon_path = out_root / icon_rel
    if not icon_path.exists():
        return None
    thumb_rel = f"{ICON_THUMB_DIR}/{slug}.png"
    thumb_path = out_root / thumb_rel
    pipeline_marker = thumb_path.with_suffix(f".{MONO_PIPELINE_VERSION}")
    if (
        thumb_path.exists()
        and pipeline_marker.exists()
        and thumb_path.stat().st_mtime >= icon_path.stat().st_mtime
    ):
        return thumb_rel
    img = monochrome_structure_icon(Image.open(icon_path))
    if img.width > ICON_THUMB_MAX_WIDTH:
        ratio = ICON_THUMB_MAX_WIDTH / img.width
        img = resize_monochrome_icon(img, (ICON_THUMB_MAX_WIDTH, int(img.height * ratio)))
    thumb_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(thumb_path, "PNG", optimize=True, compress_level=9)
    pipeline_marker.write_text(MONO_PIPELINE_VERSION, encoding="utf-8")
    return thumb_rel


def build_display_icons(out_root: Path, icons_full: dict[str, str]) -> tuple[dict[str, str], str, str]:
    """Card/hero thumbs per structure plus default LS Menu fallback paths."""
    from generate_adaptation_icons import LS_MENU_ICON_REL, ensure_ls_menu_icon

    ensure_ls_menu_icon(out_root)
    icon_thumbs = ensure_icon_thumbs(out_root, icons_full)
    ls_menu_thumb = _ensure_icon_thumb(out_root, "ls-menu", LS_MENU_ICON_REL)
    default_display = ls_menu_thumb or LS_MENU_ICON_REL
    display_icons = {
        slug: icon_thumbs.get(slug, icons_full[slug])
        for slug in icons_full
        if (out_root / icons_full[slug]).exists()
    }
    return display_icons, default_display, LS_MENU_ICON_REL


def minify_js(js: str) -> str:
    js = re.sub(r"/\*[\s\S]*?\*/", "", js)
    js = re.sub(r"\n\s+", "\n", js)
    return js.strip()


def write_build_manifest(out_root: Path, manifest: dict[str, object]) -> None:
    (out_root / "assets" / MANIFEST_NAME).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def bundle_css(out_root: Path) -> tuple[dict[str, str], str]:
    css_dir = out_root / "assets" / "css"
    parts = [(css_dir / name).read_text(encoding="utf-8") for name in CSS_BUNDLE_SOURCES]
    content = minify_css("\n".join(parts))
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()[:10]
    bundle_name = f"site.{digest}.css"
    bundle_path = css_dir / bundle_name
    bundle_path.write_text(content, encoding="utf-8")
    for old in css_dir.glob("site.*.css"):
        if old.name != bundle_name:
            old.unlink(missing_ok=True)
    manifest: dict[str, object] = {"css": f"css/{bundle_name}"}
    write_build_manifest(out_root, manifest)
    return manifest, content


def bundle_js(out_root: Path) -> None:
    js_dir = out_root / "assets" / "js"
    manifest_path = out_root / "assets" / MANIFEST_NAME
    manifest: dict[str, object] = {}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    js_manifest: dict[str, str] = {}
    for name in JS_SOURCES:
        src = js_dir / name
        if not src.exists():
            continue
        content = minify_js(src.read_text(encoding="utf-8"))
        stem = src.stem
        digest = hashlib.sha256(content.encode("utf-8")).hexdigest()[:10]
        bundle_name = f"{stem}.{digest}.js"
        (js_dir / bundle_name).write_text(content + "\n", encoding="utf-8")
        for old in js_dir.glob(f"{stem}.*.js"):
            if old.name != bundle_name:
                old.unlink(missing_ok=True)
        js_manifest[stem] = f"js/{bundle_name}"
    manifest["js"] = js_manifest
    write_build_manifest(out_root, manifest)


def resolve_asset_bundle(path: str, out_root: Path) -> str:
    css_keys = {f"assets/{name}" for name in CSS_BUNDLE_SOURCES} | {f"assets/{CSS_BUNDLE_VIRTUAL}"}
    manifest_path = out_root / "assets" / MANIFEST_NAME
    if not manifest_path.exists():
        return path
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if path in css_keys:
        bundle = manifest.get("css")
        return f"assets/{bundle}" if bundle else path
    js_match = re.match(r"assets/js/([\w-]+)\.js$", path)
    if js_match:
        bundle = manifest.get("js", {}).get(js_match.group(1))
        return f"assets/{bundle}" if bundle else path
    return path


def resolve_css_bundle(path: str, out_root: Path) -> str:
    return resolve_asset_bundle(path, out_root)


def make_env(templates_dir: Path, out_root: Path) -> Environment:
    env = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=select_autoescape(["html", "xml"]),
    )
    env.globals.setdefault("default_structure_icon", "")
    env.globals.setdefault("tracking", load_tracking_config())

    @pass_context
    def site_filter(ctx, path: str) -> str:
        return resolve_url(path, ctx["page_path"], ctx["out_root"])

    @pass_context
    def asset_filter(ctx, path: str) -> str:
        normalized = path if path.startswith("assets/") else f"assets/{path.lstrip('/')}"
        resolved = resolve_asset_bundle(normalized, ctx["out_root"])
        return resolve_url(resolved, ctx["page_path"], ctx["out_root"])

    env.filters["site"] = site_filter
    env.filters["asset"] = asset_filter
    return env


def _og_font(size: int, *, bold: bool = False, serif: bool = False):
    from PIL import ImageFont

    if serif and bold:
        candidates = (
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        )
    else:
        candidates = (
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        )
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def ensure_og_png(out_root: Path) -> None:
    """Rasterize the default Open Graph card (1200x630 PNG) for social crawlers."""
    from PIL import Image, ImageDraw

    png_path = out_root / OG_IMAGE_REL
    svg_path = out_root / "assets/images/og.svg"
    if png_path.exists() and svg_path.exists() and png_path.stat().st_mtime >= svg_path.stat().st_mtime:
        return

    png_path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (OG_IMAGE_WIDTH, OG_IMAGE_HEIGHT), "#496275")
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((64, 64, 1136, 566), radius=24, fill="#f8fafb")
    title_font = _og_font(72, bold=True, serif=True)
    sub_font = _og_font(36, serif=False)
    draw.text((120, 280), "Liberating.it", fill="#1a2329", font=title_font, anchor="ls")
    draw.text(
        (120, 360),
        "Formati pratici per riunioni e workshop",
        fill="#3f4f5c",
        font=sub_font,
        anchor="ls",
    )
    img.save(png_path, "PNG", optimize=True)


def _square_ls_menu_icon(img, size: int):
    """Center the LS Menu card on a white square and scale to size."""
    from PIL import Image

    width, height = img.size
    side = max(width, height)
    square = Image.new("RGB", (side, side), "#ffffff")
    square.paste(img.convert("RGB"), ((side - width) // 2, (side - height) // 2))
    return square.resize((size, size), Image.Resampling.LANCZOS)


def ensure_favicon(out_root: Path) -> None:
    """Rasterize favicons from the LS Menu structure icon."""
    from generate_adaptation_icons import LS_MENU_ICON_REL

    from PIL import Image

    source = out_root / LS_MENU_ICON_REL
    if not source.exists():
        raise SystemExit(f"LS Menu icon not found: {source}")

    ico_path = out_root / FAVICON_ICO
    png_path = out_root / FAVICON_PNG
    apple_path = out_root / FAVICON_APPLE
    sources_mtime = source.stat().st_mtime
    if (
        ico_path.exists()
        and png_path.exists()
        and apple_path.exists()
        and ico_path.stat().st_mtime >= sources_mtime
        and png_path.stat().st_mtime >= sources_mtime
        and apple_path.stat().st_mtime >= sources_mtime
    ):
        return

    with Image.open(source) as card:
        ico_sizes = [(size, size) for size in FAVICON_SIZES[:3]]
        ico_images = [_square_ls_menu_icon(card, size) for size in FAVICON_SIZES[:3]]
        ico_images[0].save(
            ico_path,
            format="ICO",
            sizes=ico_sizes,
            append_images=ico_images[1:],
        )
        _square_ls_menu_icon(card, 32).save(png_path, "PNG", optimize=True)
        _square_ls_menu_icon(card, FAVICON_SIZES[3]).save(apple_path, "PNG", optimize=True)


def _wrap_og_text(text: str, font, draw, max_width: int, max_lines: int = 3) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        candidate = " ".join(current + [word])
        if draw.textlength(candidate, font=font) <= max_width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
        if len(lines) >= max_lines:
            break
    if current and len(lines) < max_lines:
        lines.append(" ".join(current))
    if len(lines) == max_lines and len(words) > sum(len(line.split()) for line in lines):
        lines[-1] = lines[-1].rstrip(".,;:") + "…"
    return lines


def _structure_og_title_image(structure: dict, out_root: Path) -> str:
    """OG card with structure title when no icon is available."""
    from PIL import Image, ImageDraw

    slug = structure["slug"]
    out_path = out_root / "assets/images/og" / f"{slug}.png"
    title = structure.get("title") or structure.get("h1") or slug
    svg_path = out_root / "assets/images/og.svg"
    ensure_og_png(out_root)
    source_mtime = svg_path.stat().st_mtime
    if out_path.exists() and out_path.stat().st_mtime >= source_mtime:
        return f"{SITE_ORIGIN}/assets/images/og/{slug}.png"

    card = Image.open(out_root / OG_IMAGE_REL).convert("RGBA")
    draw = ImageDraw.Draw(card)
    title_font = _og_font(52, bold=True, serif=True)
    sub_font = _og_font(28, serif=False)
    lines = _wrap_og_text(title, title_font, draw, 720)
    block_h = len(lines) * 62 + 36
    y = (OG_IMAGE_HEIGHT - block_h) // 2
    for line in lines:
        draw.text((120, y), line, fill="#1a2329", font=title_font, anchor="ls")
        y += 62
    draw.text((120, y + 8), "Liberating.it", fill="#3f4f5c", font=sub_font, anchor="ls")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    card.convert("RGB").save(out_path, "PNG", optimize=True)
    return f"{SITE_ORIGIN}/assets/images/og/{slug}.png"


def structure_og_image_url(structure: dict, out_root: Path) -> str:
    """OG image URL: structure icon composited on the default card, or title-only card."""
    icon_rel = structure.get("icon_full") or structure.get("icon")
    slug = structure["slug"]
    if not icon_rel:
        return _structure_og_title_image(structure, out_root)

    icon_path = out_root / icon_rel
    if not icon_path.exists():
        return _structure_og_title_image(structure, out_root)

    out_path = out_root / "assets/images/og" / f"{slug}.png"
    svg_path = out_root / "assets/images/og.svg"
    from icon_mono import MONO_PIPELINE_VERSION, monochrome_structure_icon, resize_monochrome_icon

    sources_mtime = max(icon_path.stat().st_mtime, svg_path.stat().st_mtime)
    og_marker = out_path.with_suffix(f".{MONO_PIPELINE_VERSION}")
    if (
        out_path.exists()
        and og_marker.exists()
        and out_path.stat().st_mtime >= sources_mtime
    ):
        return f"{SITE_ORIGIN}/assets/images/og/{slug}.png"

    from PIL import Image

    ensure_og_png(out_root)
    card = Image.open(out_root / OG_IMAGE_REL).convert("RGBA")
    icon = monochrome_structure_icon(Image.open(icon_path))
    max_h = 380
    scale = max_h / icon.height
    new_size = (int(icon.width * scale), max_h)
    icon = resize_monochrome_icon(icon, new_size)
    x = OG_IMAGE_WIDTH - 64 - new_size[0] - 48
    y = (OG_IMAGE_HEIGHT - new_size[1]) // 2
    card.paste(icon, (x, y))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    card.convert("RGB").save(out_path, "PNG", optimize=True)
    og_marker.write_text(MONO_PIPELINE_VERSION, encoding="utf-8")
    return f"{SITE_ORIGIN}/assets/images/og/{slug}.png"


def clean_orphan_og_images(structures: list[dict], out_root: Path) -> None:
    """Remove per-structure OG PNGs for slugs no longer in the catalog."""
    og_dir = out_root / "assets/images/og"
    if not og_dir.exists():
        return
    valid = {s["slug"] for s in structures}
    for path in og_dir.glob("*.png"):
        if path.stem not in valid:
            path.unlink(missing_ok=True)


def render(env: Environment, template: str, out_path: Path, out_root: Path, **ctx) -> None:
    ctx.setdefault("active_nav", None)
    ctx.setdefault("active_per_bisogno", None)
    ctx.setdefault("jsonld", None)
    ctx.setdefault("og_type", "website")
    ctx.setdefault("og_image", f"{SITE_ORIGIN}/{OG_IMAGE_REL}")
    ctx.setdefault("og_image_width", str(OG_IMAGE_WIDTH))
    ctx.setdefault("og_image_height", str(OG_IMAGE_HEIGHT))
    ctx.setdefault("og_image_type", "image/png")
    ctx.setdefault("og_image_alt", OG_DEFAULT_ALT)
    ctx.setdefault("llms_url", f"{SITE_ORIGIN}/llms.txt")
    ctx.setdefault("share", None)
    ctx.setdefault("reading_time_label", None)
    if ctx.get("meta_description"):
        ctx["meta_description"] = format_meta_description(ctx["meta_description"])
    ctx["page_path"] = out_path
    ctx["out_root"] = out_root
    ctx = italian_typography_ctx(ctx)
    html = minify_html(env.get_template(template).render(**ctx))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")


def clean_generated(out_root: Path) -> None:
    for name in GENERATED_DIRS:
        path = out_root / name
        if path.exists():
            shutil.rmtree(path)
    for name in GENERATED_FILES:
        path = out_root / name
        if path.exists():
            path.unlink()


def build_home(env: Environment, content_root: Path, out_root: Path, structure_count: int) -> None:
    home_path = content_root.parent / "v1" / "pagine" / "home.md"
    if not home_path.exists():
        home_path = content_root / "pagine" / "home.md"
    meta, body = parse_frontmatter(home_path.read_text(encoding="utf-8")) if home_path.exists() else ({}, "")

    n = structure_count
    default_meta = (
        f"Liberating Structures in italiano: {n} formati per riunioni e workshop. "
        "Passaggi pronti per facilitatori e team. Inizia da 1-2-4-All."
    )
    home_faq = build_home_faq(structure_count)

    ctx = {
        "page_type": "home",
        "page_title": format_page_title(meta.get("title", "Liberating Structures in italiano")),
        "meta_description": default_meta,
        "canonical": "https://liberating.it/",
        "active_nav": None,
        "has_path_nav": False,
        "home": {
            "h1": "Cambia il modo in cui il tuo team lavora, decide e crea",
            "hero_subtitle": f"{n} formati pratici per riunioni e workshop. Scegli una struttura e provala domani.",
            "toc_items": [
                {"text": f"{n} schede con passaggi, tempi e consigli pratici"},
                {"text": "Percorsi guidati per iniziare subito", "url": "/complessita/iniziare-subito/"},
                {"text": "I 10 principi dietro ogni struttura", "url": "/10-principi-fondamentali-liberating-structures/"},
            ],
            "sections": [
                {
                    "title": "Il problema che conosci",
                    "bullets": [
                        "Riunioni che non finiscono mai e non portano da nessuna parte",
                        "Decisioni prese a porte chiuse, poi presentate al team",
                        "Persone introverse che non dicono mai la loro",
                        "Workshop costosi che producono post-it e poco altro",
                    ],
                },
                {
                    "title": "Cosa sono (in due righe)",
                    "body": "Ogni riunione ha una struttura nascosta: chi parla, per quanto, in che ordine. Le Liberating Structures ti danno formati pronti per far parlare tutti, generare idee, prendere decisioni.",
                },
                {
                    "title": "Tre cose che le rendono diverse",
                    "features": [
                        {"title": "Inclusione", "body": "Ogni struttura prevede un turno per ogni persona, anche in gruppi grandi."},
                        {"title": "Semplicita'", "prefix": "La piu' usata,", "link": {"label": "1-2-4-All", "url": "/structures/1-2-4-all/"}, "body": "si spiega in un minuto e si fa in quindici."},
                        {"title": "Autonomia", "body": "Prendi, adatti, combini. Nessun dogma metodologico."},
                    ],
                },
            ],
            "start_links": [
                {"name": "1-2-4-All", "url": "/structures/1-2-4-all/", "reason": "far emergere idee da tutti in 15 minuti"},
                {"name": "Impromptu Networking", "url": "/structures/impromptu-networking/", "reason": "rompere il ghiaccio in 10 minuti"},
                {
                    "name": "Heard, Seen, Respected (HSR)",
                    "url": "/structures/heard-seen-respected-hsr/",
                    "reason": "quando qualcuno non si sente ascoltato o rispettato",
                },
                {"name": "What, So What, Now What?", "url": "/structures/w3-what-so-what-now-what/", "reason": "capire cosa fare dopo una discussione"},
                {"name": "15% Solutions", "url": "/structures/15-solutions/", "reason": "trovare cosa puoi fare subito"},
            ],
            "leggi_anche": [
                {"name": "I 10 principi fondamentali", "url": "/10-principi-fondamentali-liberating-structures/", "reason": "le regole d'oro dietro ogni struttura"},
                {"name": "Catalogo completo", "url": "/structures/", "reason": "tutte le strutture, filtrabili"},
                {"name": "Per iniziare subito", "url": "/complessita/iniziare-subito/", "reason": "percorso guidato per chi parte da zero"},
            ],
            "cta_text": "Scegli 1-2-4-All, prepara una domanda concreta per il tuo team e provaci nella riunione di domani.",
            "cta_url": "/structures/1-2-4-all/",
            "cta_label": "Prova 1-2-4-All domani",
            "definition": (
                "Le Liberating Structures sono formati di facilitazione con passaggi e tempi definiti "
                "per far partecipare tutti in riunioni e workshop, anche senza esperienza come facilitatore."
            ),
        },
        "jsonld": merge_jsonld(
            build_organization_jsonld(),
            build_website_jsonld(default_meta),
            build_faq_jsonld(home_faq),
        ),
        "home_faq": home_faq,
    }
    render(env, "home.html", out_root / "index.html", out_root, **ctx)


def build_principles(env: Environment, content_root: Path, out_root: Path, structure_count: int) -> None:
    principles_path = content_root.parent / "v1" / "pagine" / "10-principi-fondamentali-liberating-structures.md"
    if not principles_path.exists():
        principles_path = content_root / "pagine" / "10-principi-fondamentali-liberating-structures.md"

    faq = build_principles_faq(structure_count)

    if principles_path.exists():
        meta, _ = parse_frontmatter(principles_path.read_text(encoding="utf-8"))
        editorial = apply_structure_counts(parse_editorial_page(principles_path, faq), structure_count)
        editorial["faq"] = faq
        page_title = format_page_title(meta.get("title", "I 10 principi fondamentali"))
        meta_description = normalize_structure_count_text(
            meta.get(
                "meta_description",
                "Le regole d'oro dietro ogni Liberating Structure: inclusione, distribuzione, semplicita' e altro.",
            ),
            structure_count,
        )
    else:
        meta = {}
        page_title = format_page_title("I 10 principi fondamentali")
        meta_description = (
            "Le regole d'oro dietro ogni Liberating Structure: inclusione, distribuzione, semplicita' e altro."
        )
        editorial = {
            "h1": "I 10 principi fondamentali delle Liberating Structures",
            "lead": "Ogni struttura si regge su principi semplici. Capirli ti aiuta a usarle meglio e ad adattarle al tuo contesto.",
            "sections": [
                {"title": "Includere chi per tipologia di riunione resta fuori", "body": "Progetta turni e passaggi in cui ogni voce ha spazio, non solo chi parla di piu'."},
                {"title": "Distribuire la partecipazione", "body": "Evita il ping-pong plenario. Usa coppie, gruppi piccoli e passaggi individuali."},
                {"title": "Combinare attivazione e liberazione", "body": "Strutture brevi che aprono spazio a conversazioni piu' profonde."},
                {"title": "Rendere semplice cio' che e' complesso", "body": "Pochi passaggi chiari, tempi espliciti, materiali minimi."},
            ],
            "leggi_anche": [
                {"name": "Catalogo strutture", "url": "/structures/", "reason": "applica i principi in pratica"},
                {"name": "Per iniziare subito", "url": "/complessita/iniziare-subito/", "reason": "percorso guidato per chi parte da zero"},
            ],
            "faq": faq,
            "cta_text": "Scegli un principio che ti sta piu' a cuore. Poi trova la struttura collegata e provaci nella prossima riunione.",
            "cta_url": "/structures/1-2-4-all/",
            "cta_label": "Prova 1-2-4-All domani",
        }

    ctx = {
        "page_type": "editorial",
        "page_title": page_title,
        "meta_description": meta_description,
        "canonical": "https://liberating.it/10-principi-fondamentali-liberating-structures/",
        "active_nav": "principles",
        "has_path_nav": False,
        "breadcrumbs": [
            {"name": "Home", "url": "/"},
            {"name": "I 10 principi fondamentali", "url": None},
        ],
        "editorial": editorial,
        "jsonld": page_jsonld(
            [
                {"name": "Home", "url": "/"},
                {"name": "I 10 principi fondamentali", "url": None},
            ],
            "https://liberating.it/10-principi-fondamentali-liberating-structures/",
            build_faq_jsonld(editorial.get("faq") or faq),
        ),
    }
    render(env, "editorial.html", out_root / "10-principi-fondamentali-liberating-structures" / "index.html", out_root, **ctx)


def build_legal_pages(env: Environment, content_root: Path, out_root: Path) -> None:
    pages_root = content_root.parent / "v1" / "pagine"
    for slug in LEGAL_PAGES:
        path = pages_root / f"{slug}.md"
        if not path.exists():
            continue
        meta, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        legal = parse_legal_page(path)
        page_title = format_page_title(meta.get("title", legal["h1"]))
        meta_description = meta.get("meta_description", legal["lead"])
        canonical = f"https://liberating.it/{slug}/"
        breadcrumbs = [
            {"name": "Home", "url": "/"},
            {"name": legal["h1"], "url": None},
        ]
        ctx = {
            "page_type": "legal",
            "page_title": page_title,
            "meta_description": meta_description,
            "canonical": canonical,
            "active_nav": None,
            "has_path_nav": False,
            "breadcrumbs": breadcrumbs,
            "legal": legal,
            "jsonld": page_jsonld(breadcrumbs, canonical),
        }
        render(env, "legal.html", out_root / slug / "index.html", out_root, **ctx)


def build_catalog(env: Environment, structures: list[dict], out_root: Path, display_icons: dict[str, str], default_icon: str) -> None:
    cards = [
        {
            "slug": s["slug"],
            "title": s["title"],
            "brief": truncate_text(s["brief_plain"], 160),
            "difficolta": s["difficolta"],
            "durata": s["durata"],
            "difficolta_slug": s["difficolta_slug"],
            "complessita_slug": s["complessita_slug"],
            "durata_slug": s["durata_slug"],
            "fase_slug": s["fase_slug"],
            "icon": display_icons.get(s["slug"], default_icon),
        }
        for s in structures
    ]
    breadcrumbs = [
        {"name": "Home", "url": "/"},
        {"name": "Le strutture", "url": None},
    ]
    canonical = "https://liberating.it/structures/"
    ctx = {
        "page_type": "catalog",
        "page_title": format_page_title("Le strutture"),
        "meta_description": "Catalogo delle Liberating Structures: filtra per difficoltà, durata, fase e percorso.",
        "canonical": canonical,
        "active_nav": "structures",
        "has_path_nav": False,
        "breadcrumbs": breadcrumbs,
        "structures": cards,
        "fase_filters": FASE_FILTER_OPTIONS,
        "jsonld": page_jsonld(
            breadcrumbs,
            canonical,
            build_collection_jsonld(
                "Le strutture",
                "Catalogo delle Liberating Structures: filtra per difficoltà, durata, fase e percorso.",
                canonical,
                len(cards),
            ),
            build_item_list_jsonld("Catalogo Liberating Structures", cards, canonical),
        ),
    }
    render(env, "catalog.html", out_root / "structures" / "index.html", out_root, **ctx)


def build_structures(
    env: Environment,
    structures: list[dict],
    out_root: Path,
    icons_full: dict[str, str],
    display_icons: dict[str, str],
    default_icon: str,
    default_icon_full: str,
) -> None:
    for s in structures:
        s["icon"] = display_icons.get(s["slug"], default_icon)
        s["icon_full"] = icons_full.get(s["slug"]) or default_icon_full
        reading_mins = structure_reading_minutes(s)
        ctx = {
            "page_type": "structure",
            "page_title": format_page_title(s["title"]),
            "meta_description": s["meta_description"],
            "canonical": s["url"],
            "og_type": "article",
            "og_image": structure_og_image_url(s, out_root),
            "og_image_alt": f"{s['h1']}: Liberating Structure in italiano",
            "reading_time_label": format_reading_time_label(reading_mins),
            "share": build_share_links(s["url"], s["h1"]),
            "active_nav": "structures",
            "has_path_nav": bool(s["path_prev"] or s["path_next"]),
            "structure": s,
            "breadcrumbs": s["breadcrumbs"],
            "jsonld": page_jsonld(
                s["breadcrumbs"],
                s["url"],
                build_faq_jsonld(s["faq"]),
                build_howto_jsonld(s),
                build_defined_term_jsonld(s),
            ),
        }
        render(env, "structure.html", out_root / "structures" / s["slug"] / "index.html", out_root, **ctx)


def build_taxonomy_hubs(
    env: Environment,
    structures: list[dict],
    out_root: Path,
    display_icons: dict[str, str],
    default_icon: str,
) -> None:
    for slug, hub in HUBS_COMPLESSITA.items():
        filt_key, filt_val = hub["filter"]
        filtered = [s for s in structures if s[f"{filt_key}_slug"] == filt_val]
        path_list = None
        intro = hub["intro"]
        if slug == "iniziare-subito":
            intro = (
                "Il percorso Per iniziare subito elenca cinque Liberating Structures facili in sequenza: "
                "Impromptu Networking, 1-2-4-All, What So What Now What?, 15% Solutions e Troika Consulting. "
                f"Qui trovi anche le altre {len(filtered)} strutture classificate per chi parte da zero."
            )
        if slug == "team-rodati":
            intro = (
                f"Le Liberating Structures per team rodati sono {len(filtered)} formati intermedi: "
                "il gruppo conosce gia' turni e plenaria e vuole conversazioni piu' profonde o prioritizzazione "
                "su molte idee. TRIZ, 25/10 Crowd Sourcing e Drawing Together sono il punto di partenza piu' usato."
            )
        if hub.get("path_list"):
            path_list = [{"slug": ps, "name": DISPLAY_NAMES.get(ps, ps)} for ps in PATH_ORDER]
        _render_hub(
            env,
            out_root,
            f"complessita/{slug}",
            hub,
            filtered,
            path_list=path_list,
            icons=display_icons,
            intro_override=intro,
            default_icon=default_icon,
        )

    for slug, hub in HUBS_DIFFICOLTA.items():
        filtered = [s for s in structures if s["difficolta_slug"] == slug]
        intro_override = None
        if slug == "intermedia":
            intro_override = (
                f"Le Liberating Structures intermedie sono {len(filtered)} formati con piu' passaggi "
                "delle versioni facili: servono quando il gruppo conosce gia' turni e plenaria. "
                "TRIZ, Ecocycle Planning e Wicked Questions sono il punto di partenza piu' usato."
            )
        _render_hub(
            env,
            out_root,
            f"difficolta/{slug}",
            hub,
            filtered,
            icons=display_icons,
            intro_override=intro_override,
            default_icon=default_icon,
        )

    for slug, hub in HUBS_DURATA.items():
        filtered = [s for s in structures if s["durata_slug"] == slug]
        _render_hub(
            env, out_root, f"durata/{slug}", hub, filtered, icons=display_icons, default_icon=default_icon,
        )

    for slug, hub in HUBS_FASE.items():
        filtered = [s for s in structures if s["fase_slug"] == slug]
        _render_hub(
            env, out_root, f"design-thinking/{slug}", hub, filtered, icons=display_icons, default_icon=default_icon,
        )


def _hub_cards(structures: list[dict], icons: dict[str, str] | None, default_icon: str) -> list[dict]:
    icons = icons or {}
    return [
        {
            "slug": s["slug"],
            "title": s["title"],
            "brief": truncate_text(s["brief_plain"], 140),
            "difficolta": s["difficolta"],
            "durata": s["durata"],
            "difficolta_slug": s["difficolta_slug"],
            "durata_slug": s["durata_slug"],
            "icon": icons.get(s["slug"], default_icon),
        }
        for s in structures
    ]


def _render_hub(
    env,
    out_root,
    url_path,
    hub: dict,
    structures,
    *,
    path_list=None,
    icons=None,
    intro_override=None,
    breadcrumbs: list[dict] | None = None,
    active_nav=None,
    active_per_bisogno=None,
    default_icon: str = "",
):
    title = hub["title"]
    intro = intro_override or hub["intro"]
    faq = hub.get("faq") or []
    cards = _hub_cards(structures, icons, default_icon)
    canonical = f"https://liberating.it/{url_path}/"
    seo_description = format_meta_description(hub_meta_description(hub))
    if breadcrumbs is None:
        breadcrumbs = [
            {"name": "Home", "url": "/"},
            {"name": "Le strutture", "url": "/structures/"},
            {"name": title, "url": None},
        ]
    ctx = {
        "page_type": "hub",
        "page_title": hub_page_title(hub),
        "meta_description": seo_description,
        "canonical": canonical,
        "active_nav": active_nav,
        "active_per_bisogno": active_per_bisogno,
        "has_path_nav": False,
        "breadcrumbs": breadcrumbs,
        "hub": {"title": title, "intro": intro, "path_list": path_list, "faq": faq},
        "structures": cards,
        "jsonld": page_jsonld(
            breadcrumbs,
            canonical,
            build_collection_jsonld(title, seo_description, canonical, len(cards)),
            build_item_list_jsonld(title, cards, canonical),
            build_faq_jsonld(faq),
        ),
    }
    render(env, "hub.html", out_root / url_path / "index.html", out_root, **ctx)


def build_per_bisogno(
    env: Environment,
    structures: list[dict],
    out_root: Path,
    display_icons: dict[str, str],
    default_icon: str,
) -> None:
    by_slug = {s["slug"]: s for s in structures}
    hubs = []
    for slug, hub in PER_BISOGNO.items():
        hubs.append({
            "url": f"/per-bisogno/{slug}/",
            "title": hub["title"],
            "intro": hub["intro"],
            "examples": hub["examples"],
        })
        filtered = [by_slug[s] for s in hub["slugs"] if s in by_slug]
        _render_hub(
            env,
            out_root,
            f"per-bisogno/{slug}",
            hub,
            filtered,
            icons=display_icons,
            breadcrumbs=[
                {"name": "Home", "url": "/"},
                {"name": "Per bisogno", "url": "/per-bisogno/"},
                {"name": hub["title"], "url": None},
            ],
            active_nav="per-bisogno",
            active_per_bisogno=slug,
            default_icon=default_icon,
        )

    ctx = {
        "page_type": "per-bisogno",
        "page_title": format_page_title("Per bisogno"),
        "meta_description": PER_BISOGNO_INDEX_META,
        "canonical": "https://liberating.it/per-bisogno/",
        "active_nav": "per-bisogno",
        "has_path_nav": False,
        "hubs": hubs,
        "faq": PER_BISOGNO_INDEX_FAQ,
        "breadcrumbs": [
            {"name": "Home", "url": "/"},
            {"name": "Per bisogno", "url": None},
        ],
        "jsonld": page_jsonld(
            [{"name": "Home", "url": "/"}, {"name": "Per bisogno", "url": None}],
            "https://liberating.it/per-bisogno/",
            build_collection_jsonld(
                "Per bisogno",
                PER_BISOGNO_INDEX_META,
                "https://liberating.it/per-bisogno/",
                len(hubs),
            ),
            build_faq_jsonld(PER_BISOGNO_INDEX_FAQ),
        ),
    }
    render(env, "per-bisogno-index.html", out_root / "per-bisogno" / "index.html", out_root, **ctx)


def write_index_json(structures: list[dict], out_root: Path) -> None:
    data = {
      "structures": [
          {
              "slug": s["slug"],
              "title": s["title"],
              "brief": s["brief_plain"],
              "difficolta": s["difficolta_slug"],
              "complessita": s["complessita_slug"],
              "durata": s["durata_slug"],
              "fase": s["fase_slug"],
              "url": f"/structures/{s['slug']}/",
              "sort_order": s["sort_order"],
          }
          for s in structures
      ],
      "path_order": PATH_ORDER,
    }
    (out_root / "structures" / "index.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def path_lastmod(path: Path | None, fallback: str) -> str:
    if path and path.is_file():
        return datetime.fromtimestamp(path.stat().st_mtime).date().isoformat()
    return fallback


def resolve_editorial_path(content_root: Path, name: str) -> Path | None:
    for candidate in (
        content_root.parent / "v1" / "pagine" / name,
        content_root / "pagine" / name,
    ):
        if candidate.is_file():
            return candidate
    return None


def write_sitemap(structures: list[dict], out_root: Path, *, content_root: Path | None = None) -> None:
    from datetime import date

    build_date = date.today().isoformat()
    url_lastmod: dict[str, str] = {}

    if content_root:
        home = resolve_editorial_path(content_root, "home.md")
        url_lastmod[f"{SITE_ORIGIN}/"] = path_lastmod(home, build_date)
        principles = resolve_editorial_path(content_root, "10-principi-fondamentali-liberating-structures.md")
        url_lastmod[f"{SITE_ORIGIN}/10-principi-fondamentali-liberating-structures/"] = path_lastmod(
            principles, build_date
        )
    else:
        url_lastmod[f"{SITE_ORIGIN}/"] = build_date
        url_lastmod[f"{SITE_ORIGIN}/10-principi-fondamentali-liberating-structures/"] = build_date

    url_lastmod[f"{SITE_ORIGIN}/structures/"] = build_date
    url_lastmod[f"{SITE_ORIGIN}/per-bisogno/"] = build_date
    if content_root:
        for slug in LEGAL_PAGES:
            legal_path = resolve_editorial_path(content_root, f"{slug}.md")
            url_lastmod[f"{SITE_ORIGIN}/{slug}/"] = path_lastmod(legal_path, build_date)
    else:
        for slug in LEGAL_PAGES:
            url_lastmod[f"{SITE_ORIGIN}/{slug}/"] = build_date
    for slug in HUBS_COMPLESSITA:
        url_lastmod[f"{SITE_ORIGIN}/complessita/{slug}/"] = build_date
    for slug in HUBS_DIFFICOLTA:
        url_lastmod[f"{SITE_ORIGIN}/difficolta/{slug}/"] = build_date
    for slug in HUBS_DURATA:
        url_lastmod[f"{SITE_ORIGIN}/durata/{slug}/"] = build_date
    for slug in HUBS_FASE:
        url_lastmod[f"{SITE_ORIGIN}/design-thinking/{slug}/"] = build_date
    for slug in PER_BISOGNO:
        url_lastmod[f"{SITE_ORIGIN}/per-bisogno/{slug}/"] = build_date
    for s in structures:
        url_lastmod[f"{SITE_ORIGIN}/structures/{s['slug']}/"] = s.get("source_lastmod", build_date)

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for url, lastmod in url_lastmod.items():
        lines.append("  <url>")
        lines.append(f"    <loc>{url}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append("  </url>")
    lines.append("</urlset>")
    (out_root / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_robots(out_root: Path) -> None:
    (out_root / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n"
        f"# Panoramica per crawler AI: {SITE_ORIGIN}/llms.txt\n\n"
        f"Sitemap: {SITE_ORIGIN}/sitemap.xml\n",
        encoding="utf-8",
    )


def _llms_structure_line(by_slug: dict[str, dict], slug: str) -> str | None:
    item = by_slug.get(slug)
    if not item:
        return None
    brief = truncate_text(item["brief_plain"], 140)
    return f"- [{item['title']}]({SITE_ORIGIN}/structures/{slug}/): {brief}"


def write_llms_txt(structures: list[dict], out_root: Path) -> None:
    by_slug = {s["slug"]: s for s in structures}
    lines = [
        "# Liberating.it",
        "",
        (
            "> Liberating.it e' la guida pratica in italiano alle Liberating Structures: "
            f"{len(structures)} schede con passaggi, tempi e FAQ per riunioni e workshop."
        ),
        "",
        "## Cos'e' una Liberating Structure?",
        "",
        (
            "Le Liberating Structures sono formati di facilitazione con passaggi e tempi definiti "
            "per far partecipare tutti in riunioni e workshop, in presenza o online. "
            f"Su liberating.it trovi {len(structures)} schede in italiano con definizione, passaggi numerati e FAQ."
        ),
        "",
        "## Percorso per iniziare subito",
        "",
        (
            f"Ordine consigliato per chi prova per la prima volta "
            f"([hub completo]({SITE_ORIGIN}/complessita/iniziare-subito/)):"
        ),
        "",
    ]
    for i, slug in enumerate(PATH_ORDER, start=1):
        line = _llms_structure_line(by_slug, slug)
        if line:
            lines.append(f"{i}. {line.lstrip('- ')}")
    lines.extend(
        [
            "",
            "## Pagine principali",
            "",
        f"- [Home]({SITE_ORIGIN}/): introduzione alle Liberating Structures in italiano",
        (
            f"- [Catalogo strutture]({SITE_ORIGIN}/structures/): "
            f"{len(structures)} strutture con passaggi, tempi e consigli pratici"
        ),
        (
            f"- [I 10 principi fondamentali]({SITE_ORIGIN}/10-principi-fondamentali-liberating-structures/): "
            "regole d'oro della facilitazione partecipativa"
        ),
        f"- [Per bisogno]({SITE_ORIGIN}/per-bisogno/): percorsi per obiettivo (idee, decisioni, strategia)",
        (
            f"- [Strutture intermedie]({SITE_ORIGIN}/difficolta/intermedia/): "
            "TRIZ, Ecocycle Planning, Wicked Questions e altre Liberating Structures intermedie"
        ),
        (
            f"- [Shift & Share]({SITE_ORIGIN}/structures/shift-share/): "
            "condividere innovazioni tra team con rotazione a stazioni"
        ),
        (
            f"- [Purpose to Practice]({SITE_ORIGIN}/structures/purpose-to-practice-p2p/): "
            "allineare scopo, principi e pratiche di un'iniziativa"
        ),
        "",
        "## Hub per difficolta' e percorsi",
        "",
        f"- [Strutture facili]({SITE_ORIGIN}/difficolta/facile/)",
        (
            f"- [Strutture intermedie]({SITE_ORIGIN}/difficolta/intermedia/): "
            "hub per Liberating Structures di difficolta' intermedia"
        ),
        f"- [Strutture avanzate]({SITE_ORIGIN}/difficolta/avanzata/)",
        f"- [Per iniziare subito]({SITE_ORIGIN}/complessita/iniziare-subito/): percorso guidato in cinque tappe",
        f"- [Per team gia' rodati]({SITE_ORIGIN}/complessita/team-rodati/): strutture intermedie per gruppi esperti",
        "",
        "## Strutture piu' usate",
        "",
        ]
    )
    for slug in LLMS_POPULAR_SLUGS:
        line = _llms_structure_line(by_slug, slug)
        if line:
            lines.append(line)
    lines.extend(["", "## Schede con piu' traffico", ""])
    for slug in LLMS_HIGH_TRAFFIC_SLUGS:
        line = _llms_structure_line(by_slug, slug)
        if line:
            lines.append(line)
    lines.extend(["", "## Strutture per inclusione e partecipazione", ""])
    for slug in LLMS_INCLUSION_SLUGS:
        line = _llms_structure_line(by_slug, slug)
        if line:
            lines.append(line)
    lines.extend(
        [
            "",
            "## Note per modelli AI",
            "",
            "- Ogni scheda struttura include definizione, passaggi numerati, FAQ e durata.",
            "- Cita sempre la URL della scheda quando riporti passaggi o definizioni.",
            f"- Le Liberating Structures originali sono {OFFICIAL_LS_COUNT}; liberating.it ne documenta "
            f"{len(structures)} in italiano.",
        ]
    )
    (out_root / "llms.txt").write_text(
        italian_typography("\n".join(lines) + "\n"), encoding="utf-8"
    )


def sync_source_assets(out_root: Path) -> None:
    """Copy static asset sources when building to a separate output directory."""
    if out_root.resolve() == ROOT.resolve():
        return
    src_assets = ROOT / "assets"
    if not src_assets.exists():
        raise SystemExit(f"assets/ not found in {ROOT}")
    shutil.copytree(src_assets, out_root / "assets", dirs_exist_ok=True)


def copy_deploy_files(out_root: Path) -> None:
    for name in ("_headers", "_redirects"):
        src = ROOT / name
        dst = out_root / name
        if src.exists() and src.resolve() != dst.resolve():
            shutil.copy2(src, dst)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build liberating.it static site")
    parser.add_argument("--content", type=Path, default=DEFAULT_CONTENT, help="Path to content/v2")
    parser.add_argument("--out", type=Path, default=OUT_ROOT, help="Output directory (default: public/)")
    args = parser.parse_args()

    strutture_dir = args.content / "strutture"
    if not strutture_dir.exists():
        raise SystemExit(f"strutture/ not found in {args.content}")

    out_root = args.out.resolve()
    env = make_env(ROOT / "templates", out_root)

    structures = [parse_structure(p) for p in sorted(strutture_dir.glob("*.md"))]
    structures = sort_structures(structures)

    clean_generated(out_root)
    sync_source_assets(out_root)
    css_manifest, css_inline = bundle_css(out_root)
    env.globals["css_inline"] = css_inline
    bundle_js(out_root)
    ensure_og_png(out_root)

    from generate_adaptation_icons import ensure_adaptation_icons

    ensure_adaptation_icons(out_root)
    ensure_favicon(out_root)
    icons_full = load_icon_manifest(out_root)
    display_icons, default_icon, default_icon_full = build_display_icons(out_root, icons_full)
    env.globals["default_structure_icon"] = default_icon

    build_home(env, args.content, out_root, len(structures))
    build_principles(env, args.content, out_root, len(structures))
    build_legal_pages(env, args.content, out_root)
    build_catalog(env, structures, out_root, display_icons, default_icon)
    build_structures(env, structures, out_root, icons_full, display_icons, default_icon, default_icon_full)
    clean_orphan_og_images(structures, out_root)
    build_taxonomy_hubs(env, structures, out_root, display_icons, default_icon)
    build_per_bisogno(env, structures, out_root, display_icons, default_icon)
    write_index_json(structures, out_root)
    write_sitemap(structures, out_root, content_root=args.content)
    write_robots(out_root)
    write_llms_txt(structures, out_root)
    copy_deploy_files(out_root)

    print(f"Built {len(structures)} structures -> {out_root}")
    print(f"CSS bundle: assets/{css_manifest['css']}")
    print(f"Open: {out_root / 'index.html'}")


if __name__ == "__main__":
    main()
