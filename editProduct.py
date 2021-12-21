import tkinter as tk
from tkinter import ttk
from db import Database

db = Database("store.db")


class EditProduct:
    def __init__(self, product):
        root = tk.Tk()
        self.product = product

        def updateProduct():
            db.update("product", "productName", entry1.get(), "productName", self.product)
            self.product = entry1.get()

        frame1 = tk.Frame(root, relief=tk.RIDGE, borderwidth=1)
        frame1.grid(row=0, column=1)

        tk.Label(frame1, text="Nazwa: ").grid(row=0, column=0)
        entry1 = ttk.Entry(frame1)
        entry1.grid(row=0, column=1)
        button = tk.Button(frame1, text="Edytuj", command=lambda: updateProduct())
        button.grid(row=0, column=2)

        tk.Label(frame1, text="Tytuł: ").grid(row=1, column=0)
        entry2 = ttk.Entry(frame1)
        entry2.grid(row=1, column=1)
        button = tk.Button(frame1, text="Edytuj",
                           command=lambda: db.update("product", "title", entry2.get(), "productName", self.product))
        button.grid(row=1, column=2)

        tk.Label(frame1, text="Cena: ").grid(row=2, column=0)
        entry3 = ttk.Entry(frame1)
        entry3.grid(row=2, column=1)
        button = tk.Button(frame1, text="Edytuj",
                           command=lambda: db.update("product", "price", entry3.get(), "productName", self.product))
        button.grid(row=2, column=2)

        tk.Label(frame1, text="Opis: ").grid(row=3, column=0)
        entry4 = ttk.Entry(frame1)
        entry4.grid(row=3, column=1)
        button = tk.Button(frame1, text="Edytuj",
                           command=lambda: db.update("product", "description", entry4.get(), "productName",
                                                     self.product))
        button.grid(row=3, column=2)

        # tk.Label(frame1, text="Kategoria: ").grid(row=2, column=0)
        # entry3 = ttk.Entry(frame1)
        # entry3.grid(row=2, column=1)
        # button = tk.Button(frame1, text="Edytuj", command=lambda: db.update("product", "category", entry1.get(), "productName", product))
        # button.grid(row=2, column=2)

        root.mainloop()
