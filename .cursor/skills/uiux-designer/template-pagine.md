# Template pagine - liberating.it

Wireframe testuale e struttura HTML per ogni tipo di pagina. Tutti i template condividono `SiteHeader`, `main.ls-main`, `SiteFooter`. CSS da [design-system.md](design-system.md), componenti da [componenti.md](componenti.md).

---

## Struttura HTML comune

```html
<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{meta_description}">
  <link rel="canonical" href="{url}">
  <link rel="stylesheet" href="/assets/css/tokens.css">
  <link rel="stylesheet" href="/assets/css/base.css">
  <link rel="stylesheet" href="/assets/css/components.css">
</head>
<body class="ls-page ls-page--{type}" data-slug="{slug}">
  <!-- SiteHeader -->
  <main id="main" class="ls-main">
    <!-- contenuto per tipo -->
  </main>
  <!-- SiteFooter -->
  <script src="/assets/js/nav.js" defer></script>
  <!-- script aggiuntivi per tipo -->
</body>
</html>
```

---

## Home

**Sorgente:** `content/v1/pagine/home.md` (da portare in `content/v2/pagine/home.md`)  
**Registro:** Manifesto  
**URL:** `/`

### Wireframe

```
┌─────────────────────────────────────────┐
│ SiteHeader                              │
├─────────────────────────────────────────┤
│ HERO                                    │
│ H1: Cambia come lavora il tuo team      │
│ Sottotitolo: 35 strumenti pratici       │
│ [CTA filled: Scegli una struttura]      │
├─────────────────────────────────────────┤
│ IL PROBLEMA (H2)                        │
│ • elenco scansionabile 3-4 pain point   │
├─────────────────────────────────────────┤
│ LA SOLUZIONE (H2)                       │
│ 3 colonne: inclusione | semplicita' |    │
│ autonomia + link catalogo               │
├─────────────────────────────────────────┤
│ PER INIZIARE (H2)                       │
│ 3-4 StructureCard compatte              │
├─────────────────────────────────────────┤
│ CTA finale (ls-cta)                     │
├─────────────────────────────────────────┤
│ LEGGI ANCHE (opzionale)                 │
│ 2-3 link editoriali                     │
├─────────────────────────────────────────┤
│ SiteFooter                              │
└─────────────────────────────────────────┘
```

### Struttura

```html
<main id="main" class="ls-main ls-main--home">
  <section class="ls-hero">
    <h1 class="ls-hero__title">Cambia come lavora il tuo team</h1>
    <p class="ls-hero__subtitle">35 strumenti pratici per riunioni che producono risultati.</p>
    <a href="/structures/" class="ls-btn ls-btn--filled">Scegli una struttura da provare domani</a>
  </section>

  <section class="ls-section" aria-labelledby="problema-heading">
    <h2 id="problema-heading">Ti riconosci?</h2>
    <ul class="ls-list ls-list--scan">
      <li>Riunioni che non finiscono mai</li>
      <li>Parlano sempre gli stessi due</li>
      <li>Idee che restano nel cassetto</li>
    </ul>
  </section>

  <section class="ls-section" aria-labelledby="soluzione-heading">
    <h2 id="soluzione-heading">Cosa sono le Liberating Structures</h2>
    <div class="ls-grid ls-grid--3">
      <article><!-- inclusione --></article>
      <article><!-- semplicita' --></article>
      <article><!-- autonomia --></article>
    </div>
    <p><a href="/structures/">Esplora il catalogo</a></p>
  </section>

  <section class="ls-section" aria-labelledby="iniziare-heading">
    <h2 id="iniziare-heading">Per iniziare</h2>
    <div class="ls-grid ls-grid--cards">
      <!-- 3-4 StructureCard -->
    </div>
  </section>

  <section class="ls-cta"><!-- CTA unica --></section>
</main>
```

**Classi pagina:** `ls-page--home`; hero con optional `ls-font-serif` su H1.

---

## Catalogo

**Sorgente:** IA § catalogo in [01-architettura.md](../../../content/v2/01-architettura.md)  
**URL:** `/structures/`

### Wireframe

```
┌──────────┬──────────────────────────────┐
│ FILTRI   │ H1: Le strutture             │
│ (sidebar │ Intro breve                  │
│  lg+)    │ ┌────┐ ┌────┐ ┌────┐        │
│          │ │card│ │card│ │card│        │
│ diff     │ └────┘ └────┘ └────┘        │
│ compl.   │ ┌────┐ ┌────┐ ┌────┐        │
│ durata   │ │card│ │card│ │card│        │
│ fase     │ └────┘ └────┘ └────┘        │
└──────────┴──────────────────────────────┘
Mobile: [Filtra ▼] apre drawer
```

### Struttura

```html
<main id="main" class="ls-main ls-main--catalog">
  <header class="ls-page-header">
    <h1>Le strutture</h1>
    <p class="ls-page-header__intro">Trova lo strumento giusto per il tuo bisogno, non in ordine alfabetico.</p>
  </header>

  <div class="ls-catalog-layout">
    <aside class="ls-filters"><!-- FilterBar --></aside>
    <div class="ls-catalog">
      <p class="ls-catalog__count" aria-live="polite">41 strutture</p>
      <div class="ls-grid ls-grid--cards" id="structure-grid">
        <!-- 41 StructureCard, ordinamento default per complessita'/bisogno -->
      </div>
      <p class="ls-catalog__empty" hidden>Nessuna struttura corrisponde ai filtri.</p>
    </div>
  </div>
</main>
<script src="/assets/js/filters.js" defer></script>
```

**Default sort:** per hub `complessita` (Per iniziare subito prima), non alfabetico.

**Data source:** `structures/index.json` generato in build (vedi [mapping-contenuti.md](mapping-contenuti.md)).

---

## Scheda struttura

**Sorgente:** `content/v2/strutture/{slug}.md`  
**URL:** `/structures/{slug}/`

### Wireframe

```
┌─────────────────────────────────────────┐
│ SiteHeader (sticky)                     │
│ MiniNav: Panoramica | Come fare | ...   │
├─────────────────────────────────────────┤
│ Breadcrumb                              │
│ H1                                      │
│ ┌─ CAP ─────────────────────────────┐   │
│ │ In breve                          │   │
│ │ QuickInfoTable                    │   │
│ │ TaxonomyChips                     │   │
│ └───────────────────────────────────┘   │
│ ┌─ FARE ────────────────────────────┐   │
│ │ H2 Domanda da portare             │   │
│ │ H2 Cosa ti serve                  │   │
│ │ H2 I passaggi (StepList)          │   │
│ └───────────────────────────────────┘   │
│ ┌─ NAVIGA ──────────────────────────┐   │
│ │ Quando / Consiglio / Errori       │   │
│ │ FAQ (details)                     │   │
│ │ RelatedLinks                      │   │
│ └───────────────────────────────────┘   │
│ PathNav (sticky bottom mobile)          │
│ SiteFooter                              │
└─────────────────────────────────────────┘
```

### Struttura

```html
<main id="main" class="ls-main ls-main--structure">
  <article class="ls-article"
    data-slug="1-2-4-all"
    data-difficolta="facile"
    data-complessita="iniziare-subito"
    data-durata="breve"
    data-fase="ideate">

    <nav class="ls-mininav" aria-label="Sezioni della scheda">...</nav>
    <nav class="ls-breadcrumb">...</nav>

    <header class="ls-article__header">
      <h1>1-2-4-All</h1>
    </header>

    <section id="cap" class="ls-cap ls-zone" aria-label="Panoramica">
      <p class="ls-cap__brief"><strong>In breve</strong> - ...</p>
      <dl class="ls-quick-info">...</dl>
      <div class="ls-chips">...</div>
    </section>

    <section id="fare" class="ls-zone" aria-label="Come fare">
      <h2>Domanda da portare</h2>
      <ul>...</ul>
      <h2>Cosa ti serve</h2>
      <ul>...</ul>
      <h2>I passaggi</h2>
      <ol class="ls-step-list">...</ol>
    </section>

    <section id="naviga" class="ls-zone" aria-label="Approfondisci">
      <h2>Quando usarla</h2>
      <h2>Il consiglio del facilitatore</h2>
      <h2>Errori da evitare</h2>
      <section class="ls-faq">...</section>
      <aside class="ls-related">...</aside>
    </section>
  </article>

  <nav class="ls-path-nav" aria-label="Percorso guidato">...</nav>
</main>
<script src="/assets/js/scroll-spy.js" defer></script>
<script type="application/ld+json">{ FAQPage }</script>
```

**Body class:** aggiungi `ls-has-path-nav` se PathNav presente (padding-bottom mobile).

---

## Hub tassonomia

**Sorgente:** IA § filtri  
**URL:** `/complessita/{slug}/`, `/difficolta/{slug}/`, `/durata/{slug}/`, `/design-thinking/{slug}/`

### Wireframe

```
Breadcrumb: Home > Le strutture > {Hub label}
H1: {Hub title}
Intro 2-3 frasi sul filtro
Griglia StructureCard (solo strutture filtrate)
Link: Torna al catalogo completo
```

### Struttura

```html
<main id="main" class="ls-main ls-main--hub">
  <nav class="ls-breadcrumb">...</nav>
  <header class="ls-page-header">
    <h1>Per iniziare subito</h1>
    <p>5 strutture facili per provare le Liberating Structures senza esperienza precedente.</p>
  </header>
  <div class="ls-grid ls-grid--cards">
    <!-- StructureCard filtrate -->
  </div>
  <p><a href="/structures/" class="ls-btn ls-btn--outlined">Vedi tutte le strutture</a></p>
</main>
```

Hub `complessita/iniziare-subito`: mostra anche sequenza PathNav come lista numerata con link.

---

## Hub Per bisogno

**Sorgente:** IA § sottomenu  
**URL:** `/per-bisogno/{slug}/` (nuovi path — aggiungere a `_redirects` se necessario)

### Wireframe

```
H1: {Obiettivo} — es. Generare idee
Intro
Griglia StructureCard (5-8 strutture tipiche)
Link a catalogo filtrato
```

### Landing index `/per-bisogno/`

```
H1: Trova la struttura per il tuo bisogno
4 card obiettivo (2x2 grid):
  Generare idee | Prendere decisioni
  Analizzare problemi | Fare strategia
```

```html
<div class="ls-grid ls-grid--2">
  <a href="/per-bisogno/generare-idee/" class="ls-card ls-card--hub">
    <h2>Generare idee</h2>
    <p>Per team bloccati e workshop creativi.</p>
    <ul class="ls-card__examples">
      <li>1-2-4-All</li>
      <li>TRIZ</li>
    </ul>
  </a>
  <!-- ... -->
</div>
```

---

## Pagina editoriale

**Sorgente:** template v2 in [02-template.md](../../../content/v2/02-template.md)  
**File:** `content/v2/pagine/{slug}.md`  
**Registri:** Manifesto (home, posizionamento) o Diario di bordo (blog, risorse)

### Wireframe

```
H1
Hook (1-2 frasi)
Cosa trovi qui (bullet 3)
H2 sezioni body
Leggi anche (2-3 link)
E adesso? (ls-cta, una sola CTA)
```

```html
<main id="main" class="ls-main ls-main--editorial">
  <article class="ls-article">
    <h1>{Titolo}</h1>
    <p class="ls-lead">{Hook}</p>
    <aside class="ls-toc-inline" aria-label="Cosa trovi qui">
      <p><strong>Cosa trovi qui</strong></p>
      <ul>...</ul>
    </aside>
    <!-- body H2 sections -->
    <section aria-labelledby="leggi-heading">
      <h2 id="leggi-heading">Leggi anche</h2>
      <ul class="ls-related__list">...</ul>
    </section>
    <section class="ls-cta">...</section>
  </article>
</main>
```

**10 principi:** un H2 per principio, esempio concreto ciascuno; registro Diario di bordo leggero.

---

## Pagina legale

**URL:** `/privacy-policy/`, `/termini-di-servizio/`

Layout minimale: breadcrumb, H1, body prose senza componenti decorativi. Opzionale indice laterale su `lg+` per sezioni H2 lunghe.

```html
<main id="main" class="ls-main ls-main--legal">
  <article class="ls-article ls-article--legal">
    <h1>Privacy policy</h1>
    <!-- contenuto legale invariato, solo riformattato -->
  </article>
</main>
```

---

## Riepilogo script per tipo

| Tipo pagina | Script |
|-------------|--------|
| Tutte | `nav.js` |
| Catalogo | `filters.js` |
| Scheda struttura | `scroll-spy.js` |
| Home, hub, editoriale, legale | solo `nav.js` |
