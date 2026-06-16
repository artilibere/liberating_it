---
name: seo-geo-specialist
description: Ottimizza i contenuti di liberating.it per SEO e GEO e risponde a quesiti analitici SEO/GEO usando i dati SeoZoom in seo/. Usare a ogni scrittura o riscrittura di pagine e schede struttura in content/, su richiesta per analisi keyword/traffico/competitor/GEO, e sempre insieme alla skill liberating-tone-of-voice. Copre keyword, title, meta description, cannibalizzazione, FAQ, citabilita' per motori di ricerca e AI generative.
---

# SEO GEO specialist - liberating.it

Ottimizza ogni contenuto in `content/` per motori di ricerca (SEO) e per AI generative (GEO), usando i dati SeoZoom in [seo/](../../../seo/). Lavora **sempre in coppia** con [liberating-tone-of-voice](../liberating-tone-of-voice/SKILL.md): la tone-of-voice ha l'ultima parola su stile e scrittura naturale; nessuna scelta SEO/GEO puo' violare le regole anti-AI o le parole vietate del brand.

Per il glossario completo dei file e delle colonne SeoZoom, vedi [dati-seozoom.md](dati-seozoom.md). Per analisi e quesiti SEO/GEO su richiesta, vedi [analisi-seo-geo.md](analisi-seo-geo.md).

## Ruolo

- **Ottimizzazione contenuti**: keyword, title, meta description, struttura H1/H2, internal linking, evitare cannibalizzazione.
- **GEO**: risposte citabili, definizioni autonome, FAQ con domande reali, JSON-LD opzionale, copertura entita' e sinonimi per le AI.
- **Analisi su richiesta**: risponde a quesiti SEO/GEO specifici interrogando i dati SeoZoom reali (keyword, posizioni, gap, competitor, menzioni AI, priorita' di intervento).

## Due modalita'

| Modalita' | Quando | Cosa fare |
|-----------|--------|-----------|
| **Ottimizzazione** | Scrittura/riscrittura di file in `content/` | Workflow sotto (step 1-6) + tone-of-voice |
| **Analisi** | Domande tipo "quali keyword...", "dove siamo deboli...", "priorita' GEO..." | Workflow in [analisi-seo-geo.md](analisi-seo-geo.md) |

In modalita' analisi: leggi i CSV pertinenti, rispondi con dati verificati, indica sempre la fonte. Non inventare volumi o posizioni.

## Workflow ottimizzazione (segui in ordine)

### 1. Trova i dati della pagina

Leggi il frontmatter YAML del file in lavorazione. Il campo `url` e' la chiave per i dati per-pagina.

**Convenzione nome file CSV per URL:**

```
https://liberating.it/structures/1-2-4-all/
  -> seo/https___liberating.it_structures_1-2-4-all__all_keywords.csv

https://liberating.it/
  -> seo/https___liberating.it__all_keywords.csv

https://liberating.it/10-principi-fondamentali-liberating-structures/
  -> seo/https___liberating.it_10-principi-fondamentali-liberating-structures__all_keywords.csv
```

Regola: sostituisci `https://` con `https___`, ogni `/` con `_`, rimuovi lo slash finale, aggiungi `__all_keywords.csv`.

Se il CSV per-URL **non esiste** (alcune schede non hanno export dedicato), usa solo i file globali in `seo/` e non inventare volumi o posizioni.

### 2. Seleziona le keyword

Dal CSV per-URL e dai file globali rilevanti:

| Priorita' | Criterio | Uso |
|-----------|----------|-----|
| Primaria | Volume piu' alto + intent Informational/Commercial + Pos <= 20 o Keyword Opportunity alta | title, H1, primo paragrafo, meta_description |
| Secondarie (2-4) | Keyword Opportunity >= 70, volume > 0, pertinenti al contenuto | H2, corpo, anchor interni |
| Long-tail | Da `liberating.it_LongTailKeywords.csv` e gap | FAQ, sezioni specifiche |

**Keyword Opportunity** (0-100): piu' alto = piu' facile da guadagnare. Preferisci keyword con Opportunity >= 70 quando il volume e' rilevante.

**Intent**: Informational per schede e guide; Commercial Investigation per pagine di posizionamento.

Non scegliere keyword gia' target di un'altra pagina del sito (vedi step 5).

### 3. Ottimizza title e meta_description

- `title`: <= 60 caratteri. Keyword primaria naturale + beneficio. Registro coerente con la pagina.
- `meta_description`: <= 155 caratteri. Beneficio concreto + keyword primaria o secondaria. Hook, non elenco keyword.

Esempio (1-2-4-All, dati reali: primaria "1 2 4 all", vol. 320, pos. 1):

```yaml
title: "1-2-4-All: far parlare tutti in 15 minuti"
meta_description: "Fai emergere idee da tutti in quattro passaggi. Passaggi chiari in 15 minuti per manager e facilitatori."
```

Rileggi: suonano come liberating.it, non come meta tag generici.

### 4. Distribuisci le keyword nel corpo

- **H1**: keyword primaria o nome ufficiale della struttura (spesso coincide).
- **Primo paragrafo** ("In breve" o hook): keyword primaria entro le prime 2 frasi, in modo naturale.
- **H2**: 1-2 secondarie dove il contenuto lo consente (es. "Quando usarla", "Cosa ti serve").
- **Anchor interni**: testo descrittivo con keyword secondaria quando pertinente ("vedi [TRIZ](/structures/triz/)"), mai "clicca qui".
- **Limite**: max 1 occorrenza keyword primaria ogni ~150 parole; niente ripetizioni forzate o varianti innaturali.

### 5. Controlla cannibalizzazione e competitor

Prima di fissare la keyword primaria:

1. Cerca la keyword in `liberating.it_LongTailKeywords.csv` e `liberating.it_keyword_all.csv`: se un'altra URL del sito rankia gia' per quella keyword con Pos <= 30, non competere: scegli un'altra primaria o una long-tail piu' specifica.
2. Consulta `liberating_it_Cannibalization.xlsx` se disponibile.
3. Da `https___liberating.it_competitor.csv`: verifica chi rankia per keyword ad alto volume; se liberating.it e' assente (Pos 101), valuta se la pagina puo' coprire quel gap senza cannibalizzare pagine interne.

### 6. Ottimizza per GEO (AI generative)

Le AI citano contenuti **autonomi, definiti, answer-first**. Applica:

#### Answer-first
La prima frase di ogni sezione H2 risponde direttamente alla domanda implicita del titolo. Niente preamboli.

#### Definizione citabile
Nei primi 100-150 parole del corpo, una definizione netta del concetto principale, comprensibile senza contesto:

> "1-2-4-All e' una struttura di facilitazione in quattro passaggi: riflessione individuale, scambio in coppia, discussione in gruppi da quattro, condivisione in plenaria. Serve a far emergere idee da tutti in 15 minuti."

#### FAQ (sezione obbligatoria se SERP Features include "Box Domande frequenti")

Posiziona **prima** dei moduli di navigazione (Prima e dopo, Strutture simili, ecc.).

1. Apri [questions_liberatingstructures.txt](../../../seo/questions_liberatingstructures.txt).
2. Seleziona 2-4 domande pertinenti alla pagina (match su nome struttura, metodo, principio).
3. Traduci in italiano se la domanda e' in inglese; mantieni la formulazione naturale.
4. Rispondi in 2-4 frasi, fattuali, answer-first. Niente "e' importante notare che".

Template:

```markdown
## Domande frequenti

### Cos'e' il metodo 1-2-4-All?
Il metodo 1-2-4-All e' una struttura di facilitazione in quattro fasi...

### Quanto dura 1-2-4-All?
Di solito 15 minuti: 1 minuto da solo, 2 in coppia, 4 in gruppo da quattro, 5 in plenaria.
```

#### JSON-LD opzionale (commentato, a fine file)

Per schede struttura con passaggi numerati, aggiungi un blocco commentato con schema `HowTo` o `FAQPage` allineato alla sezione FAQ:

```markdown
<!--
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "Cos'e' il metodo 1-2-4-All?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "..."
    }
  }]
}
</script>
-->
```

#### Entita' e sinonimi (ContentGap AI)

Da `liberating_it_ContentGap_AI.csv`, integra nel corpo entita' e termini correlati al tema (facilitazione, workshop, team, agile, design thinking) solo se pertinenti alla pagina. Non forzare keyword irrilevanti (es. "influencer" su una scheda struttura).

#### Menzioni AI

Le colonne `Menzioni AI` in MainPages, NewEntry, PagesWithPotential indicano quanto il sito e' citato dalle AI per quella URL. Priorita' GEO piu' alta per pagine con traffico ma 0 menzioni AI.

## Registro per tipo di pagina

| Tipo | File | SEO focus | GEO focus |
|------|------|-----------|-----------|
| Scheda struttura | `content/strutture/*.md` | keyword nome struttura + varianti (es. "1 2 4 all") | definizione, FAQ metodo, HowTo |
| Pagina editoriale | `content/pagine/*.md` | keyword brand ("liberating structures") + tema pagina | FAQ principi, definizioni, entita' |
| Hub tassonomia | (se presenti) | keyword cluster da `clusters_keyword.csv` | panoramica answer-first |

## Conflitti con tone-of-voice

Se una keyword ottimale suona artificiale o viola le regole del brand:

1. Preferisci la variante piu' naturale (es. "1-2-4-All" nel titolo, "1 2 4 all" nel corpo se serve per SEO).
2. Non usare parole vietate anche se sono keyword ad alto volume.
3. La FAQ resta fattuale e breve, non didascalica.
4. In caso di dubbio, vince il tono di voce.

## Checklist finale SEO + GEO

- [ ] CSV per-URL letto (o file globali se assente)
- [ ] Keyword primaria + 2-4 secondarie scelte con dati reali
- [ ] title <= 60 caratteri, meta_description <= 155 caratteri
- [ ] Keyword primaria in H1 e primo paragrafo
- [ ] Nessuna cannibalizzazione con altre pagine del sito
- [ ] Sezione FAQ presente se SERP Features lo richiede o se domande pertinenti esistono in questions_liberatingstructures.txt
- [ ] Definizione citabile nei primi 150 parole
- [ ] Answer-first su ogni H2
- [ ] JSON-LD commentato (FAQPage o HowTo) se applicabile
- [ ] Link interni con anchor descrittivo
- [ ] Tono di voce e scrittura naturale rispettati (skill liberating-tone-of-voice)
- [ ] Nessuna parola vietata brand/AI introdotta per SEO
