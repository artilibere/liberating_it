# Documentazione (liberating.it)

## Objective

Aggiornare la documentazione operativa del repository **liberating.it** (contenuti Markdown, build statico, SEO/GEO, deploy Cloudflare Pages) dopo cambiamenti significativi a build, architettura o workflow.

## Fonti di verità

| Cosa | Dove |
|------|------|
| Panoramica repo | `README.md` |
| Build, PageSpeed, cache, deploy | `docs/sito-statico.md` |
| Architettura contenuti / IA | `content/v2/01-architettura.md` |
| Template scheda / hub | `content/v2/02-template.md`, `02-template-hub.md` |
| Stato SEO editoriale | `content/seo-batch-tracker.md` |
| Skill agenti | `.cursor/skills/`, `.cursor/agents/` |
| Dati SeoZoom | `seo/{YYMMDD}/` |

## Process

1. Leggere `git log` recente e diff se il task riguarda una release specifica.
2. Verificare che `README.md` e `docs/sito-statico.md` riflettano:
   - struttura cartelle (`content/`, `public/`, `seo/`, `scripts/`)
   - comandi build e test
   - architettura PageSpeed (CSS bundle, catalog JSON, GTM post-consenso)
   - workflow SEO/GEO (audit, tracker, skill)
3. Aggiornare `content/seo-batch-tracker.md` se chiudi batch editoriali (non duplicare tutto in `docs/`).
4. Non documentare segreti (GTM ID ok se già in repo; no API key).
5. Dopo edit sostanziali: `cd public && python3 scripts/build.py && python3 scripts/test_build.py`.

## Checklist

- [ ] `README.md` allineato (quick start + link)
- [ ] `docs/sito-statico.md` aggiornato se toccati build/template/CSS/_headers
- [ ] Tracker SEO aggiornato se batch contenuti chiusi
- [ ] Nessun segreto in chiaro
- [ ] Comandi in doc verificati (build + test)

## Expected output

- Elenco file documentazione toccati
- Breve riepilogo in chat di cosa è stato documentato
- Suggerimento commit `docs:` se l'utente chiede commit

## Usage

```
/document
/document PageSpeed
/document SEO workflow
```

## Notes

- Per snapshot git puntuali usare `/snapshot` (se adattato al repo).
- Per bump versione npm usare `/version` solo nel repo WTP App (non applicabile qui).
- I piani in `.cursor/plans/` sono storico decisionale; preferire `docs/` e `content/` per doc operativa.
