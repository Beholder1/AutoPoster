import tkinter as tk
from tkinter import ttk

from script import mainScript


class ChooseProducts:
    def __init__(self, db, number_of_products, hide: bool, only_one: bool, accounts, incognito: bool):
        self.db = db
        activeColor = "#FDA50F"
        menuColor = '#FD6A02'

        def open_script(hide, accounts, products, images, incognito):
            root.destroy()
            mainScript.MainScript(self.db, hide, accounts, products, images, incognito)

        def on_select(event):
            number_of_images['text'] = "Liczba zdjęć: " + str(self.db.count_all_images_by_product(combo1.get()))

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
        if only_one:
            ttk.Label(frame, text="Produkt: ", background="#FCFCFF", foreground="black", font=('Verdana', 12)).grid(
                row=0, column=0)
            number_of_images = ttk.Label(frame, background="#FCFCFF", foreground="black", font=('Verdana', 12))
            number_of_images.grid(row=0, column=2)
            combo1 = ttk.Combobox(frame, state="readonly", values=l)
            combo1.grid(row=0, column=1)
            combo1.bind('<<ComboboxSelected>>', on_select)

            while i <= number_of_products:
                count = "Produkt " + str(i) + ": "
                ttk.Label(frame, text=count, background="#FCFCFF", foreground="black", font=('Verdana', 12)).grid(row=i,
                                                                                                                  column=0)
                image = ttk.Entry(frame)
                image.grid(row=i, column=2)
                entries.append(image)
                i += 1
        else:
            while i <= number_of_products:
                count = "Produkt " + str(i) + ": "
                ttk.Label(frame, text=count).grid(row=i, column=0)
                combo = ttk.Combobox(frame, state="readonly", values=l)
                combo.grid(row=i, column=1)
                combos.append(combo)
                image = tk.Entry(frame)
                image.grid(row=i, column=3)
                entries.append(image)
                i += 1

        def products_get():
            products = []
            if only_one:
                j = 0
                while j < number_of_products:
                    products.append(combo1.get())
                    j += 1
            else:
                for combo in combos:
                    products.append(combo.get())
            return products

        def images_get():
            images = []
            for entry in entries:
                images.append(list(entry.get().split(",")))
            return images

        button = tk.Button(frame, text="Uruchom", background=menuColor, activebackground=activeColor, relief=tk.SOLID,
                           borderwidth=1,
                           command=lambda: open_script(hide, accounts, products_get(), images_get(), incognito))
        button.grid(row=number_of_products + 1, column=1)

        root.mainloop()
