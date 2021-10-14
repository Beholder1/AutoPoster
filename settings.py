import tkinter as tk
from tkinter import ttk
from db import Database
from account import addAccount


class Settings:
    def __init__(self):
        db = Database("store.db")

        root = tk.Tk()
        root.title("Ustawienia")
        canvas = tk.Canvas(root, height=700, width=700)
        canvas.pack()


        frame = tk.Frame(root)
        frame.place(relwidth=1, relheight=1)

        email = tk.Label(frame, text="E-mail: ")
        email.grid(row=0, column=0)

        combo = ttk.Combobox(frame, state="readonly", value=db.fetchEmails())
        combo.grid(row=0, column=1)

        saveButton1 = tk.Button(frame, text = "Dodaj...", command = openNewAccount)
        saveButton1.grid(row=0, column=2)

        root.mainloop()

def openNewAccount():
    addAccount.NewAccount()