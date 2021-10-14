import tkinter as tk
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

        email = tk.Entry(frame, textvariable=tk.StringVar())
        email.grid(row=0, column=1)

        tk.Label(frame, text="Cena: ").grid(row=1, column=0)

        password = tk.Entry(frame, textvariable=tk.StringVar())
        password.grid(row=1, column=1)

        tk.Label(frame, text="Opis: ").grid(row=2, column=0)

        password = tk.Entry(frame, textvariable=tk.StringVar())
        password.grid(row=2, column=1)

        button = tk.Button(frame, text="Dodaj", command=db.insert(email.get(), password.get()))
        button.grid(row=3, column=1)

        root.mainloop()