import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS absensi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT NOT NULL,
        tanggal TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        keterangan TEXT NOT NULL
    )
''')
connection.commit()
connection.close()
print("Database Berhasil Dibuat!")
