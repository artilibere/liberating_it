#!/usr/bin/env python3
"""Generate the 15 editorial guide pages in content/v1/pagine/. Run once, then build.py."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "content" / "v1" / "pagine"

GUIDES = [
    {
        "slug": "facilitazione-strutturata-microstrutture",
        "title": "Facilitazione strutturata con microstrutture",
        "meta_description": "Cosa sono le microstrutture di facilitazione e come usarle in riunione. Formati brevi con passaggi e tempi per far parlare tutti.",
        "guide_category": "Fondamenti",
        "guide_order": 1,
        "guide_intro": "Formati brevi con passaggi e tempi: cosa sono e da dove iniziare.",
        "h1": "Facilitazione strutturata con microstrutture",
        "lead": "In molte riunioni il problema non e' il tema. E' il formato: chi parla troppo, chi non trova spazio, discussioni che girano a vuoto. Le microstrutture di facilitazione risolvono questo con passaggi e tempi chiari.",
        "toc": [
            "Cosa intendiamo per microstruttura",
            "Perche' funzionano meglio del libero dibattito",
            "Tre strutture per iniziare subito",
            "Come scegliere la struttura giusta",
        ],
        "sections": [
            (
                "Cosa intendiamo per microstruttura",
                "Una microstruttura e' un formato breve e ripetibile: chi parla, per quanto, in che ordine. "
                "Le [Liberating Structures](/structures/) sono 41 microstrutture liberanti con passaggi gia' pronti. "
                "Non devi inventare la riunione da zero. Scegli il formato, leggi i passaggi, adatta la domanda al tuo contesto.",
            ),
            (
                "Perche' funzionano meglio del libero dibattito",
                "Nel dibattito aperto le voci piu' forti dominano. Chi e' introverso o junior resta fuori. "
                "Le microstrutture distribuiscono il tempo: prima pensi da solo, poi in coppia, poi in gruppo. "
                "Il silenzio iniziale non e' vuoto. E' tempo per formulare un'idea prima di esporla al plenario.",
            ),
            (
                "Tre strutture per iniziare subito",
                "[1-2-4-All](/structures/1-2-4-all/) e' la piu' usata: 15 minuti, quattro passaggi, tutti contribuiscono. "
                "[Impromptu Networking](/structures/impromptu-networking/) rompe il ghiaccio in gruppi grandi. "
                "[What, So What, Now What?](/structures/w3-what-so-what-now-what/) trasforma un'esperienza condivisa in lezioni e azioni.",
            ),
            (
                "Come scegliere la struttura giusta",
                "Parti dall'obiettivo: idee nuove, decisione, analisi, fiducia nel gruppo? "
                "Usa l'hub [Per bisogno](/per-bisogno/) per smistare. "
                "Se e' la prima volta, resta su strutture brevi e con pochi passaggi. "
                "Una struttura fatta bene vale piu' di tre scelte a caso nella stessa riunione.",
            ),
        ],
        "faq": [
            (
                "Cosa sono le microstrutture di facilitazione?",
                "Sono formati brevi che strutturano chi parla e per quanto tempo in una riunione o workshop. "
                "Le Liberating Structures ne offrono 41 con passaggi e tempi gia' definiti, in italiano su liberating.it.",
            ),
            (
                "Servono competenze da facilitatore esperto?",
                "No. Strutture come 1-2-4-All si leggono in cinque minuti e si provano subito. "
                "L'esperienza aiuta ad adattare tempi e domande, ma non e' un prerequisito per iniziare.",
            ),
            (
                "Microstrutture e Liberating Structures sono la stessa cosa?",
                "Le Liberating Structures sono un insieme specifico di microstrutture liberanti, con regole condivise e un catalogo ufficiale. "
                "Il concetto e' lo stesso: formato breve, partecipazione distribuita.",
            ),
        ],
        "leggi_anche": [
            ("I 10 principi fondamentali", "/10-principi-fondamentali-liberating-structures/", "il perche' dietro ogni struttura"),
            ("Per iniziare subito", "/complessita/iniziare-subito/", "percorso guidato per chi parte da zero"),
            ("1-2-4-All", "/structures/1-2-4-all/", "la struttura piu' semplice per provare domani"),
        ],
        "cta_text": "Scegli una microstruttura e provala nella prossima riunione. Una sola, con i passaggi davanti a te.",
        "cta_url": "/structures/1-2-4-all/",
        "cta_label": "Prova 1-2-4-All domani",
    },
    {
        "slug": "brainstorming-alternative-liberating-structures",
        "title": "Brainstorming: alternative con le Liberating Structures",
        "meta_description": "Il brainstorming classico spesso non funziona. Ecco formati strutturati per generare idee in gruppo senza dominanza delle voci forti.",
        "guide_category": "Fondamenti",
        "guide_order": 2,
        "guide_intro": "Perche' il brainstorming libero fallisce e quali strutture usare al suo posto.",
        "h1": "Brainstorming: alternative con le Liberating Structures",
        "lead": "Hai mai finito un brainstorming con le solite idee dette dalle solite persone? Non sei solo. Il formato conta quanto l'argomento.",
        "toc": [
            "Perche' il brainstorming classico delude",
            "Cosa cambia con una struttura",
            "Strutture per generare idee in gruppo",
            "Come evitare che il plenario uccida le idee migliori",
        ],
        "sections": [
            (
                "Perche' il brainstorming classico delude",
                "Post-it a raffica, niente tempi, nessun passaggio intermedio. "
                "Chi parla per primo orienta il gruppo. Chi ha bisogno di tempo per pensare resta indietro. "
                "Il risultato sembra produttivo ma spesso ripete cio' che gia' sapevate.",
            ),
            (
                "Cosa cambia con una struttura",
                "Una Liberating Structure definisce ordine e durata: riflessione individuale, scambio in coppia, sintesi in gruppo. "
                "Le idee si mescolano prima di arrivare al plenario. "
                "Non e' piu' brainstorming. E' generazione distribuita.",
            ),
            (
                "Strutture per generare idee in gruppo",
                "[1-2-4-All](/structures/1-2-4-all/) raccoglie idee in 15 minuti. "
                "[25/10 Crowd Sourcing](/structures/25-10-crowd-sourcing/) funziona con gruppi grandi: molte proposte, votazione rapida. "
                "[TRIZ](/structures/triz/) parte dai vincoli e spinge verso soluzioni inaspettate. "
                "Per un percorso completo vedi [Generare idee](/per-bisogno/generare-idee/).",
            ),
            (
                "Come evitare che il plenario uccida le idee migliori",
                "Raccogli prima in piccolo, poi sintetizza. "
                "Non chiedere subito \"chi ha un'idea?\". "
                "Dai due minuti di silenzio, poi coppie, poi gruppi da quattro. "
                "Al plenario arrivano gia' idee incrociate, non monologhi isolati.",
            ),
        ],
        "faq": [
            (
                "Le Liberating Structures sostituiscono il brainstorming?",
                "Si', nel senso che offrono formati piu' efficaci per far emergere idee da tutti. "
                "Non e' un divieto di post-it: e' un modo diverso di organizzare il tempo e i turni.",
            ),
            (
                "Quale struttura uso per un workshop di ideazione?",
                "Con meno di 12 persone, 1-2-4-All piu' una sessione di 25/10 se serve priorizzare. "
                "Con gruppi grandi o misti, parti da 25/10 Crowd Sourcing.",
            ),
            (
                "Funziona anche online?",
                "Si. Stessi passaggi, breakout room al posto dei tavoli. "
                "Vedi la guida sulla [facilitazione remota](/facilitazione-remota-liberating-structures/).",
            ),
        ],
        "leggi_anche": [
            ("Generare idee", "/per-bisogno/generare-idee/", "hub con tutte le strutture per l'ideazione"),
            ("TRIZ", "/structures/triz/", "idee partendo dai vincoli"),
            ("25/10 Crowd Sourcing", "/structures/25-10-crowd-sourcing/", "priorita' rapide in gruppo grande"),
        ],
        "cta_text": "Nella prossima sessione di idee, sostituisci il brainstorming libero con 1-2-4-All. Stessa durata, risultati diversi.",
        "cta_url": "/structures/1-2-4-all/",
        "cta_label": "Prova 1-2-4-All domani",
    },
    {
        "slug": "decision-making-gruppo-liberating-structures",
        "title": "Decision making di gruppo con le Liberating Structures",
        "meta_description": "Come prendere decisioni in team senza ostruzionismo o accordi di facciata. Strutture per allineare il gruppo e decidere insieme.",
        "guide_category": "Fondamenti",
        "guide_order": 3,
        "guide_intro": "Formati per decidere insieme senza riunioni infinite ne' yes-man.",
        "h1": "Decision making di gruppo con le Liberating Structures",
        "lead": "Decidere in gruppo e' lento quando manca chiarezza su cosa si sta decidendo. E' veloce ma fragile quando manca ascolto. Serve un formato che tenga insieme entrambe le cose.",
        "toc": [
            "Dove si inceppa il decision making di gruppo",
            "Prima chiarisce, poi decidi",
            "Strutture per allineare e scegliere",
            "Quando non serve una decisione plenaria",
        ],
        "sections": [
            (
                "Dove si inceppa il decision making di gruppo",
                "Si discute senza aver definito la domanda. "
                "Si vota prima di capire le opzioni. "
                "Chi dissente non ha spazio per spiegare il perche'. "
                "Il risultato e' un compromesso stanco o un finto consenso.",
            ),
            (
                "Prima chiarisce, poi decidi",
                "[Agreement-Certainty Matrix](/structures/agreement-certainty-matrix/) separa cio' su cui siete allineati da cio' che richiede piu' lavoro. "
                "[Min Specs](/structures/min-specs/) definisce le regole minime indispensabili. "
                "Senza questo passaggio, ogni decisione riapre lo stesso dibattito.",
            ),
            (
                "Strutture per allineare e scegliere",
                "[15% Solutions](/structures/15-solutions/) chiede cosa puoi fare tu, adesso, senza aspettare permessi. "
                "Utile quando la decisione \"ufficiale\" e' lontana ma serve muoversi. "
                "[Shift & Share](/structures/shift-share/) fa circolare proposte tra sottogruppi prima di una sintesi comune. "
                "Percorso completo: [Prendere decisioni](/per-bisogno/prendere-decisioni/).",
            ),
            (
                "Quando non serve una decisione plenaria",
                "Non tutto va votato in aula. "
                "A volte serve esplorare opzioni con [1-2-4-All](/structures/1-2-4-all/), poi delegare a un sottogruppo la scelta finale. "
                "La struttura ti dice dove finisce l'esplorazione e dove inizia la decisione.",
            ),
        ],
        "faq": [
            (
                "Le Liberating Structures sostituiscono il voto o il consenso?",
                "No. Offrono formati per preparare una decisione: esplorare, allineare, rendere visibili le divergenze. "
                "Il meccanismo finale (voto, consenso, delega) resta una scelta del team.",
            ),
            (
                "Quale struttura per decisioni strategiche?",
                "Parti da Agreement-Certainty Matrix per mappare accordi e incertezze. "
                "Per obiettivi condivisi, [Purpose to Practice (P2P)](/structures/purpose-to-practice-p2p/).",
            ),
            (
                "Come gestire chi blocca ogni decisione?",
                "Dai spazio strutturato alla voce dissenziente con [Heard, Seen, Respected (HSR)](/structures/heard-seen-respected-hsr/) "
                "prima di forzare il voto. Spesso il blocco e' mancanza di ascolto, non mancanza di opzioni.",
            ),
        ],
        "leggi_anche": [
            ("Prendere decisioni", "/per-bisogno/prendere-decisioni/", "tutte le strutture per le decisioni di gruppo"),
            ("Agreement-Certainty Matrix", "/structures/agreement-certainty-matrix/", "mappa accordi e incertezze"),
            ("15% Solutions", "/structures/15-solutions/", "agire senza aspettare il via libera"),
        ],
        "cta_text": "Alla prossima decisione difficile, mappa prima accordi e incertezze con Agreement-Certainty Matrix.",
        "cta_url": "/structures/agreement-certainty-matrix/",
        "cta_label": "Prova Agreement-Certainty Matrix",
    },
    {
        "slug": "riunioni-efficaci-struttura-partecipazione",
        "title": "Riunioni efficaci: struttura e partecipazione",
        "meta_description": "Come rendere le riunioni piu' utili con formati che distribuiscono la parola. Meno monologhi, piu' risultati concreti.",
        "guide_category": "Riunioni e team",
        "guide_order": 4,
        "guide_intro": "Meno ore sprecate: formati brevi per riunioni che producono qualcosa.",
        "h1": "Riunioni efficaci: struttura e partecipazione",
        "lead": "La riunione e' finita e non sai perche' c'eri. Succede spesso. Il problema raramente e' il calendario pieno. E' il formato vuoto.",
        "toc": [
            "Il costo delle riunioni senza struttura",
            "Tre abitudini che cambiano il ritmo",
            "Strutture per riunioni ricorrenti",
            "Come chiudere con un passo concreto",
        ],
        "sections": [
            (
                "Il costo delle riunioni senza struttura",
                "Agenda generica, aggiornamenti a cascata, domanda finale \"altro?\". "
                "Chi non parla si disimpegna. Chi parla troppo monopolizza. "
                "Tutti escono con la sensazione di aver perso tempo.",
            ),
            (
                "Tre abitudini che cambiano il ritmo",
                "Apri con un passaggio individuale breve, non con \"allora, com'e' andata la settimana?\". "
                "Alterna plenario e lavoro in piccolo. "
                "Chiudi sempre con un \"cosa facciamo adesso\", non con un vago \"ci sentiamo\".",
            ),
            (
                "Strutture per riunioni ricorrenti",
                "[1-2-4-All](/structures/1-2-4-all/) per raccogliere input in 15 minuti. "
                "[What, So What, Now What?](/structures/w3-what-so-what-now-what/) per retrospettive leggere. "
                "[Troika Consulting](/structures/troika-consulting/) quando serve un consiglio rapido tra pari.",
            ),
            (
                "Come chiudere con un passo concreto",
                "Ogni riunione dovrebbe lasciare una traccia: una decisione, un esperimento, un follow-up con nome e data. "
                "[15% Solutions](/structures/15-solutions/) chiede cosa puoi fare tu entro la prossima settimana. "
                "Piccolo, ma reale.",
            ),
        ],
        "faq": [
            (
                "Quanto tempo aggiungono le strutture a una riunione?",
                "Strutture come 1-2-4-All durano 15 minuti. "
                "Spesso sostituiscono 30 minuti di dibattito improduttivo. "
                "Il saldo netto e' a favore della struttura.",
            ),
            (
                "Funziona con riunioni gia' piene di argomenti?",
                "Meglio una struttura su un solo punto critico che zero struttura su tutto. "
                "Scegli il tema dove serve davvero input da tutti.",
            ),
            (
                "Il manager deve facilitare?",
                "Puo' farlo chiunque legga i passaggi. "
                "Anzi, alternare il facilitatore distribuisce le competenze nel team.",
            ),
        ],
        "leggi_anche": [
            ("Inclusione e partecipazione", "/inclusione-partecipazione-riunioni/", "far parlare chi resta in silenzio"),
            ("Icebreaker per riunioni di team", "/icebreaker-riunione-team-liberating-structures/", "aprire senza imbarazzo"),
            ("Catalogo strutture", "/structures/", "tutti i formati disponibili"),
        ],
        "cta_text": "Nella prossima riunione ricorrente, sostituisci il giro di aggiornamenti con un 1-2-4-All su un solo tema.",
        "cta_url": "/structures/1-2-4-all/",
        "cta_label": "Prova 1-2-4-All domani",
    },
    {
        "slug": "facilitazione-remota-liberating-structures",
        "title": "Facilitazione remota con le Liberating Structures",
        "meta_description": "Come facilitare workshop e riunioni online con le Liberating Structures. Breakout room, timer e passaggi che funzionano su Zoom e Teams.",
        "guide_category": "Organizzazione",
        "guide_order": 5,
        "guide_intro": "Stessi passaggi del presenziale, adattati a schermo e breakout room.",
        "h1": "Facilitazione remota con le Liberating Structures",
        "lead": "Online e' piu' facile disimpegnarsi: telecamera spenta, chat silenziosa, multitasking. Le strutture tengono il gruppo dentro il processo anche a distanza.",
        "toc": [
            "Cosa cambia (e cosa no) online",
            "Setup minimo per facilitare bene",
            "Strutture che funzionano meglio da remoto",
            "Errori frequenti da evitare",
        ],
        "sections": [
            (
                "Cosa cambia (e cosa no) online",
                "I passaggi restano gli stessi: individuale, coppia, gruppo, plenario. "
                "Cambia il supporto: breakout room al posto dei tavoli, timer condiviso al posto del cronometro a vista. "
                "Le energie sono piu' basse: sessioni piu' brevi, pause esplicite.",
            ),
            (
                "Setup minimo per facilitare bene",
                "Video attivo per chi puo'. "
                "Breakout room preconfigurate (coppie da 2, gruppi da 4). "
                "Un documento condiviso o board per il plenario. "
                "Istruzioni scritte in chat prima di ogni passaggio, non solo a voce.",
            ),
            (
                "Strutture che funzionano meglio da remoto",
                "[1-2-4-All](/structures/1-2-4-all/) e' ideale: tempi corti, breakout chiari. "
                "[Impromptu Networking](/structures/impromptu-networking/) con room da due persone. "
                "[25/10 Crowd Sourcing](/structures/25-10-crowd-sourcing/) con votazione in chat o in board.",
            ),
            (
                "Errori frequenti da evitare",
                "Saltare il passaggio individuale \"perche' siamo pochi online\". "
                "Dimenticare di richiamare tutti dalla breakout. "
                "Prolungare il plenario quando le idee sono gia' nei gruppi piccoli.",
            ),
        ],
        "faq": [
            (
                "Serve un tool specifico?",
                "No. Zoom, Teams, Meet vanno bene se hanno le breakout room. "
                "Per board condivise puoi usare Miro, Mural o un semplice documento.",
            ),
            (
                "Quante persone massimo online?",
                "Dipende dalla struttura. 1-2-4-All scala fino a 30-40 con breakout ben gestite. "
                "Oltre, valuta 25/10 o Open Space con sessioni parallele.",
            ),
            (
                "Come coinvolgere chi tiene la camera spenta?",
                "Parti da passaggi scritti (chat, documento) prima del parlato. "
                "Non forzare il video: forza la partecipazione strutturata.",
            ),
        ],
        "leggi_anche": [
            ("Riunioni efficaci", "/riunioni-efficaci-struttura-partecipazione/", "struttura anche in presenza"),
            ("1-2-4-All", "/structures/1-2-4-all/", "la struttura piu' adatta al remoto"),
            ("Open Space e World Cafe", "/open-space-world-cafe-liberating-structures/", "eventi grandi online e offline"),
        ],
        "cta_text": "Prossimo meeting online: apri con 1-2-4-All in breakout da 4. Quindici minuti, tutti coinvolti.",
        "cta_url": "/structures/1-2-4-all/",
        "cta_label": "Prova 1-2-4-All online",
    },
    {
        "slug": "retrospettiva-agile-liberating-structures",
        "title": "Retrospettiva agile con le Liberating Structures",
        "meta_description": "Formati per retrospective Scrum e team agile che vanno oltre Start-Stop-Continue. Strutture brevi per riflettere e decidere il prossimo passo.",
        "guide_category": "Organizzazione",
        "guide_order": 6,
        "guide_intro": "Retrospective che producono azioni, non solo post-it dimenticati.",
        "h1": "Retrospettiva agile con le Liberating Structures",
        "lead": "Start-Stop-Continue ha salvato molte retrospective. E poi le ha rese prevedibili. Se il team sbadiglia quando vede il board, e' ora di cambiare formato.",
        "toc": [
            "Perche' le retrospective si consumano",
            "Cosa chiedere invece di Start-Stop-Continue",
            "Strutture consigliate per Scrum e team agile",
            "Chiudere con un impegno concreto",
        ],
        "sections": [
            (
                "Perche' le retrospective si consumano",
                "Stesso formato, stesse categorie, stesse frasi. "
                "Il team impara a dire cose accettabili senza toccare i nodi veri. "
                "Serve varieta' nella struttura, non solo nel tema.",
            ),
            (
                "Cosa chiedere invece di Start-Stop-Continue",
                "[What, So What, Now What?](/structures/w3-what-so-what-now-what/) parte da un fatto concreto dello sprint. "
                "[9 Whys](/structures/9-whys/) va alla radice di un problema ricorrente. "
                "[TRIZ](/structures/triz/) chiede come peggiorare per poi capire come migliorare.",
            ),
            (
                "Strutture consigliate per Scrum e team agile",
                "Sprint breve: 1-2-4-All su \"cosa ci ha sorpreso?\". "
                "Sprint con tensione nel team: HSR prima di qualsiasi analisi. "
                "Sprint con debito tecnico nascosto: 9 Whys in coppia, poi plenario.",
            ),
            (
                "Chiudere con un impegno concreto",
                "Una retro senza azione e' un debrief. "
                "Chiudi con [15% Solutions](/structures/15-solutions/): cosa puoi fare tu, nel prossimo sprint, senza chiedere permesso. "
                "Una sola azione a testa, non una lista di team.",
            ),
        ],
        "faq": [
            (
                "Le Liberating Structures sostituiscono le retrospective classiche?",
                "Le arricchiscono. Puoi usare una LS come cuore della retro (30-45 minuti) "
                "o come singolo passaggio dentro un formato piu' lungo.",
            ),
            (
                "Quale struttura per un team che non si fida?",
                "Inizia con [Heard, Seen, Respected (HSR)](/structures/heard-seen-respected-hsr/). "
                "Senza fiducia, ogni retro produce lamentele senza follow-up.",
            ),
            (
                "Funziona con retrospective remote?",
                "Si. W³ e 1-2-4-All sono tra le piu' usate online. "
                "Vedi anche la guida sulla [facilitazione remota](/facilitazione-remota-liberating-structures/).",
            ),
        ],
        "leggi_anche": [
            ("What, So What, Now What?", "/structures/w3-what-so-what-now-what/", "retro leggera in tre passaggi"),
            ("9 Whys", "/structures/9-whys/", "root cause in coppia"),
            ("Analizzare problemi", "/per-bisogno/analizzare-problemi/", "altre strutture per la riflessione"),
        ],
        "cta_text": "Prossima retro: sostituisci Start-Stop-Continue con W³ su un episodio concreto dello sprint.",
        "cta_url": "/structures/w3-what-so-what-now-what/",
        "cta_label": "Prova W³ nella retro",
    },
    {
        "slug": "open-space-world-cafe-liberating-structures",
        "title": "Open Space, World Cafe e Liberating Structures",
        "meta_description": "Confronto pratico tra Open Space Technology, World Cafe e Liberating Structures. Quando usare quale formato per workshop e conferenze.",
        "guide_category": "Metodi e confronti",
        "guide_order": 7,
        "guide_intro": "Tre famiglie di formati partecipativi: differenze e quando scegliere cosa.",
        "h1": "Open Space, World Cafe e Liberating Structures",
        "lead": "Open Space, World Cafe e Liberating Structures parlano tutti di partecipazione. Ma non sono intercambiabili. Confonderli porta a workshop mal progettati.",
        "toc": [
            "Tre logiche diverse",
            "Open Space Technology in sintesi",
            "World Cafe: cosa e' e cosa non e'",
            "Dove entrano le Liberating Structures",
        ],
        "sections": [
            (
                "Tre logiche diverse",
                "Open Space delega l'agenda ai partecipanti. "
                "World Cafe favorisce conversazioni a tavoli rotanti su domande fisse. "
                "Le Liberating Structures sono micro-formati con passaggi precisi, usabili dentro o fuori eventi grandi.",
            ),
            (
                "Open Space Technology in sintesi",
                "[Open Space Technology (OST)](/structures/open-space-technology-ost/) funziona con 20+ persone e mezza giornata o piu'. "
                "Chi ha passione propone sessioni, chi partecipa sceglie. "
                "Serve un tema ampio e un facilitatore che tenga lo spazio, non il contenuto.",
            ),
            (
                "World Cafe: cosa e' e cosa non e'",
                "World Cafe non e' una Liberating Structure. "
                "[Conversation Cafe](/structures/conversation-cafe/) e' l'adattamento LS piu' vicino: conversazione profonda a tavolo, non rotazione rapida. "
                "Se cerchi World Cafe su liberating.it, trovi la disambiguazione nella scheda Conversation Cafe.",
            ),
            (
                "Dove entrano le Liberating Structures",
                "In un Open Space, una LS apre o chiude una sessione. "
                "In un workshop breve, una LS e' l'intero evento. "
                "Non serve scegliere un solo metodo per sempre: combina in base a durata, numero e obiettivo.",
            ),
        ],
        "faq": [
            (
                "Conversation Cafe e World Cafe sono la stessa cosa?",
                "No. World Cafe e' un metodo con rotazione tra tavoli. "
                "Conversation Cafe e' una Liberating Structure per conversazioni profonde senza rotazione. "
                "Sono complementari, non equivalenti.",
            ),
            (
                "Quante persone servono per Open Space?",
                "Di solito almeno 15-20, con tempo sufficiente (3-4 ore minimo). "
                "Sotto quella soglia, formati piu' brevi come 1-2-4-All sono piu' adatti.",
            ),
            (
                "Posso mescolare LS e Open Space nello stesso evento?",
                "Si. OST per l'agenda libera, LS per aprire, chiudere o approfondire singole sessioni.",
            ),
        ],
        "leggi_anche": [
            ("Open Space Technology", "/structures/open-space-technology-ost/", "scheda completa OST"),
            ("Conversation Cafe", "/structures/conversation-cafe/", "vs World Cafe, chiarimenti"),
            ("Facilitazione remota", "/facilitazione-remota-liberating-structures/", "eventi grandi anche online"),
        ],
        "cta_text": "Se hai un evento da mezza giornata in su, leggi la scheda OST e valuta se e' il formato giusto.",
        "cta_url": "/structures/open-space-technology-ost/",
        "cta_label": "Scopri Open Space Technology",
    },
    {
        "slug": "root-cause-analysis-gruppo-liberating-structures",
        "title": "Root cause analysis di gruppo con le Liberating Structures",
        "meta_description": "Analisi delle cause profonde in team con 9 Whys e altre strutture LS. Oltre i 5 Perche' senza perdere il gruppo.",
        "guide_category": "Fondamenti",
        "guide_order": 8,
        "guide_intro": "Andare alla radice di un problema senza interrogatorio ne' supposizioni.",
        "h1": "Root cause analysis di gruppo con le Liberating Structures",
        "lead": "Il sintomo e' chiaro. La causa no. E se chiedi in plenario \"perche' e' successo?\", ottieni supposizioni o colpevolizzazioni. Serve un formato che costruisca la catena insieme.",
        "toc": [
            "Perche' la root cause analysis fallisce in gruppo",
            "9 Whys: come funziona in pratica",
            "Altre strutture per analizzare problemi",
            "Dal perche' all'azione",
        ],
        "sections": [
            (
                "Perche' la root cause analysis fallisce in gruppo",
                "Si mescolano fatti e opinioni. "
                "Chi e' vicino al problema non ha voce. "
                "Si ferma al primo \"perche'\" comodo. "
                "Il gruppo esce con un'etichetta, non con comprensione.",
            ),
            (
                "9 Whys: come funziona in pratica",
                "[9 Whys](/structures/9-whys/) lavora in coppia: un partner chiede \"perche'?\" fino a nove volte, l'altro risponde. "
                "Poi si scambiano i ruoli su un altro tema. "
                "Il plenario raccoglie pattern, non monologhi.",
            ),
            (
                "Altre strutture per analizzare problemi",
                "[TRIZ](/structures/triz/) chiede come peggiorare deliberatamente: utile per vedere cosa manca. "
                "[What, So What, Now What?](/structures/w3-what-so-what-now-what/) per incidenti recenti. "
                "Hub completo: [Analizzare problemi](/per-bisogno/analizzare-problemi/).",
            ),
            (
                "Dal perche' all'azione",
                "La root cause senza azione e' accademica. "
                "Dopo 9 Whys, chiudi con [15% Solutions](/structures/15-solutions/): cosa puoi fare tu sulla causa emersa. "
                "Piccolo, specifico, entro una settimana.",
            ),
        ],
        "faq": [
            (
                "9 Whys e i 5 Perche' sono la stessa cosa?",
                "Simili nell'idea, diversi nel formato. "
                "9 Whys e' una Liberating Structure con ruoli, tempi e scambio in coppia. "
                "I 5 Perche' classici spesso restano un esercizio individuale su lavagna.",
            ),
            (
                "Quanto dura una sessione di root cause con LS?",
                "9 Whys richiede circa 30 minuti. "
                "Con W³ o TRIZ puoi stare su un'ora totale in riunione.",
            ),
            (
                "Funziona su problemi \"politici\"?",
                "HSR prima, analisi dopo. "
                "Senza ascolto delle parti coinvolte, la root cause diventa spostamento di colpa.",
            ),
        ],
        "leggi_anche": [
            ("9 Whys", "/structures/9-whys/", "scheda con passaggi e tempi"),
            ("TRIZ", "/structures/triz/", "analisi partendo dai vincoli"),
            ("Retrospettiva agile", "/retrospettiva-agile-liberating-structures/", "root cause nelle retro"),
        ],
        "cta_text": "Prossimo incidente o problema ricorrente: prova 9 Whys in coppia prima del dibattito in plenario.",
        "cta_url": "/structures/9-whys/",
        "cta_label": "Prova 9 Whys",
    },
    {
        "slug": "inclusione-partecipazione-riunioni",
        "title": "Inclusione e partecipazione nelle riunioni",
        "meta_description": "Come far partecipare chi resta in silenzio nelle riunioni. Strutture che danno voce a tutti senza imbarazzo forzato.",
        "guide_category": "Riunioni e team",
        "guide_order": 9,
        "guide_intro": "Non e' questione di carattere: e' questione di design della riunione.",
        "h1": "Inclusione e partecipazione nelle riunioni",
        "lead": "Non e' che le persone quiete non abbiano nulla da dire. E' che la riunione non glielo chiede nel modo giusto. Cambiare il formato cambia chi parla.",
        "toc": [
            "Perche' alcune voci restano fuori",
            "Tempo individuale prima del plenario",
            "Strutture per inclusione reale",
            "Quando serve ricostruire fiducia",
        ],
        "sections": [
            (
                "Perche' alcune voci restano fuori",
                "Cultura aziendale che premia chi parla per primo. "
                "Gerarchia percepita. "
                "Lingua diversa da quella del dibattito. "
                "Introversione trattata come disinteresse.",
            ),
            (
                "Tempo individuale prima del plenario",
                "Due minuti di silenzio per scrivere o pensare. "
                "Poi coppia, poi gruppo da quattro. "
                "Al plenario arrivano idee gia' formulate, non improvvisazione sotto pressione.",
            ),
            (
                "Strutture per inclusione reale",
                "[1-2-4-All](/structures/1-2-4-all/) garantisce un turno a ognuno nel gruppo da quattro. "
                "[Impromptu Networking](/structures/impromptu-networking/) abbassa la soglia con incontri brevi uno a uno. "
                "[User Experience Fishbowl](/structures/user-experience-fishbowl/) mette al centro chi vive il problema.",
            ),
            (
                "Quando serve ricostruire fiducia",
                "Se il gruppo e' in conflitto o ha perso fiducia, nessuna struttura \"creativa\" basta da sola. "
                "Inizia con [Heard, Seen, Respected (HSR)](/structures/heard-seen-respected-hsr/). "
                "Poi passa a formati piu' operativi.",
            ),
        ],
        "faq": [
            (
                "Forzare tutti a parlare in plenario e' inclusivo?",
                "No. L'inclusione e' dare spazio strutturato, non mettere in imbarazzo. "
                "1-2-4-All permette di contribuire prima in piccolo.",
            ),
            (
                "Come includere chi partecipa in lingua non madre?",
                "Passaggi scritti, tempo extra per la riflessione, coppie stabili per tutta la sessione. "
                "Evita dibattiti rapidi a turno di parola.",
            ),
            (
                "HSR o 1-2-4-All per iniziare?",
                "Se c'e' tensione nel gruppo, HSR. "
                "Se il gruppo e' neutro ma abitudinato al monologo, 1-2-4-All.",
            ),
        ],
        "leggi_anche": [
            ("Heard, Seen, Respected (HSR)", "/structures/heard-seen-respected-hsr/", "ricostruire fiducia nel gruppo"),
            ("I 10 principi", "/10-principi-fondamentali-liberating-structures/", "inclusione reale come principio"),
            ("Dinamiche di gruppo", "/dinamiche-di-gruppo-facilitazione/", "gestire conflitti e ruoli"),
        ],
        "cta_text": "Prossima riunione: due minuti individuali, poi 1-2-4-All. Vedrai comparire voci che non sentivi da mesi.",
        "cta_url": "/structures/1-2-4-all/",
        "cta_label": "Prova 1-2-4-All domani",
    },
    {
        "slug": "helping-heuristics-aiutare-senza-controllare",
        "title": "Helping heuristics: aiutare senza controllare",
        "meta_description": "Le regole di aiuto delle Liberating Structures: come supportare un team senza prendere il comando. Dal consiglio non richiesto alla domanda giusta.",
        "guide_category": "Metodi e confronti",
        "guide_order": 10,
        "guide_intro": "Smettere di \"aiutare\" dominando la conversazione.",
        "h1": "Helping heuristics: aiutare senza controllare",
        "lead": "Vuoi aiutare il team e finisci per decidere tu. Oppure resti in silenzio e il gruppo gira a vuoto. Le helping heuristics sono regole semplici per stare nel mezzo giusto.",
        "toc": [
            "Quando l'aiuto diventa controllo",
            "Le tre regole in sintesi",
            "Strutture che applicano le heuristics",
            "Per manager, coach e HR",
        ],
        "sections": [
            (
                "Quando l'aiuto diventa controllo",
                "Consigli non richiesti. "
                "Risposte al posto delle domande. "
                "Soluzioni portate prima che il gruppo abbia finito di esplorare. "
                "Sembra efficienza. E' sottrazione di ownership.",
            ),
            (
                "Le tre regole in sintesi",
                "Chi ha il problema e' la persona giusta per risolverlo. "
                "Il compito dell'helper e' far emergere la soluzione, non fornirla. "
                "Se vuoi aiutare, chiedi permesso prima di entrare.",
            ),
            (
                "Strutture che applicano le heuristics",
                "[Troika Consulting](/structures/troika-consulting/) mette un \"cliente\" al centro e due consulenti che ascoltano prima di rispondere. "
                "[Wise Crowds](/structures/wise-crowds/) distribuisce ruoli di aiuto espliciti. "
                "[What I Need From You (WINFY)](/structures/what-i-need-from-you-winfy/) chiede cosa serve, non cosa offrire.",
            ),
            (
                "Per manager, coach e HR",
                "Se sei il capo, il gruppo dira' si' anche quando non e' d'accordo. "
                "Usa strutture che ti tolgono il centro della scena. "
                "Osserva, cronometra, fai domande. Non sommare la tua soluzione alla fine.",
            ),
        ],
        "faq": [
            (
                "Cosa sono le helping heuristics nelle Liberating Structures?",
                "Sono tre regole per aiutare un gruppo senza imporre la propria soluzione: "
                "chi ha il problema risolve, l'helper facilita, chiedi permesso prima di intervenire.",
            ),
            (
                "Un manager puo' usare Troika Consulting?",
                "Si, come facilitatore o come \"cliente\" che espone un problema reale. "
                "Evita di chiudere tu la sessione con la \"risposta giusta\".",
            ),
            (
                "Helping heuristics e coaching: sono compatibili?",
                "Si. Il coach che fa domande invece di dare risposte applica gia' queste regole. "
                "Le LS le rendono esplicite e ripetibili in gruppo.",
            ),
        ],
        "leggi_anche": [
            ("Troika Consulting", "/structures/troika-consulting/", "consiglio tra pari strutturato"),
            ("Wise Crowds", "/structures/wise-crowds/", "ruoli di aiuto distribuiti"),
            ("I 10 principi", "/10-principi-fondamentali-liberating-structures/", "fiducia e libertà responsabile"),
        ],
        "cta_text": "Prossima volta che il team chiede un consiglio, prova Troika Consulting invece di rispondere tu.",
        "cta_url": "/structures/troika-consulting/",
        "cta_label": "Prova Troika Consulting",
    },
    {
        "slug": "pianificazione-strategica-partecipativa",
        "title": "Pianificazione strategica partecipativa",
        "meta_description": "Workshop di strategic planning con le Liberating Structures. Coinvolgere il team nella strategia senza slide infinite ne' top-down.",
        "guide_category": "Organizzazione",
        "guide_order": 11,
        "guide_intro": "Strategia che il team riconosce perche' l'ha costruita insieme.",
        "h1": "Pianificazione strategica partecipativa",
        "lead": "La strategia finisce in un cassetto quando e' stata scritta da tre persone in una stanza chiusa. Coinvolgere non significa un sondaggio. Significa strutturare il pensiero collettivo.",
        "toc": [
            "Perche' la strategia top-down non regge",
            "Domande giuste prima del piano",
            "Strutture per workshop strategici",
            "Da visione a passi concreti",
        ],
        "sections": [
            (
                "Perche' la strategia top-down non regge",
                "Chi esegue non riconosce le priorita'. "
                "I compromessi politici restano nascosti. "
                "Al primo ostacolo, tutti tornano alle vecchie abitudini.",
            ),
            (
                "Domande giuste prima del piano",
                "[Wicked Questions](/structures/wicked-questions/) tiene insieme due obiettivi in tensione invece di risolverli a finti. "
                "[Purpose to Practice (P2P)](/structures/purpose-to-practice-p2p/) allinea scopo, principi e pratiche. "
                "Senza domande, il workshop produce slide.",
            ),
            (
                "Strutture per workshop strategici",
                "[Ecocycle Planning](/structures/ecocycle-planning/) mappa cosa lasciare, cosa innovare, cosa accelerare. "
                "[25/10 Crowd Sourcing](/structures/25-10-crowd-sourcing/) priorizza iniziative in gruppo grande. "
                "Percorso: [Fare strategia](/per-bisogno/fare-strategia/).",
            ),
            (
                "Da visione a passi concreti",
                "Ogni sessione strategica chiude con [15% Solutions](/structures/15-solutions/) o [Min Specs](/structures/min-specs/). "
                "Cosa fai tu, con quello che hai, entro 30 giorni. "
                "La strategia vive nei comportamenti, non nel documento.",
            ),
        ],
        "faq": [
            (
                "Quanto dura un workshop di strategic planning con LS?",
                "Da mezza giornata (un tema, 2-3 strutture) a due giorni per un ciclo Ecocycle completo. "
                "Meglio poche strutture fatte bene che un tour forzato del catalogo.",
            ),
            (
                "Serve un facilitatore esterno?",
                "Utile se ci sono tensioni di potere. "
                "Un manager interno puo' facilitare se usa strutture che lo tengono fuori dal contenuto.",
            ),
            (
                "Wicked Questions per la strategia: esempio?",
                "Come possiamo essere piu' snelli e piu' vicini al cliente allo stesso tempo? "
                "La tensione resta visibile invece di essere nascosta nel piano.",
            ),
        ],
        "leggi_anche": [
            ("Fare strategia", "/per-bisogno/fare-strategia/", "hub strutture per la strategia"),
            ("Ecocycle Planning", "/structures/ecocycle-planning/", "mappa il portafoglio"),
            ("Wicked Questions", "/structures/wicked-questions/", "domande in tensione"),
        ],
        "cta_text": "Prossimo workshop strategico: apri con una Wicked Question invece che con lo slide deck.",
        "cta_url": "/structures/wicked-questions/",
        "cta_label": "Prova Wicked Questions",
    },
    {
        "slug": "cambiamento-organizzativo-15-percent-solutions",
        "title": "Cambiamento organizzativo con 15% Solutions",
        "meta_description": "Come avviare il cambiamento senza aspettare il via libera. 15% Solutions per team e organizzazioni che vogliono muoversi subito.",
        "guide_category": "Organizzazione",
        "guide_order": 12,
        "guide_intro": "Agire nel tuo 15% di autonomia invece di aspettare il grande progetto.",
        "h1": "Cambiamento organizzativo con 15% Solutions",
        "lead": "Il piano di change management e' pronto tra sei mesi. Intanto il team continua come prima. 15% Solutions chiede: cosa puoi cambiare tu, adesso, senza permesso?",
        "toc": [
            "Perche' il cambiamento si blocca",
            "Cos'e' il tuo 15%",
            "Come funziona la struttura",
            "Dal piccolo esperimento alla scala",
        ],
        "sections": [
            (
                "Perche' il cambiamento si blocca",
                "Si aspetta il mandato dall'alto. "
                "Si disegna un piano perfetto che non parte mai. "
                "Chi e' in basso nella gerarchia sente di non poter fare nulla.",
            ),
            (
                "Cos'e' il tuo 15%",
                "E' la parte del lavoro che controlli gia': come organizzi la riunione, come rispondi al cliente, come condividi informazioni. "
                "Non e' rivoluzione. E' movimento reale nel tuo raggio d'azione.",
            ),
            (
                "Come funziona la struttura",
                "[15% Solutions](/structures/15-solutions/) chiede: senza budget extra e senza permesso formale, cosa puoi fare entro questa settimana? "
                "Prima individuale, poi in coppia per affinare, poi condivisione al gruppo. "
                "Le azioni piccole si sommano e creano prove per il cambiamento piu' grande.",
            ),
            (
                "Dal piccolo esperimento alla scala",
                "Raccogli cosa ha funzionato con [What, So What, Now What?](/structures/w3-what-so-what-now-what/). "
                "Porta le prove al management con dati, non con lamentele. "
                "Il 15% diventa argomento per il 100%.",
            ),
        ],
        "faq": [
            (
                "15% Solutions e' solo per individui?",
                "No. Funziona in team, reparti, persino in workshop plenari. "
                "Ognuno propone il proprio 15%, poi il gruppo vede pattern comuni.",
            ),
            (
                "E se il management blocca ogni iniziativa?",
                "Il 15% e' per definizione sotto la soglia del permesso. "
                "Se anche quello e' bloccato, il problema e' culturale: servono prima HSR o Conversation Cafe.",
            ),
            (
                "Quanto dura una sessione?",
                "Circa 20-30 minuti. "
                "Ideale come chiusura di una riunione o come apertura di un ciclo di cambiamento.",
            ),
        ],
        "leggi_anche": [
            ("15% Solutions", "/structures/15-solutions/", "scheda con passaggi"),
            ("Pianificazione strategica partecipativa", "/pianificazione-strategica-partecipativa/", "cambiamento a livello strategico"),
            ("I 10 principi", "/10-principi-fondamentali-liberating-structures/", "ottimismo pragmatico"),
        ],
        "cta_text": "Chiedi al team: cosa puoi cambiare tu questa settimana, senza chiedere permesso?",
        "cta_url": "/structures/15-solutions/",
        "cta_label": "Prova 15% Solutions",
    },
    {
        "slug": "design-thinking-liberating-structures",
        "title": "Design thinking e Liberating Structures",
        "meta_description": "Come combinare design thinking e Liberating Structures in workshop di innovazione. Empatia, ideazione e test con formati partecipativi.",
        "guide_category": "Metodi e confronti",
        "guide_order": 13,
        "guide_intro": "Due linguaggi, un obiettivo: innovare con il team, non per il team.",
        "h1": "Design thinking e Liberating Structures",
        "lead": "Design thinking e Liberating Structures vengono spesso usati negli stessi workshop. Non sono la stessa cosa. Ma si completano bene se sai dove mettere ciascuno.",
        "toc": [
            "Cosa condividono, cosa separa",
            "LS per la fase Empathize e Define",
            "LS per Ideate e Test",
            "Un percorso combinato in una giornata",
        ],
        "sections": [
            (
                "Cosa condividono, cosa separa",
                "Entrambi mettono le persone al centro. "
                "Il design thinking e' un processo a fasi (empatia, definizione, ideazione, prototipo, test). "
                "Le LS sono formati concreti con passaggi e tempi. "
                "Le LS non sostituiscono il DT: lo rendono piu' partecipativo.",
            ),
            (
                "LS per la fase Empathize e Define",
                "[User Experience Fishbowl](/structures/user-experience-fishbowl/) mette al centro chi vive il problema. "
                "[9 Whys](/structures/9-whys/) approfondisce bisogni nascosti. "
                "[What, So What, Now What?](/structures/w3-what-so-what-now-what/) sintetizza osservazioni in insight.",
            ),
            (
                "LS per Ideate e Test",
                "[1-2-4-All](/structures/1-2-4-all/) e [25/10 Crowd Sourcing](/structures/25-10-crowd-sourcing/) per generare e priorizzare idee. "
                "[Troika Consulting](/structures/troika-consulting/) per feedback rapido su prototipi concettuali.",
            ),
            (
                "Un percorso combinato in una giornata",
                "Mattina: Fishbowl + W³ per empatia e sintesi. "
                "Pomeriggio: 1-2-4-All + 25/10 per idee e scelta. "
                "Chiudi con 15% Solutions: cosa testi questa settimana. "
                "Filtra le strutture per fase DT nel [catalogo](/structures/).",
            ),
        ],
        "faq": [
            (
                "Devo scegliere tra design thinking e Liberating Structures?",
                "No. Usa il DT per il percorso e le LS per i singoli momenti del workshop. "
                "Sono complementari.",
            ),
            (
                "Quali LS per la fase Define?",
                "9 Whys per il problema, Min Specs per i vincoli, Wicked Questions se ci sono tensioni strategiche.",
            ),
            (
                "Funziona in contesti non \"creativi\"?",
                "Si. HR, operations, sanita': ovunque ci siano utenti da ascoltare e idee da testare.",
            ),
        ],
        "leggi_anche": [
            ("Hub design thinking", "/design-thinking/empathize/", "strutture per fase DT"),
            ("Brainstorming alternativo", "/brainstorming-alternative-liberating-structures/", "ideazione strutturata"),
            ("User Experience Fishbowl", "/structures/user-experience-fishbowl/", "empatia in gruppo"),
        ],
        "cta_text": "Prossimo workshop DT: sostituisci il brainstorm libero con 1-2-4-All nella fase ideate.",
        "cta_url": "/structures/1-2-4-all/",
        "cta_label": "Prova 1-2-4-All nel workshop",
    },
    {
        "slug": "dinamiche-di-gruppo-facilitazione",
        "title": "Dinamiche di gruppo e facilitazione",
        "meta_description": "Gestire conflitti, silenzi e dominanza nelle riunioni. Come le Liberating Structures intervengono sulle dinamiche di gruppo.",
        "guide_category": "Riunioni e team",
        "guide_order": 14,
        "guide_intro": "Il formato influenza chi parla, chi tace e come si decide.",
        "h1": "Dinamiche di gruppo e facilitazione",
        "lead": "Ogni gruppo ha i suoi pattern: chi domina, chi sparisce, chi fa ostruzionismo silenzioso. Puoi lasciare che accadano. Oppure puoi cambiare il formato che li alimenta.",
        "toc": [
            "Pattern comuni nelle riunioni",
            "Il formato come leva",
            "Strutture per tensioni diverse",
            "Quando serve fermarsi e ascoltare",
        ],
        "sections": [
            (
                "Pattern comuni nelle riunioni",
                "Il monologo del capo. "
                "Il dibattito tra due persone mentre gli altri guardano. "
                "Il silenzio che viene letto come consenso. "
                "La persona che blocca ogni proposta senza alternative.",
            ),
            (
                "Il formato come leva",
                "Non correggere la persona. Cambia il passaggio. "
                "Coppie invece di plenario. "
                "Scrittura individuale prima del parlato. "
                "Ruoli espliciti (cliente, consulente, osservatore) come in Troika.",
            ),
            (
                "Strutture per tensioni diverse",
                "Dominanza: [1-2-4-All](/structures/1-2-4-all/) con tempi rigidi. "
                "Conflitto aperto: [Heard, Seen, Respected (HSR)](/structures/heard-seen-respected-hsr/). "
                "Disallineamento strategico: [Wicked Questions](/structures/wicked-questions/).",
            ),
            (
                "Quando serve fermarsi e ascoltare",
                "Se le tensioni sono alte, nessuna struttura \"operativa\" funziona. "
                "HSR o [Conversation Cafe](/structures/conversation-cafe/) prima. "
                "Solo dopo torna a decisioni e idee.",
            ),
        ],
        "faq": [
            (
                "Il facilitatore deve essere neutrale?",
                "Deve essere chiaro sui passaggi, non sui contenuti. "
                "Puoi avere un'opinione, ma non chiudere tu la discussione.",
            ),
            (
                "Come gestire chi monopolizza la parola?",
                "Timer visibile, passaggi in coppia, regola \"una idea per turno\" in 1-2-4-All. "
                "Il formato limita il monologo meglio di un \"sii breve\".",
            ),
            (
                "Dinamiche di gruppo e team building: sono la stessa cosa?",
                "No. Le LS non sono giochi. "
                "Sono formati per lavoro reale che, come effetto collaterale, migliorano come il gruppo collabora.",
            ),
        ],
        "leggi_anche": [
            ("Inclusione e partecipazione", "/inclusione-partecipazione-riunioni/", "far parlare chi tace"),
            ("Helping heuristics", "/helping-heuristics-aiutare-senza-controllare/", "aiutare senza controllare"),
            ("Conversation Cafe", "/structures/conversation-cafe/", "conversazioni difficili"),
        ],
        "cta_text": "Se il gruppo e' in tensione, non aprire con idee. Apri con HSR.",
        "cta_url": "/structures/heard-seen-respected-hsr/",
        "cta_label": "Prova HSR",
    },
    {
        "slug": "icebreaker-riunione-team-liberating-structures",
        "title": "Icebreaker per riunioni di team con le Liberating Structures",
        "meta_description": "Aprire riunioni e workshop senza imbarazzo. Icebreaker strutturati che preparano al lavoro vero, non solo al divertimento forzato.",
        "guide_category": "Riunioni e team",
        "guide_order": 15,
        "guide_intro": "Aprire bene conta: non giochi a caso, ma passaggi leggeri e utili.",
        "h1": "Icebreaker per riunioni di team con le Liberating Structures",
        "lead": "L'icebreaker puo' essere il momento piu' imbarazzante della giornata. Oppure puo' preparare il gruppo al tema vero. La differenza e' nella struttura, non nell'energia forzata.",
        "toc": [
            "Perche' molti icebreaker non funzionano",
            "Icebreaker che collegano al tema",
            "Tre strutture per aprire in 10-15 minuti",
            "Quando saltare l'icebreaker",
        ],
        "sections": [
            (
                "Perche' molti icebreaker non funzionano",
                "Domande troppo personali. "
                "Giochi che umiliano chi e' timido. "
                "Nessun collegamento con il lavoro che segue. "
                "Il gruppo li subisce e poi si disimpegna dal resto.",
            ),
            (
                "Icebreaker che collegano al tema",
                "Un buon apertura e' una versione leggera della struttura principale. "
                "Stessi passaggi, domanda piu' semplice, tempi piu' corti. "
                "Il gruppo impara il formato senza accorgersene.",
            ),
            (
                "Tre strutture per aprire in 10-15 minuti",
                "[Impromptu Networking](/structures/impromptu-networking/) con una domanda legata al tema. "
                "1-2-4-All abbreviato (1 min + 2 min + 4 min) su \"cosa ti aspetti da oggi?\". "
                "[Heard, Seen, Respected (HSR)](/structures/heard-seen-respected-hsr/) leggero se c'e' tensione nel team.",
            ),
            (
                "Quando saltare l'icebreaker",
                "Gruppo che si conosce bene e ha urgenza operativa. "
                "Meglio un check-in da 2 minuti che un gioco da 20. "
                "L'obiettivo e' attivare, non intrattenere.",
            ),
        ],
        "faq": [
            (
                "Un icebreaker LS dura quanto?",
                "Da 5 a 15 minuti. "
                "Impromptu Networking puo' bastare in 10 minuti con 3-4 round.",
            ),
            (
                "Funziona con team che si vedono solo online?",
                "Si. Impromptu Networking in breakout da due e' uno dei migliori apertura remote.",
            ),
            (
                "Icebreaker e team building sono la stessa cosa?",
                "No. Un icebreaker LS prepara al tema della sessione. "
                "Il team building e' un obiettivo diverso, spesso piu' lungo.",
            ),
        ],
        "leggi_anche": [
            ("Impromptu Networking", "/structures/impromptu-networking/", "scheda completa"),
            ("Riunioni efficaci", "/riunioni-efficaci-struttura-partecipazione/", "struttura per tutta la riunione"),
            ("Facilitazione remota", "/facilitazione-remota-liberating-structures/", "aperture online"),
        ],
        "cta_text": "Prossima riunione: apri con Impromptu Networking su una domanda legata al tema. Dieci minuti.",
        "cta_url": "/structures/impromptu-networking/",
        "cta_label": "Prova Impromptu Networking",
    },
]


def yaml_scalar(value: str) -> str:
    if not value:
        return '""'
    if '"' in value and "'" not in value:
        return f"'{value}'"
    if '"' in value:
        return ">" + "\n  " + value.replace("\n", "\n  ")
    return f'"{value}"'


def render_guide(g: dict) -> str:
    lines = [
        "---",
        f"slug: {g['slug']}",
        f"title: {yaml_scalar(g['title'])}",
        f"meta_description: {yaml_scalar(g['meta_description'])}",
        "registro: diario-di-bordo",
        f"url: {yaml_scalar('https://liberating.it/' + g['slug'] + '/')}",
        f"guide_category: {g['guide_category']}",
        f"guide_order: {g['guide_order']}",
        f"guide_intro: {yaml_scalar(g['guide_intro'])}",
        f"cta_url: {g['cta_url']}",
        f"cta_label: {yaml_scalar(g['cta_label'])}",
        "---",
        "",
        f"# {g['h1']}",
        "",
        g["lead"],
        "",
        "**Cosa trovi qui**",
        "",
    ]
    for item in g["toc"]:
        lines.append(f"- {item}")
    lines.append("")
    for i, (title, body) in enumerate(g["sections"], start=1):
        lines.extend([f"## {i}. {title}", "", body, ""])
    lines.extend(["## Domande frequenti", ""])
    for q, a in g["faq"]:
        lines.extend([f"### {q}", "", a, ""])
    lines.extend(["## Leggi anche", ""])
    for name, url, reason in g["leggi_anche"]:
        lines.append(f"- [{name}]({url}) - {reason}")
    lines.extend(["", "## E adesso?", "", g["cta_text"], ""])
    return "\n".join(lines)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for g in GUIDES:
        path = OUT_DIR / f"{g['slug']}.md"
        path.write_text(render_guide(g), encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
