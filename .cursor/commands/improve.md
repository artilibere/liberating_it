# Miglioramenti codice (WTP App)

## Objective

Analizzare e proporre (o applicare con approvazione) miglioramenti mirati al codice **frontend** (React 19, Vite 8, MUI) e **backend** (Express 5, MongoDB, Zod), senza refactor gratuiti.

## Process

1. **Contesto**: identificare file/area in lavorazione (liste WTP, job, cataloghi, scheda cliente, i18n, ecc.).
2. **Qualità** (solo ciò che ha senso in JS):
   - Duplicazioni evitabili, nomi chiari, percorsi d’errore gestiti
   - Validazione lato server (Zod) e coerenza con `wtpLimits.js`
   - Allineamento `frontend/src/wtp/limits.js` se cambiano i tetti
   - Testo UI / generato: `docs/ui-copy-brand-voice.md`, `data/prompts.js` dove applicabile
3. **Sicurezza**: niente segreti in codice; auth opzionale `WTP_API_KEY` come da `wtp-app-1.3.md`
4. Dopo modifiche sostanziali: `cd backend && npm test` e, se toccato il frontend, `cd frontend && npm run lint` e `npm run test`
5. Evitare di “pulire” file non toccati dal task.

## Checklist

- [ ] Miglioramenti pertinenti al task corrente
- [ ] Limiti e schemi Zod coerenti se si toccano input API
- [ ] Test backend (e lint/test frontend se rilevanti) dopo edit
- [ ] Nessun refactor di massa non richiesto

## Expected output

- Elenco suggerimenti prioritizzati
- Se applicati: diff sintetico + esito comandi di verifica

## Usage

```
/improve
```

## Notes

- Per revisione mirata a PR/diff usare `/review`.
- Per esecuzione test completa usare `/test`.
