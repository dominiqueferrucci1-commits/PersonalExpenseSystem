# Sistema di Gestione delle Spese Personali e del Budget

Applicazione console in Python per la gestione personale di spese, categorie e budget mensili. Utilizza SQLite come database locale.

## Requisiti

- **Python 3.10+** (necessario per lo statement `match`; testato su Python 3.11)
- **Libreria standard `sqlite3`** (inclusa in Python, nessuna installazione aggiuntiva richiesta)
- Sistema operativo: Windows, Linux, macOS

## Struttura del Progetto

```
PersonalExpenseSystem/
├── src/
│   └── main.py              # Codice sorgente principale
├── sql/
│   ├── database.sql         # Script SQL per creazione tabelle e dati di esempio
│   └── spese.db             # Database SQLite (creato automaticamente al primo avvio)
├── demo/
│   └── demo_video.mp4       # Video dimostrativo del funzionamento
└── README.md                # Questo file
```

## Installazione e Avvio

### 1. Clona il repository

```bash
git clone https://github.com/dominiqueferrucci1-commits/PersonalExpenseSystem.git
cd PersonalExpenseSystem
```

### 2. Esegui il programma

```bash
python src/main.py
```

> **Nota**: Al primo avvio, il database `sql/spese.db` viene creato automaticamente eseguendo lo script `sql/database.sql` che include la struttura delle tabelle e dati di esempio.

## Funzionalità

### Menu Principale
1. **Gestione Categorie** - Aggiungi nuove categorie di spesa
2. **Inserisci Spesa** - Registra una nuova spesa con data, importo, categoria e descrizione
3. **Definisci Budget Mensile** - Imposta limiti di spesa per categoria per un dato mese
4. **Visualizza Report** - Accedi ai report disponibili
5. **Esci** - Chiude l'applicazione

### Report Disponibili
1. **Totale spese per categoria** - Somma di tutte le spese raggruppate per categoria
2. **Spese mensili vs budget** - Confronto tra spese effettive e budget per mese/categoria con stato (SUPERAMENTO BUDGET / NEI LIMITI / BUDGET ESAURITO)
3. **Elenco completo delle spese** - Tutte le spese ordinate cronologicamente

## Validazioni Implementate

- **Categorie**: Nome non vuoto, unicità (no duplicati)
- **Spese**: Data formato YYYY-MM-DD valida, importo > 0, categoria deve esistere
- **Budget**: Mese formato YYYY-MM valido, importo > 0, categoria deve esistere, un solo budget per categoria al mese

## Database Schema

Tutti i campi dichiarano esclusivamente **tipi di dato standard SQL (SQL:2014)**: `INTEGER`, `VARCHAR(n)`, `NUMERIC(precisione, scala)`, `DATE`, `TIMESTAMP`.

### Tabella `categorie`
| Campo | Tipo | Vincoli |
|-------|------|---------|
| id_categoria | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| nome | VARCHAR(100) | NOT NULL, UNIQUE, CHECK (non vuoto) |
| data_creazione | DATE | NOT NULL, DEFAULT date('now') |

### Tabella `spese`
| Campo | Tipo | Vincoli |
|-------|------|---------|
| id_spesa | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| data | DATE | NOT NULL, CHECK (formato data valido) |
| importo | NUMERIC(10,2) | NOT NULL, CHECK (> 0) |
| id_categoria | INTEGER | NOT NULL, FOREIGN KEY → categorie.id_categoria |
| descrizione | VARCHAR(200) | NULLABLE |
| data_inserimento | TIMESTAMP | NOT NULL, DEFAULT datetime('now') |

### Tabella `budget_mensili`
| Campo | Tipo | Vincoli |
|-------|------|---------|
| id_budget | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| mese | VARCHAR(7) | NOT NULL, CHECK (formato YYYY-MM valido) |
| id_categoria | INTEGER | NOT NULL, FOREIGN KEY → categorie.id_categoria |
| importo_budget | NUMERIC(10,2) | NOT NULL, CHECK (> 0) |
| data_creazione | TIMESTAMP | NOT NULL, DEFAULT datetime('now') |
| UNIQUE(mese, id_categoria) | | Un solo budget per categoria al mese |

## Nota sui tipi temporali in SQLite (type affinity)

Lo schema DDL usa **esclusivamente tipi di dato standard SQL:2014**. Va segnalato, per correttezza, come SQLite interpreti i tipi temporali, dato che SQLite adotta la cosiddetta **type affinity**: al posto di imporre il tipo dichiarato, assegna alla colonna un'affinità e memorizza il valore secondo la sua natura.

| Colonna dichiarata | Affinità SQLite | Valore inserito | Classe di archiviazione (`typeof`) |
|---|---|---|---|
| `DATE` / `TIMESTAMP` | NUMERIC | `'2025-01-05'` (non convertibile in numero) | `text` |
| `NUMERIC(10,2)` | NUMERIC | `45.5` | `real` |

Questo comporta due differenze rispetto a un DBMS con tipi temporali nativi (es. PostgreSQL, MySQL), entrambe **già compensate** nel progetto:

1. **Nessuna validazione automatica del calendario.** SQLite non rifiuta di per sé date come `2025-13-45`. Il progetto applica una duplice barriera:
   - a livello SQL: il vincolo `CHECK (date(data) IS NOT NULL)` — la funzione `date()` restituisce `NULL` su date malformate, quindi il vincolo le blocca;
   - a livello applicativo: la data viene validata in Python con `datetime.strptime` prima dell'INSERT.
2. **Confronti e ordinamenti.** Le date sono conservate come stringhe, ma nel formato ISO 8601 (`YYYY-MM-DD`) l'ordinamento lessicografico coincide con l'ordinamento cronologico: le operazioni `ORDER BY data` e il confronto `substr(data, 1, 7) = mese` (usato nel report spese/budget) producono risultati corretti.

Il vantaggio di questa scelta è la **portabilità**: lo script SQL funziona identico su un DBMS con tipi temporali reali, perché tutti i valori inseriti sono stringhe ISO 8601 e il DDL non richiede alcuna modifica. Infine, la libreria standard `sqlite3` è inclusa in ogni installazione di Python, senza dipendenze esterne.

## Esempi di Utilizzo

### Aggiungere una categoria
```
1. Gestione Categorie
Inserisci il nome della categoria: Alimentari
> Categoria inserita correttamente.
```

### Inserire una spesa
```
2. Inserisci Spesa
Data (YYYY-MM-DD): 2025-01-15
Importo: 25.50
Nome della categoria: Alimentari
Descrizione (facoltativa): Pranzo al ristorante
> Spesa inserita correttamente.
```

### Definire un budget
```
3. Definisci Budget Mensile
Mese (YYYY-MM): 2025-01
Nome della categoria: Alimentari
Importo del budget: 300
> Budget mensile salvato correttamente.
```

### Visualizzare report
```
4. Visualizza Report
1. Totale spese per categoria
2. Spese mensili vs budget
3. Elenco completo delle spese ordinate per data
4. Ritorna al menu principale
Inserisci la tua scelta: 2

Mese: 2025-01, Categoria: Alimentari, Budget: 300.00, Speso: 320.50, Stato: SUPERAMENTO BUDGET
```

## Gestione Errori

Il programma gestisce e segnala chiaramente:
- Scelte menu non valide
- Categorie duplicate
- Importi negativi o zero
- Categorie inesistenti
- Formati data/mese non validi
- Errori di integrità database (foreign key, check constraints)

## Licenza

Progetto didattico - Libero utilizzo a scopo educativo.