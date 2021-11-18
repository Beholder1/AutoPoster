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

#canvas = tk.Canvas(root, height = 500, width = 500)
#canvas.pack()






# min_w = 50 # Minimum width of the frame
# max_w = 200 # Maximum width of the frame
# cur_width = min_w # Increasing width of the frame
# expanded = False # Check if it is completely exanded
#
# def expand():
#     global cur_width, expanded
#     rep = root.after(5, expand)
#     if expanded == False:
#         cur_width += 10 # Increase the width by 10
#         frame.config(width=cur_width) # Change the width to new increase width
#     if cur_width >= max_w: # If width is greater than maximum width
#         expanded = True # Frame is expended
#         root.after_cancel(rep) # Stop repeating the func
#         fill()
#
# def contract():
#     global cur_width, expanded
#     cur_width -= 10 # Reduce the width by 10
#     rep = root.after(5,contract) # Call this func every 5 ms
#     frame.config(width=cur_width) # Change the width to new reduced width
#     if cur_width <= min_w: # If it is back to normal width
#         expanded = False # Frame is not expanded
#         root.after_cancel(rep) # Stop repeating the func
#         fill()
#
# def fill():
#     if expanded:
#         menuButton.config(image=closeIcon, command=contract)
#         homeButton.config(image="", text="Strona główna")
#         accountButton.config(image="", text="Konta")
#         productButton.config(image="", text="Produkty")
#         locationButton.config(image="", text="Lokalizacje")
#     else:
#         menuButton.config(image=homeIcon, command=expand)
#         homeButton.config(image=closeIcon)
#         accountButton.config(image=closeIcon)
#         productButton.config(image=closeIcon)
#         locationButton.config(image=closeIcon)
#
# closeIcon = tk.PhotoImage(file='icons/home.png')
# homeIcon = tk.PhotoImage(file='icons/menu.png')
# root.update() # For the width to get updated
# frame = tk.Frame(root,bg=menuColor,width=50,height=root.winfo_height())
# frame.grid(row=0,column=0, sticky='nws')
#
#
# menuButton = tk.Button(frame,image=homeIcon,background=menuColor, fg=fontColor, relief='flat', command=expand)
# menuButton.grid(row=1,column=0,pady=5)
# homeButton = tk.Button(frame,image=closeIcon,background=menuColor, fg=fontColor,relief='flat', command=expand)
# homeButton.grid(row=2,column=0,pady=5)
# accountButton = tk.Button(frame,image=closeIcon,background=menuColor, fg=fontColor,relief='flat', command=expand)
# accountButton.grid(row=3,column=0,pady=5)
# productButton = tk.Button(frame,image=closeIcon,background=menuColor, fg=fontColor,relief='flat', command=expand)
# productButton.grid(row=4,column=0,pady=5)
# locationButton = tk.Button(frame,image=closeIcon,background=menuColor, fg=fontColor,relief='flat', command=expand)
# locationButton.grid(row=5,column=0,pady=5)
#
#
# # Bind to the frame, if entered or left
# #frame.bind('<Enter>',lambda e: expand())
# #frame.bind('<Leave>',lambda e: contract())
#
# # So that it does not depend on the widgets inside the frame
# frame.grid_propagate(False)







myMenu = tk.Menu(root)
root.config(menu=myMenu)

menuPart("Konto", openAddAccount, openEditAccount, openDeleteAccount)

menuPart("Produkt", openAddProduct, openEditProduct, openDeleteProduct)

menuPart("Lokalizacja", openAddLocation, openEditLocation, openDeleteLocation)


frame1 = tk.Frame(root, bg=bgColor)
frame1.grid(row=0, column=1, sticky="nw")
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