# Materiali grafici mancanti — proposte di integrazione

Documento di riferimento per integrare worksheet e diagrammi ufficiali delle Liberating Structures nelle schede di liberating.it. Audit su [liberatingstructures.com](https://www.liberatingstructures.com/) (giugno 2026).

**Asset scaricati:** [`public/assets/worksheets/`](../public/assets/worksheets/) (18 file, manifest in `manifest.json`).  
**Script di aggiornamento:** [`scripts/fetch_ls_worksheets.py`](../scripts/fetch_ls_worksheets.py).

---

## 1. Scopo e criteri

### Cosa conta come materiale grafico essenziale

Un materiale e' **essenziale** quando, senza vederlo, il facilitatore non sa:

- cosa disegnare su lavagna o poster (template Ecocycle, matrice, bussola STAR);
- come disporre la sala (layout WINFY);
- quali simboli usare e con quale significato (Drawing Together).

**Non essenziali** (esclusi da questo documento come target di integrazione):

- slide «constellation» generiche in fondo a ogni pagina LS;
- illustrazioni dei 10 principi LS (file `*Color.png`);
- icone menu della struttura.

### Ambito

- **Incluso:** collateral ufficiale su liberatingstructures.com per le 41 schede nel repo.
- **Escluso:** adattamenti locali senza pagina LS (4-2-1-Storming, Mad Love, Liquid Courage, Pixies Reflection, Tiny Demons).

### Licenza e attribuzione

I worksheet restano proprieta' intellettuale di Liberating Structures (Henri Lipmanowicz, Keith McCandless e co-autori indicati nelle singole pagine). Su liberating.it vanno:

- copiati in locale (no hotlink al CDN Squarespace);
- citati con didascalia sotto ogni immagine;
- usati con finalita' educativa e attribuzione esplicita.

Formato didascalia obbligatorio:

```markdown
*Fonte: [Nome struttura](URL pagina LS) — Liberating Structures (Henri Lipmanowicz & Keith McCandless).*
```

---

## 2. Inventario completo (41 schede)

| Slug | Pagina LS | Worksheet essenziale | Priorita' | Asset in repo |
|------|-----------|---------------------|-----------|---------------|
| `1-2-4-all` | [1-2-4-all](https://www.liberatingstructures.com/1-2-4-all/) | Nessuno | — | — |
| `impromptu-networking` | [impromptu-networking](https://www.liberatingstructures.com/impromptu-networking/) | Nessuno | — | — |
| `w3-what-so-what-now-what` | [what-so-what-now-what](https://www.liberatingstructures.com/what-so-what-now-what/) | Nessuno | — | — |
| `15-solutions` | [15-percent-solutions](https://www.liberatingstructures.com/15-percent-solutions/) | Nessuno | — | — |
| `troika-consulting` | [troika-consulting](https://www.liberatingstructures.com/troika-consulting/) | Nessuno | — | — |
| `25-10-crowd-sourcing` | [25-10-crowdsourcing](https://www.liberatingstructures.com/25-10-crowdsourcing/) | Nessuno | — | — |
| `4-2-1-storming` | — | Escluso (adattamento locale) | Escluso | — |
| `9-whys` | [nine-whys](https://www.liberatingstructures.com/nine-whys/) | Nessuno | — | — |
| `agreement-certainty-matrix` | [agreement-and-certainty](https://www.liberatingstructures.com/agreement-and-certainty/) | Matrice + esempio | **P1** | Si |
| `appreciative-interviews-ai` | [appreciative-interviews](https://www.liberatingstructures.com/appreciative-interviews/) | Nessuno | — | — |
| `celebrity-interview` | [celebrity-interview](https://www.liberatingstructures.com/celebrity-interview/) | Nessuno | — | — |
| `conversation-cafe` | [conversation-cafe](https://www.liberatingstructures.com/conversation-cafe/) | Nessuno | — | — |
| `critical-uncertainties` | [critical-uncertainties](https://www.liberatingstructures.com/critical-uncertainties/) | Template 2x2 + esempio | **P1** | Si |
| `design-storyboards` | [design-storyboards](https://www.liberatingstructures.com/design-storyboards/) | Storyboard + Matchmaker | **P2** | Si |
| `discovery-action-dialogue-dad` | [discovery-and-action-dialogue](https://www.liberatingstructures.com/discovery-and-action-dialogue/) | Nessuno | — | — |
| `drawing-together` | [drawing-together](https://www.liberatingstructures.com/drawing-together/) | Handout simboli | **P1** | Si |
| `ecocycle-planning` | [ecocycle-planning](https://www.liberatingstructures.com/ecocycle-planning/) | Template Ecocycle | **P1** | Si |
| `generative-relationship-star` | [generative-relationships-star](https://www.liberatingstructures.com/generative-relationships-star/) | Bussola STAR | **P2** | Si |
| `heard-seen-respected-hsr` | [heard-seen-respected](https://www.liberatingstructures.com/heard-seen-respected/) | Nessuno | — | — |
| `helping-heuristics` | [helping-heuristics](https://www.liberatingstructures.com/helping-heuristics/) | Nessuno | — | — |
| `improv-prototyping` | [improv-prototyping](https://www.liberatingstructures.com/improv-prototyping/) | Nessuno | — | — |
| `integrated-autonomy` | [integrated-autonomy](https://www.liberatingstructures.com/integrated-autonomy/) | Worksheet IA | **P2** | Si |
| `liquid-courage` | — | Escluso (adattamento locale) | Escluso | — |
| `mad-love` | — | Escluso (adattamento locale) | Escluso | — |
| `mad-tea` | [mad-tea-calm-tea](https://www.liberatingstructures.com/mad-tea-calm-tea/) | Nessuno | — | — |
| `min-specs` | [min-specs](https://www.liberatingstructures.com/min-specs/) | Esempio max→min | Opzionale | Si |
| `open-space-technology-ost` | — | Nessun worksheet LS standard | — | — |
| `panarchy` | [panarchy](https://www.liberatingstructures.com/panarchy/) | Chart + esempio | **P1** | Si |
| `pixies-reflection` | — | Escluso (adattamento locale) | Escluso | — |
| `purpose-to-practice-p2p` | [purpose-to-practice](https://www.liberatingstructures.com/purpose-to-practice/) | Template P2P | **P2** | Si |
| `shift-share` | [shift-and-share](https://www.liberatingstructures.com/shift-and-share/) | Nessuno | — | — |
| `simple-ethnography` | [simple-ethnography](https://www.liberatingstructures.com/simple-ethnography/) | Nessuno | — | — |
| `social-network-webbing` | [social-network-webbing](https://www.liberatingstructures.com/social-network-webbing/) | Esempio mappa | **P3** | Si |
| `spiral-journal` | [spiral-journal](https://www.liberatingstructures.com/spiral-journal/) | Layout pagina | **P3** | Si |
| `talking-with-pixies` | [talking-with-pixies](https://www.liberatingstructures.com/talking-with-pixies/) | Nessuno | — | — |
| `tiny-demons` | — | Escluso (adattamento locale) | Escluso | — |
| `triz` | [creative-destruction](https://www.liberatingstructures.com/creative-destruction/) | Nessuno | — | — |
| `user-experience-fishbowl` | [user-experience-fishbowl](https://www.liberatingstructures.com/user-experience-fishbowl/) | Nessuno | — | — |
| `what-i-need-from-you-winfy` | [what-i-need-from-you](https://www.liberatingstructures.com/what-i-need-from-you/) | Layout + 4 risposte | **P2** | Si |
| `wicked-questions` | [wicked-questions](https://www.liberatingstructures.com/wicked-questions/) | Solo testo in pagina | Opzionale | — |
| `wise-crowds` | [wise-crowds](https://www.liberatingstructures.com/wise-crowds/) | Nessuno | — | — |

**Sintesi:** 12 strutture con worksheet essenziale (P1–P3), 1 opzionale con asset (Min Specs), 5 escluse, 23 senza materiale grafico obbligatorio sul sito ufficiale.

---

## 3. Wave di implementazione suggerite

| Wave | Schede | Obiettivo |
|------|--------|-----------|
| **1** | Ecocycle, Panarchy, Critical Uncertainties, Agreement & Certainty, Drawing Together | Sbloccare le schede strategiche piu' incomprensibili senza diagramma |
| **2** | Integrated Autonomy, Generative STAR, P2P, Design StoryBoards, WINFY | Worksheet per trasformazione e progettazione incontri |
| **3** | Social Network Webbing, Spiral Journal | Esempi visivi per reti e riflessione individuale |
| **Opzionale** | Min Specs, Wicked Questions | Min Specs: esempio max→min; Wicked Questions: creare card italiana (formula nel testo LS) |

---

## 4. Schede prioritarie — dettaglio e anteprima

### P1 — Ecocycle Planning

**Gap attuale** (`ecocycle-planning.md`): «Mappa Ecocycle vuota per ogni partecipante e una versione grande su poster (4 fasi: nascita, maturita', release creativa, rinnovo)» — senza immagine del ciclo e delle trappole Rigidity/Scarcity.

**Asset:** `assets/worksheets/ecocycle-planning/ecocycle-template.png`

![Template Ecocycle vuoto con le quattro fasi e le trappole di rigidita' e scarsita'](/assets/worksheets/ecocycle-planning/ecocycle-template.png)

*Fonte: [Ecocycle Planning](https://www.liberatingstructures.com/ecocycle-planning/) — Liberating Structures (Henri Lipmanowicz & Keith McCandless).*

**Proposta integrazione** — inserire dopo `## Cosa ti serve`:

```markdown
## Materiali grafici

![Template Ecocycle vuoto con le quattro fasi e le trappole di rigidita' e scarsita'](/assets/worksheets/ecocycle-planning/ecocycle-template.png)

*Fonte: [Ecocycle Planning](https://www.liberatingstructures.com/ecocycle-planning/) — Liberating Structures (Henri Lipmanowicz & Keith McCandless).*
```

**Nota per `strutture-sintesi.md`:** aggiungere flag `richiede_worksheet: sì` su Ecocycle Planning.

---

### P1 — Panarchy

**Gap attuale:** «Grafico Panarchy a tre livelli» descritto a parole; manca il diagramma adattivo con dinamiche creative/conservative.

**Asset:**

![Worksheet Panarchy vuoto](/assets/worksheets/panarchy/panarchy-worksheet.png)

*Fonte: [Panarchy](https://www.liberatingstructures.com/panarchy/) — Liberating Structures (Henri Lipmanowicz & Keith McCandless).*

![Esempio Panarchy compilato (progetto multisito)](/assets/worksheets/panarchy/panarchy-example.png)

*Fonte: [Panarchy](https://www.liberatingstructures.com/panarchy/) — Liberating Structures (Henri Lipmanowicz & Keith McCandless).*

**Proposta integrazione:** sezione `## Materiali grafici` con entrambe le figure (prima il template, poi l'esempio).

---

### P1 — Critical Uncertainties

**Gap attuale:** «Template matrice 2x2 vuota su poster» senza riferimento visivo agli assi e ai quattro quadranti.

**Asset:**

![Template Critical Uncertainties — matrice 2x2 vuota](/assets/worksheets/critical-uncertainties/critical-uncertainties-template.png)

*Fonte: [Critical Uncertainties](https://www.liberatingstructures.com/critical-uncertainties/) — Liberating Structures (Henri Lipmanowicz & Keith McCandless).*

![Esempio Critical Uncertainties — trasporti durante il COVID-19](/assets/worksheets/critical-uncertainties/critical-uncertainties-example.png)

*Fonte: [Critical Uncertainties](https://www.liberatingstructures.com/critical-uncertainties/) — Liberating Structures (Henri Lipmanowicz & Keith McCandless).*

---

### P1 — Agreement & Certainty Matrix

**Gap attuale:** tabella testuale dei quadranti presente, ma manca la matrice vuota da stampare e un esempio di post-it su parete.

**Pagina LS:** `agreement-and-certainty` (non `agreement-certainty-matrix`).

**Asset:**

![Template Agreement & Certainty Matrix vuoto](/assets/worksheets/agreement-certainty-matrix/agreement-certainty-template.png)

*Fonte: [Agreement & Certainty Matrix](https://www.liberatingstructures.com/agreement-and-certainty/) — Liberating Structures (Henri Lipmanowicz & Keith McCandless).*

![Esempio con i quattro tipi di sfida e post-it sul display](/assets/worksheets/agreement-certainty-matrix/agreement-certainty-display.png)

*Fonte: [Agreement & Certainty Matrix](https://www.liberatingstructures.com/agreement-and-certainty/) — Liberating Structures (Henri Lipmanowicz & Keith McCandless).*

---

### P1 — Drawing Together

**Gap attuale:** i 5 simboli sono elencati in testo con significati **non allineati** all'handout ufficiale:

| Simbolo | Testo attuale liberating.it | Handout LS ufficiale |
|---------|----------------------------|----------------------|
| Cerchio | unita' | wholeness, completion, self |
| Rettangolo | struttura | foundation, support |
| Triangolo | obiettivo | goals, aspirations |
| Stella | visione | **star person — relationships** |
| Freccia | movimento | *(assente)* — LS usa **spirale** per change/transformation |

**Azione:** allineare `drawing-together.md` ai significati dell'handout quando si integra l'immagine.

**Asset:**

![Handout Drawing Together — cinque simboli](/assets/worksheets/drawing-together/drawing-together-symbols.png)

*Fonte: [Drawing Together](https://www.liberatingstructures.com/drawing-together/) — Liberating Structures (Henri Lipmanowicz & Keith McCandless).*

---

### P2 — Integrated Autonomy

**Gap attuale:** «Worksheet Integrated Autonomy (matrice attivita' x paradosso)» senza visual.

**Asset:**

![Template Integrated Autonomy — sezioni A, B, C](/assets/worksheets/integrated-autonomy/integrated-autonomy-template.png)

*Fonte: [Integrated~Autonomy](https://www.liberatingstructures.com/integrated-autonomy/) — Liberating Structures (Henri Lipmanowicz & Keith McCandless).*

---

### P2 — Generative Relationship STAR

**Gap attuale:** «Bussola STAR disegnata su flip-chart» — i quattro assi (Separateness, Tuning, Action, Reason) vanno visti.

**Asset:**

![Template Generative Relationships STAR — bussola a quattro assi](/assets/worksheets/generative-relationship-star/generative-star-template.png)

*Fonte: [Generative Relationships STAR](https://www.liberatingstructures.com/generative-relationships-star/) — Liberating Structures (Brenda Zimmerman; adattato da Henri Lipmanowicz & Keith McCandless).*

---

### P2 — Purpose to Practice (P2P)

**Gap attuale:** le 5 domande P2P sono nel testo; manca il template visivo con Purpose, Principles, Participants, Structure, Practices.

**Asset:**

![Template Purpose to Practice](/assets/worksheets/purpose-to-practice-p2p/purpose-to-practice-template.png)

*Fonte: [Purpose-to-Practice (P2P)](https://www.liberatingstructures.com/purpose-to-practice/) — Liberating Structures (Henri Lipmanowicz & Keith McCandless).*

---

### P2 — Design StoryBoards

**Gap attuale:** «Template storyboard: colonne per Scopo, Partecipanti, Struttura, Microstruttura LS, Tempo» senza esempio visivo.

**Asset:**

![Esempio di design storyboard compilato](/assets/worksheets/design-storyboards/design-storyboard-example.png)

*Fonte: [Design Storyboards](https://www.liberatingstructures.com/design-storyboards/) — Liberating Structures (Henri Lipmanowicz, Nancy White & Keith McCandless).*

![Estratto LS Selection Matchmaker per abbinare strutture agli obiettivi](/assets/worksheets/design-storyboards/ls-selection-matchmaker-excerpt.png)

*Fonte: [Design Storyboards](https://www.liberatingstructures.com/design-storyboards/) — Liberating Structures (Henri Lipmanowicz, Nancy White & Keith McCandless).*

**Link correlato:** [LS Selection Matchmaker](https://www.liberatingstructures.com/matching-matrix/) (PDF completo sul sito ufficiale).

---

### P2 — What I Need From You (WINFY)

**Gap attuale:** layout cluster + cerchio centrale e le quattro risposte sono descritti ma non mostrati.

**Asset:**

![Layout sala WINFY — cluster funzionali e cerchio portavoce](/assets/worksheets/what-i-need-from-you-winfy/winfy-room-layout.png)

*Fonte: [What I Need from You (WINFY)](https://www.liberatingstructures.com/what-i-need-from-you/) — Liberating Structures (Henri Lipmanowicz & Keith McCandless).*

![Le quattro risposte WINFY: Yes, No, Huh?, Whatever](/assets/worksheets/what-i-need-from-you-winfy/winfy-responses.png)

*Fonte: [What I Need from You (WINFY)](https://www.liberatingstructures.com/what-i-need-from-you/) — Liberating Structures (Henri Lipmanowicz & Keith McCandless).*

---

### P3 — Social Network Webbing

**Gap attuale:** legenda colori e core/periferia senza esempio di mappa compilata.

**Asset:**

![Esempio Social Network Webbing in corso — core, rete immediata, periferia](/assets/worksheets/social-network-webbing/social-network-webbing-example.png)

*Fonte: [Social Network Webbing](https://www.liberatingstructures.com/social-network-webbing/) — Liberating Structures (Henri Lipmanowicz & Keith McCandless).*

---

### P3 — Spiral Journal

**Gap attuale:** «spirale disegnata» e domande tipo senza layout del foglio.

**Asset:**

![Esempio layout Spiral Journal — spirale e quattro quadranti](/assets/worksheets/spiral-journal/spiral-journal-example.png)

*Fonte: [Spiral Journal](https://www.liberatingstructures.com/spiral-journal/) — Liberating Structures (Fisher Qua & Anna Jackson).*

---

### Opzionale — Min Specs

**Asset:**

![Esempio riduzione da Max Specs a Min Specs](/assets/worksheets/min-specs/min-specs-example.png)

*Fonte: [Min Specs](https://www.liberatingstructures.com/min-specs/) — Liberating Structures (Henri Lipmanowicz & Keith McCandless).*

### Opzionale — Wicked Questions

Nessun file immagine dedicato sulla pagina ufficiale: formula ed esempi sono solo testo. **Proposta:** creare in fase 2 una card italiana minimal (SVG locale) con la formula «Come possiamo essere ___ e contemporaneamente ___?» — non copiare dal sito LS.

---

## 5. Appendice — requisiti tecnici (fase 2)

Integrare le figure nelle schede pubblicate richiede modifiche al pipeline statico.

### 5.1 Contenuto (`content/v2/`)

- Aggiungere sezione opzionale `## Materiali grafici` in [`02-template.md`](02-template.md), subito dopo `## Cosa ti serve`.
- Inserire blocchi `![alt](/assets/worksheets/...)` + didascalia in ciascuna scheda P1–P3.
- Allineare testo Drawing Together ai simboli ufficiali (vedi tabella sopra).

### 5.2 Build ([`public/scripts/build.py`](../public/scripts/build.py))

Oggi `md_inline()` gestisce solo grassetto e link. Serve una delle due opzioni:

**A (consigliata):** parser dedicato per `## Materiali grafici`:

```python
def parse_graphics_section(text: str) -> list[dict]:
    # figure: {src, alt, caption_html}
    ...
```

**B:** estendere `md_inline` con regex `!\[([^\]]+)\]\((/[^)]+)\)` → `<figure class="ls-figure">...</figure>`.

Passare `graphics` al template Jinja `structure.html` nella zona `#fare`, dopo la lista «Cosa ti serve».

### 5.3 Template HTML ([`public/templates/structure.html`](../public/templates/structure.html))

```html
{% if graphics %}
<section class="ls-graphics" aria-label="Materiali grafici">
  <h2>Materiali grafici</h2>
  {% for fig in graphics %}
  <figure class="ls-figure">
    <img src="{{ fig.src | asset(out_root) }}" alt="{{ fig.alt }}" loading="lazy" decoding="async">
    {% if fig.caption %}<figcaption class="ls-figure__caption">{{ fig.caption | safe }}</figcaption>{% endif %}
  </figure>
  {% endfor %}
</section>
{% endif %}
```

### 5.4 CSS ([`public/assets/css/components.css`](../public/assets/css/components.css))

```css
.ls-figure { margin: var(--space-4) 0; }
.ls-figure img { max-width: 100%; height: auto; border: 1px solid var(--md-sys-color-outline-variant); border-radius: var(--radius-md); }
.ls-figure__caption { margin-top: var(--space-2); font-size: 0.875rem; color: var(--md-sys-color-on-surface-variant); font-style: italic; }
```

### 5.5 Asset e deploy

- Worksheet in `public/assets/worksheets/{slug}/` (gia' popolato).
- Rigenerare HTML: `python3 public/scripts/build.py`.
- Aggiornare asset: `python3 scripts/fetch_ls_worksheets.py --optional`.

### 5.6 SEO e accessibilita'

- `alt` in italiano, descrittivo (non ripetere solo il titolo file).
- Didascalia visibile con link alla pagina LS (citabilita' e conformita' attribuzione).
- Opzionale: `ImageObject` in JSON-LD solo se si espone la sezione in HTML pubblico.

### 5.7 `strutture-sintesi.md`

Per le 5 schede P1, aggiungere in sintesi:

```markdown
- **Richiede worksheet:** sì — vedi assets/worksheets/{slug}/
```

---

## 6. Checklist qualita'

- [x] 41 schede mappate a pagina LS o marcate escluse
- [x] 18 asset P1–P3 (+ Min Specs) scaricati in `public/assets/worksheets/`
- [x] Ogni immagine in questo documento ha didascalia con URL pagina LS
- [x] Proposta `## Materiali grafici` per ogni scheda prioritaria
- [x] Appendice tecnica per fase 2 (build + template + CSS)
- [ ] Integrazione nelle schede MD (fase 2)
- [ ] Allineamento simboli Drawing Together (fase 2)
- [ ] Flag `richiede_worksheet` in strutture-sintesi.md (fase 2)
