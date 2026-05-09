import os
import sqlite3
from contextlib import contextmanager


# import psycopg


class Database:
    def __init__(self, db):
        # hostname = ''
        # database = ''
        # username = ''
        # password = ''
        # port =
        #
        # self.conn = psycopg.connect(
        #     host=hostname,
        #     dbname=database,
        #     user=username,
        #     password=password,
        #     port=port)
        # self.cur = self.conn.cursor()

        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self._tx_depth = 0
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS parts (id INTEGER PRIMARY KEY, email text, password text, name text, profile text)")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS product (id INTEGER PRIMARY KEY, productName text, title text, price INTEGER, description text, category INTEGER, FOREIGN KEY(category) REFERENCES categories(id))")
        self.cur.execute("CREATE TABLE IF NOT EXISTS localizations (id INTEGER PRIMARY KEY, localization text)")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS photos (id INTEGER PRIMARY KEY, path text, product INTEGER, FOREIGN KEY(product) REFERENCES products(id))")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS categoriesForProducts (id INTEGER PRIMARY KEY, product INTEGER, category INTEGER, FOREIGN KEY(product) REFERENCES products(id), FOREIGN KEY(category) REFERENCES categories(id))")
        self.cur.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)")
        self._commit()

    def _commit(self):
        if self._tx_depth == 0:
            self.conn.commit()

    @contextmanager
    def transaction(self):
        """Group multiple writes into one atomic unit. Nesting is supported."""
        self._tx_depth += 1
        try:
            yield
        except BaseException:
            self._tx_depth = 0
            self.conn.rollback()
            raise
        else:
            self._tx_depth -= 1
            if self._tx_depth == 0:
                self.conn.commit()

    def get_or_create_profile(self, account, profiles_dir):
        profile = self.getA("profile", account)
        if profile and os.path.isdir(os.path.join(profiles_dir, profile)):
            return profile
        profile = account
        self.update("parts", "profile", profile, "name", account)
        return profile

    def get_setting(self, key, default=None):
        self.cur.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = self.cur.fetchone()
        return row[0] if row is not None else default

    def set_setting(self, key, value):
        self.cur.execute(
            "INSERT INTO settings (key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, str(value)),
        )
        self._commit()
        # k = self.fetch("product", "*")
        # for i in k:
        #     self.cur.execute("INSERT INTO categoriesForProducts VALUES (NULL, " + str(i[0]) + ", " + str(i[5]) + ")")
        #     self.conn.commit()
        # self.cur.execute("PRAGMA foreign_keys=off;")
        # self.cur.execute("BEGIN TRANSACTION;")
        # self.cur.execute("ALTER TABLE product RENAME TO sfdg;")
        # self.cur.execute("CREATE TABLE product (id INTEGER PRIMARY KEY, productName text, title text, price INTEGER, description text);")
        # self.cur.execute("INSERT INTO product SELECT id, productName, title, price, description FROM sfdg;")
        # self.cur.execute("COMMIT;")
        # self.cur.execute("PRAGMA foreign_keys=on;")
        # self.conn.commit()

    def fetch(self, table, column):
        self.cur.execute(f"SELECT {column} FROM {table}")
        data = self.cur.fetchall()
        return data

    def remove(self, table, column, criterion):
        self.cur.execute(f"DELETE FROM {table} WHERE {column} = ?", (criterion,))
        self._commit()

    def delete_categories_for_products_by_id(self, product_id, category_id):
        self.cur.execute("DELETE FROM categoriesForProducts WHERE product = ? AND category = ?",
                         (product_id, category_id,))
        self._commit()

    def delete_all_images_by_product(self, product):
        id = self.find_product_by_name(product)[0]
        self.cur.execute("DELETE FROM photos WHERE product = ?", (id,))
        self._commit()

    def delete_all_categories_for_products_by_product(self, product):
        id = self.find_product_by_name(product)[0]
        self.cur.execute("DELETE FROM categoriesForProducts WHERE product = ?", (id,))
        self._commit()

    def getA(self, column, name):
        self.cur.execute(f"SELECT {column} FROM parts WHERE name = ?", (name,))
        data = self.cur.fetchone()
        return data[0]

    def insert(self, email, password, name, profile):
        self.cur.execute("INSERT INTO parts VALUES (NULL, ?, ?, ?, ?)", (email, password, name, profile))
        self._commit()

    def update(self, table, column, new, criterion_column, old):
        self.cur.execute(f"UPDATE {table} SET {column} = ? WHERE {criterion_column} = ?", (new, old))
        self._commit()

    def update_category(self, new_category, product_id, category_id):
        self.cur.execute("UPDATE categoriesForProducts SET category = ? WHERE product = ? AND category = ?",
                         (new_category, product_id, category_id,))
        self._commit()

    def save_location(self, location):
        self.cur.execute("INSERT INTO localizations VALUES (NULL, ?)", (location,))
        self._commit()

    def find_location_by_id(self, id):
        self.cur.execute("SELECT localization FROM localizations WHERE id = ?", (id,))
        data = self.cur.fetchone()
        return data[0]

    def count_all_locations(self):
        self.cur.execute("SELECT COUNT(*) FROM localizations")
        data = self.cur.fetchone()
        return data[0]

    def save_product(self, product_name, title, price, description):
        self.cur.execute("INSERT INTO product VALUES (NULL, ?, ?, ?, ?)",
                         (product_name, title, price, description))
        self._commit()

    def find_product_by_name(self, product_name):
        self.cur.execute("SELECT * FROM product WHERE productName = ?", (product_name,))
        data = self.cur.fetchone()
        return data

    def find_all_product_categories_by_product_id(self, product_id):
        self.cur.execute("SELECT category FROM categoriesForProducts WHERE product = ?", (product_id,))
        data = self.cur.fetchall()
        return data

    def find_category(self, category):
        self.cur.execute("SELECT id FROM categories WHERE category = ?", (category,))
        id = self.cur.fetchall()
        return id[0][0]

    def save_categories_for_products(self, product, category):
        self.cur.execute("INSERT INTO categoriesForProducts VALUES (NULL, ?, ?)", (product, category,))
        self._commit()

    def save_image(self, path, product):
        self.cur.execute("INSERT INTO photos VALUES (NULL, ?, ?)", (path, product,))
        self._commit()

    def find_all_images_by_product(self, product):
        id = self.find_product_by_name(product)[0]
        self.cur.execute("SELECT path FROM photos WHERE product = ?", (id,))
        images = self.cur.fetchall()
        return images

    def count_all_images_by_product(self, product_name):
        product = self.find_product_by_name(product_name)
        self.cur.execute("SELECT COUNT(*) FROM photos WHERE product = ?", (product[0],))
        number_of_images = self.cur.fetchall()
        return number_of_images[0][0]

    def close(self):
        try:
            self.conn.close()
        except Exception:
            pass

    def __del__(self):
        self.close()
