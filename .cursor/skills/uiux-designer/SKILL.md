---
name: uiux-designer
description: Progetta interfaccia e struttura grafica del sito statico liberating.it (HTML+JS+CSS) a partire da content/v2/, con design system Material 3 tokens, componenti, template pagina e deploy Cloudflare Pages via GitHub. Usare quando si crea o modifica il frontend, wireframe, CSS, layout schede strutture, catalogo filtrabile, o si configura il repo site separato.
---

# UI/UX Designer - liberating.it statico

Progetta l'interfaccia del sito statico HTML+JS+CSS a partire dai contenuti in `content/v2/`. Il frontend vive in un **repo GitHub separato** (es. `liberating-it-site`); questo repo e' content-only.

Documentazione di dettaglio (progressive disclosure):

| File | Contenuto |
|------|-----------|
| [design-system.md](design-system.md) | Token Material 3, tipografia, palette, spacing, motion |
| [componenti.md](componenti.md) | Spec HTML/CSS/ARIA per ogni componente `ls-*` |
| [template-pagine.md](template-pagine.md) | Layout per tipo pagina (home, catalogo, scheda, hub) |
| [mapping-contenuti.md](mapping-contenuti.md) | Frontmatter MD → HTML, build script, JSON index |
| [cloudflare-pages.md](cloudflare-pages.md) | Repo site, deploy, `_headers`, `_redirects` |

## Prima di progettare

Leggi in ordine:

1. [content/v2/01-architettura.md](../../../content/v2/01-architettura.md) — menu, hub, URL, modello 3 zone, internal linking
2. [content/v2/02-template.md](../../../content/v2/02-template.md) — moduli obbligatori per scheda e pagina editoriale
3. Scheda di riferimento: [content/v2/strutture/1-2-4-all.md](../../../content/v2/strutture/1-2-4-all.md)
4. [liberating-tone-of-voice](../liberating-tone-of-voice/SKILL.md) — microcopy UI (CTA, label, aria-label)
5. [seo-geo-specialist](../seo-geo-specialist/SKILL.md) — `<title>`, meta, JSON-LD FAQ, gerarchia heading

## Principi UX (priorita' assolute)

| Principio | Implicazione UI |
|-----------|-----------------|
| Manuale operativo, non vetrina | Layout arioso, tipografia leggibile, zero decorazioni superflue |
| Scannerizzabile in 10 sec (zona Cap) | Above-the-fold con gerarchia chiara; scheda rapida compatta |
| Inclusione e autonomia | Una CTA per pagina; prev/next visibile; filtri accessibili |
| v2 rompe con WP legacy | **No emoji** negli heading; niente stile Avada/Fusion; layout 3 zone |
| Community gratuita | Nessun pattern e-commerce; footer leggero; niente popup |

### Tre obiettivi operativi

1. **Semplicita' e praticita'** — colonna singola per il body (max 72ch); zona Cap unificata; una sola CTA primaria
2. **Rapidita' di fruizione** — mini-nav Cap/Fare/Naviga; passaggi con badge tempo; FAQ con `<details>` nativo
3. **Navigazione tra contenuti** — PathNav sticky su mobile; RelatedLinks unificato; chip tassonomia sempre cliccabili; catalogo con filtri facet e URL condivisibili

## Tipi di pagina

| Tipo | Sorgente | Template |
|------|----------|----------|
| Home | `content/v1/pagine/home.md` (da portare in v2) | [template-pagine.md § Home](template-pagine.md#home) |
| Catalogo | IA § catalogo | [template-pagine.md § Catalogo](template-pagine.md#catalogo) |
| Scheda struttura | `content/v2/strutture/*.md` | [template-pagine.md § Scheda](template-pagine.md#scheda-struttura) |
| Hub tassonomia | IA § filtri | [template-pagine.md § Hub tassonomia](template-pagine.md#hub-tassonomia) |
| Hub "Per bisogno" | IA § sottomenu | [template-pagine.md § Per bisogno](template-pagine.md#hub-per-bisogno) |
| Editoriale | template v2 pagine | [template-pagine.md § Editoriale](template-pagine.md#pagina-editoriale) |
| Legale | privacy/termini | [template-pagine.md § Legale](template-pagine.md#pagina-legale) |

## Modello scheda a 3 zone

Ogni scheda struttura segue Cap → Fare → Naviga (vedi [02-template.md](../../../content/v2/02-template.md)):

```
Cap     → breadcrumb, In breve, scheda rapida, chip tassonomia
Fare    → Domanda da portare, Cosa ti serve, I passaggi
Naviga  → Quando usarla, Consiglio, Errori, FAQ, Prima/Dopo, Simili, Percorso, Torna al catalogo
```

Percorso guidato "Per iniziare subito" (prev/next hardcoded):

1. impromptu-networking → 2. 1-2-4-all → 3. w3-what-so-what-now-what → 4. 15-solutions → 5. troika-consulting

Fonte: [scripts/generate_structure_v2.py](../../../scripts/generate_structure_v2.py) (`PATH_ORDER`).

## Workflow operativo

```
Task Progress:
- [ ] 1. Leggere 01-architettura + 02-template + scheda esempio
- [ ] 2. Identificare tipo pagina e moduli obbligatori
- [ ] 3. Applicare design system (design-system.md)
- [ ] 4. Comporre HTML semantico con componenti ls-* (componenti.md)
- [ ] 5. Verificare microcopy con tone-of-voice
- [ ] 6. Verificare SEO: title, meta, H1, JSON-LD FAQ (seo-geo-specialist)
- [ ] 7. Test responsive (mobile-first) e accessibilita' (focus, contrasto, accordion)
- [ ] 8. Aggiornare _redirects se nuovi slug
- [ ] 9. Validare build locale + preview Cloudflare
```

## Integrazione con altre skill

| Skill | Ruolo nel frontend |
|-------|-------------------|
| liberating-tone-of-voice | Label, CTA, aria-label, no emoji, una CTA per pagina |
| seo-geo-specialist | Meta, FAQ schema, struttura H1/H2, canonical |
| ls-content-specialist | Coerenza moduli 3 zone, chip tassonomia, string |

**Regola di conflitto:** accessibilita' e leggibilita' > decorazione; tone-of-voice > copy marketing UI.

## Sync content → site

Tre modalita' (default consigliato: **GitHub Actions checkout**):

1. **Git submodule** — `content/` nel repo site punta al repo liberating.it
2. **GitHub Actions checkout** — workflow scarica `content/v2/` al build
3. **Export manuale** — script copia MD in `site/content/`

Dettaglio deploy: [cloudflare-pages.md](cloudflare-pages.md).

## Cosa NON fare

- Framework CSS pesanti (Bootstrap, Tailwind) — vanilla CSS con custom properties M3
- SPA/router client-side per contenuto indicizzabile — pagina HTML statica per ogni URL
- Copiare layout WP a 5 sezioni con emoji
- Multipli CTA in competizione sulla stessa pagina
- Font/icon pack esterni non necessari
- Material Web Components o bundler obbligatori — solo token M3 in CSS

## Checklist finale

- [ ] Tipo pagina e moduli obbligatori identificati
- [ ] Token M3 applicati (`tokens.css`)
- [ ] Componenti `ls-*` con stati focus/hover e ARIA
- [ ] Zona Cap scannable in 10 sec; mini-nav su scheda
- [ ] Navigazione correlati: PathNav + RelatedLinks + chip
- [ ] Microcopy verificato (tone-of-voice)
- [ ] SEO: title <= 60, meta <= 155, FAQ JSON-LD
- [ ] Mobile-first, contrasto WCAG AA, keyboard navigabile
- [ ] `_redirects` allineati a [sitemap-enriched.json](../../../sitemap-enriched.json)
- [ ] Build locale + preview Cloudflare OK
