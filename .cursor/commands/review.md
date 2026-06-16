# Code review (WTP App)

## Objective

Revisione manuale (checklist) del diff o dell’area indicata, adatta a **monorepo** React + Express (liste WTP, job asincroni, artefatti).

## Process

1. **Funzionalità**: il comportamento corrisponde al task? Edge case (input vuoti, job falliti, file mancanti)?
2. **API** (`backend/src/routes/wtp/`, schemi Zod): validazione, status HTTP, messaggi d’errore utili; limiti in `wtpLimits.js`.
3. **UI** (`frontend/src/`): stati loading/errore, i18n (`it.po` / `en.po`), accessibilità base MUI.
4. **Sicurezza**: niente segreti hardcoded; path file/job sanitizzati dove serve; `WTP_API_KEY` / CORS come da doc.
5. **Coerenza doc**: se cambiano contratti o limiti, è aggiornato `docs/` (vedi `.cursorrules`)?
6. **Test**: esistono o vanno aggiunti test mirati in `backend/src/**/*.test.js` per la logica nuova?
7. Output: report in chat; opzionalmente file `docs/reviews/CODE_REVIEW_YYYY-MM-DD.md` **solo se** l’utente vuole tracciamento persistente (creare cartella se assente).

## Checklist

- [ ] Correttezza e gestione errori
- [ ] Zod + limiti allineati a `wtpLimits.js` / `limits.js`
- [ ] Stringhe e tono (brand voice) se UI o copy generato
- [ ] Nessun segreto nel codice
- [ ] Doc toccata se necessario
- [ ] Test backend (almeno i file correlati) consigliati o eseguiti

## Expected output

- Lista finding (blocker / nice-to-have)
- Suggerimenti concreti (file + idea fix)
- Opzionale: path del file review in `docs/reviews/` se creato

## Usage

```
/review
```

## Notes

- Non confondere con `/test` (esecuzione automatica suite).
- Rispettare lo stile esistente (CommonJS backend, ESM frontend).
