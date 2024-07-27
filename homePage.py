import tkinter as tk
from tkinter import ttk

import chooseAccounts
import chooseProducts


class HomePage:
    def __init__(self, root, db, bgColor, menuColor, activeColor):
        self.homePage = tk.Frame(root, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
        self.homePage.grid(row=0, column=1, sticky="nwse")
        ttk.Label(self.homePage, text="Ukryj: ").grid(row=0, column=0)
        var1 = tk.IntVar(value=0)
        ttk.Checkbutton(self.homePage, variable=var1).grid(row=0, column=1, sticky="w")
        ttk.Label(self.homePage, text="Incognito: ").grid(row=1, column=0)
        var3 = tk.IntVar(value=0)
        ttk.Checkbutton(self.homePage, variable=var3).grid(row=1, column=1, sticky="w")
        ttk.Label(self.homePage, text="Jeden rodzaj: ").grid(row=2, column=0)
        var2 = tk.IntVar(value=1)
        ttk.Checkbutton(self.homePage, variable=var2).grid(row=2, column=1, sticky="w")
        ttk.Label(self.homePage, text="Ile kont: ").grid(row=3, column=0)
        numberOfAccounts = ttk.Entry(self.homePage, textvariable=tk.IntVar(value=1))
        # combo1.current(0)
        numberOfAccounts.grid(row=3, column=1, sticky="w")
        ttk.Label(self.homePage, text="Wszystkie konta: ").grid(row=4, column=0)
        var4 = tk.IntVar(value=0)
        ttk.Checkbutton(self.homePage, variable=var4).grid(row=4, column=1, sticky="w")
        ttk.Label(self.homePage, text="Ile ogłoszeń: ").grid(row=5, column=0)
        iterations = ttk.Entry(self.homePage, textvariable=tk.IntVar(value=1))
        iterations.grid(row=5, column=1, sticky="w")

        def chooseNextStep(skipChoosingAccounts):
            if skipChoosingAccounts == 1:
                accounts = []
                for i in db.fetch("parts", "name"):
                    accounts.append(i[0])
                chooseProducts.ChooseProducts(db, int(iterations.get()), var1.get(), var2.get(), accounts, var3.get())
            else:
                chooseAccounts.ChooseAccounts(db, int(iterations.get()), var1.get(),
                                              var2.get(),
                                              int(numberOfAccounts.get()), var3.get())

        runButton = tk.Button(self.homePage, background=menuColor, width=8, text="Uruchom",
                              activebackground=activeColor, relief=tk.SOLID, borderwidth=1,
                              command=lambda: chooseNextStep(var4.get()))
        runButton.grid(row=6, column=1, sticky="w")

    def getPage(self):
        return self.homePage
