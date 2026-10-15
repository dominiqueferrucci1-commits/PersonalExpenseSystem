-- Schema e dati per il database Spese Personali (SQLite)

DROP TABLE IF EXISTS spese;
DROP TABLE IF EXISTS budget_mensili;
DROP TABLE IF EXISTS categorie;

-- Categorie spese
CREATE TABLE categorie (
    id_categoria     INTEGER PRIMARY KEY AUTOINCREMENT,
    nome             TEXT NOT NULL UNIQUE CHECK (length(trim(nome)) > 0),
    data_creazione   TEXT NOT NULL DEFAULT (date('now'))
);

-- Spese registrate
CREATE TABLE spese (
    id_spesa         INTEGER PRIMARY KEY AUTOINCREMENT,
    data             TEXT NOT NULL CHECK (date(data) IS NOT NULL),
    importo          REAL NOT NULL CHECK (importo > 0),
    id_categoria     INTEGER NOT NULL,
    descrizione      TEXT,
    data_inserimento TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (id_categoria) REFERENCES categorie(id_categoria) ON DELETE RESTRICT
);

-- Budget mensile per categoria
CREATE TABLE budget_mensili (
    id_budget        INTEGER PRIMARY KEY AUTOINCREMENT,
    mese             TEXT NOT NULL CHECK (substr(mese, 1, 4) BETWEEN '2000' AND '2100' AND substr(mese, 6, 2) BETWEEN '01' AND '12'),
    id_categoria     INTEGER NOT NULL,
    importo_budget   REAL NOT NULL CHECK (importo_budget > 0),
    data_creazione   TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (id_categoria) REFERENCES categorie(id_categoria) ON DELETE RESTRICT,
    UNIQUE (mese, id_categoria)
);

-- Indici per velocizzare le query di filtro e join
CREATE INDEX idx_spese_data ON spese(data);
CREATE INDEX idx_spese_categoria ON spese(id_categoria);
CREATE INDEX idx_budget_mese_categoria ON budget_mensili(mese, id_categoria);

-- Categorie base
INSERT INTO categorie (nome) VALUES ('Alimentari');
INSERT INTO categorie (nome) VALUES ('Trasporti');
INSERT INTO categorie (nome) VALUES ('Intrattenimento');
INSERT INTO categorie (nome) VALUES ('Salute');
INSERT INTO categorie (nome) VALUES ('Abbigliamento');
INSERT INTO categorie (nome) VALUES ('Utenze');
INSERT INTO categorie (nome) VALUES ('Altro');

-- Spese di test (Gennaio e Febbraio 2025)
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES ('2025-01-05', 45.50, 1, 'Spesa settimanale supermercato');
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES ('2025-01-08', 25.00, 1, 'Pranzo fuori');
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES ('2025-01-10', 60.00, 2, 'Abbonamento mensile bus');
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES ('2025-01-12', 35.00, 3, 'Cinema e cena');
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES ('2025-01-15', 120.00, 4, 'Visita specialistica');
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES ('2025-01-18', 89.90, 5, 'Scarpe nuove');
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES ('2025-01-20', 150.00, 6, 'Bolletta luce e gas');
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES ('2025-01-22', 15.00, 1, 'Colazione al bar');
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES ('2025-01-25', 42.00, 3, 'Videogioco');

INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES ('2025-02-03', 52.30, 1, 'Spesa settimanale');
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES ('2025-02-07', 30.00, 2, 'Taxi aeroporto');
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES ('2025-02-10', 200.00, 3, 'Concerto');
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES ('2025-02-14', 75.00, 1, 'Cena romantica');
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES ('2025-02-18', 95.00, 4, 'Farmaci');
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES ('2025-02-22', 180.00, 5, 'Giacca invernale');
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES ('2025-02-25', 130.00, 6, 'Bolletta internet e telefono');

-- Budget di test
INSERT INTO budget_mensili (mese, id_categoria, importo_budget) VALUES ('2025-01', 1, 300.00);
INSERT INTO budget_mensili (mese, id_categoria, importo_budget) VALUES ('2025-01', 2, 100.00);
INSERT INTO budget_mensili (mese, id_categoria, importo_budget) VALUES ('2025-01', 3, 150.00);
INSERT INTO budget_mensili (mese, id_categoria, importo_budget) VALUES ('2025-01', 4, 200.00);
INSERT INTO budget_mensili (mese, id_categoria, importo_budget) VALUES ('2025-01', 5, 100.00);
INSERT INTO budget_mensili (mese, id_categoria, importo_budget) VALUES ('2025-01', 6, 150.00);

INSERT INTO budget_mensili (mese, id_categoria, importo_budget) VALUES ('2025-02', 1, 350.00);
INSERT INTO budget_mensili (mese, id_categoria, importo_budget) VALUES ('2025-02', 2, 120.00);
INSERT INTO budget_mensili (mese, id_categoria, importo_budget) VALUES ('2025-02', 3, 200.00);
INSERT INTO budget_mensili (mese, id_categoria, importo_budget) VALUES ('2025-02', 4, 150.00);
INSERT INTO budget_mensili (mese, id_categoria, importo_budget) VALUES ('2025-02', 5, 200.00);
INSERT INTO budget_mensili (mese, id_categoria, importo_budget) VALUES ('2025-02', 6, 150.00);

-- Query di test vincoli (decommentare per verificare gli errori)
-- INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES ('2025-01-01', 10.00, 999, 'Test FK non valida');
-- INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES ('2025-01-01', -10.00, 1, 'Test importo negativo');
-- INSERT INTO categorie (nome) VALUES ('Alimentari');