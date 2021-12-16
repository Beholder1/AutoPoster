import tkinter as tk
from tkinter import ttk
from db import Database

db = Database("store.db")

class EditLocation:
    def __init__(self, location):
        root = tk.Tk()
        self.location=location
        def updateLocation():
            db.update("localizations", "localization", entry1.get(), "localization", self.location)
            self.location = entry1.get()

        frame1 = tk.Frame(root, relief=tk.RIDGE, borderwidth=1)
        frame1.grid(row=0, column=1)

        tk.Label(frame1, text="Nazwa: ").grid(row=0, column=0)
        entry1 = ttk.Entry(frame1)
        entry1.grid(row=0, column=1)
        button = tk.Button(frame1, text="Edytuj", command=lambda: updateLocation())
        button.grid(row=0, column=2)

        root.mainloop()