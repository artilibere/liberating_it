# Versioning release (WTP App)

## Objective

Allineare **versione prodotto** e **semver npm** per una release Sales Coach / WTP App, come descritto in `docs/wtp-app-1.8.md` (e file analoghi per bump futuri).

## Fonti di verità

| Cosa | Dove |
|------|------|
| Versione prodotto (es. **1.8**) | Titolo UI `ListsWtpTitle` in `frontend/public/locales/it.po` e `en.po`; `<title>` in `frontend/index.html` |
| Semver pacchetti (**1.8.0**) | `frontend/package.json`, `backend/package.json` e relativi **`package-lock.json`** |
| Doc release | `docs/wtp-app-1.8.md` (per la lineage 1.8); per nuova major/minor creare/aggiornare il file doc di release corrispondente e link in README se serve |
| Specifiche utente | `docs/SPEC-WTPAPP_v1.8.md` (rinominare/duplicare pattern per nuova versione) |

**Non** esiste in questo progetto un `VERSION=…` in `.env` per la release app: la versione è nei file sopra.

## Process

1. Leggere versioni attuali da `frontend/package.json`, `backend/package.json` e stringhe in `.po` / `index.html`.
2. Se l’utente chiede un bump:
   - **Patch** (1.8.0 → 1.8.1): aggiornare semver in entrambi i `package.json` + lockfile; changelog in `docs/wtp-app-1.8.md`.
   - **Minor/Major prodotto** (es. 1.8 → 1.9): aggiornare anche titoli `.po`, `index.html`, doc release e SPEC come da convenzione del repo.
3. Eseguire `cd backend && npm test` dopo modifiche che toccano codice condiviso.
4. Non committare segreti.

## Checklist

- [ ] `version` allineata in `frontend/package.json` e `backend/package.json`
- [ ] `package-lock.json` aggiornati (`npm install` nella cartella interessata se serve)
- [ ] Titolo UI / `<title>` coerenti con versione prodotto
- [ ] `docs/wtp-app-1.8.md` (o doc release target) aggiornato
- [ ] SPEC rinominata/aggiornata se cambia major doc utente

## Expected output

- Tabella “prima / dopo” delle versioni
- Elenco file toccati
- Comandi `git` suggeriti per il commit di release

## Usage

```
/version
```

## Notes

- Per solo “stato repo” senza bump usare `/snapshot`.
- Allineare `.cursorrules` / README se il documento “release corrente” cambia nome (es. passaggio a `wtp-app-1.9.md`).
