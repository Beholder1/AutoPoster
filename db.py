import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS parts (id INTEGER PRIMARY KEY, email text, password text)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM parts")
        rows = self.cur.fetchall()
        return rows

    def insert(self, email, password):
        self.cur.execute("INSERT INTO parts VALUES (NULL, ?, ?)", (email, password))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM parts WHERE id = ?", (id))
        self.conn.commit()

    def update(self, id, email, password):
        self.cur.execute("UPDATE parts SET email = ?, password = ? WHERE id = ?", (email, password, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

db = Database('store.db')

