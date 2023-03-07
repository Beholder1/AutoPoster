import tkinter as tk
from tkinter import ttk

import mainScript


class ChooseProducts:
    def __init__(self, db, numberOfProducts, hide, onlyOne, accounts, incognito):
        self.db = db
        activeColor = "#FDA50F"
        menuColor = '#FD6A02'

        def openScript(hide, accounts, products, images, incognito):
            root.destroy()
            mainScript.MainScript(self.db, hide, accounts, products, images, incognito)

        def on_select(event):
            numberOfImages['text'] = "Liczba zdjęć: " + str(self.db.countI(combo1.get()))

        root = tk.Tk()

        frame = tk.Frame(root, background='#FCFCFF')
        frame.grid(row=0, column=0)

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
            ttk.Label(frame, text="Produkt: ", background="#FCFCFF", foreground="black", font=('Verdana', 12)).grid(
                row=0, column=0)
            numberOfImages = ttk.Label(frame, background="#FCFCFF", foreground="black", font=('Verdana', 12))
            numberOfImages.grid(row=0, column=2)
            combo1 = ttk.Combobox(frame, state="readonly", value=l)
            combo1.grid(row=0, column=1)
            combo1.bind('<<ComboboxSelected>>', on_select)

            while i <= numberOfProducts:
                count = "Produkt " + str(i) + ": "
                ttk.Label(frame, text=count, background="#FCFCFF", foreground="black", font=('Verdana', 12)).grid(row=i,
                                                                                                                  column=0)
                image = ttk.Entry(frame)
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

        button = tk.Button(frame, text="Uruchom", background=menuColor, activebackground=activeColor, relief=tk.SOLID,
                           borderwidth=1,
                           command=lambda: openScript(hide, accounts, productsGet(), imagesGet(), incognito))
        button.grid(row=numberOfProducts + 1, column=1)

        root.mainloop()
