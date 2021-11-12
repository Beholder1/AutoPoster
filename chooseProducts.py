import tkinter as tk
from tkinter import ttk
from db import Database
import mainScript

db = Database("store.db")

class ChooseProducts:
    def __init__(self, numberOfProducts, hide, email):
        def openScript(hide, email, products):
            mainScript.MainScript(hide, email, products)
        root = tk.Tk()
        canvas = tk.Canvas(root, height=500, width=500)
        canvas.pack()

        frame = tk.Frame(root)
        frame.place(relwidth=1, relheight=1)

        l =[]
        for i in db.fetchP():
            l.append(i[0])

        i=1
        combos=[]
        while(i<=numberOfProducts):
            count = "Produkt "+str(i)+": "
            tk.Label(frame, text=count).grid(row=i-1, column=0)
            combo = ttk.Combobox(frame, state="readonly", value=l)
            combo.grid(row=i-1, column=1)
            combos.append(combo)
            i+=1

        products=[]
        for combo in combos:
            products.append(combo.get())

        button = tk.Button(frame, text="Uruchom", command=lambda: openScript(hide, email, products))
        button.grid(row=numberOfProducts, column=1)

        root.mainloop()