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

Tutti i campi usano tipi di dato standard SQL: `INTEGER`, `VARCHAR(n)`, `NUMERIC(precisione, scala)`, `DATE`, `TIMESTAMP`.

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

## Nota sui tipi temporali in SQLite

Lo schema usa solo tipi di dato standard SQL (`INTEGER`, `VARCHAR(n)`, `NUMERIC(p,s)`, `DATE`, `TIMESTAMP`). SQLite però gestisce i tipi in modo diverso dagli altri DBMS: applica la cosiddetta *type affinity*, cioè assegna a ogni colonna un'affinità e salva il valore in base alla sua forma, non in base al tipo dichiarato.

| Colonna dichiarata | Come viene salvato il valore | Esempio |
|---|---|---|
| `DATE` / `TIMESTAMP` | testo | `'2025-01-05'` |
| `NUMERIC(10,2)` | numero | `45.5` |

Questo comporta due differenze rispetto agli altri DBMS, entrambe già gestite nel programma:

1. SQLite non verifica che una data esista davvero nel calendario, quindi la validità è controllata su due livelli: il vincolo `CHECK (date(data) IS NOT NULL)` nello script SQL (la funzione `date()` restituisce NULL se la data non è valida) e il controllo con `datetime.strptime` in Python prima dell'inserimento.
2. Le date sono salvate come stringhe, ma nel formato `YYYY-MM-DD` l'ordine alfabetico coincide con quello cronologico. Di conseguenza `ORDER BY data` e il confronto `substr(data, 1, 7) = mese` usato nel report spese/budget danno risultati corretti.

Lo script SQL resta quindi portabile: anche su un DBMS con tipi temporali propri (PostgreSQL, MySQL) struttura e INSERT funzionano senza modifiche.

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