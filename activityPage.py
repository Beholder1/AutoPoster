import tkinter as tk
from tkinter import ttk

import chooseAccounts
from homePage import _bool_var, _int_var
from script import activityScript


class ActivityPage:
    def __init__(self, root, db, bg_color: str, menu_color: str, active_color: str):
        self.activity_page = tk.Frame(root, bg=bg_color, borderwidth=1, relief=tk.RIDGE)
        self.activity_page.grid(row=0, column=1, sticky="nwse")

        self.all_accounts_var = _bool_var(db, "activity.all_accounts", True)

        ttk.Label(self.activity_page, text="Ile kont: ").grid(row=0, column=0)
        number_of_accounts = ttk.Entry(self.activity_page,
                                        textvariable=_int_var(db, "activity.number_of_accounts", 1))
        number_of_accounts.grid(row=0, column=1, sticky="w")
        ttk.Label(self.activity_page, text="Wszystkie konta: ").grid(row=1, column=0)
        ttk.Checkbutton(self.activity_page, variable=self.all_accounts_var).grid(row=1, column=1, sticky="w")
        ttk.Label(self.activity_page, text="Ile postów: ").grid(row=2, column=0)
        number_of_posts = ttk.Entry(self.activity_page,
                                     textvariable=_int_var(db, "activity.number_of_posts", 5))
        number_of_posts.grid(row=2, column=1, sticky="w")

        def choose_next_step(skip_choosing_accounts: bool):
            if skip_choosing_accounts:
                accounts = []
                for i in db.fetch("parts", "name"):
                    accounts.append(i[0])
                activityScript.ActivityScript(db, accounts, int(number_of_posts.get()))
            else:
                chooseAccounts.ChooseAccountsForActivity(db, int(number_of_accounts.get()),
                                                         int(number_of_posts.get()))

        run_button = tk.Button(self.activity_page, background=menu_color, width=8, text="Uruchom",
                               activebackground=active_color, relief=tk.SOLID, borderwidth=1,
                               command=lambda: choose_next_step(self.all_accounts_var.get()))
        run_button.grid(row=3, column=1, sticky="w")

    def get_page(self) -> tk.Frame:
        return self.activity_page
