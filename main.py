import tkinter as tk
from tkinter import filedialog, Text
import os

from mainScript import MainScript

import settings
import addProduct
import addLocalization

from db import Database
db = Database("store.db")


root = tk.Tk()

root.title("Tworzenie ogłoszeń")

def openSettings():
    settings.Settings()
def openAddProduct():
    addProduct.AddProduct()
def openAddLocalization():
    addLocalization.AddLocalization()
def openScript():
    MainScript()

canvas = tk.Canvas(root, height = 700, width = 700)
canvas.pack()

frameMenu = tk.Frame(root)
frameMenu.place(relwidth=1, relheight=0.1)

settingsButton = tk.Button(frameMenu, text = "Ustawienia", command = openSettings)
settingsButton.grid(row=0, column=0)

productButton = tk.Button(frameMenu, text = "Produkty", command = openAddProduct)
productButton.grid(row=0, column=1)

localizationButton = tk.Button(frameMenu, text = "Lokalizacje", command = openAddLocalization)
localizationButton.grid(row=0, column=2)

runButton = tk.Button(root, text = "Uruchom", command = openScript)
runButton.pack()

root.mainloop()

