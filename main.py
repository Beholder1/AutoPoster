import tkinter as tk

from mainScript import MainScript

from product import addProduct
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

def openScript(hide):
    MainScript(hide)

canvas = tk.Canvas(root, height = 700, width = 700)
canvas.pack()

myMenu = tk.Menu(root)
root.config(menu=myMenu)

settingsMenu = tk.Menu(myMenu, tearoff="off")
myMenu.add_cascade(label="Konto", menu=settingsMenu)
settingsMenu.add_command(label="Dodaj", command=openAddAccount)
settingsMenu.add_command(label="Edytuj", command=openEditAccount)
settingsMenu.add_command(label="Usuń", command=openDeleteAccount)

productsMenu = tk.Menu(myMenu, tearoff="off")
myMenu.add_cascade(label="Produkt", menu=productsMenu)
productsMenu.add_command(label="Dodaj", command=openAddProduct)
productsMenu.add_command(label="Edytuj", command=openAddProduct)
productsMenu.add_command(label="Usuń", command=openDeleteProduct)

localizationMenu = tk.Menu(myMenu, tearoff="off")
myMenu.add_cascade(label="Lokalizacja", menu=localizationMenu)
localizationMenu.add_command(label="Dodaj", command=openAddLocation)
localizationMenu.add_command(label="Edytuj", command=openEditLocation)
localizationMenu.add_command(label="Usuń", command=openDeleteLocation)

frame = tk.Frame(root)
frame.place(relwidth=1, relheight=1)
tk.Label(frame, text="Ukryj przed znajomymi: ").grid(row=0, column=0)
var1 = tk.IntVar()
tk.Checkbutton(frame, variable=var1).grid(row=0, column=1)

runButton = tk.Button(root, text="Uruchom", command=lambda: openScript(var1.get()))
runButton.pack()

root.mainloop()

