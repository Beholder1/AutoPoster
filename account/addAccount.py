import tkinter as tk
from tkinter import ttk
from db import Database

db = Database("store.db")

class AddAccount:
    def __init__(self):
        root = tk.Tk()

        #DODAJ
        frame = tk.Frame(root, relief=tk.RIDGE, borderwidth=1)
        frame.grid(row=0, column=0)

        tk.Label(frame, text="E-mail: ").grid(row=0, column=0)

        email = tk.Entry(frame, textvariable=tk.StringVar())
        email.grid(row=0, column=1)

        tk.Label(frame, text="Hasło: ").grid(row=1, column=0)

        password = tk.Entry(frame, textvariable=tk.StringVar())
        password.grid(row=1, column=1)

        button = tk.Button(frame, text="Zapisz", command=lambda: db.insert(email.get(), password.get()))
        button.grid(row=3, column=1)

        #EDYTUJ
        frame1 = tk.Frame(root, relief=tk.RIDGE, borderwidth=1)
        frame1.grid(row=0, column=1)

        tk.Label(frame1, text="Email: ").grid(row=0, column=0)

        combo = ttk.Combobox(frame1, state="readonly", value=db.fetchEmails())
        combo.grid(row=0, column=1)

        button = tk.Button(frame1, text="Edytuj")
        button.grid(row=0, column=2)

        #USUŃ
        def updateCombo(combo):
            db.deleteA(combo.get())
            emails=db.fetchEmails()
            combo.config(value=emails[0])
            combo.set(emails)

        frame2 = tk.Frame(root, relief=tk.RIDGE, borderwidth=1)
        frame2.grid(row=1, column=0)

        tk.Label(frame2, text="Email: ").grid(row=0, column=0)

        combo = ttk.Combobox(frame2, state="readonly", value=db.fetchEmails())
        combo.grid(row=0, column=1)

        button = tk.Button(frame2, text="Usuń", command=lambda: updateCombo(combo))
        button.grid(row=0, column=2)

        root.mainloop()