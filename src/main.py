#!/usr/bin/env python3
"""
Progetto Spese Personali e Budget - Console CLI
"""

import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Per corsi relativi ai file SQL e DB
DB_PATH = Path(__file__).parent.parent / "sql" / "spese.db"
SQL_SCRIPT_PATH = Path(__file__).parent.parent / "sql" / "database.sql"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_database():
    """Inizializza il DB eseguendo lo script SQL se non esiste."""
    if not SQL_SCRIPT_PATH.exists():
        print(f"Errore: File SQL non trovato in {SQL_SCRIPT_PATH}")
        sys.exit(1)

    with open(SQL_SCRIPT_PATH, "r", encoding="utf-8") as f:
        sql_script = f.read()

    conn = get_db_connection()
    try:
        conn.executescript(sql_script)
        conn.commit()
        print("Database inizializzato con successo.")
    except sqlite3.Error as e:
        print(f"Errore nell'inizializzazione del database: {e}")
        sys.exit(1)
    finally:
        conn.close()


def gestione_categorie():
    print("\n--- GESTIONE CATEGORIE ---")
    nome = input("Inserisci il nome della categoria: ").strip()

    if not nome:
        print("Errore: il nome della categoria non può essere vuoto.")
        return

    conn = get_db_connection()
    try:
        cursor = conn.execute(
            "SELECT id_categoria FROM categorie WHERE nome = ?", (nome,)
        )
        if cursor.fetchone():
            print("La categoria esiste già.")
            return

        conn.execute("INSERT INTO categorie (nome) VALUES (?)", (nome,))
        conn.commit()
        print("Categoria inserita correttamente.")

    except sqlite3.IntegrityError:
        print("La categoria esiste già.")
    except sqlite3.Error as e:
        print(f"Errore database: {e}")
    finally:
        conn.close()


def inserisci_spesa():
    print("\n--- INSERIMENTO SPESE ---")

    data = input("Data (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(data, "%Y-%m-%d")
    except ValueError:
        print("Errore: formato data non valido. Usa YYYY-MM-DD.")
        return

    importo_str = input("Importo: ").strip()
    try:
        importo = float(importo_str)
        if importo <= 0:
            print("Errore: l'importo deve essere maggiore di zero.")
            return
    except ValueError:
        print("Errore: l'importo deve essere un numero valido.")
        return

    nome_categoria = input("Nome della categoria: ").strip()
    if not nome_categoria:
        print("Errore: il nome della categoria non può essere vuoto.")
        return

    descrizione = input("Descrizione (facoltativa): ").strip() or None

    conn = get_db_connection()
    try:
        cursor = conn.execute(
            "SELECT id_categoria FROM categorie WHERE nome = ?", (nome_categoria,)
        )
        categoria = cursor.fetchone()

        if not categoria:
            print("Errore: la categoria non esiste.")
            return

        conn.execute(
            "INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES (?, ?, ?, ?)",
            (data, importo, categoria["id_categoria"], descrizione),
        )
        conn.commit()
        print("Spesa inserita correttamente.")

    except sqlite3.IntegrityError as e:
        if "CHECK constraint failed" in str(e) and "importo" in str(e):
            print("Errore: l'importo deve essere maggiore di zero.")
        else:
            print(f"Errore database: {e}")
    except sqlite3.Error as e:
        print(f"Errore database: {e}")
    finally:
        conn.close()


def definisci_budget():
    print("\n--- DEFINIZIONE BUDGET MENSILE ---")

    mese = input("Mese (YYYY-MM): ").strip()
    try:
        datetime.strptime(mese, "%Y-%m")
    except ValueError:
        print("Errore: formato mese non valido. Usa YYYY-MM.")
        return

    nome_categoria = input("Nome della categoria: ").strip()
    if not nome_categoria:
        print("Errore: il nome della categoria non può essere vuoto.")
        return

    budget_str = input("Importo del budget: ").strip()
    try:
        budget = float(budget_str)
        if budget <= 0:
            print("Errore: il budget deve essere maggiore di zero.")
            return
    except ValueError:
        print("Errore: il budget deve essere un numero valido.")
        return

    conn = get_db_connection()
    try:
        cursor = conn.execute(
            "SELECT id_categoria FROM categorie WHERE nome = ?", (nome_categoria,)
        )
        categoria = cursor.fetchone()

        if not categoria:
            print("Errore: la categoria non esiste.")
            return

        # Aggiorna se esiste già il budget per quella categoria nel mese (UPSERT)
        conn.execute(
            """
            INSERT INTO budget_mensili (mese, id_categoria, importo_budget)
            VALUES (?, ?, ?)
            ON CONFLICT(mese, id_categoria) DO UPDATE SET
                importo_budget = excluded.importo_budget,
                data_creazione = datetime('now')
            """,
            (mese, categoria["id_categoria"], budget),
        )
        conn.commit()
        print("Budget mensile salvato correttamente.")

    except sqlite3.IntegrityError as e:
        if "CHECK constraint failed" in str(e) and "importo_budget" in str(e):
            print("Errore: il budget deve essere maggiore di zero.")
        else:
            print(f"Errore database: {e}")
    except sqlite3.Error as e:
        print(f"Errore database: {e}")
    finally:
        conn.close()


def report_totale_per_categoria():
    print("\n--- REPORT: TOTALE SPESE PER CATEGORIA ---")
    print(f"{'Categoria':.<20} {'Totale Speso':>12}")
    print("-" * 35)

    conn = get_db_connection()
    try:
        cursor = conn.execute("""
            SELECT c.nome AS Categoria, COALESCE(SUM(s.importo), 0) AS Totale_Speso
            FROM categorie c
            LEFT JOIN spese s ON c.id_categoria = s.id_categoria
            GROUP BY c.id_categoria, c.nome
            ORDER BY Totale_Speso DESC
        """)

        rows = cursor.fetchall()
        if not rows:
            print("Nessuna categoria trovata.")
            return

        for row in rows:
            print(f"{row['Categoria']:<20} {row['Totale_Speso']:>12.2f}")

    except sqlite3.Error as e:
        print(f"Errore database: {e}")
    finally:
        conn.close()


def report_spese_vs_budget():
    print("\n--- REPORT: SPESE MENSILI VS BUDGET ---")

    conn = get_db_connection()
    try:
        cursor = conn.execute("""
            SELECT b.mese AS Mese, c.nome AS Categoria, b.importo_budget AS Budget,
                   COALESCE(SUM(s.importo), 0) AS Speso
            FROM budget_mensili b
            JOIN categorie c ON b.id_categoria = c.id_categoria
            LEFT JOIN spese s ON s.id_categoria = b.id_categoria 
                AND substr(s.data, 1, 7) = b.mese
            GROUP BY b.mese, b.id_categoria, c.nome, b.importo_budget
            ORDER BY b.mese, c.nome
        """)

        rows = cursor.fetchall()
        if not rows:
            print("Nessun budget definito.")
            return

        for row in rows:
            mese = row["Mese"]
            categoria = row["Categoria"]
            budget = row["Budget"]
            speso = row["Speso"]

            if speso > budget:
                stato = "SUPERAMENTO BUDGET"
            elif speso == budget:
                stato = "BUDGET ESAURITO"
            else:
                stato = "NEI LIMITI"

            print(
                f"Mese: {mese}, Categoria: {categoria}, Budget: {budget:.2f}, Speso: {speso:.2f}, Stato: {stato}"
            )

    except sqlite3.Error as e:
        print(f"Errore database: {e}")
    finally:
        conn.close()


def report_elenco_spese():
    print("\n--- REPORT: ELENCO COMPLETO SPESE ---")
    print("Data Categoria Importo Descrizione")
    print("-" * 60)

    conn = get_db_connection()
    try:
        cursor = conn.execute("""
            SELECT s.data AS Data, c.nome AS Categoria, s.importo AS Importo, s.descrizione AS Descrizione
            FROM spese s
            JOIN categorie c ON s.id_categoria = c.id_categoria
            ORDER BY s.data, s.id_spesa
        """)

        rows = cursor.fetchall()
        if not rows:
            print("Nessuna spesa registrata.")
            return

        for row in rows:
            descrizione = row["Descrizione"] or ""
            print(f"{row['Data']} {row['Categoria']} {row['Importo']:.2f} {descrizione}")

    except sqlite3.Error as e:
        print(f"Errore database: {e}")
    finally:
        conn.close()


def menu_report():
    while True:
        print("\n--- MENU DEI REPORT ---")
        print("1. Totale spese per categoria")
        print("2. Spese mensili vs budget")
        print("3. Elenco completo delle spese ordinate per data")
        print("4. Ritorna al menu principale")

        scelta = input("Inserisci la tua scelta: ").strip()

        match scelta:
            case "1":
                report_totale_per_categoria()
            case "2":
                report_spese_vs_budget()
            case "3":
                report_elenco_spese()
            case "4":
                break
            case _:
                print("Scelta non valida. Riprovare.")


def main():
    if not DB_PATH.exists():
        init_database()

    print("\n-------------------------")
    print("SISTEMA SPESE PERSONALI")
    print("-------------------------")

    while True:
        print("\n--- MENU PRINCIPALE ---")
        print("1. Gestione Categorie")
        print("2. Inserisci Spesa")
        print("3. Definisci Budget Mensile")
        print("4. Visualizza Report")
        print("5. Esci")

        scelta = input("Inserisci la tua scelta: ").strip()

        match scelta:
            case "1":
                gestione_categorie()
            case "2":
                inserisci_spesa()
            case "3":
                definisci_budget()
            case "4":
                menu_report()
            case "5":
                print("\nArrivederci!")
                break
            case _:
                print("Scelta non valida. Riprovare.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgramma interrotto dall'utente.")
        sys.exit(0)
    except Exception as e:
        print(f"\nErrore imprevisto: {e}")
        sys.exit(1)