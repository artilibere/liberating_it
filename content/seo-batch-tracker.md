# SEO batch tracker - liberating.it

Stato contenuti statici (`content/v2/` + build `public/`). Aggiornato: 2026-06-17 (low/verylow: skill paths, validate CI, --force generatori).

Legenda: **OK** pronto | **PARZ** revisione minore | **TODO** da riscrivere

## Fase 0 - Fondamenta

| Task | Stato | Note |
|------|-------|------|
| `content/v2/02-template.md` FAQ + JSON-LD | OK | Template scheda con FAQ |
| `content/v2/02-template-hub.md` | OK | Template hub tassonomici |
| `scripts/generate_structure_drafts.py` | OK | Output v2; skip esistenti senza `--force` |
| `scripts/generate_structure_drafts.py` | OK | Output v2; skip esistenti senza `--force` |
| `scripts/generate_structure_v2.py` | OK | Output v2; skip esistenti senza `--force` |
| `scripts/validate_sitemap_enriched.py` | OK | CI: allinea enriched vs sitemap.xml |
| `scripts/audit_content_seo.py` | OK | Audit automatico v2 |
| Quick win typo facilitazioni | OK | 10 schede v2 corrette |

## Batch 1 - Schede prioritarie (7)

| Slug | Title | Meta | FAQ | Note |
|------|-------|------|-----|------|
| 1-2-4-all | OK | OK | 4 | Riferimento gold |
| triz | OK | OK | 4 | Icona adattamento generata |
| open-space-technology-ost | OK | OK | 4 | GEO: open space technology, metodologia open space |
| social-network-webbing | OK | OK | 4 | GEO: webbing, reti informali, passaggi completi |
| w3-what-so-what-now-what | OK | OK | 4 | GEO: What So What Now What, 9 passaggi, FAQ w3 |
| ecocycle-planning | OK | OK | 3 | |
| drawing-together | OK | OK | 4 | GEO: definizione citabile, passaggi riscritti |

## Batch 2 - Calo traffico (SeoZoom PagesWithTrafficDown)

| Slug | Stato | Note |
|------|-------|------|
| 1-2-4-all | OK | Monitorare pos. 1 organico |
| ecocycle-planning | OK | GEO: modello Ecocycle, 4 FAQ, passaggi completi |
| triz | OK | |
| 9-whys | OK | GEO: tecnica 9 whys, FAQ answer-first |
| open-space-technology-ost | OK | |
| wicked-questions | OK | GEO: wicked question, strategic planning |
| shift-share | OK | GEO: shift and share, 4 FAQ |
| heard-seen-respected-hsr | OK | |
| user-experience-fishbowl | OK | FAQ riscritta |
| min-specs | OK | |
| discovery-action-dialogue-dad | OK | FAQ riscritta |
| panarchy | OK | GEO: modello panarchy, link Ecocycle |

## Batch 3 - GEO zero menzioni AI (PagesWithPotential)

| Slug / URL | Stato | Note |
|------------|-------|------|
| difficolta/intermedia | OK | Hub intro GEO in build |
| shift-share | OK | Riscritta sessione 2026-06-16 |
| purpose-to-practice-p2p | OK | 5 elementi P2P, 4 FAQ |
| improv-prototyping | OK | Meta fix, 4 FAQ |
| complessita/iniziare-subito | OK | Hub FAQ in build |
| complessita/facilitazioni-complesse | OK | Hub FAQ+intro GEO |
| complessita/team-rodati | OK | Hub page_title, 4 FAQ, intro GEO |
| home `/` | OK | Title/meta keyword brand, FAQ build |

## Batch 4 - Adattamenti legacy (meta + GEO)

| Slug | Stato | Note |
|------|-------|------|
| mad-tea | OK | Meta fix, cerchi concentrici, 4 FAQ |
| spiral-journal | OK | Spirale + quadranti, 4 FAQ |
| liquid-courage | OK | Variante Impromptu, 4 FAQ |
| pixies-reflection | OK | 4 domande guida, link TRIZ/Pixies |
| talking-with-pixies | OK | Meta e title SERP-friendly |
| mad-love | OK | Meta riscritta |
| tiny-demons | OK | Meta riscritta |

## Batch 5 - Restanti schede v2

41/41 schede presenti, audit SEO `--strict` OK (title, meta, FAQ).

## Hub tassonomici (17)

| Tipo | Stato | Note |
|------|-------|------|
| complessita (4) | OK build | FAQ + JSON-LD in `build.py` |
| difficolta (3) | OK build | |
| durata (4) | OK build | |
| design-thinking (6) | OK build | |
| per-bisogno (5) | OK build | |

## Pagine editoriali

| URL | Stato | Note |
|-----|-------|------|
| `/` home | OK | Title "Liberating Structures in italiano", meta brand |
| `/10-principi-fondamentali-liberating-structures/` | OK | FAQ generate in build |
| `/privacy-policy/` | OK | Allineata sito statico + GTM |
| `/termini-di-servizio/` | OK | Allineati a privacy policy (sito statico) |

## Asset

| Asset | Stato |
|-------|-------|
| Icone strutture | **41/41** |
| OG strutture | 41/41 |
| `sitemap-enriched.json` | OK | Refresh statico via `scripts/refresh_sitemap_enriched.py` |
| Sitemap statica | 68 URL |
| Title SERP (41 schede) | OK | `title` <= 43 char, no ellissi in build |
| Title SERP (hub) | OK | Tutti gli hub <= 60 char nel build |

## Batch 6 - Fix SEO SeoZoom 260702

| Slug / URL | Stato | Note |
|------------|-------|------|
| triz | OK | GEO: distinzione TRIZ ingegneristica, FAQ citabili |
| 25-10-crowd-sourcing | OK | crowd sourcing / crowdsourcing |
| 9-whys | OK | root cause, 5 perche' |
| open-space-technology-ost | OK | OST, metodologia open space, cos'e' |
| social-network-webbing | OK | webbing keyword |
| ecocycle-planning | OK | eco cycle planning, ecocycle, template |
| w3-what-so-what-now-what | OK | What So What Now What, anti-cannibalizzazione hub |
| heard-seen-respected-hsr | OK | HSR acronimo, 4 FAQ GEO |
| troika-consulting | OK | troika consulting method, GEO |
| 1-2-4-all | OK | 2 4 1 variant |
| conversation-cafe | OK | vs World Cafe |
| agreement-certainty-matrix | OK | decision making, agreement certainty |
| complessita/iniziare-subito | OK | FAQ W³ punta a scheda struttura |
| difficolta/intermedia | OK | Conversation Cafe in intro + FAQ |
| design-thinking/define | OK | decision making FAQ |
| design-thinking/ideate | OK | pensiero creativo FAQ |
| per-bisogno/prendere-decisioni | OK | agreement certainty matrix |
| per-bisogno/analizzare-problemi | OK | root cause / 5 perche' |

Aggiornato: 2026-07-02.

## Comandi utili

```bash
python3 scripts/audit_content_seo.py
python3 scripts/audit_content_seo.py --strict
python3 scripts/refresh_sitemap_enriched.py
python3 scripts/validate_sitemap_enriched.py
cd public && python3 scripts/build.py --content ../content/v2 --out . && python3 scripts/test_build.py
```
