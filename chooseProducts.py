import tkinter as tk
from tkinter import ttk
from db import Database
import mainScript

db = Database("store.db")

class ChooseProducts:
    def __init__(self, numberOfProducts, hide, onlyOne, email):
        def openScript(hide, email, products, images):
            root.destroy()
            mainScript.MainScript(hide, email, products, images)
        root = tk.Tk()

        frame = tk.Frame(root)
        frame.grid(row=0, column=0)

        l =[]
        for i in db.fetch("product", "productName"):
            l.append(i[0])
        l.sort()
        i=1
        combos=[]
        entries=[]
        if onlyOne == 0:
            while(i<=numberOfProducts):
                count = "Produkt "+str(i)+": "
                tk.Label(frame, text=count).grid(row=i, column=0)
                combo = ttk.Combobox(frame, state="readonly", value=l)
                combo.grid(row=i, column=1)
                combos.append(combo)
                image = tk.Entry(frame)
                image.grid(row=i,column=3)
                entries.append(image)
                i+=1
        else:
            ttk.Label(frame, text="Produkt: ").grid(row=0, column=0)
            combo1 = ttk.Combobox(frame, state="readonly", value=l)
            combo1.grid(row=0, column=1)
            while i <= numberOfProducts:
                count = "Produkt " + str(i) + ": "
                tk.Label(frame, text=count).grid(row=i, column=0)
                image = tk.Entry(frame)
                image.grid(row=i, column=3)
                entries.append(image)
                i += 1


        def productsGet():
            products=[]
            if onlyOne == 0:
                for combo in combos:
                    products.append(combo.get())
            else:
                j = 0
                while j < numberOfProducts:
                    products.append(combo1.get())
                    j += 1
            return products

        def imagesGet():
            images=[]
            for entry in entries:
                images.append(list(entry.get().split(",")))
            return images

        button = tk.Button(frame, text="Uruchom", command=lambda: openScript(hide, email, productsGet(), imagesGet()))
        button.grid(row=numberOfProducts+1, column=1)

        root.mainloop()