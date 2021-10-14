import tkinter as tk
from db import Database

db = Database("store.db")


class AddLocalization:
    def __init__(self):
        root = tk.Tk()
        canvas = tk.Canvas(root, height=75, width=150)
        canvas.pack()

        frame = tk.Frame(root)
        frame.place(relwidth=1, relheight=1)

        tk.Label(frame, text="Lokalizacja: ").grid(row=0, column=0)

        localization = tk.Entry(frame, textvariable=tk.StringVar())
        localization.grid(row=0, column=1)

        button = tk.Button(frame, text="Dodaj", command=lambda: self.insertLocalization(localization))
        button.grid(row=3, column=1)

        root.mainloop()

    def insertLocalization(self, localization):
        db.insertL(localization.get())