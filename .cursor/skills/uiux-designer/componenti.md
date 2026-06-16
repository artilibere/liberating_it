# Componenti UI - liberating.it

Libreria componenti HTML/CSS vanilla con prefisso BEM `ls-*`. Ogni componente usa i token in [design-system.md](design-system.md). Markup semantico, stati focus/hover, note ARIA.

---

## SiteHeader (`ls-header`)

Barra superiore sticky. Top app bar M3.

```html
<header class="ls-header" role="banner">
  <div class="ls-header__inner">
    <a href="/" class="ls-header__logo" aria-label="Liberating.it - Home">
      <span class="ls-header__logo-text">Liberating.it</span>
    </a>
    <button type="button" class="ls-header__menu-btn" aria-expanded="false" aria-controls="ls-nav-drawer" aria-label="Apri menu">
      <!-- SVG hamburger -->
    </button>
    <nav class="ls-header__nav" aria-label="Navigazione principale">
      <ul class="ls-header__nav-list">
        <li><a href="/structures/">Le strutture</a></li>
        <li class="ls-header__nav-item--has-submenu">
          <button type="button" aria-expanded="false" aria-controls="ls-submenu-bisogno">Per bisogno</button>
          <ul id="ls-submenu-bisogno" class="ls-header__submenu" hidden>
            <li><a href="/per-bisogno/generare-idee/">Generare idee</a></li>
            <li><a href="/per-bisogno/prendere-decisioni/">Prendere decisioni</a></li>
            <li><a href="/per-bisogno/analizzare-problemi/">Analizzare problemi</a></li>
            <li><a href="/per-bisogno/fare-strategia/">Fare strategia</a></li>
          </ul>
        </li>
        <li><a href="/10-principi-fondamentali-liberating-structures/">I 10 principi</a></li>
        <li><a href="/risorse/">Risorse</a></li>
      </ul>
    </nav>
  </div>
</header>
```

**CSS:** `position: sticky; top: 0; z-index: 100; background: var(--md-sys-color-surface); border-bottom: 1px solid var(--md-sys-color-outline-variant); height: var(--ls-header-height);`

**JS (`nav.js`):** toggle drawer mobile; focus trap nel drawer; chiudi con Esc; submenu keyboard-navigable.

**ARIA:** `aria-expanded` su menu button e submenu; `aria-current="page"` sul link attivo.

---

## Breadcrumb (`ls-breadcrumb`)

```html
<nav class="ls-breadcrumb" aria-label="Breadcrumb">
  <ol class="ls-breadcrumb__list" itemscope itemtype="https://schema.org/BreadcrumbList">
    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      <a href="/" itemprop="item"><span itemprop="name">Home</span></a>
      <meta itemprop="position" content="1">
    </li>
    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      <a href="/structures/" itemprop="item"><span itemprop="name">Le strutture</span></a>
      <meta itemprop="position" content="2">
    </li>
    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem" aria-current="page">
      <span itemprop="name">1-2-4-All</span>
      <meta itemprop="position" content="3">
    </li>
  </ol>
</nav>
```

**Mobile:** tronca con `…` se troppo lungo; ultimo item sempre visibile.

---

## QuickInfoTable (`ls-quick-info`)

Scheda rapida da tabella MD. Responsive: definition list su mobile.

```html
<dl class="ls-quick-info">
  <div class="ls-quick-info__row">
    <dt class="ls-quick-info__label">Durata</dt>
    <dd class="ls-quick-info__value">15 minuti</dd>
  </div>
  <div class="ls-quick-info__row">
    <dt class="ls-quick-info__label">Difficolta'</dt>
    <dd class="ls-quick-info__value">Facile</dd>
  </div>
  <div class="ls-quick-info__row">
    <dt class="ls-quick-info__label">Gruppo</dt>
    <dd class="ls-quick-info__value">illimitato</dd>
  </div>
  <div class="ls-quick-info__row">
    <dt class="ls-quick-info__label">Fase</dt>
    <dd class="ls-quick-info__value">Ideate</dd>
  </div>
</dl>
```

**Desktop (`lg`):** griglia 4 colonne in card compatta `.ls-cap__meta`.

---

## TaxonomyChips (`ls-chips`)

Assist chip M3 — link verso hub filtrati.

```html
<div class="ls-chips" role="list" aria-label="Filtri tassonomia">
  <a href="/complessita/iniziare-subito/" class="ls-chip" role="listitem">Per iniziare subito</a>
  <a href="/difficolta/facile/" class="ls-chip" role="listitem">Facile</a>
  <a href="/durata/breve/" class="ls-chip" role="listitem">Breve (max 45 min)</a>
  <a href="/design-thinking/ideate/" class="ls-chip" role="listitem">Ideate</a>
</div>
```

**CSS:** `display: inline-flex; padding: 6px 12px; border-radius: var(--md-sys-shape-corner-full); border: 1px solid var(--md-sys-color-outline); font: var(--md-sys-typescale-label-medium);`

---

## MiniNav (`ls-mininav`)

Tab bar anchor per zone Cap / Fare / Naviga. Sticky sotto header su `lg+`.

```html
<nav class="ls-mininav" aria-label="Sezioni della scheda">
  <ul class="ls-mininav__list">
    <li><a href="#cap" class="ls-mininav__link ls-mininav__link--active">Cap</a></li>
    <li><a href="#fare" class="ls-mininav__link">Fare</a></li>
    <li><a href="#naviga" class="ls-mininav__link">Naviga</a></li>
  </ul>
</nav>
```

**JS (`scroll-spy.js`):** aggiorna `--active` su scroll; `scroll-margin-top` sulle sezioni per compensare header sticky.

**Label UI:** usa testi leggibili in produzione — "Panoramica", "Come fare", "Approfondisci" (non "Cap/Fare/Naviga" visibili all'utente).

---

## Cap block (`ls-cap`)

Contenitore zona Cap unificata.

```html
<section id="cap" class="ls-cap" aria-labelledby="page-title">
  <!-- breadcrumb, in breve, quick-info, chips -->
  <p class="ls-cap__brief"><strong>In breve</strong> - 1-2-4-All e' una struttura...</p>
</section>
```

---

## StepList (`ls-step-list`)

Passaggi numerati con badge tempo.

```html
<ol class="ls-step-list">
  <li class="ls-step">
    <span class="ls-step__number" aria-hidden="true">1</span>
    <div class="ls-step__content">
      <p class="ls-step__action">Poni la domanda al gruppo</p>
      <span class="ls-step__time">1 min</span>
    </div>
  </li>
</ol>
```

**CSS:** numero in cerchio `--md-sys-color-primary-container`; tempo come `ls-chip` ridotto.

---

## FaqAccordion (`ls-faq`)

Preferire `<details>` nativo (zero JS, accessibile).

```html
<section class="ls-faq" aria-labelledby="faq-heading">
  <h2 id="faq-heading">Domande frequenti</h2>
  <details class="ls-faq__item">
    <summary class="ls-faq__question">Cos'e' 1-2-4-All?</summary>
    <div class="ls-faq__answer">
      <p>1-2-4-All e' una struttura di facilitazione...</p>
    </div>
  </details>
</section>
```

**CSS:** `summary { cursor: pointer; font: var(--md-sys-typescale-title-medium); }` — freccia con `list-style` o pseudo-element.

**JSON-LD:** generato in build da stesse domande/risposte (vedi [mapping-contenuti.md](mapping-contenuti.md)).

---

## PathNav (`ls-path-nav`)

Prev/next percorso "Per iniziare subito". Sticky bottom su mobile.

```html
<nav class="ls-path-nav" aria-label="Percorso guidato">
  <a href="/structures/impromptu-networking/" class="ls-path-nav__prev">
    <span class="ls-path-nav__label">Precedente</span>
    <span class="ls-path-nav__title">Impromptu Networking</span>
  </a>
  <a href="/structures/w3-what-so-what-now-what/" class="ls-path-nav__next">
    <span class="ls-path-nav__label">Successiva</span>
    <span class="ls-path-nav__title">What, So What, Now What?</span>
  </a>
</nav>
```

**CSS mobile:** `position: fixed; bottom: 0; left: 0; right: 0; padding-bottom: env(safe-area-inset-bottom); box-shadow: var(--md-sys-elevation-2);`

**Padding body:** `padding-bottom` su mobile quando PathNav presente.

---

## RelatedLinks (`ls-related`)

Prima/Dopo, Simili, Torna al catalogo in card outlined.

```html
<aside class="ls-related" aria-labelledby="related-heading">
  <h2 id="related-heading" class="visually-hidden">Strutture correlate</h2>

  <div class="ls-related__group">
    <h3 class="ls-related__title">Prima e dopo</h3>
    <ul class="ls-related__list">
      <li>
        <a href="/structures/impromptu-networking/" class="ls-card ls-card--outlined ls-related__link">
          <span class="ls-related__name">Impromptu Networking</span>
          <span class="ls-related__reason">rompe il ghiaccio prima di raccogliere idee</span>
        </a>
      </li>
    </ul>
  </div>

  <div class="ls-related__group">
    <h3 class="ls-related__title">Strutture simili</h3>
    <!-- ... -->
  </div>

  <p class="ls-related__back">
    <a href="/structures/" class="ls-btn ls-btn--outlined">Esplora tutte le strutture</a>
  </p>
</aside>
```

Ogni link include **motivo esplicito** (5-10 parole) dal Markdown.

---

## StructureCard (`ls-card`)

Card catalogo con elevation-1.

```html
<article class="ls-card" data-slug="1-2-4-all" data-difficolta="facile" data-complessita="iniziare-subito" data-durata="breve" data-fase="ideate">
  <h2 class="ls-card__title">
    <a href="/structures/1-2-4-all/">1-2-4-All: far parlare tutti in 15 minuti</a>
  </h2>
  <p class="ls-card__brief">Fai emergere idee da tutti in quattro passaggi...</p>
  <div class="ls-chips ls-card__chips">
    <span class="ls-chip ls-chip--static">Facile</span>
    <span class="ls-chip ls-chip--static">15 minuti</span>
  </div>
</article>
```

**Hover:** `box-shadow: var(--md-sys-elevation-2);` transizione breve.

---

## FilterBar (`ls-filters`)

Facet client-side sul catalogo. Filter chip M3.

```html
<aside class="ls-filters" aria-label="Filtra strutture">
  <fieldset class="ls-filters__group">
    <legend>Difficolta'</legend>
    <div class="ls-chips">
      <button type="button" class="ls-chip ls-chip--filter" data-filter="difficolta" data-value="facile" aria-pressed="false">Facile</button>
      <button type="button" class="ls-chip ls-chip--filter" data-filter="difficolta" data-value="intermedia" aria-pressed="false">Intermedia</button>
    </div>
  </fieldset>
  <!-- complessita, durata, fase -->
  <button type="button" class="ls-filters__clear">Rimuovi filtri</button>
</aside>
```

**JS (`filters.js`):**

- Filtra `.ls-card` via `data-*` attributes
- Sincronizza stato con `URLSearchParams` (`?difficolta=facile&durata=breve`)
- `aria-pressed="true"` su chip attivi
- Annuncio screen reader: region `aria-live="polite"` con conteggio risultati

**Mobile:** filtri in drawer `.ls-drawer` aperto da bottone "Filtra".

---

## CtaBlock (`ls-cta`)

Una sola CTA filled per pagina.

```html
<section class="ls-cta" aria-labelledby="cta-heading">
  <h2 id="cta-heading" class="ls-cta__title">E adesso?</h2>
  <p class="ls-cta__text">Prova 1-2-4-All nella riunione di domani.</p>
  <a href="/structures/1-2-4-all/" class="ls-btn ls-btn--filled">Scegli 1-2-4-All</a>
</section>
```

**CSS filled button:**

```css
.ls-btn--filled {
  background: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
  padding: 12px 24px;
  border-radius: var(--md-sys-shape-corner-full);
  font: var(--md-sys-typescale-label-large);
  text-decoration: none;
  border: none;
}
```

---

## SiteFooter (`ls-footer`)

```html
<footer class="ls-footer" role="contentinfo">
  <div class="ls-footer__inner">
    <nav aria-label="Link footer">
      <ul class="ls-footer__nav">
        <li><a href="/structures/">Catalogo strutture</a></li>
        <li><a href="/10-principi-fondamentali-liberating-structures/">I 10 principi</a></li>
        <li><a href="/privacy-policy/">Privacy</a></li>
        <li><a href="/termini-di-servizio/">Termini</a></li>
      </ul>
    </nav>
    <p class="ls-footer__copy">Liberating.it - risorsa gratuita sulle Liberating Structures</p>
  </div>
</footer>
```

---

## Utility classes

```css
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}

.ls-zone { scroll-margin-top: calc(var(--ls-header-height) + var(--ls-mininav-height)); }
```

---

## Mappa componente → modulo v2

| Modulo Markdown (02-template) | Componente |
|-------------------------------|------------|
| Breadcrumb | `ls-breadcrumb` |
| In breve + tabella | `ls-cap` + `ls-quick-info` |
| Filtri / chip | `ls-chips` |
| Domanda / Prep / Passaggi | `ls-step-list` (passaggi), sezioni H2 |
| FAQ | `ls-faq` |
| Prima e dopo / Simili | `ls-related` |
| Prossimo nel percorso | `ls-path-nav` |
| Torna al catalogo | `ls-related__back` |
| Catalogo | `ls-card` + `ls-filters` |
| CTA editoriale | `ls-cta` |
