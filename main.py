import tkinter as tk
from tkinter import ttk

from mainScript import MainScript

from product import addProduct
from product import editProduct
from product import deleteProduct
from account import addAccount
from account import editAccount
from account import deleteAccount
from localization import addLocation
from localization import editLocation
from localization import deleteLocation

from db import Database
db = Database("store.db")

root = tk.Tk()

root.title("Tworzenie ogłoszeń")

def openAddProduct():
    addProduct.AddProduct()
def openDeleteProduct():
    deleteProduct.DeleteProduct()
def openEditProduct():
    editProduct.EditProduct()

def openAddAccount():
    addAccount.AddAccount()
def openEditAccount():
    editAccount.EditAccount()
def openDeleteAccount():
    deleteAccount.DeleteAccount()

def openAddLocation():
    addLocation.AddLocation()
def openEditLocation():
    editLocation.EditLocation()
def openDeleteLocation():
    deleteLocation.DeleteLocation()

def openScript(hide, title, email, iterrations):
    MainScript(hide, title, email, iterrations)


def menuPart(name, commandAdd, commandEdit, commandDelete):
    settingsMenu = tk.Menu(myMenu, tearoff="off")
    myMenu.add_cascade(label=name, menu=settingsMenu)
    settingsMenu.add_command(label="Dodaj", command=commandAdd)
    settingsMenu.add_command(label="Edytuj", command=commandEdit)
    settingsMenu.add_command(label="Usuń", command=commandDelete)

canvas = tk.Canvas(root, height = 500, width = 500)
canvas.pack()

myMenu = tk.Menu(root)
root.config(menu=myMenu)

menuPart("Konto", openAddAccount, openEditAccount, openDeleteAccount)

menuPart("Produkt", openAddProduct, openEditProduct, openDeleteProduct)

menuPart("Lokalizacja", openAddLocation, openEditLocation, openDeleteLocation)

frame = tk.Frame(root)
frame.place(relwidth=1, relheight=1)
tk.Label(frame, text="Ukryj przed znajomymi: ").grid(row=0, column=0)
var1 = tk.IntVar()
tk.Checkbutton(frame, variable=var1).grid(row=0, column=1)

tk.Label(frame, text="Produkt: ").grid(row=1, column=0)
combo = ttk.Combobox(frame, state="readonly", value=db.fetchP())
combo.current(0)
combo.grid(row=1, column=1)

tk.Label(frame, text="Konto: ").grid(row=2, column=0)
combo1 = ttk.Combobox(frame, state="readonly", value=db.fetchEmails())
combo1.current(0)
combo1.grid(row=2, column=1)

tk.Label(frame, text="Ile ogłoszeń: ").grid(row=3, column=0)
iterrations = tk.Entry(frame, textvariable=tk.IntVar(value=1))
iterrations.grid(row=3, column=1)

runButton = tk.Button(root, text="Uruchom", command=lambda: openScript(var1.get(), combo.get(), combo1.get(), iterrations.get()))
runButton.pack()

root.mainloop()

