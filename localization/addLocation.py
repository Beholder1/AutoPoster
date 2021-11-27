import tkinter as tk
from tkinter import ttk
from db import Database

db = Database("store.db")


class AddLocation:
    def __init__(self):
        root = tk.Tk()

        #DODAJ
        frame = tk.Frame(root, relief=tk.RIDGE, borderwidth=1)
        frame.grid(row=0, column=0)

        tk.Label(frame, text="Lokalizacja: ").grid(row=0, column=0)

        location = tk.Entry(frame, textvariable=tk.StringVar())
        location.grid(row=0, column=1)

        button = tk.Button(frame, text="Dodaj", command=lambda: self.insertLocalization(location))
        button.grid(row=0, column=2)

        #EDYTUJ
        frame1 = tk.Frame(root, relief=tk.RIDGE, borderwidth=1)
        frame1.grid(row=0, column=1)

        tk.Label(frame1, text="Lokalizacja: ").grid(row=0, column=0)

        combo = ttk.Combobox(frame1, state="readonly", value=db.fetchL())
        combo.grid(row=0, column=1)

        button = tk.Button(frame1, text="Edytuj")
        button.grid(row=0, column=2)

        #USUŃ
        def updateCombo(combo):
            db.deleteL(combo.get())
            locations=db.fetchL()
            combo.config(value=locations[0])
            combo.set(locations)

        frame2 = tk.Frame(root, relief=tk.RIDGE, borderwidth=1)
        frame2.grid(row=1, column=0)

        tk.Label(frame2, text="Lokalizacja: ").grid(row=0, column=0)

        combo = ttk.Combobox(frame2, state="readonly", value=db.fetchL())
        combo.grid(row=0, column=1)

        button = tk.Button(frame2, text="Usuń", command=lambda: updateCombo(combo))
        button.grid(row=0, column=2)

        root.mainloop()

    def insertLocalization(self, location):
        db.insertL(location.get())