---
name: SEO GEO specialist agent
overview: Creo un "agente" SEO/GEO per liberating.it come skill Cursor (know-how completo sui dati SeoZoom in seo/ e ottimizzazione per motori di ricerca + AI generativa), piu' una rule auto-attivata sui contenuti che la fa scattare a ogni riscrittura e la collega alla skill liberating-tone-of-voice.
todos:
  - id: skill
    content: Creare .cursor/skills/seo-geo-specialist/SKILL.md (workflow SEO+GEO, mappa CSV, blocchi GEO/FAQ, checklist) con frontmatter name+description auto-invocabile
    status: completed
  - id: reference
    content: Creare .cursor/skills/seo-geo-specialist/dati-seozoom.md con glossario di ogni file/colonna SeoZoom e come usarlo
    status: completed
  - id: rule
    content: Creare .cursor/rules/seo-geo-content.mdc con globs content/**/*.md che attiva insieme tone-of-voice e seo-geo-specialist a ogni riscrittura
    status: completed
  - id: crosslink
    content: Aggiornare liberating-tone-of-voice/SKILL.md con cross-link alla skill seo-geo-specialist (intro + voce in checklist)
    status: completed
isProject: false
---

# SEO GEO specialist per liberating.it

## Obiettivo
Un "agente" che padroneggia i dati SeoZoom in [seo/](seo/) e, a ogni riscrittura di contenuto, ottimizza title, meta, keyword e struttura sia per i motori di ricerca (SEO) sia per le AI generative (GEO). Lavora in coppia con [liberating-tone-of-voice](.cursor/skills/liberating-tone-of-voice/SKILL.md): la tone-of-voice governa stile e scrittura naturale, la nuova skill governa keyword e GEO.

Poiche' Cursor non permette di creare un subagent autonomo, l'agente e' realizzato con i primitivi disponibili: una **skill** (il know-how) + una **rule auto-attivata** (l'innesco a ogni riscrittura) + un **cross-link** dalla skill tone-of-voice.

## Come i dati mappano sui contenuti
- Pagina/scheda -> export SeoZoom per URL. Convenzione nome file: l'URL con `/` e `:` sostituiti da `_`.
  - `content/strutture/1-2-4-all.md` (url `https://liberating.it/structures/1-2-4-all/`) -> [seo/https___liberating.it_structures_1-2-4-all__all_keywords.csv](seo/https___liberating.it_structures_1-2-4-all__all_keywords.csv)
  - `content/pagine/home.md` (url `https://liberating.it/`) -> [seo/https___liberating.it__all_keywords.csv](seo/https___liberating.it__all_keywords.csv)
- File globali sempre rilevanti:
  - SEO: [liberating_it_OnPageSEO.csv](seo/liberating_it_OnPageSEO.csv), [liberating_it_ContentGap.csv](seo/liberating_it_ContentGap.csv), [liberating.it_LongTailKeywords.csv](seo/liberating.it_LongTailKeywords.csv), [liberating_it_PagesWithPotential.csv](seo/liberating_it_PagesWithPotential.csv), [https___liberating.it_competitor.csv](seo/https___liberating.it_competitor.csv), [https___liberating.it_monitored.csv](seo/https___liberating.it_monitored.csv)
  - GEO/AI: [liberating_it_ContentGap_AI.csv](seo/liberating_it_ContentGap_AI.csv), [questions_liberatingstructures.txt](seo/questions_liberatingstructures.txt), e la colonna `Menzioni AI` in MainPages/NewEntry/PagesWithPotential.
- Colonne chiave: `Volume`, `Pos`, `Keyword Difficulty`, `Keyword Opportunity` (alta = facile da guadagnare), `Intent`, `Traffico Stimato`, `SERP Features` (es. "Box Domande frequenti" -> serve FAQ).
- Gestione assenza dati: alcune schede (es. `4-2-1-storming`, `celebrity-interview`, `mad-tea`) non hanno CSV dedicato -> si usano solo i file globali, senza inventare numeri.

## 1. Nuova skill: `.cursor/skills/seo-geo-specialist/SKILL.md`
Frontmatter `name: seo-geo-specialist` + `description` in terza persona con trigger ("Ottimizza i contenuti di liberating.it per SEO e GEO usando i dati SeoZoom in seo/. Usare a ogni scrittura/riscrittura di pagine o schede struttura, e insieme alla skill liberating-tone-of-voice."). Nessun `disable-model-invocation` (auto-invocabile dal contesto). Corpo (<500 righe):
- Ruolo e principio di collaborazione: la tone-of-voice ha l'ultima parola sullo stile; nessuna scelta SEO/GEO puo' violare le regole anti-AION e le parole vietate.
- Workflow a step:
  1. Identifica il file CSV per-URL dal frontmatter `url` (convenzione nomi sopra).
  2. Leggi keyword del CSV + file globali; scegli 1 keyword primaria (volume/intent) + 2-4 secondarie/long-tail con `Keyword Opportunity` alta.
  3. Ottimizza `title` (<=60, keyword primaria naturale) e `meta_description` (<=155, beneficio + keyword) restando nel tono.
  4. Distribuisci le keyword: H1, primo paragrafo, un paio di H2, anchor interni descrittivi. Niente keyword stuffing.
  5. Cannibalizzazione: evita di puntare la stessa keyword di un'altra pagina (controlla [liberating_it_Cannibalization.xlsx](seo/liberating_it_Cannibalization.xlsx) e competitor/monitored).
- Blocco GEO (ottimizzazione per AI generativa):
  - Risposta "answer-first": prima frase di ogni sezione risponde direttamente alla domanda.
  - Definizione netta e autonoma del concetto (citabile fuori contesto).
  - Sezione FAQ con domande reali pescate da [questions_liberatingstructures.txt](seo/questions_liberatingstructures.txt) pertinenti alla pagina, risposte brevi e fattuali.
  - JSON-LD `FAQPage`/`HowTo` come blocco opzionale a fine file (commentato), allineato alle SERP Features.
  - Copertura entita'/sinonimi dai gap AI in [liberating_it_ContentGap_AI.csv](seo/liberating_it_ContentGap_AI.csv).
- Checklist finale SEO+GEO (title/meta nei limiti, keyword primaria in H1+intro, FAQ presente se SERP feature lo richiede, nessuna violazione tono/scrittura naturale, link interni descrittivi).
- File di dettaglio `dati-seozoom.md` (progressive disclosure): glossario di ogni CSV e colonna con come usarla; lo SKILL.md lo linka un solo livello.

## 2. Nuova rule: `.cursor/rules/seo-geo-content.mdc`
`globs: content/**/*.md`, `alwaysApply: false`. Contenuto breve (<50 righe): quando si crea o riscrive un file in `content/`, applica insieme due skill: prima `liberating-tone-of-voice` (stile e scrittura naturale), poi `seo-geo-specialist` (keyword + GEO), risolvendo eventuali conflitti a favore del tono di voce. Questo realizza l'innesco automatico "a ogni riscrittura".

## 3. Cross-link nella skill esistente
In [.cursor/skills/liberating-tone-of-voice/SKILL.md](.cursor/skills/liberating-tone-of-voice/SKILL.md): aggiungere una riga in testa ("Per SEO e GEO usa anche la skill `seo-geo-specialist`") e una voce in "Checklist finale" (keyword primaria e meta ottimizzate via SeoZoom; FAQ GEO se serve). Cosi' ogni invocazione della tone-of-voice richiama l'agente SEO/GEO.

## Note
- `title <=60` e `meta_description <=155` sono gia' nelle checklist esistenti: la nuova skill le rende operative coi dati reali.
- Nessuna modifica ai contenuti esistenti in questa fase: si creano solo skill + rule + cross-link. L'ottimizzazione dei singoli .md avverra' quando verranno riscritti.