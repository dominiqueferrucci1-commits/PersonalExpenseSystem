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

### Tabella `categorie`
| Campo | Tipo | Vincoli |
|-------|------|---------|
| id_categoria | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| nome | TEXT | NOT NULL, UNIQUE, CHECK (non vuoto) |
| data_creazione | TEXT | NOT NULL, DEFAULT date('now') |

### Tabella `spese`
| Campo | Tipo | Vincoli |
|-------|------|---------|
| id_spesa | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| data | TEXT | NOT NULL, CHECK (formato data valido) |
| importo | REAL | NOT NULL, CHECK (> 0) |
| id_categoria | INTEGER | NOT NULL, FOREIGN KEY → categorie.id_categoria |
| descrizione | TEXT | NULLABLE |
| data_inserimento | TEXT | NOT NULL, DEFAULT datetime('now') |

### Tabella `budget_mensili`
| Campo | Tipo | Vincoli |
|-------|------|---------|
| id_budget | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| mese | TEXT | NOT NULL, CHECK (formato YYYY-MM valido) |
| id_categoria | INTEGER | NOT NULL, FOREIGN KEY → categorie.id_categoria |
| importo_budget | REAL | NOT NULL, CHECK (> 0) |
| data_creazione | TEXT | NOT NULL, DEFAULT datetime('now') |
| UNIQUE(mese, id_categoria) | | Un solo budget per categoria al mese |

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