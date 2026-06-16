# Analisi SEO/GEO su richiesta

Usa questa guida quando l'utente chiede un quesito SEO o GEO **senza** riscrivere un contenuto: audit, priorita', confronti, gap, raccomandazioni strategiche.

**Regola base:** ogni affermazione numerica deve provenire da un file in [seo/](../../../seo/). Cita il file e, se utile, la riga o la keyword. Se i dati mancano, dillo esplicitamente.

---

## Workflow analitico (5 step)

### 1. Classifica la domanda

Identifica il tipo di quesito (tabella sotto). Se la domanda e' mista (es. "priorita' SEO e GEO per la home"), combina piu' tipi.

### 2. Seleziona le fonti

Leggi **solo** i file necessari. Non caricare tutto `seo/` se bastano 2 CSV.

### 3. Estrai i dati

Usa grep, ricerca nel file o lettura mirata. Per keyword specifiche, cerca in:
- `liberating.it_keyword_all.csv` (panoramica)
- CSV per-URL `*__all_keywords.csv` (dettaglio pagina)
- `liberating.it_LongTailKeywords.csv` (varianti e URL multiple)

### 4. Interpreta

Applica le soglie:

| Metrica | Soglia | Significato |
|---------|--------|-------------|
| `Pos` 1-3 | Forte | Mantieni, non cannibalizzare |
| `Pos` 4-20 | Opportunita' | Miglioramento realistico con ottimizzazione on-page |
| `Pos` 21-50 | Debole | Serve contenuto piu' forte o link interni |
| `Pos` 101 | Assente | Gap: non rankiamo |
| `Keyword Opportunity` >= 70 | Alta priorita' | Facile da guadagnare |
| `Volume` >= 100 | Rilevante | Impatto traffico significativo |
| `Menzioni AI` = 0 | Gap GEO | Pagina visibile ma non citata dalle AI |

### 5. Rispondi con struttura

Usa il template output sotto. Chiudi sempre con **raccomandazioni actionable** (max 3-5, ordinate per impatto).

---

## Routing: tipo domanda -> fonti

| Tipo domanda | Esempi | File principali |
|--------------|--------|-----------------|
| **Keyword pagina** | "Quali keyword rankano per 1-2-4-All?" | CSV per-URL, `keyword_all.csv` |
| **Keyword primaria** | "Quale keyword usare per TRIZ?" | CSV per-URL, `LongTailKeywords.csv`, cannibalization |
| **Cannibalizzazione** | "Stiamo competendo su liberating structures?" | `LongTailKeywords.csv`, `Cannibalization.xlsx`, `keyword_all.csv` |
| **Gap contenuto** | "Su cosa non rankiamo ma i competitor si'?" | `ContentGap.csv`, `OnPageSEO.csv`, `competitor.csv` |
| **Gap AI / GEO** | "Dove non siamo citati dalle AI?" | `ContentGap_AI.csv`, `MainPages.csv`, `PagesWithPotential.csv` (colonna Menzioni AI) |
| **Priorita' pagine** | "Quali pagine ottimizzare per prime?" | `PagesWithPotential.csv`, `PagesWithTrafficDown.csv`, `OnPageSEO.csv` |
| **Trend traffico** | "Quali pagine stanno calando?" | `PagesWithTrafficDown.csv`, `PagesWithTrafficUp.csv`, `landing-pages-all_*.csv` |
| **Competitor** | "Chi rankia per facilitazione?" | `competitor.csv`, `monitored.csv` |
| **Cluster** | "Quale URL dovrebbe coprire liberatingstructures?" | `clusters_keyword.csv`, `keywords_cluster.csv` |
| **FAQ / domande AI** | "Quali domande coprire per agile?" | `questions_liberatingstructures.txt`, CSV per-URL (SERP Features) |
| **Audit pagina** | "Audit SEO/GEO completo di /structures/triz/" | CSV per-URL + `keyword_all` + `questions` + `PagesWithPotential` |
| **Confronto pagine** | "Home vs difficolta/intermedia: dove conviene puntare?" | CSV entrambe le URL + `PagesWithPotential` |

---

## Template output analisi

Adatta le sezioni al quesito; non includere sezioni vuote.

```markdown
## [Titolo domanda]

### Sintesi
[2-3 frasi: risposta diretta con il dato piu' rilevante]

### Dati (fonte SeoZoom)
| Keyword / URL | Pos | Volume | Opportunity | Traffico stim. | Fonte |
|---------------|-----|--------|-------------|----------------|-------|
| ... | ... | ... | ... | ... | `nome_file.csv` |

### Interpretazione
[Cosa significano i numeri per liberating.it. Niente generici.]

### Raccomandazioni
1. [Azione concreta] — impatto: alto/medio/basso
2. ...
3. ...

### Limiti
[Dati mancanti, export non disponibile per quella pagina, date degli export]
```

Per audit completi aggiungi:

```markdown
### SEO
- Keyword primaria consigliata: ...
- Secondarie: ...
- Cannibalizzazione: si/no, con ...
- SERP Features attive: ...

### GEO
- Menzioni AI attuali: ...
- Domande da coprire in FAQ: ...
- Definizione citabile: presente/assente
- Gap entita' (ContentGap AI): ...
```

---

## Quesiti frequenti: come rispondere

### "Qual e' la keyword primaria per [pagina]?"

1. Trova CSV per-URL dal campo `url` o dal path.
2. Ordina per `Volume` decrescente, filtra `Intent` Informational.
3. Escludi keyword gia' target di altra pagina (Pos <= 30 in `LongTailKeywords.csv` su URL diversa).
4. Proponi 1 primaria + 2-4 secondarie con Opportunity >= 70.

### "Dove abbiamo cannibalizzazione?"

1. Cerca la keyword in `liberating.it_LongTailKeywords.csv`: piu' righe con URL diverse = cannibalizzazione.
2. Incrocia con `liberating_it_Cannibalization.xlsx` se disponibile.
3. Indica quale pagina dovrebbe "possedere" la keyword (volume piu' alto, Pos migliore, contenuto piu' pertinente).

### "Quali pagine ottimizzare per prime?"

1. `PagesWithPotential.csv`: ordina per `Traffico Potenziale` decrescente.
2. Incrocia con `PagesWithTrafficDown.csv` (urgenza).
3. Filtra pagine con `Menzioni AI` = 0 se la priorita' e' GEO.
4. Top 5 con motivazione per ciascuna.

### "Su quali keyword non rankiamo?"

1. `OnPageSEO.csv`: Pos 101, ordina per `Volume ricerca`.
2. `ContentGap.csv`: keyword competitor assenti su liberating.it.
3. Distingui: keyword brand LS (priorita' alta) vs generiche irrilevanti (priorita' bassa).

### "Come siamo posizionati vs competitor?"

1. `competitor.csv`: cerca keyword, confronta colonne Posizione per dominio.
2. Evidenzia dove liberating.it e' 101 e un competitor e' <= 10.
3. Indica URL competitor che rankia.

### "Quali domande FAQ coprire per [struttura]?"

1. Grep in `questions_liberatingstructures.txt` su nome struttura / metodo.
2. Verifica SERP Features nel CSV per-URL ("Box Domande frequenti").
3. Elenca 2-4 domande con priorita' (volume keyword associata se presente nel CSV pagina).

### "Audit SEO/GEO di [URL]"

Esegui in sequenza:
1. CSV per-URL: keyword, posizioni, SERP Features
2. `keyword_all.csv` filtrato per URL: storico e intent
3. Cannibalizzazione per keyword primaria candidata
4. `PagesWithPotential` / `MainPages`: traffico potenziale, Menzioni AI
5. `questions_liberatingstructures.txt`: FAQ mancanti
6. Confronto title/meta attuali in `content/` vs keyword consigliata

---

## Comandi utili per estrarre dati

Cerca keyword in tutti i CSV:

```bash
grep -i "triz" seo/*.csv | head -20
```

Keyword per URL specifica:

```bash
grep "liberating.it/structures/triz" seo/liberating.it_keyword_all.csv
```

Pagine con piu' traffico potenziale:

```bash
head -10 seo/liberating_it_PagesWithPotential.csv
```

Domande FAQ per struttura:

```bash
grep -i "1 2 4" seo/questions_liberatingstructures.txt
```

---

## Errori da evitare in analisi

- **Inventare numeri** se il CSV non ha la riga: dì "dati non disponibili per questa pagina".
- **Consigliare keyword irrilevanti** da ContentGap generico (es. "influencer" per una scheda LS).
- **Ignorare cannibalizzazione**: due pagine che competono sulla stessa keyword indeboliscono entrambe.
- **Confondere SEO e GEO**: rankare su Google non implica citazione nelle AI; controlla sempre `Menzioni AI`.
- **Raccomandazioni vaghe**: "migliora il contenuto" no; "riscrivi title con keyword X, aggiungi FAQ su Y" si'.

---

## Checklist analisi

- [ ] Tipo domanda identificato
- [ ] File SeoZoom letti (solo quelli pertinenti)
- [ ] Numeri citati con fonte file
- [ ] Cannibalizzazione verificata se si propone keyword primaria
- [ ] Distinzione SEO vs GEO chiara nella risposta
- [ ] Raccomandazioni actionable e ordinate per impatto
- [ ] Limiti e dati mancanti esplicitati
