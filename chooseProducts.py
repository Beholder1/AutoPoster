import tkinter as tk
from tkinter import ttk
import mainScript


class ChooseProducts:
    def __init__(self, db, numberOfProducts, hide, onlyOne, email):
        self.db = db


        def openScript(hide, email, products, images):
            root.destroy()
            mainScript.MainScript(self.db, hide, email, products, images)

        def on_select(event):
            numberOfImages['text'] = "Liczba zdjęć: " + str(self.db.countI(combo1.get()))

        root = tk.Tk()

        frame = tk.Frame(root, background='#FCFCFF')
        frame.grid(row=0, column=0)
        style = ttk.Style()
        style.configure('TLabel', background="white", foreground="black", font=('Verdana', 12))

        l = []
        for i in self.db.fetch("product", "productName"):
            l.append(i[0])
        l.sort()
        i = 1
        combos = []
        entries = []
        if onlyOne == 0:
            while i <= numberOfProducts:
                count = "Produkt " + str(i) + ": "
                ttk.Label(frame, text=count).grid(row=i, column=0)
                combo = ttk.Combobox(frame, state="readonly", value=l)
                combo.grid(row=i, column=1)
                combos.append(combo)
                image = tk.Entry(frame)
                image.grid(row=i, column=3)
                entries.append(image)
                i += 1
        else:
            ttk.Label(frame, text="Produkt: ").grid(row=0, column=0)
            numberOfImages = ttk.Label(frame)
            numberOfImages.grid(row=0, column=2)
            combo1 = ttk.Combobox(frame, state="readonly", value=l)
            combo1.grid(row=0, column=1)
            combo1.bind('<<ComboboxSelected>>', on_select)

            while i <= numberOfProducts:
                count = "Produkt " + str(i) + ": "
                ttk.Label(frame, text=count).grid(row=i, column=0)
                image = tk.Entry(frame)
                image.grid(row=i, column=2)
                entries.append(image)
                i += 1

        def productsGet():
            products = []
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
            images = []
            for entry in entries:
                images.append(list(entry.get().split(",")))
            return images

        button = tk.Button(frame, text="Uruchom", command=lambda: openScript(hide, email, productsGet(), imagesGet()))
        button.grid(row=numberOfProducts + 1, column=1)

        root.mainloop()
