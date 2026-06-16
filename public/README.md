# liberating-it-site (in-repo: public/)

Frontend statico per [liberating.it](https://liberating.it): HTML + CSS + JS vanilla, design system Material 3 tokens.

I contenuti Markdown sono in `../content/v2/`. Il build genera HTML navigabile in questa cartella.

## Aprire il sito in locale

Dopo il build, apri direttamente nel browser:

```
/var/www/liberating.it/public/index.html
```

Tutti i link usano percorsi relativi: funziona aprendo il file da disco (`file://`) senza server.

In alternativa, con server locale (URL puliti e redirect da `index.html`):

```bash
python3 scripts/serve.py --port 8080 --directory /var/www/liberating.it/public
```

Apri http://localhost:8080/

Per test rapido senza server:

```bash
python3 -m http.server 8080 --directory /var/www/liberating.it/public
```

Apri http://localhost:8080/

## Build

```bash
cd /var/www/liberating.it/public
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python scripts/build.py --content ../content/v2 --out .
```

Per aggiornare le icone ufficiali delle strutture (da [liberatingstructures.com/ls-menu-1](https://www.liberatingstructures.com/ls-menu-1)):

```bash
python3 scripts/fetch_ls_icons.py
python3 scripts/build.py --content ../content/v2 --out .
```

Output principale: `index.html`, `structures/`, hub tassonomia, `per-bisogno/`, `assets/`.

Per build in sottocartella `dist/` (deploy Cloudflare):

```bash
python scripts/build.py --content ../content/v2 --out dist
```

## Struttura

```
index.html             Home (entry point)
structures/            Catalogo + 41 schede
complessita/           Hub percorso
difficolta/            Hub difficolta'
durata/                Hub durata
design-thinking/       Hub fase DT
per-bisogno/           Hub per obiettivo
assets/                CSS (tokens M3) + JS (nav, filtri, scroll-spy)
templates/             Jinja2 (sorgenti build)
scripts/build.py       Genera HTML da content/v2/strutture/
_headers               Cache e security (Cloudflare Pages)
_redirects             Redirect SEO
```

## Deploy Cloudflare Pages

Workflow GitHub Actions in `.github/workflows/deploy.yml` (monorepo).

1. Build command: `python scripts/build.py --content ../content/v2 --out dist`
2. Output directory: `public/dist`
3. Secrets richiesti nel repo GitHub: `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`

## Skill di riferimento

`.cursor/skills/uiux-designer/` nel repo content.
