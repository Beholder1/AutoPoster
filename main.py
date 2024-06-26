import tkinter as tk
from tkinter import ttk, filedialog

from tkfontawesome import icon_to_image

import editAccount
import editLocation
import editProduct
import homePage
import refreshPage
from db import Database


class Main:
    def __init__(self):
        db = Database("store.db")
        bgColor = '#FCFCFF'
        activeColor = "#FDA50F"
        menuColor = '#FD6A02'
        fontColor = 'black'

        root = tk.Tk()
        root.configure(background=bgColor)
        root.grid_rowconfigure(0, weight=1)
        root.title("Kamil Włodarczyk to kozak")
        style = ttk.Style()
        style.configure('TLabel', background="white", foreground=fontColor, font=('Verdana', 12))
        style.configure('TCheckbutton', background="white")
        min_w = 50
        max_w = 150
        self.cur_width = min_w
        self.expanded = False

        def raise_frame(frame):
            frame.tkraise()

        def updateCombo(combo, table, column, editCombo):
            if table == "product":
                db.deleteAllImagesByProduct(combo.get())
                db.deleteAllCategoriesForProductsByProduct(combo.get())
            db.remove(table, column, combo.get())
            li = []
            for i in db.fetch(table, column):
                li.append(i[0])
            li.sort()
            combo.config(value=li)
            combo.set('')
            editCombo.config(value=li)

        def expand():
            rep = root.after(2, expand)
            if not self.expanded:
                self.cur_width += 10
                frame.config(width=self.cur_width)
            if self.cur_width >= max_w:
                self.expanded = True
                root.after_cancel(rep)
                fill()

        def contract():
            self.cur_width -= 10
            rep = root.after(2, contract)
            frame.config(width=self.cur_width)
            if self.cur_width <= min_w:
                self.expanded = False
                root.after_cancel(rep)
                fill()

        def fill():
            if self.expanded:
                menuButton.config(image=closeIcon, command=contract)
                homeButton.config(image="", text="Strona główna", borderwidth=0)
                homeButton.grid_configure(pady=0)
                refreshButton.config(image="", text="Odświeżanie", borderwidth=0)
                refreshButton.grid_configure(pady=0)
                accountButton.config(image="", text="Konta", borderwidth=0)
                accountButton.grid_configure(pady=0)
                productButton.config(image="", text="Produkty", borderwidth=0)
                productButton.grid_configure(pady=0)
                locationButton.config(image="", text="Lokalizacje", borderwidth=0)
                locationButton.grid_configure(pady=0)
            else:
                menuButton.config(image=menuIcon, command=expand)
                homeButton.config(image=homeIcon, borderwidth=0)
                homeButton.grid_configure(pady=5)
                refreshButton.config(image=refreshIcon, borderwidth=0)
                refreshButton.grid_configure(pady=5)
                accountButton.config(image=accountIcon, borderwidth=0)
                accountButton.grid_configure(pady=5)
                productButton.config(image=productIcon, borderwidth=0)
                productButton.grid_configure(pady=5)
                locationButton.config(image=locationIcon, borderwidth=0)
                locationButton.grid_configure(pady=5)

        menuIcon = icon_to_image("bars", scale_to_height=24)
        closeIcon = icon_to_image("times", scale_to_height=24)
        homeIcon = icon_to_image("home", scale_to_height=24)
        refreshIcon = icon_to_image("sync-alt", scale_to_height=24)
        accountIcon = icon_to_image("user", scale_to_height=24)
        productIcon = icon_to_image("box", scale_to_height=24)
        locationIcon = icon_to_image("map-marker-alt", scale_to_height=24)

        frame = tk.Frame(root, bg=menuColor, width=50, height=root.winfo_height())
        frame.grid(row=0, column=0, sticky='nws')

        menuButton = tk.Button(frame, image=menuIcon, background=menuColor, fg=fontColor, relief=tk.SUNKEN,
                               borderwidth=0, activebackground=menuColor, command=lambda: expand())
        menuButton.grid(row=1, column=0, pady=5, padx=(10, 10), sticky='nw')
        homeButton = tk.Button(frame, image=homeIcon, background=menuColor, fg=fontColor,
                               font=('MS Reference Sans Serif', 13), relief=tk.SUNKEN, borderwidth=0,
                               activebackground=menuColor, command=lambda: raise_frame(homeFrame))
        homeButton.grid(row=2, column=0, pady=5, sticky='nwe')
        refreshButton = tk.Button(frame, image=refreshIcon, background=menuColor, fg=fontColor,
                                  font=('MS Reference Sans Serif', 13), relief=tk.SUNKEN, borderwidth=0,
                                  activebackground=menuColor, command=lambda: raise_frame(refreshFrame))
        refreshButton.grid(row=3, column=0, pady=5, sticky='nwe')
        accountButton = tk.Button(frame, image=accountIcon, background=menuColor, fg=fontColor,
                                  font=('MS Reference Sans Serif', 13), relief=tk.SUNKEN, borderwidth=0,
                                  activebackground=menuColor, command=lambda: raise_frame(frame2))
        accountButton.grid(row=4, column=0, pady=5, sticky='nwe')
        productButton = tk.Button(frame, image=productIcon, background=menuColor, fg=fontColor,
                                  font=('MS Reference Sans Serif', 13), relief=tk.SUNKEN, borderwidth=0,
                                  activebackground=menuColor, command=lambda: raise_frame(frame3))
        productButton.grid(row=5, column=0, pady=5, sticky='nwe')
        locationButton = tk.Button(frame, image=locationIcon, background=menuColor, fg=fontColor,
                                   font=('MS Reference Sans Serif', 13), relief=tk.SUNKEN, borderwidth=0,
                                   activebackground=menuColor, command=lambda: raise_frame(frame4))
        locationButton.grid(row=6, column=0, pady=5, sticky='nwe')

        # frame.bind('<Enter>',lambda e: expand())
        # frame.bind('<Leave>',lambda e: contract())

        frame.grid_propagate(False)

        frame2 = tk.Frame(root, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
        frame2.grid(row=0, column=1, sticky="nwse")

        # DODAJ
        frame2a = tk.Frame(frame2, width=207, height=114, bg="white", relief=tk.RIDGE, borderwidth=1)
        frame2a.grid(row=0, column=0, pady=5, padx=5)
        frame2a.grid_propagate(False)
        ttk.Label(frame2a, text="Dodaj", foreground=menuColor).grid(row=0, column=0, sticky="w")
        ttk.Label(frame2a, text="Nazwa: ").grid(row=1, column=0)
        name = ttk.Entry(frame2a, textvariable=tk.StringVar())
        name.grid(row=1, column=1)
        ttk.Label(frame2a, text="E-mail: ").grid(row=2, column=0)
        email = ttk.Entry(frame2a, textvariable=tk.StringVar())
        email.grid(row=2, column=1)
        ttk.Label(frame2a, text="Hasło: ").grid(row=3, column=0)
        password = ttk.Entry(frame2a, textvariable=tk.StringVar())
        password.grid(row=3, column=1)
        button = tk.Button(frame2a, width=8, background=menuColor, activebackground=activeColor, relief=tk.SOLID,
                           borderwidth=1,
                           text="Dodaj", command=lambda: db.insert(email.get(), password.get(), name.get()))
        button.grid(row=4, column=1)

        # EDYTUJ
        frame2b = tk.Frame(frame2, bg="white", relief=tk.RIDGE, borderwidth=1)
        frame2b.grid(row=1, column=0, pady=5, padx=5)
        ttk.Label(frame2b, text="Edytuj", foreground=menuColor).grid(row=0, column=0, sticky="w")
        ttk.Label(frame2b, text="Nazwa: ").grid(row=1, column=0)
        l5 = []
        for i in db.fetch("parts", "name"):
            l5.append(i[0])
        l5.sort()
        comboAE = ttk.Combobox(frame2b, state="readonly", values=l5)
        comboAE.grid(row=1, column=1)
        button = tk.Button(frame2b, width=8, background=menuColor, activebackground=activeColor, relief=tk.SOLID,
                           borderwidth=1,
                           text="Edytuj", command=lambda: editAccount.EditAccount(comboAE.get(), db))
        button.grid(row=2, column=1)

        # USUŃ
        frame2c = tk.Frame(frame2, bg="white", relief=tk.RIDGE, borderwidth=1)
        frame2c.grid(row=2, column=0, pady=5, padx=5)
        ttk.Label(frame2c, text="Usuń", foreground=menuColor).grid(row=0, column=0, sticky="w")
        ttk.Label(frame2c, text="Nazwa: ").grid(row=1, column=0)
        comboAD = ttk.Combobox(frame2c, state="readonly", values=l5)
        comboAD.grid(row=1, column=1)
        button = tk.Button(frame2c, width=8, background=menuColor, activebackground=activeColor, relief=tk.SOLID,
                           borderwidth=1,
                           text="Usuń", command=lambda: updateCombo(comboAD, "parts", "name", comboAE))
        button.grid(row=2, column=1)

        frame3 = tk.Frame(root, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
        frame3.grid(row=0, column=1, sticky="nwse")

        # DODAJ
        self.imageNames = []

        def addImage(frame, button):
            i = 4
            self.imageNames = filedialog.askopenfilenames(initialdir="/", title="Wybierz zdjęcia", filetypes=[
                ("Obrazy", ".bmp .tif .tiff .png .gif .jpg .jpeg .jfif .pjpeg .pjp .webp")])
            # for name in self.imageNames:
            #     button.grid(row=i+1, column=1)
            #     label = tk.Label(frame, text=name)
            #     label.grid(row=i, column=2)
            #     deleteButton = tk.Button(frame, width=8, background=menuColor, text="Usuń")
            #     deleteButton.grid(row=i, column=3)
            #     i+=1

        def addProduct(product, title, price, desc, category):
            db.saveProduct(product, title, price, desc)
            p = db.findProductByName(product)[0]
            db.saveCategoriesForProducts(p, category)
            for name in self.imageNames:
                db.saveImage(name, p)

        frame3a = tk.Frame(frame3, bg="white", relief=tk.RIDGE, borderwidth=1)
        frame3a.grid(row=0, column=0, pady=5, padx=5)
        ttk.Label(frame3a, text="Dodaj", foreground=menuColor).grid(row=0, column=0, sticky="w")
        ttk.Label(frame3a, text="Produkt: ").grid(row=1, column=0)
        product = ttk.Entry(frame3a, textvariable=tk.StringVar())
        product.grid(row=1, column=1)
        ttk.Label(frame3a, text="Tytuł: ").grid(row=2, column=0)
        title = ttk.Entry(frame3a, textvariable=tk.StringVar())
        title.grid(row=2, column=1)
        ttk.Label(frame3a, text="Cena: ").grid(row=3, column=0)

        def onValidate(char):
            return char.isdigit()

        vcmd = root.register(onValidate)
        price = ttk.Entry(frame3a, textvariable=tk.IntVar(), validate="key", validatecommand=(vcmd, '%S'))
        price.grid(row=3, column=1)
        ttk.Label(frame3a, text="Opis: ").grid(row=4, column=0)
        desc = ttk.Entry(frame3a, textvariable=tk.StringVar())
        desc.grid(row=4, column=1)
        ttk.Label(frame3a, text="Kategoria: ").grid(row=5, column=0)
        l1 = []
        for i in db.fetch("categories", "category"):
            l1.append(i[0])
        comboC = ttk.Combobox(frame3a, state="readonly", values=l1)
        comboC.grid(row=5, column=1)
        ttk.Label(frame3a, text="Zdjęcia: ").grid(row=6, column=0)
        images = tk.Button(frame3a, width=8, background=menuColor, text="Wybierz", relief=tk.SOLID, borderwidth=1,
                           activebackground=activeColor, command=lambda: addImage(frame, button))
        images.grid(row=6, column=1)
        button = tk.Button(frame3a, width=8, background=menuColor, text="Dodaj", relief=tk.SOLID, borderwidth=1,
                           activebackground=activeColor,
                           command=lambda: addProduct(product.get(), title.get(), price.get(), desc.get(),
                                                      db.findCategory(comboC.get())))
        button.grid(row=7, column=1)

        # EDYTUJ
        frame3b = tk.Frame(frame3, width=241, height=70, bg="white", relief=tk.RIDGE, borderwidth=1)
        frame3b.grid(row=1, column=0, pady=5, padx=5)
        frame3b.grid_propagate(False)
        ttk.Label(frame3b, text="Edytuj", foreground=menuColor).grid(row=0, column=0, sticky="w")
        ttk.Label(frame3b, text="Produkt: ").grid(row=1, column=0)
        l = []
        for i in db.fetch("product", "productName"):
            l.append(i[0])
        l.sort()
        comboPE = ttk.Combobox(frame3b, state="readonly", values=l)
        comboPE.grid(row=1, column=1)
        button = tk.Button(frame3b, width=8, background=menuColor, activebackground=activeColor, relief=tk.SOLID,
                           borderwidth=1,
                           text="Edytuj", command=lambda: editProduct.EditProduct(comboPE.get(), db))
        button.grid(row=2, column=1)

        # USUŃ
        frame3c = tk.Frame(frame3, width=241, height=70, bg="white", relief=tk.RIDGE, borderwidth=1)
        frame3c.grid(row=2, column=0, pady=5, padx=5)
        frame3c.grid_propagate(False)
        ttk.Label(frame3c, text="Usuń", foreground=menuColor).grid(row=0, column=0, sticky="w")
        ttk.Label(frame3c, text="Produkt: ").grid(row=1, column=0)
        comboPD = ttk.Combobox(frame3c, state="readonly", values=l)
        comboPD.grid(row=1, column=1)
        button = tk.Button(frame3c, width=8, background=menuColor, activebackground=activeColor, relief=tk.SOLID,
                           borderwidth=1,
                           text="Usuń", command=lambda: updateCombo(comboPD, "product", "productname", comboPE))
        button.grid(row=2, column=1)

        frame4 = tk.Frame(root, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
        frame4.grid(row=0, column=1, sticky="nwse")

        # DODAJ
        def insertLocalization(location):
            db.saveLocation(location.get())

        frame4a = tk.Frame(frame4, width=253, height=70, bg="white", relief=tk.RIDGE, borderwidth=1)
        frame4a.grid_propagate(False)
        frame4a.grid(row=0, column=0, pady=5, padx=5)
        ttk.Label(frame4a, text="Dodaj", foreground=menuColor).grid(row=0, column=0, sticky="w")
        ttk.Label(frame4a, text="Lokalizacja: ").grid(row=1, column=0)
        location = ttk.Entry(frame4a, textvariable=tk.StringVar())
        location.grid(row=1, column=1)
        button = tk.Button(frame4a, width=8, background=menuColor, text="Dodaj", activebackground=activeColor,
                           relief=tk.SOLID,
                           borderwidth=1, command=lambda: insertLocalization(location))
        button.grid(row=2, column=1)

        # EDYTUJ
        frame4b = tk.Frame(frame4, bg="white", relief=tk.RIDGE, borderwidth=1)
        frame4b.grid(row=1, column=0, pady=5, padx=5)
        ttk.Label(frame4b, text="Edytuj", foreground=menuColor).grid(row=0, column=0, sticky="w")
        ttk.Label(frame4b, text="Lokalizacja: ").grid(row=1, column=0)
        l3 = []
        for i in db.fetch("localizations", "localization"):
            l3.append(i[0])
        l3.sort()
        comboLE = ttk.Combobox(frame4b, state="readonly", values=l3)
        comboLE.grid(row=1, column=1)
        button = tk.Button(frame4b, width=8, background=menuColor, activebackground=activeColor, relief=tk.SOLID,
                           borderwidth=1,
                           text="Edytuj", command=lambda: editLocation.EditLocation(comboLE.get(), db))
        button.grid(row=2, column=1)

        # USUŃ
        frame4c = tk.Frame(frame4, bg="white", relief=tk.RIDGE, borderwidth=1)
        frame4c.grid(row=2, column=0, pady=5, padx=5)
        ttk.Label(frame4c, text="Usuń", foreground=menuColor).grid(row=0, column=0, sticky="w")
        ttk.Label(frame4c, text="Lokalizacja: ").grid(row=1, column=0)
        comboLD = ttk.Combobox(frame4c, state="readonly", values=l3)
        comboLD.grid(row=1, column=1)
        button = tk.Button(frame4c, width=8, background=menuColor, activebackground=activeColor, text="Usuń",
                           relief=tk.SOLID,
                           borderwidth=1,
                           command=lambda: updateCombo(comboLD, "localizations", "localization", comboLE))
        button.grid(row=2, column=1)

        refreshFrame = refreshPage.RefreshPage(root, db, bgColor, menuColor, activeColor).getPage()
        homeFrame = homePage.HomePage(root, db, bgColor, menuColor, activeColor).getPage()

        root.grid_columnconfigure(1, weight=1)
        root.mainloop()


if __name__ == "__main__":
    Main()
