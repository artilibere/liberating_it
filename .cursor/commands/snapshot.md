# Snapshot progetto (WTP App)

## Objective

Catturare in un unico markdown lo **stato del repository** utile per debug, handoff o confronto (senza sostituire `git`).

## Process

1. Dalla **root del repository** raccogliere (comandi da eseguire o output incollato):
   - `git rev-parse HEAD` e `git status -sb`
   - Versione da `frontend/package.json` e `backend/package.json` (`version`)
   - `cd backend && npm test` (esito sintetico)
   - Opzionale: `cd frontend && npm run test` e `npm run lint`
2. Creare **`docs/snapshots/`** se non esiste.
3. Scrivere `docs/snapshots/SNAPSHOT_YYYY-MM-DD_HH-mm.md` con:
   - Data/ora (UTC o locale, indicata esplicitamente)
   - Commit e branch
   - Versioni npm dal `package.json`
   - Esito test (pass/fail, file fallito se noto)
   - Note libere (es. “Docker up”, “solo backend modificato”)

## Checklist

- [ ] Commit e stato git registrati
- [ ] Versioni 1.8.x da package.json
- [ ] Esito `npm test` backend (e frontend se eseguito)
- [ ] File snapshot creato sotto `docs/snapshots/`

## Expected output

- Path del file snapshot creato
- Breve riepilogo in chat

## Usage

```
/snapshot
```

## Notes

- Non committare segreti nello snapshot.
- Per solo versioning release usare `/version`.
