import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS parts (id INTEGER PRIMARY KEY, email text, password text)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS product (id INTEGER PRIMARY KEY, productName text, title text, price INTEGER, description text, category INTEGER, FOREIGN KEY(category) REFERENCES categories(id))")
        self.cur.execute("CREATE TABLE IF NOT EXISTS localizations (id INTEGER PRIMARY KEY, localization text)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS photos (id INTEGER PRIMARY KEY, path text, product INTEGER, FOREIGN KEY(product) REFERENCES products(id))")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM parts")
        rows = self.cur.fetchall()
        return rows

    def fetchEmails(self):
        self.cur.execute("SELECT email FROM parts")
        emails = self.cur.fetchall()
        return emails

    def getA(self, email):
        self.cur.execute("SELECT password FROM parts WHERE email = ?", (email,))
        data = self.cur.fetchone()
        return data[0]

    def insert(self, email, password):
        self.cur.execute("INSERT INTO parts VALUES (NULL, ?, ?)", (email, password))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM parts WHERE id = ?", (id,))
        self.conn.commit()

    def deleteA(self, email):
        self.cur.execute("DELETE FROM parts WHERE email = ?", (email,))
        self.conn.commit()

    def update(self, id, email, password):
        self.cur.execute("UPDATE parts SET email = ?, password = ? WHERE id = ?", (email, password, id))
        self.conn.commit()

    def insertL(self, localization):
        self.cur.execute("INSERT INTO localizations VALUES (NULL, ?)", (localization,))
        self.conn.commit()

    def getL(self, id):
        self.cur.execute("SELECT localization FROM localizations WHERE id = ?", (id,))
        data = self.cur.fetchone()
        return data[0]

    def fetchL(self):
        self.cur.execute("SELECT localization FROM localizations")
        emails = self.cur.fetchall()
        return emails

    def getNumberL(self):
        self.cur.execute("SELECT COUNT(*) FROM localizations")
        data = self.cur.fetchone()
        return data[0]

    def deleteL(self, localization):
        self.cur.execute("DELETE FROM localizations WHERE localization = ?", (localization,))
        self.conn.commit()

    def insertP(self, productName, title, price, description, category):
        self.cur.execute("INSERT INTO product VALUES (NULL, ?, ?, ?, ?, ?)", (productName, title, price, description, category))
        self.conn.commit()

    def fetchP(self):
        self.cur.execute("SELECT productName FROM product")
        emails = self.cur.fetchall()
        return emails

    def getP(self, productName):
        self.cur.execute("SELECT * FROM product WHERE productName = ?", (productName,))
        data = self.cur.fetchone()
        return data

    def deleteP(self, productName):
        self.cur.execute("DELETE FROM product WHERE productName = ?", (productName,))
        self.conn.commit()

    def fetchC(self):
        self.cur.execute("SELECT category FROM categories")
        categories = self.cur.fetchall()
        return categories

    def getC(self, category):
        self.cur.execute("SELECT id FROM categories WHERE category = ?", (category,))
        id = self.cur.fetchall()
        return id[0][0]

    def __del__(self):
        self.conn.close()

db = Database('store.db')

