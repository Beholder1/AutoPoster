import tkinter as tk
from tkinter import ttk
from db import Database
import mainScript

db = Database("store.db")

class ChooseProducts:
    def __init__(self, numberOfProducts, hide, email):
        def openScript(hide, email, products):
            root.destroy()
            mainScript.MainScript(hide, email, products)
        root = tk.Tk()

        frame = tk.Frame(root)
        frame.grid(row=0, column=0)

        l =[]
        for i in db.fetch("product", "productName"):
            l.append(i[0])
        l.sort()
        i=1
        combos=[]
        while(i<=numberOfProducts):
            count = "Produkt "+str(i)+": "
            tk.Label(frame, text=count).grid(row=i-1, column=0)
            combo = ttk.Combobox(frame, state="readonly", value=l)
            combo.grid(row=i-1, column=1)
            combos.append(combo)
            i+=1
        def productsGet():
            products=[]
            for combo in combos:
                products.append(combo.get())
            return products

        button = tk.Button(frame, text="Uruchom", command=lambda: openScript(hide, email, productsGet()))
        button.grid(row=numberOfProducts, column=1)

        root.mainloop()