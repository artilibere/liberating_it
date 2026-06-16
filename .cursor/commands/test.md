# Esegui test (WTP App)

## Objective

Eseguire la suite di test del **backend** e, se utile, test e lint del **frontend**, dalla root del monorepo.

## Process

1. **Backend** (obbligatorio per `/test`):
   ```bash
   cd backend && npm test
   ```
   Usa preload `src/test/preload-test-artifact-mode.js` e `--test-concurrency=1` (come in `package.json`).

2. **Coverage backend** (opzionale, su richiesta o se si indaga copertura):
   ```bash
   cd backend && npm run test:coverage
   ```

3. **Frontend** (se modifiche UI/logica client):
   ```bash
   cd frontend && npm run test
   cd frontend && npm run lint
   ```

4. **Sintassi entrypoint API** (rapido):
   ```bash
   node --check backend/src/server.js
   ```

## Dove sono i test

| Area | Percorso |
|------|-----------|
| Backend (Node `--test`) | `backend/src/**/*.test.js`, integrazione `wtpApi.integration.test.js` |
| Frontend | `frontend/src/wtp/*.test.js` (runner `npm run test`) |
| Lint UI | `frontend/eslint.config.js` → `npm run lint` |

## Checklist

- [ ] `backend`: `npm test` exit 0
- [ ] `frontend`: `npm run test` e `npm run lint` se area frontend coinvolta
- [ ] `node --check backend/src/server.js` se toccato `server.js`

## Expected output

- Log sintetico o esito per ogni comando
- Elenco test falliti con file e messaggio

## Usage

```
/test
```

## Notes

- Mongo / variabili `.env` possono influenzare test di integrazione: vedere messaggi in console.
- Non esiste `pytest` né `business/test/` in questo repo.
