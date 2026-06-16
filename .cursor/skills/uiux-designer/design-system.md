# Design system - liberating.it

Design system basato su **Material 3 tokens** implementati come CSS custom properties. Nessun framework CSS, nessun bundler obbligatorio. Riferimento semantico: [Material 3 color system](https://m3.material.io/styles/color/overview).

## Filosofia visiva

| Principio | Scelta |
|-----------|--------|
| Manuale operativo | Superfici piatte nella zona Cap; elevation solo su card catalogo e drawer |
| Scan rapido | Gerarchia tipografica netta; spazio bianco generoso |
| Brand pratico | Teal `#0D7377` come primary (non arancio WP legacy) |
| Performance CF | System font stack; nessun Google Fonts obbligatorio |

Alternativa documentata (non default): arancio LS `#E85D04` come `--md-sys-color-primary` per campagne brand.

---

## Token file: `assets/css/tokens.css`

```css
:root {
  /* Color - light scheme */
  --md-sys-color-primary: #0d7377;
  --md-sys-color-on-primary: #ffffff;
  --md-sys-color-primary-container: #b2dfdb;
  --md-sys-color-on-primary-container: #002021;

  --md-sys-color-secondary: #4a6363;
  --md-sys-color-on-secondary: #ffffff;
  --md-sys-color-secondary-container: #cce8e7;
  --md-sys-color-on-secondary-container: #051f1f;

  --md-sys-color-surface: #fafaf8;
  --md-sys-color-on-surface: #1a1a1a;
  --md-sys-color-surface-variant: #f0f0ec;
  --md-sys-color-on-surface-variant: #444746;

  --md-sys-color-outline: #747875;
  --md-sys-color-outline-variant: #c4c7c4;

  --md-sys-color-error: #ba1a1a;
  --md-sys-color-on-error: #ffffff;

  /* Typography scale */
  --md-sys-typescale-display-large: 700 2.25rem/1.2 system-ui, -apple-system, "Segoe UI", sans-serif;
  --md-sys-typescale-headline-large: 600 1.75rem/1.3 system-ui, -apple-system, "Segoe UI", sans-serif;
  --md-sys-typescale-headline-medium: 600 1.375rem/1.35 system-ui, -apple-system, "Segoe UI", sans-serif;
  --md-sys-typescale-title-large: 600 1.125rem/1.4 system-ui, -apple-system, "Segoe UI", sans-serif;
  --md-sys-typescale-title-medium: 600 1rem/1.5 system-ui, -apple-system, "Segoe UI", sans-serif;
  --md-sys-typescale-body-large: 400 1.0625rem/1.6 system-ui, -apple-system, "Segoe UI", sans-serif;
  --md-sys-typescale-body-medium: 400 1rem/1.6 system-ui, -apple-system, "Segoe UI", sans-serif;
  --md-sys-typescale-label-large: 500 0.875rem/1.4 system-ui, -apple-system, "Segoe UI", sans-serif;
  --md-sys-typescale-label-medium: 500 0.75rem/1.3 system-ui, -apple-system, "Segoe UI", sans-serif;

  /* Editorial serif (optional, self-hosted) */
  --ls-font-serif: "Source Serif 4", Georgia, "Times New Roman", serif;

  /* Shape */
  --md-sys-shape-corner-none: 0;
  --md-sys-shape-corner-extra-small: 4px;
  --md-sys-shape-corner-small: 8px;
  --md-sys-shape-corner-medium: 12px;
  --md-sys-shape-corner-full: 9999px;

  /* Elevation (box-shadow) */
  --md-sys-elevation-0: none;
  --md-sys-elevation-1: 0 1px 2px rgba(0, 0, 0, 0.06), 0 1px 3px rgba(0, 0, 0, 0.1);
  --md-sys-elevation-2: 0 2px 6px rgba(0, 0, 0, 0.08), 0 4px 12px rgba(0, 0, 0, 0.06);

  /* Motion */
  --md-sys-motion-duration-short: 150ms;
  --md-sys-motion-duration-medium: 250ms;
  --md-sys-motion-easing-standard: cubic-bezier(0.2, 0, 0, 1);

  /* Layout - liberating.it extensions */
  --ls-content-max-width: 72ch;
  --ls-page-max-width: 1200px;
  --ls-spacing-1: 4px;
  --ls-spacing-2: 8px;
  --ls-spacing-3: 16px;
  --ls-spacing-4: 24px;
  --ls-spacing-5: 32px;
  --ls-spacing-6: 48px;
  --ls-spacing-7: 64px;

  /* Sticky offsets */
  --ls-header-height: 64px;
  --ls-mininav-height: 48px;
}
```

### Dark scheme (opzionale, `prefers-color-scheme`)

```css
@media (prefers-color-scheme: dark) {
  :root {
    --md-sys-color-primary: #4db6ac;
    --md-sys-color-on-primary: #003735;
    --md-sys-color-surface: #1a1c1c;
    --md-sys-color-on-surface: #e2e3e3;
    --md-sys-color-surface-variant: #2a2c2c;
    --md-sys-color-on-surface-variant: #c4c7c4;
    --md-sys-color-outline-variant: #444746;
  }
}
```

---

## Tipografia

| Elemento | Token / stile | Uso |
|----------|---------------|-----|
| H1 pagina | `headline-large` | Titolo struttura o hero |
| H2 sezione | `headline-medium` | Domanda da portare, I passaggi, FAQ |
| H3 FAQ | `title-medium` | Domanda singola (in `<summary>`) |
| Body | `body-large` | Paragrafi, In breve |
| Meta / chip | `label-medium` | Durata, difficolta', badge tempo |
| Titoli editoriali | `ls-font-serif` + `headline-large` | Home hero, manifesto (opzionale) |

**Regole:**

- Max **72ch** per blocchi di testo (`max-width: var(--ls-content-max-width)`)
- Grassetto solo su parole chiave (tone-of-voice), non interi paragrafi
- Link: colore `--md-sys-color-primary`, sottolineatura al focus/hover

---

## Spacing e layout

```
Pagina
├── SiteHeader (sticky, --ls-header-height)
├── main.ls-main (max-width: --ls-page-max-width, margin auto, padding --ls-spacing-4)
│   ├── Breadcrumb
│   ├── article.ls-article (max-width: --ls-content-max-width per body)
│   └── aside (solo catalogo desktop: filtri)
└── SiteFooter
```

| Breakpoint | Valore | Comportamento |
|------------|--------|---------------|
| `sm` | 0–599px | Colonna singola; filtri in drawer; PathNav sticky bottom |
| `md` | 600–899px | Griglia catalogo 2 colonne |
| `lg` | 900px+ | Sidebar filtri catalogo; griglia 3 colonne; mini-nav sticky sotto header |

```css
/* Breakpoint helpers (in base.css) */
@media (min-width: 600px) { /* md */ }
@media (min-width: 900px) { /* lg */ }
```

---

## Zone scheda struttura

### Cap (above the fold)

- Sfondo `--md-sys-color-surface` (piatto, elevation-0)
- Blocco unificato `.ls-cap`: breadcrumb + In breve + QuickInfoTable + TaxonomyChips
- Obiettivo: orientamento in **10 secondi** senza scroll

### Fare (agire)

- Passaggi in `.ls-step-list` con numeri prominenti e badge tempo
- Liste bullet compatte; max 5 item in "Cosa ti serve"

### Naviga (restare sul sito)

- FAQ in `<details>` (elevation-0)
- RelatedLinks in card outlined (bordo `--md-sys-color-outline-variant`)
- PathNav: barra fissa in basso su mobile (`position: fixed; bottom: 0`)

---

## Componenti M3 mappati

| Pattern M3 | Implementazione ls-* |
|------------|---------------------|
| Top app bar | `ls-header` |
| Filled button | `ls-btn--filled` (CTA unica) |
| Outlined button | `ls-btn--outlined` (nav secondaria) |
| Assist chip | `ls-chip` (link a hub tassonomia) |
| Filter chip | `ls-chip--filter` (catalogo, stato attivo) |
| Card elevated | `ls-card` (catalogo) |
| Card outlined | `ls-card--outlined` (correlati) |
| Navigation drawer | `ls-drawer` (menu mobile) |

---

## Stati interattivi

Tutti i controlli focusabili:

```css
:focus-visible {
  outline: 2px solid var(--md-sys-color-primary);
  outline-offset: 2px;
}
```

- Contrasto testo/sfondo: minimo **WCAG AA** (4.5:1 body, 3:1 large text)
- `:hover` su link e chip: leggero cambio background (`--md-sys-color-surface-variant`)
- Transizioni: solo `color`, `background-color`, `box-shadow` con `--md-sys-motion-duration-short`

---

## Icone

Preferire **SVG inline** minimali (freccia, menu, close) — nessun icon font esterno. Se servono piu' icone, self-hostare un subset o usare `currentColor` su path semplici.

---

## Anti-pattern visivi

- Emoji negli heading o nei chip
- Ombre pesanti o gradienti decorativi
- Piu' di un colore accento in competizione
- Card annidate eccessivamente
- Font size sotto 16px per body su mobile
