import tkinter as tk
from tkinter import ttk


class EditAccount:
    def __init__(self, account, db):
        self.db = db
        root = tk.Toplevel()
        self.account = account

        def update_account():
            self.db.update("parts", "name", entry1.get(), "name", self.account)
            self.account = entry1.get()

        frame1 = tk.Frame(root, relief=tk.RIDGE, borderwidth=1)
        frame1.grid(row=0, column=1)

        tk.Label(frame1, text="Nazwa: ").grid(row=0, column=0)
        entry1 = ttk.Entry(frame1)
        entry1.grid(row=0, column=1)
        button = tk.Button(frame1, text="Edytuj", command=lambda: update_account())
        button.grid(row=0, column=2)

        tk.Label(frame1, text="Email: ").grid(row=1, column=0)
        entry2 = ttk.Entry(frame1)
        entry2.grid(row=1, column=1)
        button = tk.Button(frame1, text="Edytuj",
                           command=lambda: db.update("parts", "email", entry2.get(), "name", self.account))
        button.grid(row=1, column=2)

        tk.Label(frame1, text="Hasło: ").grid(row=2, column=0)
        entry3 = ttk.Entry(frame1)
        entry3.grid(row=2, column=1)
        button = tk.Button(frame1, text="Edytuj",
                           command=lambda: db.update("parts", "password", entry3.get(), "name", self.account))
        button.grid(row=2, column=2)
