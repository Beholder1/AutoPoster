import tkinter as tk
from tkinter import ttk

import chooseAccounts
from script import refreshScript


class RefreshPage:
    def __init__(self, root, db, bg_color: str, menu_color: str, active_color: str):
        self.refresh_page = tk.Frame(root, bg=bg_color, borderwidth=1, relief=tk.RIDGE)
        self.refresh_page.grid(row=0, column=1, sticky="nwse")

        self.incognito_var = tk.BooleanVar(value=False)
        self.all_accounts_var = tk.BooleanVar(value=True)
        self.to_end_var = tk.BooleanVar(value=False)

        ttk.Label(self.refresh_page, text="Incognito: ").grid(row=0, column=0)
        ttk.Checkbutton(self.refresh_page, variable=self.incognito_var).grid(row=0, column=1, sticky="w")
        ttk.Label(self.refresh_page, text="Ile kont: ").grid(row=1, column=0)
        number_of_accounts = ttk.Entry(self.refresh_page, textvariable=tk.IntVar(value=1))
        # combo1.current(0)
        number_of_accounts.grid(row=1, column=1, sticky="w")
        ttk.Label(self.refresh_page, text="Wszystkie konta: ").grid(row=2, column=0)
        ttk.Checkbutton(self.refresh_page, variable=self.all_accounts_var).grid(row=2, column=1, sticky="w")
        ttk.Label(self.refresh_page, text="Do końca: ").grid(row=3, column=0)
        ttk.Checkbutton(self.refresh_page, variable=self.to_end_var).grid(row=3, column=1, sticky="w")

        def chooseNextStep(skip_choosing_accounts: bool):
            if skip_choosing_accounts:
                accounts = []
                for i in db.fetch("parts", "name"):
                    accounts.append(i[0])
                refreshScript.RefreshScript(db, accounts, self.incognito_var.get(), self.to_end_var.get())
            else:
                chooseAccounts.ChooseAccountsForRefresh(db, int(number_of_accounts.get()), self.incognito_var.get(), self.to_end_var.get())

        run_button = tk.Button(self.refresh_page, background=menu_color, width=8, text="Uruchom",
                              activebackground=active_color, relief=tk.SOLID, borderwidth=1,
                              command=lambda: chooseNextStep(self.all_accounts_var.get()))
        run_button.grid(row=4, column=1, sticky="w")

    def getPage(self) -> tk.Frame:
        return self.refresh_page
