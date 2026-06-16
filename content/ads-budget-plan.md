# Piano budget Google Ads — liberating.it

Documento operativo per la campagna Search + Remarketing descritta nell'appendice del [piano SEO operativo](../.cursor/plans/piano_seo_operativo_a2c0a0e2.plan.md).

**Prerequisito:** pubblicare le landing del Batch 1 SEO prima di attivare le ads (Quality Score e bounce rate).

**Fonti dati:** `seo/liberating.it_keyword_all.csv`, `seo/https___liberating.it_competitor.csv`, `seo/liberating_it_MainPages.csv`, `seo/landing-pages-all_2026-05-18_2026-06-15.csv` (GA4).

**Baseline traffico:** ~150 sessioni/mese, ~83 utenti unici/mese (maggio–giugno 2026).

---

## 1. Sintesi budget

| Scenario | Cap giornaliero totale | Spesa mensile stimata (netta) | Spesa mensile lorda (IVA 22%) | Click ads/mese stimati |
|----------|------------------------|-------------------------------|-------------------------------|------------------------|
| **Lean** (test 60 gg) | EUR 4,50/g | EUR 55–75 | EUR 67–92 | 25–35 |
| **Growth** (consigliato) | EUR 9,50/g | EUR 100–150 | EUR 122–183 | 40–60 |
| **Aggressive** (boost strutture) | EUR 18,00/g | EUR 200–320 | EUR 244–390 | 80–120 |

**Nota importante:** i cap giornalieri sono **tetti massimi** impostati in Google Ads. Su un sito di nicchia con volumi bassi, la spesa reale resta sotto il cap — soprattutto nei primi 30 giorni (audience remarketing ancora piccola).

**Trimestre Growth:** EUR 300–450 netti / EUR 366–549 lordi.

---

## 2. Perché la spesa Search è bassa

1. **Volumi di nicchia:** le keyword LS in Italia sommano poche centinaia di ricerche/mese (non migliaia come keyword generiche tipo "facilitazione").
2. **Organico già forte:** su `1 2 4 all` (pos. 1), `liberating structures` (pos. 2), `drawing together` (pos. 3) non conviene comprare traffico.
3. **CPC contenuti:** CPC SeoZoom EUR 0–1,05; stima auction reale EUR 0,40–1,20 sul brand, EUR 0,35–0,70 sulle strutture.
4. **Intent Informational:** CTR paid tipico 5–9%; conversioni dirette rare — il valore è in engagement, non in lead immediati.

Il budget si concentra quindi su **brand difensivo** + **poche strutture in pos. 9–30** + **remarketing**.

---

## 3. Dettaglio per campagna (scenario Growth)

### Campagna A — Brand difensiva

| | |
|---|---|
| **Landing** | `https://liberating.it/` |
| **Cap giornaliero** | EUR 2,50 |
| **Cap mensile** | EUR 75 |
| **Spesa stimata** | EUR 25–35/mese |

| Keyword | Vol./mese | CPC stimato | Pos. org. | IS target paid | Click stimati | Costo stimato |
|---------|-----------|-------------|-----------|----------------|---------------|---------------|
| liberatingstructures | 2.900 | EUR 0,65 | 2 | 25% | 36 | EUR 24 |
| liberating structures | 140 | EUR 1,20 | 2 | 30% | 3 | EUR 3 |
| liberatingstructures.com | 30 | EUR 0,55 | 2 | 35% | 1 | EUR 1 |
| liberating | 20 | EUR 0,40 | 2 | 20% | 1 | EUR 0 |

**Match type:** Exact + Phrase. Negativi: `corso`, `certificazione`, `formazione`, `libro`, `pdf` (intent formativo/commerciale non vostro).

**Perché spendere se siete già pos. 2?** agileway.it (pos. 9–10) e liberatingstructures.com (pos. 1 su varianti) intercettano ricerche brand. Il paid garantisce presenza above-the-fold e sitelink verso il catalogo.

---

### Campagna B — Onboarding guidato

| | |
|---|---|
| **Landing** | `https://liberating.it/complessita/iniziare-subito/` |
| **Cap giornaliero** | EUR 1,00 |
| **Cap mensile** | EUR 30 |
| **Spesa stimata** | EUR 5–15/mese |

| Keyword | Vol./mese stimato | CPC stimato | Pos. org. | Click stimati | Costo stimato |
|---------|-------------------|-------------|-----------|---------------|---------------|
| come iniziare con le liberating structures | 40 | EUR 0,55 | 6 | 1–2 | EUR 1 |
| liberating structures per riunioni online efficaci | 25 | EUR 0,55 | 2 | 1–2 | EUR 1 |
| guida completa liberating structures | 20 | EUR 0,50 | 3 | 1 | EUR 1 |

**Nota:** volumi stimati da `monitored.csv` e long-tail (molte keyword senza volume SeoZoom esplicito). Campagna a basso volume ma **alto valore per micro-conversione** (ingresso nel percorso guidato).

**CPA target:** EUR 3–8 per visita al percorso "iniziare subito" con 2+ pagine viste.

---

### Campagna C — Strutture priorità 1

| | |
|---|---|
| **Cap giornaliero** | EUR 3,00 |
| **Cap mensile** | EUR 90 |
| **Spesa stimata** | EUR 15–30/mese |

| Landing | Keyword | Vol. | CPC | Pos. org. | Click stim. | Costo stim. |
|---------|---------|------|-----|-----------|-------------|-------------|
| `/structures/open-space-technology-ost/` | open space technology | 210 | EUR 0,70 | 11 | 6 | EUR 4 |
| `/structures/open-space-technology-ost/` | metodologia open space | 10 | EUR 0,60 | 11 | 1 | EUR 1 |
| `/structures/w3-what-so-what-now-what/` | What So What Now What | 140 | EUR 0,50 | 30 | 5 | EUR 3 |
| `/structures/social-network-webbing/` | webbing | 210 | EUR 0,65 | 12 | 6 | EUR 4 |
| `/structures/social-network-webbing/` | Social Network Webbing | 15 | EUR 0,55 | 2 | 0–1 | EUR 0 |

**Competitor da monitorare:** loci.it (OST pos. 2), agileway.it (w3 pos. 9, OST pos. 37).

---

### Campagna D — Strutture long-tail LS

| | |
|---|---|
| **Cap giornaliero** | EUR 1,00 |
| **Cap mensile** | EUR 30 |
| **Spesa stimata** | EUR 5–12/mese |

| Landing | Keyword | Vol. | CPC | Pos. org. | Click stim. | Costo stim. |
|---------|---------|------|-----|-----------|-------------|-------------|
| `/structures/triz/` | triz liberating structures | 50 | EUR 0,40 | 4 | 1 | EUR 0 |
| `/structures/triz/` | liberating structures triz | 50 | EUR 0,40 | 3 | 1 | EUR 0 |
| `/structures/troika-consulting/` | troika consulting | 10 | EUR 0,45 | 4 | 1 | EUR 0 |
| `/structures/troika-consulting/` | troika liberating structures | 10 | EUR 0,40 | 2 | 1 | EUR 0 |
| `/structures/wicked-questions/` | wicked question | 20 | EUR 0,40 | 3 | 1 | EUR 0 |

**Esclusione esplicita:** `triz` generica (vol. 480, pos. 101) — CPC alto stimato EUR 1,50+, landing non allineata.

---

### Campagna E — Remarketing

| | |
|---|---|
| **Landing** | `/complessita/iniziare-subito/` (primaria), `/` (secondaria) |
| **Cap giornaliero** | EUR 2,00 |
| **Cap mensile** | EUR 60 |
| **Spesa stimata** | EUR 20–60/mese (cresce con l'audience) |

| Parametro | Valore |
|-----------|--------|
| Audience | Visitatori con 2+ pagine struttura OR sessione > 45s su home |
| Durata cookie | 30 giorni |
| CPM stimato | EUR 2–5 |
| Frequenza cap | 4 impressioni/utente/settimana |
| Audience size attuale | ~60–80 utenti/mese → **sotto soglia ottimale** |

**Mese 1–2:** Google potrebbe spendere solo EUR 10–20 (audience piccola). Budget utile da **mese 3** in poi, quando l'elenco supera 200–300 utenti.

---

## 4. Distribuzione budget mensile (Growth)

```
Brand          ████████████████░░░░  30%  (EUR 25–35 effettivi / EUR 75 cap)
Strutture P1   ██████████████░░░░░░  25%  (EUR 15–30 / EUR 90 cap)
Remarketing    ████████████████████  35%  (EUR 20–60 / EUR 60 cap)
Onboarding     ████░░░░░░░░░░░░░░░░   5%  (EUR 5–15 / EUR 30 cap)
Strutture P2   ████░░░░░░░░░░░░░░░░   5%  (EUR 5–12 / EUR 30 cap)
```

---

## 5. Scenari alternativi

### Lean — EUR 4,50/giorno (EUR 135 cap, ~EUR 55–75 spend)

| Campagna | Cap/g | Note |
|----------|-------|------|
| Brand | EUR 1,50 | Solo `liberatingstructures` exact |
| Strutture P1 | EUR 1,50 | Solo OST + w3 |
| Remarketing | EUR 1,00 | Minimo |
| Onboarding + P2 | OFF | Attivare dopo 60 gg |

**Quando usarlo:** primi 60 giorni di test, landing appena pubblicate, conversion tracking da validare.

### Aggressive — EUR 18,00/giorno (EUR 540 cap, ~EUR 200–320 spend)

| Campagna | Cap/g | Variazione vs Growth |
|----------|-------|----------------------|
| Brand | EUR 5,00 | IS target 40% su liberatingstructures |
| Strutture P1 | EUR 7,00 | +ecocycle, +shift-share, IS 50% |
| Strutture P2 | EUR 3,00 | +conversation cafe, +9 whys LS, +fishbowl LS |
| Remarketing | EUR 2,50 | +audience "visitatori 1 struttura" |
| Onboarding | EUR 0,50 | Invariato |

**Quando usarlo:** dopo 90 gg con Quality Score >= 7 e bounce < 50% sulle landing ads.

---

## 6. Calendario di spesa (primi 90 giorni)

| Periodo | Budget | Azione |
|---------|--------|--------|
| **Settimana 0** | EUR 0 | Pubblicare landing Batch 1. Installare GA4 + conversioni. |
| **Settimane 1–2** | Lean (EUR 4,50/g) | Solo Brand + OST. Verificare tracking. |
| **Settimane 3–4** | Lean → Growth | Aggiungere w3, webbing, onboarding. |
| **Mese 2** | Growth (EUR 9,50/g) | Attivare remarketing. Primo report ROI. |
| **Mese 3** | Growth o Aggressive | Scale se CPA micro-conversione < EUR 8. |

**Buffer mese 1:** +15% per fase di apprendimento algoritmo Google (CTR e CPC instabili).

---

## 7. Micro-conversioni e CPA target

Il sito non vende direttamente — misurare **engagement qualificato**, non acquisti.

| Evento GA4 | Definizione | Valore attribuito | CPA target (Growth) |
|------------|-------------|-------------------|---------------------|
| `view_structure` | 2+ schede struttura in sessione | EUR 2,00 | < EUR 8 |
| `start_path` | Visita `/complessita/iniziare-subito/` | EUR 4,00 | < EUR 12 |
| `engaged_session` | > 45s o 2+ pagine | EUR 1,00 | < EUR 5 |
| `scroll_75` | Scroll 75% su scheda | EUR 1,50 | < EUR 6 |

**Esempio ROI Growth (mese 2, scenario medio):**

- Spesa: EUR 120
- Click: ~50
- CPC medio: EUR 2,40
- Se 30% raggiunge `view_structure` (15 sessioni qualificate): CPA qualificato = EUR 8
- Se 10% entra nel percorso iniziare-subito (5 visite): CPA percorso = EUR 24

Confronto: acquisire lo stesso traffico qualificato solo via content marketing costa tempo editoriale (~8h/scheda × EUR 40/h = EUR 320 per scheda). Le ads su keyword "quasi pagina 1" hanno senso come **acceleratore**, non come canale principale.

---

## 8. Keyword da escludere (risparmio stimato EUR 50–200/mese)

| Keyword / cluster | Motivo | Rischio se inclusa |
|-------------------|--------|---------------------|
| `1 2 4 all`, `together drawings` | Pos. 1–3 organico | Spreco puro |
| `triz` (generica) | Pos. 101, intento ampio | CPC alto, bounce |
| `facilitazione` | Pos. 101, competitor formativi | CPC EUR 2+, CPA inaccettabile |
| `corso liberating structures` | Intent transactional | Utente cerca formazione a pagamento |
| `certificazione facilitatore` | Intent formativo | Non siete scuola |
| `leadership`, `change management` | Fuori perimetro | Budget bruciato |

**Lista negativi condivisa** (applicare a tutte le campagne):

```
corso, corsi, certificazione, formazione, master, scuola, libro, pdf, download,
gratis pdf, ppt, slide, video corso, acquista, prezzo, stipendio
```

---

## 9. Estensioni annuncio (incluse nel budget, costo zero)

| Estensione | Contenuto |
|------------|-----------|
| **Sitelink** | Catalogo strutture, Percorso iniziare subito, 1-2-4-All, 10 principi |
| **Callout** | 35 strutture in italiano, Passaggi pronti, 15 minuti per iniziare |
| **Snippet strutturati** | Facile / Intermedia / Avanzata (tassonomia difficolta) |

Impatto atteso: +10–15% CTR → stesso budget, più click.

---

## 10. KPI e soglie di controllo

### Report settimanale

| KPI | Soglia verde | Soglia rossa | Azione se rosso |
|-----|--------------|--------------|-----------------|
| CTR Search | > 4% | < 2% | Rivedere copy annunci |
| Quality Score | >= 7 | < 5 | Migliorare landing (FAQ, H1) |
| Bounce rate landing ads | < 55% | > 70% | Bloccare keyword, fix pagina |
| CPC medio | < EUR 1,50 | > EUR 2,50 | Ridurre IS o pausare keyword |
| Conv. rate `view_structure` | > 25% | < 10% | Spostare budget su remarketing |

### Regole di ottimizzazione automatica

1. **Pausa keyword** se spend > EUR 15 e 0 micro-conversioni in 14 gg.
2. **Scale +20% cap** se CPA `view_structure` < EUR 6 per 7 gg consecutivi.
3. **Shift budget** da Brand a Strutture P1 se impression share organica brand > 40% (Search Console).
4. **Stop campagna** se spend mensile > 150% della stima senza miglioramento conversioni.

---

## 11. Costi una tantum (fuori media budget)

| Voce | Stima tempo | Costo opportunità |
|------|-------------|-------------------|
| Setup account + conversioni GA4 | 4h | — |
| Scrittura 12 RSA (3 per campagna) | 3h | — |
| Creative remarketing (3 banner) | 2h | EUR 0 se fai internamente |
| Landing Batch 1 (prerequisito SEO) | già in piano SEO | — |
| Monitoraggio mensile | 2h/mese | — |

---

## 12. Riepilogo decisionale

| Se il budget mensile è... | Configurazione consigliata |
|---------------------------|----------------------------|
| **< EUR 80** | Solo Brand (EUR 2/g) + OST (EUR 1/g). Niente remarketing fino a mese 3. |
| **EUR 80–150** | **Growth** completo. Configurazione ottimale per liberating.it oggi. |
| **EUR 150–300** | Growth + Aggressive su Strutture P1 per 60 gg, poi valutare. |
| **> EUR 300** | Non giustificato dai volumi attuali. Reinvestire in contenuti (piano SEO) con ROI superiore. |

**Raccomandazione:** partire con **Growth a EUR 9,50/giorno** (EUR 285 cap, spesa reale attesa EUR 100–150/mese). Rivalutare a 90 giorni con dati GA4 reali.

---

*Generato il 16/06/2026. CPC stimati dove SeoZoom riporta 0: EUR 0,35–0,70 (nicchia informational IT). Volumi onboarding stimati da `monitored.csv` dove assenti in keyword_all.*
