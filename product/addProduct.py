import tkinter as tk
from tkinter import ttk
from db import Database
from tkinter import filedialog

db = Database("store.db")

class AddProduct:
    def __init__(self):
        #DODAJ
        self.imageNames=[]
        def addImage(frame, button):
            i=4
            self.imageNames=filedialog.askopenfilenames(initialdir="/", title="Wybierz zdjęcia", filetypes=[("Obrazy",".bmp .tif .tiff .png .gif .jpg .jpeg .jfif .pjpeg .pjp")])
            for name in self.imageNames:
                button.grid(row=i+1, column=1)
                label = tk.Label(frame, text=name)
                label.grid(row=i, column=2)
                deleteButton = tk.Button(frame, text="Usuń")
                deleteButton.grid(row=i, column=3)
                i+=1

        def addProduct(product, title, price, desc, category):
            db.insertP(product, title, price, desc, category)
            p = db.getP(product)[0]
            for name in self.imageNames:
                db.insertI(name, p)

        root = tk.Tk()

        frame = tk.Frame(root, relief=tk.RIDGE, borderwidth=1)
        frame.grid(row=0, column=0)

        tk.Label(frame, text="Produkt: ").grid(row=0, column=0)
        product = tk.Entry(frame, textvariable=tk.StringVar())
        product.grid(row=0, column=1)

        tk.Label(frame, text="Tytuł: ").grid(row=1, column=0)
        title = tk.Entry(frame, textvariable=tk.StringVar())
        title.grid(row=1, column=1)

        tk.Label(frame, text="Cena: ").grid(row=2, column=0)
        price = tk.Entry(frame, textvariable=tk.IntVar())
        price.grid(row=2, column=1)

        tk.Label(frame, text="Opis: ").grid(row=3, column=0)
        desc = tk.Entry(frame, textvariable=tk.StringVar())
        desc.grid(row=3, column=1)

        tk.Label(frame, text="Kategoria: ").grid(row=4, column=0)

        l =[]
        for i in db.fetchC():
            l.append(i[0])

        combo = ttk.Combobox(frame, state="readonly", value=l)
        combo.grid(row=4, column=1)

        tk.Label(frame, text="Zdjęcia: ").grid(row=5, column=0)
        images = tk.Button(frame, text="Wybierz", command=lambda: addImage(frame, button))
        images.grid(row=5, column=1)

        button = tk.Button(frame, text="Dodaj", command=lambda: addProduct(product.get(), title.get(), price.get(), desc.get(), db.getC(combo.get())))
        button.grid(row=6, column=1)

        #EDYTUJ
        frame1 = tk.Frame(root, relief=tk.RIDGE, borderwidth=1)
        frame1.grid(row=0, column=1)

        tk.Label(frame1, text="Produkt: ").grid(row=0, column=0)

        l = []
        for i in db.fetchP():
            l.append(i[0])

        combo = ttk.Combobox(frame1, state="readonly", value=l)
        combo.grid(row=0, column=1)

        button = tk.Button(frame1, text="Edytuj")
        button.grid(row=0, column=2)

        #USUŃ
        def updateCombo(combo):
            db.deleteP(combo.get())
            products=db.fetchP()
            combo.config(value=products[0])
            combo.set(products)

        frame = tk.Frame(root, relief=tk.RIDGE, borderwidth=1)
        frame.grid(row=1, column=0)

        tk.Label(frame, text="Produkt: ").grid(row=0, column=0)

        combo = ttk.Combobox(frame, state="readonly", value=db.fetchP())
        combo.grid(row=0, column=1)

        button = tk.Button(frame, text="Usuń", command=lambda: updateCombo(combo))
        button.grid(row=0, column=2)

        root.mainloop()