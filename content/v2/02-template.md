# Template contenuti - liberating.it (v2)

Modelli fissi per schede strutture e pagine editoriali. Ogni bozza in `content/v2/` segue questi template e la skill [liberating-tone-of-voice](../../.cursor/skills/liberating-tone-of-voice/SKILL.md).

---

## Scheda struttura (modello a 3 zone)

**Registro:** Manuale operativo  
**File:** `content/v2/strutture/{slug}.md`

Tre zone, in ordine:

1. **Cap** (10 secondi): breadcrumb, in breve, scheda rapida, chip tassonomia
2. **Fare** (agire): domanda, preparazione, passaggi
3. **Naviga** (restare sul sito): quando usarla, consigli, errori, link correlati

```markdown
---
slug: {slug}
title: "{Nome struttura}: {beneficio in poche parole}"
meta_description: "{beneficio concreto + parola chiave, max 155 caratteri}"
registro: manuale-operativo
durata: "{es. 15 minuti}"
difficolta: "{Facile | Intermedia | Avanzata}"
partecipanti: "{es. illimitato, 5-30}"
fase: "{Empathize | Define | Ideate | Prototype | Test | Multi fase}"
complessita: "{Per iniziare subito | ...}"
url: "https://liberating.it/structures/{slug}/"
---

# {Nome struttura}

[Home](/) > [Le strutture](/structures/) > {Nome}

**In breve** - {1 frase beneficio}

| Durata | Difficolta' | Gruppo | Fase |
|--------|-------------|--------|------|
| {15 min} | {Facile} | {illimitato} | {Ideate} |

**Filtri:** [{Percorso}](/complessita/{slug}/) · [{Difficolta'}](/difficolta/{slug}/) · [{Durata}](/durata/{slug}/) · [{Fase}](/design-thinking/{slug}/)

## Domanda da portare

- "{esempio concreto}"
- "{esempio concreto}"

## Cosa ti serve

- {spazio / materiali / remoto, max 5 bullet}

## Materiali grafici

![{alt descrittivo in italiano}](/assets/worksheets/{slug}/{file}.png)

*Fonte: [{Nome struttura}](https://www.liberatingstructures.com/{ls-slug}/) - Liberating Structures (Henri Lipmanowicz & Keith McCandless).*

## I passaggi

1. {azione} - {tempo}
2. {azione} - {tempo}

## Quando usarla

- {caso d'uso / punto di dolore}

## Il consiglio del facilitatore

{2-4 frasi}

## Errori da evitare

- {errore}

## Domande frequenti

### {Domanda 1}
{Risposta 2-4 frasi, answer-first}

### {Domanda 2}
{...}

## Prima e dopo

- **Prima:** [{Struttura}](/structures/{slug}/) - {perche' in 5-10 parole}
- **Dopo:** [{Struttura}](/structures/{slug}/) - {perche' in 5-10 parole}

## Strutture simili

- [{Nome}](/structures/{slug}/) - {stesso livello o durata simile}

## Prossimo nel percorso

← [{Precedente}](/structures/{slug}/) · → [{Successiva}](/structures/{slug}/)

(Solo se la struttura appartiene a un percorso guidato, es. "Per iniziare subito")

## Torna al catalogo

[Esplora tutte le strutture](/structures/) · [{Correlata}](/structures/{slug}/) - {perche'}

<!--
<script type="application/ld+json">
{ FAQPage schema allineato alle domande sopra }
</script>
-->
```

### Regole moduli di navigazione

| Modulo | Quando | Quanti link |
|--------|--------|-------------|
| **Prima e dopo** | Sempre | 1-2 ciascuno, con motivo esplicito (string) |
| **Strutture simili** | Sempre | 2-3, stessa difficolta' o durata simile |
| **Prossimo nel percorso** | Solo se in hub `complessita` | prev + next nel percorso guidato |
| **Torna al catalogo** | Sempre | catalogo + 1-2 correlati per bisogno |

### Note operative scheda

- Breadcrumb **in alto**, non in fondo pagina.
- Tabella scheda rapida: metadati visibili al lettore (non solo YAML).
- Chip tassonomia cliccabili verso hub filtrati.
- Passaggi: verbo imperativo, tempo esplicito; se >6 passaggi, raggruppa in sotto-fasi.
- Domanda da portare: 2-3 esempi concreti, virgolette dritte.
- Cosa ti serve: max 5 bullet, solo cio' che serve davvero.
- Niente trattino lungo (—); usa " - " per separare azione e tempo.
- SEO frontmatter obbligatorio: title <= 60 char, meta_description <= 155 char.
- FAQ obbligatoria (2-4 domande) + JSON-LD commentato in fondo file.
- Generazione batch: `python3 scripts/generate_structure_v2.py` -> `content/v2/strutture/`.

---

## Pagina editoriale

**Registro:** Manifesto (home, posizionamento) o Diario di bordo (blog, risorse, casi)  
**File:** `content/v2/pagine/{slug}.md`

```markdown
---
slug: {slug}
title: "{beneficio orientato al lettore, max 60 caratteri}"
meta_description: "{hook + beneficio, max 155 caratteri}"
registro: {manifesto | diario-di-bordo}
url: "https://liberating.it/{slug}/"
---

# {Titolo orientato al beneficio}

{Hook: 1-2 frasi sul problema reale del lettore. Registro Manifesto = tagliente; Diario = narrativo.}

**Cosa trovi qui**

- {punto 1}
- {punto 2}
- {punto 3}

## {Sottotitolo a beneficio}

{Corpo: sezioni brevi, elenchi, grassetti su parole chiave. Link contestuali inline alla prima menzione di [strutture](/structures/) o concetti.}

## {Altro sottotitolo, se serve}

{Contenuto. Burstiness: alterna frasi lunghe e corte.}

## Leggi anche

- [{Pagina o struttura}](/path/) - {perche' continua il percorso}
- [{Pagina o struttura}](/path/) - {perche' continua}

## E adesso?

{Una sola CTA orientata all'azione autonoma. Es: "Scegli [1-2-4-All](/structures/1-2-4-all/) e provala nella riunione di domani."}
```

### Note operative pagina editoriale

- Home: registro Manifesto, sezioni Problema / Soluzione / Per iniziare / CTA.
- 10 principi: registro Diario di bordo leggero, un principio per sezione H2, esempio concreto per ciascuno.
- Termini e privacy: solo riformattazione Markdown, contenuto legale invariato.

---

## Checklist pre-pubblicazione (scheda struttura)

- [ ] Frontmatter YAML completo (slug, title, meta_description, url)
- [ ] Breadcrumb in alto + tabella scheda rapida visibile
- [ ] Chip tassonomia con link funzionanti
- [ ] Domanda da portare (2-3 esempi) + Cosa ti serve (max 5 bullet)
- [ ] Passaggi numerati con tempi
- [ ] Prima/Dopo/Simili con motivo su ogni link
- [ ] Prossimo nel percorso (se applicabile)
- [ ] FAQ presente (2-4 domande) + JSON-LD commentato
- [ ] title <= 60, meta_description <= 155 caratteri
- [ ] Nessun trattino lungo, virgolette dritte, niente emoji
