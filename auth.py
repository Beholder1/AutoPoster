import tkinter as tk
from tkinter import ttk


class AuthWindow:
    """Okno logowania/rejestracji oparte o backend (JWT).
    show() blokuje i zwraca True po zalogowaniu, None gdy okno zamknieto."""

    def __init__(self, api):
        self.api = api
        self.logged_in = None

        bg_color = '#FCFCFF'
        active_color = "#FDA50F"
        menu_color = '#FD6A02'

        self.root = tk.Tk()
        self.root.title("AutoPoster — logowanie")
        self.root.configure(background=bg_color)
        self.root.resizable(False, False)
        style = ttk.Style()
        style.configure('TLabel', background="white", foreground='black', font=('Verdana', 12))

        def make_button(parent, text, command):
            return tk.Button(parent, width=14, background=menu_color, activebackground=active_color,
                             relief=tk.SOLID, borderwidth=1, text=text, command=command)

        def make_link(parent, text, command):
            return tk.Button(parent, text=text, background="white", activebackground="white",
                             foreground=menu_color, relief=tk.FLAT, borderwidth=0, cursor="hand2",
                             command=command)

        container = tk.Frame(self.root, bg=bg_color)
        container.grid(row=0, column=0, padx=40, pady=30)

        # --- logowanie ---
        self.login_frame = tk.Frame(container, bg="white", relief=tk.RIDGE, borderwidth=1)
        self.login_frame.grid(row=0, column=0)
        ttk.Label(self.login_frame, text="Logowanie", foreground=menu_color).grid(
            row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))
        ttk.Label(self.login_frame, text="E-mail: ").grid(row=1, column=0, padx=(10, 0), sticky="e")
        self.login_email = ttk.Entry(self.login_frame)
        self.login_email.grid(row=1, column=1, padx=(0, 10), pady=2)
        ttk.Label(self.login_frame, text="Hasło: ").grid(row=2, column=0, padx=(10, 0), sticky="e")
        self.login_pass = ttk.Entry(self.login_frame, show="•")
        self.login_pass.grid(row=2, column=1, padx=(0, 10), pady=2)
        self.login_error = tk.Label(self.login_frame, text="", background="white",
                                    foreground="red", font=('Verdana', 9), wraplength=220)
        self.login_error.grid(row=3, column=0, columnspan=2)
        make_button(self.login_frame, "Zaloguj", self._do_login).grid(
            row=4, column=0, columnspan=2, pady=(5, 2))
        make_link(self.login_frame, "Nie masz konta? Zarejestruj się",
                  lambda: self._show_frame(self.register_frame)).grid(
            row=5, column=0, columnspan=2, pady=(0, 10))

        # --- rejestracja ---
        self.register_frame = tk.Frame(container, bg="white", relief=tk.RIDGE, borderwidth=1)
        self.register_frame.grid(row=0, column=0)
        ttk.Label(self.register_frame, text="Rejestracja", foreground=menu_color).grid(
            row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))
        ttk.Label(self.register_frame, text="E-mail: ").grid(row=1, column=0, padx=(10, 0), sticky="e")
        self.reg_email = ttk.Entry(self.register_frame)
        self.reg_email.grid(row=1, column=1, padx=(0, 10), pady=2)
        ttk.Label(self.register_frame, text="Hasło: ").grid(row=2, column=0, padx=(10, 0), sticky="e")
        self.reg_pass = ttk.Entry(self.register_frame, show="•")
        self.reg_pass.grid(row=2, column=1, padx=(0, 10), pady=2)
        ttk.Label(self.register_frame, text="Powtórz hasło: ").grid(row=3, column=0, padx=(10, 0), sticky="e")
        self.reg_pass2 = ttk.Entry(self.register_frame, show="•")
        self.reg_pass2.grid(row=3, column=1, padx=(0, 10), pady=2)
        self.reg_error = tk.Label(self.register_frame, text="", background="white",
                                  foreground="red", font=('Verdana', 9), wraplength=220)
        self.reg_error.grid(row=4, column=0, columnspan=2)
        make_button(self.register_frame, "Załóż konto", self._do_register).grid(
            row=5, column=0, columnspan=2, pady=(5, 2))
        make_link(self.register_frame, "← Wróć do logowania",
                  lambda: self._show_frame(self.login_frame)).grid(
            row=6, column=0, columnspan=2, pady=(0, 10))

        self._active_frame = self.login_frame
        self.login_frame.tkraise()
        self.root.bind('<Return>', self._on_enter)
        self.login_email.focus_set()

    def _show_frame(self, frame):
        self._active_frame = frame
        frame.tkraise()
        (self.login_email if frame is self.login_frame else self.reg_email).focus_set()

    def _on_enter(self, _event):
        if self._active_frame is self.login_frame:
            self._do_login()
        else:
            self._do_register()

    def _do_login(self):
        try:
            ok = self.api.login(self.login_email.get().strip(), self.login_pass.get())
        except Exception as e:
            self.login_error.config(text=str(e))
            return
        if not ok:
            self.login_error.config(text="Błędny e-mail lub hasło")
            return
        self.logged_in = True
        self.root.destroy()

    def _do_register(self):
        email = self.reg_email.get().strip()
        password = self.reg_pass.get()
        if not email or not password:
            self.reg_error.config(text="Podaj e-mail i hasło")
            return
        if password != self.reg_pass2.get():
            self.reg_error.config(text="Hasła się różnią")
            return
        try:
            self.api.register(email, password)
            if not self.api.login(email, password):
                raise RuntimeError("Konto założone, ale logowanie nieudane — spróbuj się zalogować")
        except Exception as e:
            self.reg_error.config(text=str(e))
            return
        self.logged_in = True
        self.root.destroy()

    def show(self):
        self.root.mainloop()
        return self.logged_in
