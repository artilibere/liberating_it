# Dati SeoZoom - glossario e uso

Cartella: [seo/](../../../seo/). Export SeoZoom aggiornati a giugno 2026. Leggere i file pertinenti prima di ottimizzare un contenuto.

## Mappa URL -> file per-pagina

| URL pattern | File CSV |
|-------------|----------|
| `https://liberating.it/` | `https___liberating.it__all_keywords.csv` |
| `https://liberating.it/structures/{slug}/` | `https___liberating.it_structures_{slug}__all_keywords.csv` |
| `https://liberating.it/{slug}/` | `https___liberating.it_{slug}__all_keywords.csv` |
| `https://liberating.it/complessita/{hub}/` | `https___liberating.it_complessita_{hub}__all_keywords.csv` |
| `https://liberating.it/difficolta/{livello}/` | `https___liberating.it_difficolta_{livello}__all_keywords.csv` |
| `https://liberating.it/durata/{tipo}/` | `https___liberating.it_durata_{tipo}__all_keywords.csv` |

**Nota:** non tutte le schede in `content/strutture/` hanno un CSV dedicato. In assenza, usa i file globali.

---

## File per-pagina (`*__all_keywords.csv`)

Un file per URL indicizzata. Colonne tipiche:

| Colonna | Significato | Come usarla |
|---------|-------------|--------------|
| `Keyword` | Query di ricerca | Scegli primaria (volume alto) e secondarie |
| `Pos` | Posizione attuale su Google.it | Pos 1-3 = gia' forte, mantieni; Pos 4-20 = opportunita' miglioramento; Pos > 50 = gap |
| `Var` | Variazione posizione | Positivo = migliorato, negativo = peggiorato |
| `Volume` | Ricerche mensili stimate | Priorita' keyword |
| `Traffico Stimato` | Click stimati/mese | Valuta impatto reale |
| `Keyword Difficulty` | Difficolta' rankare (0-100) | Basso = piu' facile |
| `Keyword Opportunity` | Opportunita' di guadagno (0-100) | **>= 70 = priorita' alta** |

---

## File globali SEO

### `liberating.it_keyword_all.csv`
Tutte le keyword del dominio con storico mensile, intent, SERP features, URL di ranking.

| Colonna extra | Uso |
|---------------|-----|
| `Intent` | Informational, Commercial, Navigational, Transactional |
| `Feature` / `SERP Features` | "Box Domande frequenti" -> aggiungi FAQ; "Foto Carousel" -> considera immagini |
| `URL` | Quale pagina rankia per quella keyword |
| `Gen`...`Dic` | Stagionalita' mensile |

### `liberating.it_LongTailKeywords.csv`
Long-tail con posizione per URL. Utile per FAQ e sezioni specifiche. Controlla che la keyword long-tail non cannibalizzi un'altra pagina.

### `liberating_it_OnPageSEO.csv`
Keyword con volume ma Pos 101 (non rankiamo). Gap on-page: keyword da integrare nel contenuto esistente.

| Colonna | Uso |
|---------|-----|
| `Keyword` | Termine da coprire |
| `Volume ricerca` | Priorita' |
| `Pos` | 101 = assente dalle SERP |
| `URL` | Pagina target (spesso vuota = da assegnare) |

### `liberating_it_ContentGap.csv`
Keyword per cui i competitor rankiano ma liberating.it no. Volume e intent per nuovi contenuti o ampliamenti.

| Colonna | Uso |
|---------|-----|
| `Intent` | Tipo di contenuto da creare |
| `CPC` | Valore commerciale (alto = piu' competitivo) |
| `Volume ricerca` | Priorita' |

### `liberating_it_PagesWithPotential.csv`
Pagine con traffico potenziale non sfruttato.

| Colonna | Uso |
|---------|-----|
| `URL` | Pagina da ottimizzare per prima |
| `Traffico Potenziale` | Stima guadagno se ottimizzata |
| `Keyword` | Numero keyword rankanti |
| `Menzioni AI` | Citazioni da AI (0 = gap GEO) |

### `liberating_it_PagesWithMoreKeywords.csv`
Pagine che rankiano per piu' keyword del previsto. Verifica coerenza contenuto.

### `liberating_it_PagesWithTrafficUp.csv` / `PagesWithTrafficDown.csv`
Trend traffico. Priorita' a pagine in calo per revisione contenuto.

### `liberating_it_MainPages.csv` / `NewEntry.csv`
Pagine principali e nuove entry in SERP. `Menzioni AI` per priorita' GEO.

### `liberating_it_Cannibalization.xlsx`
Keyword per cui piu' pagine del sito competono tra loro. Evita di rafforzare la pagina sbagliata.

### `https___liberating.it_competitor.csv`
Confronto posizioni vs competitor (liberatingstructures.it, facilitazionemaieutica.it, agileway.it, ecc.) per keyword ad alto volume.

| Colonna | Uso |
|---------|-----|
| `Keyword` | Termine competitivo |
| `Volume` | Priorita' |
| `{dominio} Posizione` | Pos competitor; 101 = non rankia |
| `{dominio} URL` | Pagina competitor che rankia |

### `https___liberating.it_monitored.csv`
Keyword monitorate con andamento storico, SERP features, tags.

| Colonna | Uso |
|---------|-----|
| `Andamento` | Storico posizioni (date) |
| `SERP Features` | Feature attive in SERP |
| `Tags` | Etichette custom SeoZoom |

### `clusters_keyword.csv` / `keywords_cluster.csv`
Cluster keyword per URL. Keyword principale del cluster e volume aggregato.

| Colonna | Uso |
|---------|-----|
| `Keyword Principale` | Termine hub del cluster |
| `Volume Totale` | Volume cluster |
| `Volume non ottenuto` | Traffico perso |
| `URL` | Pagina che dovrebbe coprire il cluster |

---

## File globali GEO / AI

### `liberating_it_ContentGap_AI.csv`
Gap di contenuto rilevanti per le AI generative. Keyword con intent Informational e volume alto non coperti.

| Colonna | Uso |
|---------|-----|
| `Keyword` | Entita' o tema da coprire |
| `Intent` | Preferisci Informational per GEO |
| `Keyword Opportunity` | Priorita' integrazione |

Integra entita' e sinonimi pertinenti nel corpo; non forzare keyword irrilevanti.

### `questions_liberatingstructures.txt`
Domande reali (inglese) che le persone e le AI pongono su Liberating Structures. Una domanda per riga.

**Uso:** seleziona 2-4 domande pertinenti alla pagina, traduci in italiano, rispondi in sezione FAQ answer-first.

Esempi di match:
- Scheda 1-2-4-All -> "What is the 1 2 4 all method?", "What is the 1 2 4 all icebreaker?"
- Scheda TRIZ -> "What is Triz liberating structures?", "What is the triz method liberating structures?"
- Pagina principi -> "What are the five elements of Liberating Structures?", "What are the principles of liberating structures?"

### Colonna `Menzioni AI`
Presente in MainPages, NewEntry, PagesWithPotential. Numero di citazioni del sito nelle risposte AI. **0 = priorita' GEO alta** per quella URL.

---

## File analytics (supporto prioritizzazione)

### `landing-pages-all_2026-05-18_2026-06-15.csv`
Landing page con sessioni e metriche GA (periodo indicato nel nome file).

### `exit-pages_2026-05-18_2026-06-15.csv`
Pagine di uscita. Utili per capire dove migliorare engagement e internal linking.

### `https___liberating.it_Page-Speed.csv`
Metriche PageSpeed. Non impatta direttamente keyword ma segnala pagine lente.

### `liberating_it_Social.csv`
Metriche social. Bassa priorita' per ottimizzazione contenuto.

---

## Colonne comuni - riferimento rapido

| Colonna | Range | Interpretazione |
|---------|-------|-----------------|
| `Keyword Difficulty` | 0-100 | Basso = facile rankare |
| `Keyword Opportunity` | 0-100 | **Alto = priorita'** |
| `Pos` / `Posizione` | 1-100+ | 1 = primo risultato; 101 = non in SERP |
| `Volume` / `Vol.` | 0+ | Ricerche/mese; 0 = trascurabile |
| `Intent` | testo | Informational = guide/FAQ; Commercial = confronto; Navigational = brand |
| `CPC` | euro | Valore commerciale keyword |
| `Traffico Stimato` | numero | Click/mese stimati |

---

## Ordine di lettura consigliato

Per ottimizzare una pagina:

1. CSV per-URL (`*__all_keywords.csv`)
2. `liberating.it_keyword_all.csv` (filtro per URL o keyword)
3. `questions_liberatingstructures.txt` (FAQ GEO)
4. `liberating_it_Cannibalization.xlsx` o `LongTailKeywords.csv` (anti-cannibalizzazione)
5. `liberating_it_ContentGap_AI.csv` (entita' GEO)
6. `PagesWithPotential.csv` o `MainPages.csv` (priorita' se la pagina e' strategica)
