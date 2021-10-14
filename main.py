import tkinter as tk
from tkinter import filedialog, Text
import os

from mainScript import MainScript

import settings
import addProduct

from db import Database
db = Database("store.db")


root = tk.Tk()

root.title("Tworzenie ogłoszeń")

def openSettings():
    settings.Settings()
def openAddProduct():
    addProduct.AddProduct()
def openScript():
    MainScript()

canvas = tk.Canvas(root, height = 700, width = 700)
canvas.pack()

frameMenu = tk.Frame(root)
frameMenu.place(relwidth=1, relheight=0.1)

settingsButton = tk.Button(frameMenu, text = "Ustawienia", command = openSettings)
settingsButton.grid(row=0, column=0)

productButton = tk.Button(frameMenu, text = "Dodaj produkt", command = openAddProduct)
productButton.grid(row=0, column=1)

runButton = tk.Button(root, text = "Uruchom", command = openScript)
runButton.pack()

root.mainloop()

