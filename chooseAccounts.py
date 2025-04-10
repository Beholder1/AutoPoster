import tkinter as tk
from tkinter import ttk

import chooseProducts
from script import refreshScript


class ChooseAccounts:
    def __init__(self, db, number_of_products, hide: bool, only_one: bool, number_of_accounts, incognito: bool):
        self.db = db
        activeColor = "#FDA50F"
        menuColor = '#FD6A02'

        def open_script(number_of_products, hide, only_one, accounts, incognito):
            root.destroy()
            chooseProducts.ChooseProducts(self.db, number_of_products, hide,
                                          only_one,
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
        while i <= number_of_accounts:
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
                           borderwidth=1, command=lambda: open_script(number_of_products, hide,
                                                                     only_one,
                                                                     accountsGet(), incognito))
        button.grid(row=number_of_accounts + 1, column=1)

        root.mainloop()


class ChooseAccountsForRefresh:
    def __init__(self, db, number_of_accounts, incognito, refresh):
        self.db = db
        activeColor = "#FDA50F"
        menuColor = '#FD6A02'

        def open_script(accounts, incognito, refresh):
            root.destroy()
            refreshScript.RefreshScript(self.db, accounts, incognito, refresh)

        root = tk.Tk()

        frame = tk.Frame(root, background='#FCFCFF')
        frame.grid(row=0, column=0)

        l = []
        for i in self.db.fetch("parts", "name"):
            l.append(i[0])
        l.sort()
        i = 1
        combos = []
        while i <= number_of_accounts:
            count = "Konto " + str(i) + ": "
            ttk.Label(frame, text=count, background="#FCFCFF", foreground="black", font=('Verdana', 12)).grid(row=i,
                                                                                                              column=0)
            combo = ttk.Combobox(frame, state="readonly", values=l)
            combo.grid(row=i, column=1)
            combos.append(combo)
            i += 1

        def accounts_get():
            accounts = []
            for combo in combos:
                accounts.append(combo.get())
            return accounts

        button = tk.Button(frame, text="Uruchom", background=menuColor, activebackground=activeColor, relief=tk.SOLID,
                           borderwidth=1, command=lambda: open_script(accounts_get(), incognito, refresh))
        button.grid(row=number_of_accounts + 1, column=1)

        root.mainloop()
