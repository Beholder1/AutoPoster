import tkinter as tk

from mainScript import MainScript

from product import addProduct
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

def openScript():
    MainScript()

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
productsMenu.add_command(label="Usuń", command=openAddProduct)

localizationMenu = tk.Menu(myMenu, tearoff="off")
myMenu.add_cascade(label="Lokalizacja", menu=localizationMenu)
localizationMenu.add_command(label="Dodaj", command=openAddLocation)
localizationMenu.add_command(label="Edytuj", command=openEditLocation)
localizationMenu.add_command(label="Usuń", command=openDeleteLocation)

runButton = tk.Button(root, text = "Uruchom", command = openScript)
runButton.pack()

root.mainloop()

