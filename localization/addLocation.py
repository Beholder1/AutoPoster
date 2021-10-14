import tkinter as tk
from db import Database

db = Database("store.db")


class AddLocation:
    def __init__(self):
        root = tk.Tk()
        canvas = tk.Canvas(root, height=25, width=250)
        canvas.pack()

        frame = tk.Frame(root)
        frame.place(relwidth=1, relheight=1)

        tk.Label(frame, text="Lokalizacja: ").grid(row=0, column=0)

        location = tk.Entry(frame, textvariable=tk.StringVar())
        location.grid(row=0, column=1)

        button = tk.Button(frame, text="Dodaj", command=lambda: self.insertLocalization(location))
        button.grid(row=0, column=2)

        root.mainloop()

    def insertLocalization(self, location):
        db.insertL(location.get())