import tkinter as tk
from db import Database

db = Database("store.db")

class AddAccount:
    def __init__(self):
        root = tk.Tk()
        canvas = tk.Canvas(root, height=75, width=175)
        canvas.pack()

        frame = tk.Frame(root)
        frame.place(relwidth=1, relheight=1)

        tk.Label(frame, text="E-mail: ").grid(row=0, column=0)

        email = tk.Entry(frame, textvariable=tk.StringVar())
        email.grid(row=0, column=1)

        tk.Label(frame, text="Hasło: ").grid(row=1, column=0)

        password = tk.Entry(frame, textvariable=tk.StringVar())
        password.grid(row=1, column=1)

        button = tk.Button(frame, text="Zapisz", command=lambda: db.insert(email.get(), password.get()))
        button.grid(row=3, column=1)

        root.mainloop()