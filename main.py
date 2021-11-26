import tkinter as tk
from tkinter import ttk

from product import addProduct
from product import editProduct
from product import deleteProduct
from account import addAccount
from account import editAccount
from account import deleteAccount
from localization import addLocation
from localization import editLocation
from localization import deleteLocation
import chooseProducts
from db import Database
db = Database("store.db")
bgColor = '#181818'
menuColor = '#212121'
fontColor = 'white'


root = tk.Tk()
root.configure(background=bgColor)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.title("Tworzenie ogłoszeń")

style = ttk.Style()
style.configure('TLabel', background=bgColor, foreground=fontColor, font=('Verdana', 12))
style.configure('TCheckbutton', background=bgColor)

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

def openChooseProducts(iterrations, hide, email):
    chooseProducts.ChooseProducts(iterrations, hide, email)

def menuPart(name, commandAdd, commandEdit, commandDelete):
    settingsMenu = tk.Menu(myMenu, tearoff="off")
    myMenu.add_cascade(label=name, menu=settingsMenu)
    settingsMenu.add_command(label="Dodaj", command=commandAdd)
    settingsMenu.add_command(label="Edytuj", command=commandEdit)
    settingsMenu.add_command(label="Usuń", command=commandDelete)

myMenu = tk.Menu(root)
root.config(menu=myMenu)

menuPart("Konto", openAddAccount, openEditAccount, openDeleteAccount)

menuPart("Produkt", openAddProduct, openEditProduct, openDeleteProduct)

menuPart("Lokalizacja", openAddLocation, openEditLocation, openDeleteLocation)


frame1 = tk.Frame(root, bg=bgColor)
frame1.grid(row=0, column=1)
#frame1.place(relwidth=1, relheight=1)
ttk.Label(frame1, text="Ukryj przed znajomymi: ").grid(row=0, column=0)
var1 = tk.IntVar()
ttk.Checkbutton(frame1, variable=var1).grid(row=0, column=1)

ttk.Label(frame1, text="Konto: ").grid(row=2, column=0)
combo1 = ttk.Combobox(frame1, state="readonly", value=db.fetchEmails())
#combo1.current(0)
combo1.grid(row=2, column=1)

ttk.Label(frame1, text="Ile ogłoszeń: ").grid(row=3, column=0)
iterrations = tk.Entry(frame1, textvariable=tk.IntVar(value=1))
iterrations.grid(row=3, column=1)

runButton = tk.Button(frame1, text="Uruchom", command=lambda: openChooseProducts(int(iterrations.get()), var1.get(), combo1.get()))
runButton.grid(row=4, column=1)

root.mainloop()