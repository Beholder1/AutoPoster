import tkinter as tk
from tkinter import ttk

import chooseAccounts
import chooseProducts


class HomePage:
    def __init__(self, root, db, bg_color: str, menu_color: str, active_color: str):
        self.homePage = tk.Frame(root, bg=bg_color, borderwidth=1, relief=tk.RIDGE)
        self.homePage.grid(row=0, column=1, sticky="nwse")
        ttk.Label(self.homePage, text="Ukryj: ").grid(row=0, column=0)
        var1 = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.homePage, variable=var1).grid(row=0, column=1, sticky="w")
        ttk.Label(self.homePage, text="Incognito: ").grid(row=1, column=0)
        var3 = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.homePage, variable=var3).grid(row=1, column=1, sticky="w")
        ttk.Label(self.homePage, text="Jeden rodzaj: ").grid(row=2, column=0)
        var2 = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.homePage, variable=var2).grid(row=2, column=1, sticky="w")
        ttk.Label(self.homePage, text="Ile kont: ").grid(row=3, column=0)
        number_of_accounts = ttk.Entry(self.homePage, textvariable=tk.IntVar(value=1))
        # combo1.current(0)
        number_of_accounts.grid(row=3, column=1, sticky="w")
        ttk.Label(self.homePage, text="Wszystkie konta: ").grid(row=4, column=0)
        var4 = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.homePage, variable=var4).grid(row=4, column=1, sticky="w")
        ttk.Label(self.homePage, text="Ile ogłoszeń: ").grid(row=5, column=0)
        iterations = ttk.Entry(self.homePage, textvariable=tk.IntVar(value=1))
        iterations.grid(row=5, column=1, sticky="w")

        def choose_next_step(skipChoosingAccounts: bool):
            if skipChoosingAccounts:
                accounts = []
                for i in db.fetch("parts", "name"):
                    accounts.append(i[0])
                chooseProducts.ChooseProducts(db, int(iterations.get()), var1.get(), var2.get(), accounts, var3.get())
            else:
                chooseAccounts.ChooseAccounts(db, int(iterations.get()), var1.get(),
                                              var2.get(),
                                              int(number_of_accounts.get()), var3.get())

        runButton = tk.Button(self.homePage, background=menu_color, width=8, text="Uruchom",
                              activebackground=active_color, relief=tk.SOLID, borderwidth=1,
                              command=lambda: choose_next_step(var4.get()))
        runButton.grid(row=6, column=1, sticky="w")

    def get_page(self):
        return self.homePage
