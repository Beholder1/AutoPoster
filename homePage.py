import tkinter as tk
from tkinter import ttk

import chooseAccounts
import chooseProducts


def _bool_var(db, key, default):
    var = tk.BooleanVar(value=db.get_setting(key, "1" if default else "0") == "1")
    var.trace_add("write", lambda *_: db.set_setting(key, "1" if var.get() else "0"))
    return var


def _int_var(db, key, default):
    var = tk.StringVar(value=db.get_setting(key, str(default)))

    def on_change(*_):
        value = var.get()
        if value.isdigit():
            db.set_setting(key, value)

    var.trace_add("write", on_change)
    return var


class HomePage:
    def __init__(self, root, db, bg_color: str, menu_color: str, active_color: str):
        self.home_page = tk.Frame(root, bg=bg_color, borderwidth=1, relief=tk.RIDGE)
        self.home_page.grid(row=0, column=1, sticky="nwse")
        ttk.Label(self.home_page, text="Ukryj: ").grid(row=0, column=0)
        var1 = _bool_var(db, "home.hide", False)
        ttk.Checkbutton(self.home_page, variable=var1).grid(row=0, column=1, sticky="w")
        ttk.Label(self.home_page, text="Jeden rodzaj: ").grid(row=1, column=0)
        var2 = _bool_var(db, "home.only_one", True)
        ttk.Checkbutton(self.home_page, variable=var2).grid(row=1, column=1, sticky="w")
        ttk.Label(self.home_page, text="Ile kont: ").grid(row=2, column=0)
        number_of_accounts = ttk.Entry(self.home_page, textvariable=_int_var(db, "home.number_of_accounts", 1))
        number_of_accounts.grid(row=2, column=1, sticky="w")
        ttk.Label(self.home_page, text="Wszystkie konta: ").grid(row=3, column=0)
        var4 = _bool_var(db, "home.all_accounts", False)
        ttk.Checkbutton(self.home_page, variable=var4).grid(row=3, column=1, sticky="w")
        ttk.Label(self.home_page, text="Ile ogłoszeń: ").grid(row=4, column=0)
        iterations = ttk.Entry(self.home_page, textvariable=_int_var(db, "home.iterations", 1))
        iterations.grid(row=4, column=1, sticky="w")

        def choose_next_step(skip_choosing_accounts: bool):
            if skip_choosing_accounts:
                accounts = []
                for i in db.fetch("parts", "name"):
                    accounts.append(i[0])
                chooseProducts.ChooseProducts(db, int(iterations.get()), var1.get(), var2.get(), accounts)
            else:
                chooseAccounts.ChooseAccounts(db, int(iterations.get()), var1.get(),
                                              var2.get(),
                                              int(number_of_accounts.get()))

        run_button = tk.Button(self.home_page, background=menu_color, width=8, text="Uruchom",
                              activebackground=active_color, relief=tk.SOLID, borderwidth=1,
                              command=lambda: choose_next_step(var4.get()))
        run_button.grid(row=5, column=1, sticky="w")

    def get_page(self):
        return self.home_page
