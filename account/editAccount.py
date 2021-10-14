import tkinter as tk
from tkinter import ttk
from db import Database

db = Database("store.db")

class EditAccount:
    def __init__(self):
        root = tk.Tk()
        canvas = tk.Canvas(root, height=25, width=225)
        canvas.pack()

        frame = tk.Frame(root)
        frame.place(relwidth=1, relheight=1)

        tk.Label(frame, text="Email: ").grid(row=0, column=0)

        combo = ttk.Combobox(frame, state="readonly", value=db.fetchEmails())
        combo.grid(row=0, column=1)

        button = tk.Button(frame, text="Edytuj")
        button.grid(row=0, column=2)

        root.mainloop()
