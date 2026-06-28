# Sito statico — build, performance, deploy

Documentazione tecnica per `public/` e pipeline di build. Aggiornato: 2026-06-28.

## Pipeline

```
content/v2/strutture/*.md
content/v1/pagine/*.md
        │
        ▼
public/scripts/build.py  (+ Jinja templates in public/templates/)
        │
        ▼
public/                  ← root deploy Cloudflare Pages
  index.html
  structures/{slug}/index.html
  structures/catalog.json
  assets/css/site.{hash}.css
  assets/js/*.js
  sitemap.xml
```

### Comandi

| Comando | Scopo |
|---------|--------|
| `cd public && python3 scripts/build.py` | Build completo |
| `python3 scripts/test_build.py` | Test unitari build (78) |
| `python3 scripts/serve.py` | Server locale |
| `python3 ../scripts/audit_content_seo.py --strict` | Title, meta, FAQ min 3 |
| `python3 ../scripts/refresh_sitemap_enriched.py` | Sitemap arricchita |
| `python3 ../scripts/validate_sitemap_enriched.py` | CI allineamento sitemap |

Argomenti build: `--content`, `--out` (default `content/v2` → `public/`).

## Tipi di pagina e sorgenti

| Tipo | Output | Sorgente contenuto |
|------|--------|-------------------|
| Scheda struttura | `/structures/{slug}/` | `content/v2/strutture/{slug}.md` |
| Catalogo | `/structures/` | `build.py` + `catalog.json` |
| Hub tassonomia | `/difficolta/`, `/durata/`, … | Dict `HUBS_*` in `build.py` |
| Per bisogno | `/per-bisogno/` | `PER_BISOGNO` in `build.py` |
| Home, principi | `/`, `/10-principi-…/` | `build.py` + `content/v1/pagine/` |
| Legali | `/privacy-policy/`, … | `content/v1/pagine/` |

### Limiti SEO (build)

- Schede: `title` ≤ 43 caratteri (`TITLE_SERP_BUDGET`) + suffix ` | Liberating.it`
- Hub/editoriali: `page_title` ≤ 60 caratteri
- `meta_description` ≤ 155 caratteri, frase completa
- FAQ: minimo 3 per scheda; JSON-LD `FAQPage` generato in build
- Catalogo: `ItemList` JSON-LD + `<noscript>` con link alle schede

## Architettura PageSpeed

Ottimizzazioni attive (non regressione):

| Area | Implementazione | File |
|------|-----------------|------|
| CSS | Bundle hashato esterno + `preload as="style"` | `bundle_css`, `templates/base.html` |
| JS | Bundle per tipo pagina, `defer` | `PAGE_JS_BUNDLES` in `build.py` |
| GTM | Caricamento solo dopo consenso cookie | `tracking-deferred.html`, `consent.js` |
| Catalogo | Hydration da `catalog.json`; HTML leggero | `catalog-render.js`, `write_catalog_json` |
| LCP scheda | Preload icona struttura | `templates/structure.html` |
| Below-fold | `content-visibility: auto` | `.ls-zone--defer` in `components.css` |
| Sticky paint | `backdrop-filter` solo ≥900px | `.ls-header`, `.ls-mininav` |
| Cache | Asset 1y immutable; HTML must-revalidate | `public/_headers` |
| HTML | Minificato | `minify_html` |

### Bundle JS per pagina

```python
PAGE_JS_BUNDLES = {
    "structure": ("scroll-spy.js", "share.js"),
    "catalog": ("catalog-render.js", "filters-panel.js", "filters.js"),
}
```

Globale su tutte le pagine: `nav.js`; se tracking + consenso: `consent.js`.

## Verifica PageSpeed

1. Deploy su Cloudflare Pages (branch `main`).
2. [PageSpeed Insights](https://pagespeed.web.dev/) — mobile first.
3. Baseline storica: `seo/260616/https___liberating.it_Page-Speed.csv`.

### Risultati PSI (28 giu 2026, live)

| URL | Mobile Perf | LCP | CLS | Note |
|-----|-------------|-----|-----|------|
| `/` | 100 | 0,8 s | 0 | — |
| `/structures/` | 100 | 1,5 s | 0,028 | shift post-hydration card |
| `/structures/1-2-4-all/` | 99 | 0,9 s | 0,073 | layout shift mobile |
| `/structures/1-2-4-all/` desktop | 100 | 0,4 s | 0 | — |

Opportunità residue (basso impatto): CSS render-blocking ~130 ms; cache marginale ~5 KiB.

## Deploy Cloudflare Pages

- **Root directory:** `public/`
- **Build command:** opzionale `python3 scripts/build.py` in CI se si rigenera da `content/`
- **Headers:** `public/_headers` (cache, sicurezza)
- Dettagli: `.cursor/skills/uiux-designer/cloudflare-pages.md`

## SEO / dati

- Export SeoZoom in `seo/{YYMMDD}/` (cartella data più recente)
- Workflow: skill `.cursor/skills/seo-geo-specialist/`, agente `.cursor/agents/seo-geo-specialist.md`
- Tracker batch: `content/seo-batch-tracker.md`

## Asset

- Icone strutture: 41/41 (`public/scripts/generate_adaptation_icons.py`)
- Manifest icone: `public/assets/images/structures/manifest.json`
- CSS manifest: `public/assets/build-manifest.json` (path hashati)
