import tkinter as tk

from mainScript import MainScript

import settings
from product import addProduct
from localization import addLocation
from localization import editLocation

from db import Database
db = Database("store.db")


root = tk.Tk()

root.title("Tworzenie ogłoszeń")

def openSettings():
    settings.Settings()
def openAddProduct():
    addProduct.AddProduct()
def openAddLocation():
    addLocation.AddLocation()
def openEditLocation():
    editLocation.EditLocation()
def openScript():
    MainScript()

canvas = tk.Canvas(root, height = 700, width = 700)
canvas.pack()

myMenu = tk.Menu(root)
root.config(menu=myMenu)

settingsMenu = tk.Menu(myMenu, tearoff="off")
myMenu.add_cascade(label="Konto", menu=settingsMenu)
settingsMenu.add_command(label="Dodaj", command=openSettings)
settingsMenu.add_command(label="Edytuj", command=openSettings)
settingsMenu.add_command(label="Usuń", command=openSettings)

productsMenu = tk.Menu(myMenu, tearoff="off")
myMenu.add_cascade(label="Produkt", menu=productsMenu)
productsMenu.add_command(label="Dodaj", command=openAddProduct)
productsMenu.add_command(label="Edytuj", command=openAddProduct)
productsMenu.add_command(label="Usuń", command=openAddProduct)

localizationMenu = tk.Menu(myMenu, tearoff="off")
myMenu.add_cascade(label="Lokalizacja", menu=localizationMenu)
localizationMenu.add_command(label="Dodaj", command=openAddLocation)
localizationMenu.add_command(label="Edytuj", command=openEditLocation)
localizationMenu.add_command(label="Usuń", command=openAddLocation)

runButton = tk.Button(root, text = "Uruchom", command = openScript)
runButton.pack()

root.mainloop()

