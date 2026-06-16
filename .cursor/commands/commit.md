# Pre-commit (WTP App)

## Objective

Verificare che le modifiche siano pronte per il commit nel monorepo **Sales Coach / WTP App** (React + Express, MongoDB) e proporre messaggio e comando `git`.

## Process

1. Dalla **root del repository** (`WTP_App`), in base a cosa è cambiato:
   - **Backend**: `cd backend && npm test`
   - **Frontend** (se toccato `frontend/src` o test): `cd frontend && npm run test`
   - **Frontend lint** (se toccato `frontend/`): `cd frontend && npm run lint`
   - **Entry API** (se toccato `backend/src/server.js`): `node --check backend/src/server.js`
2. Controllare `git status` e il diff: niente segreti (`.env`, chiavi API, token) nei file tracciati.
3. Se il cambiamento tocca **HTTP, job, auth, limiti**: verificare che sia aggiornata la doc già narrata in `docs/` (vedi `.cursorrules`).
4. Se il cambiamento tocca **limiti condivisi**: `backend/src/schemas/wtpLimits.js` e `frontend/src/wtp/limits.js` allineati.
5. **Stringhe UI / i18n**: se modificate, `frontend/public/locales/it.po` e `en.po` coerenti con `docs/ui-copy-brand-voice.md`.
6. Generare messaggio di commit (conventional) e comando `git add` / `git commit` suggerito.

## Checklist

- [ ] `npm test` in `backend/` (se rilevante)
- [ ] `npm run test` / `npm run lint` in `frontend/` (se rilevante)
- [ ] `node --check backend/src/server.js` (se toccato entrypoint)
- [ ] Nessun segreto nel commit
- [ ] Limiti API/UI allineati se applicabile
- [ ] Doc `docs/` aggiornata se contratti o comportamento HTTP cambiano

## Commit message (conventional)

Esempi:

- `feat:` nuova funzionalità utente/API
- `fix:` correzione bug
- `docs:` solo documentazione
- `chore:` tooling, dipendenze, config
- `refactor:` ristrutturazione senza cambio comportamento

Messaggio in **frasi complete**, inglese o italiano come nel resto del repo (coerente col diff).

## Expected output

- Esito comandi eseguiti
- Checklist sintetica
- Messaggio commit proposto + `git add …` e `git commit -m "…"`

## Usage

```
/commit
```

## Notes

- Non esiste `CHANGELOG.md` obbligatorio in root: il versioning release è in `docs/wtp-app-1.8.md` e semver in `package.json` (vedi `/version`).
- `.env` non va committato (è in `.gitignore`).
