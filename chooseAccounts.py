import tkinter as tk
from tkinter import ttk

import chooseProducts
import refreshScript


class ChooseAccounts:
    def __init__(self, db, numberOfProducts, hide, onlyOne, numberOfAccounts, incognito):
        self.db = db
        activeColor = "#FDA50F"
        menuColor = '#FD6A02'

        def openScript(numberOfProducts, hide, onlyOne, accounts, incognito):
            root.destroy()
            chooseProducts.ChooseProducts(self.db, numberOfProducts, hide,
                                          onlyOne,
                                          accounts, incognito)

        root = tk.Tk()

        frame = tk.Frame(root, background='#FCFCFF')
        frame.grid(row=0, column=0)

        l = []
        for i in self.db.fetch("parts", "name"):
            l.append(i[0])
        l.sort()
        i = 1
        combos = []
        while i <= numberOfAccounts:
            count = "Konto " + str(i) + ": "
            ttk.Label(frame, text=count, background="#FCFCFF", foreground="black", font=('Verdana', 12)).grid(row=i,
                                                                                                              column=0)
            combo = ttk.Combobox(frame, state="readonly", values=l)
            combo.grid(row=i, column=1)
            combos.append(combo)
            i += 1

        def accountsGet():
            accounts = []
            for combo in combos:
                accounts.append(combo.get())
            return accounts

        button = tk.Button(frame, text="Uruchom", background=menuColor, activebackground=activeColor, relief=tk.SOLID,
                           borderwidth=1, command=lambda: openScript(numberOfProducts, hide,
                                                                     onlyOne,
                                                                     accountsGet(), incognito))
        button.grid(row=numberOfAccounts + 1, column=1)

        root.mainloop()


class ChooseAccountsForRefresh:
    def __init__(self, db, numberOfAccounts, incognito):
        self.db = db
        activeColor = "#FDA50F"
        menuColor = '#FD6A02'

        def openScript(accounts, incognito):
            root.destroy()
            refreshScript.RefreshScript(self.db, accounts, incognito)

        root = tk.Tk()

        frame = tk.Frame(root, background='#FCFCFF')
        frame.grid(row=0, column=0)

        l = []
        for i in self.db.fetch("parts", "name"):
            l.append(i[0])
        l.sort()
        i = 1
        combos = []
        while i <= numberOfAccounts:
            count = "Konto " + str(i) + ": "
            ttk.Label(frame, text=count, background="#FCFCFF", foreground="black", font=('Verdana', 12)).grid(row=i,
                                                                                                              column=0)
            combo = ttk.Combobox(frame, state="readonly", values=l)
            combo.grid(row=i, column=1)
            combos.append(combo)
            i += 1

        def accountsGet():
            accounts = []
            for combo in combos:
                accounts.append(combo.get())
            return accounts

        button = tk.Button(frame, text="Uruchom", background=menuColor, activebackground=activeColor, relief=tk.SOLID,
                           borderwidth=1, command=lambda: openScript(accountsGet(), incognito))
        button.grid(row=numberOfAccounts + 1, column=1)

        root.mainloop()
