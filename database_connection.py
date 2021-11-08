import sqlite3


def init_database():
    conn = sqlite3.connect('rezepte.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS rezepte "
                   "(Rezept_ID INTEGER NOT NULL PRIMARY KEY, "
                   "Rezept_Name text, Rezept_Beschreibung text, Rezept_Bild text)")
    cursor.execute("CREATE TABLE IF NOT EXISTS zutaten "
                   "(Zutat_ID INTEGER NOT NULL PRIMARY KEY, "
                   "Zutat_Name text, Zutat_Menge real, Zutat_Einheit text, Rezept_ID int)")
    conn.commit()
    conn.close()


def write_to_database(query_string, *args):
    conn = sqlite3.connect('rezepte.db')
    cursor = conn.cursor()
    if args:
        cursor.execute(query_string, tuple(args))
    else:
        cursor.execute(query_string)
    conn.commit()
    conn.close()


def read_from_database(query_string, *args):
    conn = sqlite3.connect('rezepte.db')
    cursor = conn.cursor()
    if args:
        cursor.execute(query_string, tuple(args))
    else:
        cursor.execute(query_string)
    query_result = cursor.fetchall()
    conn.close()
    return query_result
