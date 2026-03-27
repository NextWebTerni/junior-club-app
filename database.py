import sqlite3

def crea_connessione():
    conn = sqlite3.connect('dati_circolo.db')
    return conn

def crea_tabelle():
    conn = crea_connessione()
    cursor = conn.cursor()

    # 🧨 DISTRUGGIAMO IL VECCHIO ARMADIO
    cursor.execute('DROP TABLE IF EXISTS soci')
    cursor.execute('DROP TABLE IF EXISTS ricevute')

    # 🛠️ CREIAMO QUELLO NUOVO SU MISURA PER TE
    cursor.execute('''
        CREATE TABLE soci (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_atleta TEXT NOT NULL,
            luogo_data_nascita TEXT,
            indirizzo TEXT,
            nome_genitore TEXT,
            codice_fiscale_genitore TEXT,
            email TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE ricevute (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            socio_id INTEGER,
            data TEXT NOT NULL,
            importo REAL NOT NULL,
            metodo_pagamento TEXT NOT NULL,
            causale TEXT NOT NULL,
            FOREIGN KEY(socio_id) REFERENCES soci(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Database raso al suolo e ricostruito con successo, capo!")

if __name__ == '__main__':
    crea_tabelle()