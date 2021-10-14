import tkinter as tk
from db import Database
import newAccount

class Settings:
    def __init__(self):
        db = Database("store.db")

        root = tk.Tk()
        root.title("Ustawienia")
        canvas = tk.Canvas(root, height=700, width=700)
        canvas.pack()

        options = [
            "p",
            "o"
        ]
        clicked = tk.StringVar(root)
        clicked.set("Wybierz konto...")

        frame = tk.Frame(root)
        frame.place(relwidth=1, relheight=1)

        email = tk.Label(frame, text="E-mail: ")
        email.grid(row=0, column=0)

        drop = tk.OptionMenu(frame, clicked, *options)
        drop.grid(row=0, column=1)

        saveButton1 = tk.Button(frame, text = "Dodaj...", command = openNewAccount)
        saveButton1.grid(row=0, column=2)

        root.mainloop()

def openNewAccount():
    newAccount.NewAccount()