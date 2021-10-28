import tkinter as tk
from tkinter import ttk
from db import Database

db = Database("store.db")

class AddProduct:
    def __init__(self):
        root = tk.Tk()
        canvas = tk.Canvas(root, height=700, width=700)
        canvas.pack()

        frame = tk.Frame(root)
        frame.place(relwidth=1, relheight=1)

        tk.Label(frame, text="Tytuł: ").grid(row=0, column=0)

        title = tk.Entry(frame, textvariable=tk.StringVar())
        title.grid(row=0, column=1)

        tk.Label(frame, text="Cena: ").grid(row=1, column=0)

        price = tk.Entry(frame, textvariable=tk.StringVar())
        price.grid(row=1, column=1)

        tk.Label(frame, text="Opis: ").grid(row=2, column=0)

        desc = tk.Entry(frame, textvariable=tk.StringVar())
        desc.grid(row=2, column=1)

        tk.Label(frame, text="Kategoria: ").grid(row=3, column=0)

        l =[]
        for i in db.fetchC():
            l.append(i[0])

        combo = ttk.Combobox(frame, state="readonly", value=l)
        combo.grid(row=3, column=1)

        button = tk.Button(frame, text="Dodaj", command=lambda: db.insertP(title.get(), price.get(), desc.get(), db.getC(combo.get())))
        button.grid(row=4, column=1)
        #
        root.mainloop()