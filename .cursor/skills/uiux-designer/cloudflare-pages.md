# Cloudflare Pages - liberating.it site

Configurazione del repo GitHub separato per il frontend statico. Il repo content (`liberating.it`) resta la sorgente Markdown; il repo site compila e deploya.

---

## Struttura repo `liberating-it-site`

```
liberating-it-site/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── scripts/
│   └── build.py                 # MD → HTML + index.json
├── templates/                   # Jinja2 (opzionale)
│   ├── base.html
│   ├── structure.html
│   ├── catalog.html
│   └── hub.html
├── assets/
│   ├── css/
│   │   ├── tokens.css
│   │   ├── base.css
│   │   └── components.css
│   └── js/
│       ├── nav.js
│       ├── filters.js
│       └── scroll-spy.js
├── content/                     # vuoto in repo; popolato in CI
├── dist/                        # output build (gitignored)
├── _headers
├── _redirects
├── .gitignore
├── requirements.txt             # se build Python
└── README.md
```

**Output deploy:** directory `dist/` (build command popola questa cartella).

---

## Sync content → site

### Default: GitHub Actions checkout (consigliato)

Il workflow scarica il repo content al build. Nessun submodule da mantenere.

```yaml
- name: Checkout content repo
  uses: actions/checkout@v4
  with:
    repository: org/liberating.it
    path: content-src
    token: ${{ secrets.GH_PAT }}
```

Poi: `python scripts/build.py --content content-src/content/v2 --out dist`

### Alternativa: git submodule

```bash
git submodule add https://github.com/org/liberating.it.git content
git submodule update --init --recursive
```

Build: `--content content/content/v2`

### Alternativa: export manuale

```bash
rsync -av /path/to/liberating.it/content/v2/ ./content/
python scripts/build.py --content content --out dist
```

---

## Cloudflare Pages (dashboard)

| Impostazione | Valore |
|--------------|--------|
| Production branch | `main` |
| Build command | `pip install -r requirements.txt && python scripts/build.py --content content-src/content/v2 --out dist` |
| Build output directory | `dist` |
| Root directory | `/` |

Variabili ambiente (se serve PAT per checkout privato): `GH_PAT`.

---

## GitHub Actions workflow

`.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloudflare Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  deployments: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout site repo
        uses: actions/checkout@v4

      - name: Checkout content repo
        uses: actions/checkout@v4
        with:
          repository: YOUR_ORG/liberating.it
          path: content-src
          token: ${{ secrets.GH_PAT }}

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Build
        run: |
          pip install -r requirements.txt
          python scripts/build.py --content content-src/content/v2 --out dist

      - name: Publish to Cloudflare Pages
        uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          projectName: liberating-it
          directory: dist
          gitHubToken: ${{ secrets.GITHUB_TOKEN }}
```

**Secrets richiesti:**

- `CLOUDFLARE_API_TOKEN` — token con permesso Cloudflare Pages Edit
- `CLOUDFLARE_ACCOUNT_ID` — ID account Cloudflare
- `GH_PAT` — solo se repo content privato

---

## `_headers`

File in root del output `dist/_headers`:

```
# Cache asset statici (1 anno)
/assets/*
  Cache-Control: public, max-age=31536000, immutable

# HTML: sempre revalidare
/*.html
  Cache-Control: public, max-age=0, must-revalidate

/
  Cache-Control: public, max-age=0, must-revalidate

# Security
/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
```

CSP base (opzionale, aggiungere quando stabile):

```
/*
  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'
```

---

## `_redirects`

Preservare i **62 URL** da [sitemap-enriched.json](../../../sitemap-enriched.json). Cloudflare Pages usa sintassi Netlify:

```
# Trailing slash coerente
/structures/:slug  /structures/:slug/  301
/complessita/:slug  /complessita/:slug/  301

# Legacy WordPress (esempi — verificare contro sitemap)
/struttura/:slug  /structures/:slug/  301
/wp-content/*  /  404

# Nuovi path hub Per bisogno (se non in sitemap legacy)
/per-bisogno  /per-bisogno/  301
```

**Processo aggiornamento redirect:**

1. Leggi `sitemap-enriched.json` → `urls[]` o indice per slug
2. Per ogni URL cambiato, aggiungi riga `vecchio  nuovo  301`
3. Testa in preview CF prima di merge su `main`

**Trailing slash:** il sito v2 usa trailing slash ovunque (`/structures/1-2-4-all/`). Redirect senza slash → con slash.

---

## Preview e validazione

1. **Locale:** `python scripts/build.py ... && npx serve dist` oppure `python -m http.server -d dist`
2. **CF Preview:** ogni PR genera URL preview (se abilitato su project Pages)
3. **Checklist pre-deploy:**
   - [ ] 41 schede in `dist/structures/{slug}/index.html`
   - [ ] Catalogo `dist/structures/index.html`
   - [ ] Hub tassonomia (17 termini da sitemap)
   - [ ] Home, principi, privacy, termini
   - [ ] `_redirects` copiato in dist
   - [ ] Link interni con trailing slash
   - [ ] Nessun 404 su URL in sitemap

---

## Dominio custom

In Cloudflare Pages → Custom domains → `liberating.it` + `www.liberating.it`

- DNS: CNAME `liberating.it` → `liberating-it.pages.dev`
- Redirect `www` → apex (o viceversa, coerente con canonical in content)

---

## README minimo repo site

Il `README.md` del repo site deve documentare:

1. Prerequisiti (Python 3.12, pip)
2. Build locale con path al content repo
3. Struttura `dist/`
4. Come aggiornare `_redirects`
5. Link alla skill [uiux-designer](https://github.com/YOUR_ORG/liberating.it/tree/main/.cursor/skills/uiux-designer) nel repo content

---

## Anti-pattern deploy

- Deployare Markdown grezzo senza build (CF Pages non renderizza MD nativamente)
- Dimenticare di copiare `_headers` e `_redirects` in `dist/`
- Build output su root repo senza `dist/` (confonde asset e sorgenti)
- Force push su `main` per fix deploy — usare nuovo commit
- SPA fallback `/* /index.html 200` — **non usare** (sito multi-pagina statico)
