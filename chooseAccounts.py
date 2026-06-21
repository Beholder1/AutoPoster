import tkinter as tk
from tkinter import ttk

import chooseProducts
from script import activityScript, refreshScript


class ChooseAccounts:
    def __init__(self, db, number_of_products, hide: bool, only_one: bool, number_of_accounts):
        self.db = db
        active_color = "#FDA50F"
        menu_color = '#FD6A02'

        def open_script(number_of_products, hide, only_one, accounts):
            root.destroy()
            chooseProducts.ChooseProducts(self.db, number_of_products, hide,
                                          only_one,
                                          accounts)

        root = tk.Toplevel()

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

        def get_accounts():
            accounts = []
            for combo in combos:
                accounts.append(combo.get())
            return accounts

        button = tk.Button(frame, text="Uruchom", background=menu_color, activebackground=active_color, relief=tk.SOLID,
                           borderwidth=1, command=lambda: open_script(number_of_products, hide,
                                                                      only_one,
                                                                      get_accounts()))
        button.grid(row=number_of_accounts + 1, column=1)


class ChooseAccountsForRefresh:
    def __init__(self, db, number_of_accounts, refresh):
        self.db = db
        active_color = "#FDA50F"
        menu_color = '#FD6A02'

        def open_script(accounts, refresh):
            root.destroy()
            refreshScript.RefreshScript(self.db, accounts, refresh)

        root = tk.Toplevel()

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

        button = tk.Button(frame, text="Uruchom", background=menu_color, activebackground=active_color, relief=tk.SOLID,
                           borderwidth=1, command=lambda: open_script(accounts_get(), refresh))
        button.grid(row=number_of_accounts + 1, column=1)


class ChooseAccountsForActivity:
    def __init__(self, db, number_of_accounts, number_of_posts):
        self.db = db
        active_color = "#FDA50F"
        menu_color = '#FD6A02'

        def open_script(accounts, number_of_posts):
            root.destroy()
            activityScript.ActivityScript(self.db, accounts, number_of_posts)

        root = tk.Toplevel()

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

        button = tk.Button(frame, text="Uruchom", background=menu_color, activebackground=active_color, relief=tk.SOLID,
                           borderwidth=1, command=lambda: open_script(accounts_get(), number_of_posts))
        button.grid(row=number_of_accounts + 1, column=1)
