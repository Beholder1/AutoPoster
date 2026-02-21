import tkinter as tk
from tkinter import ttk, filedialog

import editAccount
import editLocation
import editProduct
import homePage
import refreshPage
from db import Database


class Main:
    def __init__(self):
        db = Database("store.db")
        bg_color = '#FCFCFF'
        active_color = "#FDA50F"
        menu_color = '#FD6A02'
        font_color = 'black'

        root = tk.Tk()
        root.configure(background=bg_color)
        root.grid_rowconfigure(0, weight=1)
        root.title("Kamil Włodarczyk to kozak")
        style = ttk.Style()
        style.configure('TLabel', background="white", foreground=font_color, font=('Verdana', 12))
        style.configure('TCheckbutton', background="white")

        def raise_frame(frame_to_raise):
            frame_to_raise.tkraise()

        def update_combo(combo, table, column, edit_combo):
            if table == "product":
                db.delete_all_images_by_product(combo.get())
                db.delete_all_categories_for_products_by_product(combo.get())
            db.remove(table, column, combo.get())
            li = []
            for i in db.fetch(table, column):
                li.append(i[0])
            li.sort()
            combo.config(value=li)
            combo.set('')
            edit_combo.config(value=li)

        frame = tk.Frame(root, bg=menu_color, width=150, height=root.winfo_height())
        frame.grid(row=0, column=0, sticky='nws')

        frame.grid_propagate(False)

        frame2 = tk.Frame(root, bg=bg_color, borderwidth=1, relief=tk.RIDGE)
        frame2.grid(row=0, column=1, sticky="nwse")

        # DODAJ
        frame2a = tk.Frame(frame2, width=207, height=114, bg="white", relief=tk.RIDGE, borderwidth=1)
        frame2a.grid(row=0, column=0, pady=5, padx=5)
        frame2a.grid_propagate(False)
        ttk.Label(frame2a, text="Dodaj", foreground=menu_color).grid(row=0, column=0, sticky="w")
        ttk.Label(frame2a, text="Nazwa: ").grid(row=1, column=0)
        name = ttk.Entry(frame2a, textvariable=tk.StringVar())
        name.grid(row=1, column=1)
        ttk.Label(frame2a, text="E-mail: ").grid(row=2, column=0)
        email = ttk.Entry(frame2a, textvariable=tk.StringVar())
        email.grid(row=2, column=1)
        ttk.Label(frame2a, text="Hasło: ").grid(row=3, column=0)
        password = ttk.Entry(frame2a, textvariable=tk.StringVar())
        password.grid(row=3, column=1)
        button = tk.Button(frame2a, width=8, background=menu_color, activebackground=active_color, relief=tk.SOLID,
                           borderwidth=1,
                           text="Dodaj", command=lambda: db.insert(email.get(), password.get(), name.get()))
        button.grid(row=4, column=1)

        # EDYTUJ
        frame2b = tk.Frame(frame2, bg="white", relief=tk.RIDGE, borderwidth=1)
        frame2b.grid(row=1, column=0, pady=5, padx=5)
        ttk.Label(frame2b, text="Edytuj", foreground=menu_color).grid(row=0, column=0, sticky="w")
        ttk.Label(frame2b, text="Nazwa: ").grid(row=1, column=0)
        l5 = []
        for i in db.fetch("parts", "name"):
            l5.append(i[0])
        l5.sort()
        comboAE = ttk.Combobox(frame2b, state="readonly", values=l5)
        comboAE.grid(row=1, column=1)
        button = tk.Button(frame2b, width=8, background=menu_color, activebackground=active_color, relief=tk.SOLID,
                           borderwidth=1,
                           text="Edytuj", command=lambda: editAccount.EditAccount(comboAE.get(), db))
        button.grid(row=2, column=1)

        # USUŃ
        frame2c = tk.Frame(frame2, bg="white", relief=tk.RIDGE, borderwidth=1)
        frame2c.grid(row=2, column=0, pady=5, padx=5)
        ttk.Label(frame2c, text="Usuń", foreground=menu_color).grid(row=0, column=0, sticky="w")
        ttk.Label(frame2c, text="Nazwa: ").grid(row=1, column=0)
        comboAD = ttk.Combobox(frame2c, state="readonly", values=l5)
        comboAD.grid(row=1, column=1)
        button = tk.Button(frame2c, width=8, background=menu_color, activebackground=active_color, relief=tk.SOLID,
                           borderwidth=1,
                           text="Usuń", command=lambda: update_combo(comboAD, "parts", "name", comboAE))
        button.grid(row=2, column=1)

        frame3 = tk.Frame(root, bg=bg_color, borderwidth=1, relief=tk.RIDGE)
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
            #     deleteButton = tk.Button(frame, width=8, background=menu_color, text="Usuń")
            #     deleteButton.grid(row=i, column=3)
            #     i+=1

        def addProduct(product, title, price, desc, category):
            db.save_product(product, title, price, desc)
            p = db.find_product_by_name(product)[0]
            db.save_categories_for_products(p, category)
            for name_to_save in self.imageNames:
                db.save_image(name_to_save, p)

        frame3a = tk.Frame(frame3, bg="white", relief=tk.RIDGE, borderwidth=1)
        frame3a.grid(row=0, column=0, pady=5, padx=5)
        ttk.Label(frame3a, text="Dodaj", foreground=menu_color).grid(row=0, column=0, sticky="w")
        ttk.Label(frame3a, text="Produkt: ").grid(row=1, column=0)
        product = ttk.Entry(frame3a, textvariable=tk.StringVar())
        product.grid(row=1, column=1)
        ttk.Label(frame3a, text="Tytuł: ").grid(row=2, column=0)
        title = ttk.Entry(frame3a, textvariable=tk.StringVar())
        title.grid(row=2, column=1)
        ttk.Label(frame3a, text="Cena: ").grid(row=3, column=0)

        def on_validate(char):
            return char.isdigit()

        vcmd = root.register(on_validate)
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
        images = tk.Button(frame3a, width=8, background=menu_color, text="Wybierz", relief=tk.SOLID, borderwidth=1,
                           activebackground=active_color, command=lambda: addImage(frame, button))
        images.grid(row=6, column=1)
        button = tk.Button(frame3a, width=8, background=menu_color, text="Dodaj", relief=tk.SOLID, borderwidth=1,
                           activebackground=active_color,
                           command=lambda: addProduct(product.get(), title.get(), price.get(), desc.get(),
                                                      db.find_category(comboC.get())))
        button.grid(row=7, column=1)

        # EDYTUJ
        frame3b = tk.Frame(frame3, width=241, height=70, bg="white", relief=tk.RIDGE, borderwidth=1)
        frame3b.grid(row=1, column=0, pady=5, padx=5)
        frame3b.grid_propagate(False)
        ttk.Label(frame3b, text="Edytuj", foreground=menu_color).grid(row=0, column=0, sticky="w")
        ttk.Label(frame3b, text="Produkt: ").grid(row=1, column=0)
        l = []
        for i in db.fetch("product", "productName"):
            l.append(i[0])
        l.sort()
        comboPE = ttk.Combobox(frame3b, state="readonly", values=l)
        comboPE.grid(row=1, column=1)
        button = tk.Button(frame3b, width=8, background=menu_color, activebackground=active_color, relief=tk.SOLID,
                           borderwidth=1,
                           text="Edytuj", command=lambda: editProduct.EditProduct(comboPE.get(), db))
        button.grid(row=2, column=1)

        # USUŃ
        frame3c = tk.Frame(frame3, width=241, height=70, bg="white", relief=tk.RIDGE, borderwidth=1)
        frame3c.grid(row=2, column=0, pady=5, padx=5)
        frame3c.grid_propagate(False)
        ttk.Label(frame3c, text="Usuń", foreground=menu_color).grid(row=0, column=0, sticky="w")
        ttk.Label(frame3c, text="Produkt: ").grid(row=1, column=0)
        comboPD = ttk.Combobox(frame3c, state="readonly", values=l)
        comboPD.grid(row=1, column=1)
        button = tk.Button(frame3c, width=8, background=menu_color, activebackground=active_color, relief=tk.SOLID,
                           borderwidth=1,
                           text="Usuń", command=lambda: update_combo(comboPD, "product", "productname", comboPE))
        button.grid(row=2, column=1)

        frame4 = tk.Frame(root, bg=bg_color, borderwidth=1, relief=tk.RIDGE)
        frame4.grid(row=0, column=1, sticky="nwse")

        # DODAJ
        def insert_localization(location_to_save):
            db.save_location(location_to_save.get())

        frame4a = tk.Frame(frame4, width=253, height=70, bg="white", relief=tk.RIDGE, borderwidth=1)
        frame4a.grid_propagate(False)
        frame4a.grid(row=0, column=0, pady=5, padx=5)
        ttk.Label(frame4a, text="Dodaj", foreground=menu_color).grid(row=0, column=0, sticky="w")
        ttk.Label(frame4a, text="Lokalizacja: ").grid(row=1, column=0)
        location = ttk.Entry(frame4a, textvariable=tk.StringVar())
        location.grid(row=1, column=1)
        button = tk.Button(frame4a, width=8, background=menu_color, text="Dodaj", activebackground=active_color,
                           relief=tk.SOLID,
                           borderwidth=1, command=lambda: insert_localization(location))
        button.grid(row=2, column=1)

        # EDYTUJ
        frame4b = tk.Frame(frame4, bg="white", relief=tk.RIDGE, borderwidth=1)
        frame4b.grid(row=1, column=0, pady=5, padx=5)
        ttk.Label(frame4b, text="Edytuj", foreground=menu_color).grid(row=0, column=0, sticky="w")
        ttk.Label(frame4b, text="Lokalizacja: ").grid(row=1, column=0)
        l3 = []
        for i in db.fetch("localizations", "localization"):
            l3.append(i[0])
        l3.sort()
        comboLE = ttk.Combobox(frame4b, state="readonly", values=l3)
        comboLE.grid(row=1, column=1)
        button = tk.Button(frame4b, width=8, background=menu_color, activebackground=active_color, relief=tk.SOLID,
                           borderwidth=1,
                           text="Edytuj", command=lambda: editLocation.EditLocation(comboLE.get(), db))
        button.grid(row=2, column=1)

        # USUŃ
        frame4c = tk.Frame(frame4, bg="white", relief=tk.RIDGE, borderwidth=1)
        frame4c.grid(row=2, column=0, pady=5, padx=5)
        ttk.Label(frame4c, text="Usuń", foreground=menu_color).grid(row=0, column=0, sticky="w")
        ttk.Label(frame4c, text="Lokalizacja: ").grid(row=1, column=0)
        comboLD = ttk.Combobox(frame4c, state="readonly", values=l3)
        comboLD.grid(row=1, column=1)
        button = tk.Button(frame4c, width=8, background=menu_color, activebackground=active_color, text="Usuń",
                           relief=tk.SOLID,
                           borderwidth=1,
                           command=lambda: update_combo(comboLD, "localizations", "localization", comboLE))
        button.grid(row=2, column=1)

        refresh_frame = refreshPage.RefreshPage(root, db, bg_color, menu_color, active_color).get_page()
        home_frame = homePage.HomePage(root, db, bg_color, menu_color, active_color).get_page()

        buttons_data = [
            ("Strona główna", home_frame),
            ("Odświeżanie", refresh_frame),
            ("Konta", frame2),
            ("Produkty", frame3),
            ("Lokalizacje", frame4)
        ]

        for idx, (text, frame_target) in enumerate(buttons_data):
            btn = tk.Button(frame, text=text, background=menu_color, fg=font_color,
                            font=('MS Reference Sans Serif', 13), relief=tk.SUNKEN, borderwidth=0,
                            activebackground=menu_color,
                            command=lambda f=frame_target: raise_frame(f))
            btn.grid(row=2 + idx, column=0, pady=5, sticky='nwe')

        root.grid_columnconfigure(1, weight=1)
        root.mainloop()


if __name__ == "__main__":
    Main()
