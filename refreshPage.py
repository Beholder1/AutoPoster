import tkinter as tk
from tkinter import ttk

import chooseAccounts
from script import refreshScript


class RefreshPage:
    def __init__(self, root, db, bgColor, menuColor, activeColor):
        self.refreshPage = tk.Frame(root, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
        self.refreshPage.grid(row=0, column=1, sticky="nwse")
        ttk.Label(self.refreshPage, text="Incognito: ").grid(row=0, column=0)
        var3 = tk.IntVar(value=0)
        ttk.Checkbutton(self.refreshPage, variable=var3).grid(row=0, column=1, sticky="w")
        ttk.Label(self.refreshPage, text="Ile kont: ").grid(row=1, column=0)
        numberOfAccounts = ttk.Entry(self.refreshPage, textvariable=tk.IntVar(value=1))
        # combo1.current(0)
        numberOfAccounts.grid(row=1, column=1, sticky="w")
        ttk.Label(self.refreshPage, text="Wszystkie konta: ").grid(row=2, column=0)
        var4 = tk.IntVar(value=1)
        ttk.Checkbutton(self.refreshPage, variable=var4).grid(row=2, column=1, sticky="w")
        ttk.Label(self.refreshPage, text="Do końca: ").grid(row=3, column=0)
        var5 = tk.IntVar(value=0)
        ttk.Checkbutton(self.refreshPage, variable=var5).grid(row=3, column=1, sticky="w")

        def chooseNextStep(skipChoosingAccounts):
            if skipChoosingAccounts == 1:
                accounts = []
                for i in db.fetch("parts", "name"):
                    accounts.append(i[0])
                refreshScript.RefreshScript(db, accounts, var3.get(), var5.get())
            else:
                chooseAccounts.ChooseAccountsForRefresh(db, int(numberOfAccounts.get()), var3.get(), var5.get())

        runButton = tk.Button(self.refreshPage, background=menuColor, width=8, text="Uruchom",
                              activebackground=activeColor, relief=tk.SOLID, borderwidth=1,
                              command=lambda: chooseNextStep(var4.get()))
        runButton.grid(row=4, column=1, sticky="w")

    def getPage(self):
        return self.refreshPage
