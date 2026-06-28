# liberating.it

Sito statico in italiano sulle [Liberating Structures](https://www.liberatingstructures.com/): schede operative, catalogo filtrabile, hub per bisogno e tassonomie (difficoltà, durata, design thinking).

**Produzione:** [https://liberating.it](https://liberating.it) (Cloudflare Pages)  
**Stack:** Markdown (`content/`) → build Python/Jinja (`public/scripts/build.py`) → HTML/CSS/JS statici in `public/`

## Struttura repository

```
content/v2/strutture/   # Schede struttura (fonte attiva, 41 file)
content/v1/pagine/      # Pagine editoriali e legali
content/v2/             # Template e architettura IA
seo/{YYMMDD}/           # Export SeoZoom, Screaming Frog, analytics
public/                 # Output build + asset (deploy)
public/scripts/         # build.py, test, icone
scripts/                # Audit SEO, generatori draft, sitemap
.cursor/skills/         # Tone of voice, SEO/GEO, LS, UI/UX
```

## Quick start

```bash
# Build sito statico
cd public && python3 scripts/build.py

# Test build (78 test)
python3 scripts/test_build.py

# Anteprima locale
python3 scripts/serve.py

# Audit SEO contenuti v2 (dalla root repo)
python3 scripts/audit_content_seo.py --strict
```

Output: `public/index.html`, `public/structures/`, hub, sitemap (68 URL).

## Documentazione

| Documento | Contenuto |
|-----------|-----------|
| [docs/sito-statico.md](docs/sito-statico.md) | Build, PageSpeed, cache, deploy |
| [content/v2/01-architettura.md](content/v2/01-architettura.md) | IA, menu, hub, catalogo |
| [content/seo-batch-tracker.md](content/seo-batch-tracker.md) | Stato batch SEO/GEO |
| [.cursor/agents/seo-geo-specialist.md](.cursor/agents/seo-geo-specialist.md) | Agente SEO/GEO |

## Cursor commands

Comandi in `.cursor/commands/`: `improve`, `commit`, `document`, `test`, `review`, `snapshot`.

## Release recente (giu 2026)

- Catalogo: card idratate da `structures/catalog.json` (~26 KB HTML vs ~62 KB)
- PageSpeed: CSS bundle + preload, GTM post-consenso, JS per pagina, `backdrop-filter` solo desktop (header + mininav)
- SEO: 41/41 schede con FAQ, hub con JSON-LD, audit `--strict` OK
- PSI mobile (28 giu 2026): home e catalogo **100**; schede **99–100** (CLS mobile da monitorare)

Commit: `c9c202a` su `main`.
