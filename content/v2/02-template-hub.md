# Template hub tassonomici - liberating.it (v2)

Modello per hub filtrati: complessita', difficolta', durata, design thinking. Il build statico legge la configurazione da `public/scripts/build.py`; questo file e' la reference editoriale per allineare copy, FAQ e meta.

---

## Hub tassonomico

**File suggerito:** `content/v2/hub/{taxonomy}/{slug}.md` (opzionale, per revisione editoriale)

```markdown
---
taxonomy: difficolta
slug: intermedia
title: "Strutture intermedie"
page_title: "Liberating Structures intermedie"
meta_description: "{beneficio + keyword, max 155 caratteri}"
url: "https://liberating.it/difficolta/intermedia/"
---

# Strutture intermedie

{Intro 1-2 frasi: a chi serve questo elenco}

## Strutture in questo percorso

{Lista generata dal build: slug, titolo, difficolta, durata}

## Domande frequenti

### {Domanda 1}
{Risposta 2-4 frasi, answer-first}

### {Domanda 2}
{...}

## Link correlati

- [Catalogo completo](/structures/)
- [{Hub correlato}](/complessita/iniziare-subito/) - {perche'}
```

### Regole

- **H1** = titolo display (breve). **page_title** (se diverso) = `<title>` con keyword.
- **meta_description** <= 155 caratteri, beneficio concreto.
- **FAQ** obbligatoria: 2-3 domande per GEO e snippet.
- Non duplicare l'elenco strutture a mano nel markdown se il build lo genera: usa questo template per copy intro + FAQ + meta.

### Taxonomy disponibili

| Taxonomy | Slug esempio | URL base |
|----------|--------------|----------|
| complessita | iniziare-subito | `/complessita/{slug}/` |
| difficolta | intermedia | `/difficolta/{slug}/` |
| durata | breve | `/durata/{slug}/` |
| design-thinking | ideate | `/design-thinking/{slug}/` |

Per percorsi **Per bisogno** usa lo stesso schema FAQ in `PER_BISOGNO` nel build.
