import tkinter as tk
from tkinter import ttk, filedialog

from product import addProduct
from account import addAccount
from localization import addLocation
import chooseProducts
from db import Database

db = Database("store.db")
bgColor = 'white'
menuColor = 'white'
fontColor = 'black'

def openAddProduct():
    addProduct.AddProduct()

def openAddAccount(root):
    addAccount.AddAccount(root)

def openAddLocation():
    addLocation.AddLocation()

def openChooseProducts(iterrations, hide, email):
    chooseProducts.ChooseProducts(iterrations, hide, email)

root = tk.Tk()
root.configure(background=bgColor)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.title("Benia")

style = ttk.Style()
style.configure('TLabel', background=bgColor, foreground=fontColor, font=('Verdana', 12))
style.configure('TCheckbutton', background=bgColor)
min_w = 50
max_w = 150
cur_width = min_w
expanded = False

def raise_frame(frame):
    frame.tkraise()

def expand():
    global cur_width, expanded
    rep = root.after(5, expand)
    if expanded == False:
        cur_width += 5
        frame.config(width=cur_width)
    if cur_width >= max_w:
        expanded = True
        root.after_cancel(rep)
        fill()

def contract():
    global cur_width, expanded
    cur_width -= 5
    rep = root.after(5, contract)
    frame.config(width=cur_width)
    if cur_width <= min_w:
        expanded = False
        root.after_cancel(rep)
        fill()

def fill():
    if expanded:
        menuButton.config(image=closeIcon, command=contract)
        homeButton.config(image="", text="Strona główna", borderwidth=0)
        homeButton.grid_configure(pady=0)
        accountButton.config(image="", text="Konta", borderwidth=0)
        accountButton.grid_configure(pady=0)
        productButton.config(image="", text="Produkty", borderwidth=0)
        productButton.grid_configure(pady=0)
        locationButton.config(image="", text="Lokalizacje", borderwidth=0)
        locationButton.grid_configure(pady=0)
    else:
        menuButton.config(image=menuIcon, command=expand)
        homeButton.config(image=homeIcon, borderwidth=0)
        homeButton.grid_configure(pady=5)
        accountButton.config(image=accountIcon, borderwidth=0)
        accountButton.grid_configure(pady=5)
        productButton.config(image=productIcon, borderwidth=0)
        productButton.grid_configure(pady=5)
        locationButton.config(image=locationIcon, borderwidth=0)
        locationButton.grid_configure(pady=5)

menuIcon = tk.PhotoImage(file='icons/menu.png')
closeIcon = tk.PhotoImage(file='icons/close.png')
homeIcon = tk.PhotoImage(file='icons/home.png')
accountIcon = tk.PhotoImage(file='icons/account.png')
productIcon = tk.PhotoImage(file='icons/product.png')
locationIcon = tk.PhotoImage(file='icons/location.png')
root.update()
frameFake = tk.Frame(root, bg=menuColor, width=50, height=root.winfo_height(), borderwidth=1, relief=tk.RIDGE)
frameFake.grid(row=0, column=0, sticky='nws')
frame = tk.Frame(root, bg=menuColor, width=50, height=root.winfo_height(), borderwidth=1, relief=tk.RIDGE)
frame.grid(row=0, column=0, sticky='nws')



menuButton = tk.Button(frame, image=menuIcon, background=menuColor, fg=fontColor, relief=tk.SUNKEN, borderwidth=0, activebackground='white', command=lambda: expand())
menuButton.grid(row=1, column=0, pady=5, padx=(10, 10), sticky='nw')
homeButton = tk.Button(frame, image=homeIcon, background=menuColor, fg=fontColor, font=('MS Reference Sans Serif', 13), relief=tk.SUNKEN, borderwidth=0, activebackground='white', command=lambda: raise_frame(frame1))
homeButton.grid(row=2, column=0, pady=5, sticky='nwe')
accountButton = tk.Button(frame, image=accountIcon, background=menuColor, fg=fontColor, font=('MS Reference Sans Serif', 13), relief=tk.SUNKEN, borderwidth=0, activebackground='white', command=lambda: raise_frame(frame2))
accountButton.grid(row=3, column=0, pady=5, sticky='nwe')
productButton = tk.Button(frame, image=productIcon, background=menuColor, fg=fontColor, font=('MS Reference Sans Serif', 13), relief=tk.SUNKEN, borderwidth=0, activebackground='white', command=lambda: raise_frame(frame3))
productButton.grid(row=4, column=0, pady=5, sticky='nwe')
locationButton = tk.Button(frame, image=locationIcon, background=menuColor, fg=fontColor, font=('MS Reference Sans Serif', 13), relief=tk.SUNKEN, borderwidth=0, activebackground='white', command=lambda: raise_frame(frame4))
locationButton.grid(row=5, column=0, pady=5, sticky='nwe')

# frame.bind('<Enter>',lambda e: expand())
# frame.bind('<Leave>',lambda e: contract())

frame.grid_propagate(False)

frame2 = tk.Frame(root, bg=bgColor)
frame2.grid(row=0, column=1, sticky="nwse")

#DODAJ
frame2a = tk.Frame(frame2, relief=tk.RIDGE, borderwidth=1)
frame2a.grid(row=0, column=0)
tk.Label(frame2a, text="E-mail: ").grid(row=0, column=0)
email = tk.Entry(frame2a, textvariable=tk.StringVar())
email.grid(row=0, column=1)
tk.Label(frame2a, text="Hasło: ").grid(row=1, column=0)
password = tk.Entry(frame2a, textvariable=tk.StringVar())
password.grid(row=1, column=1)
button = tk.Button(frame2a, text="Zapisz", command=lambda: db.insert(email.get(), password.get()))
button.grid(row=3, column=1)

#EDYTUJ
frame2b = tk.Frame(frame2, relief=tk.RIDGE, borderwidth=1)
frame2b.grid(row=0, column=1)
tk.Label(frame2b, text="Email: ").grid(row=0, column=0)
combo = ttk.Combobox(frame2b, state="readonly", value=db.fetchEmails())
combo.grid(row=0, column=1)
button = tk.Button(frame2b, text="Edytuj")
button.grid(row=0, column=2)

#USUŃ
def updateCombo(combo):
    db.deleteA(combo.get())
    emails=db.fetchEmails()
    combo.config(value=emails[0])
    combo.set(emails)
frame2c = tk.Frame(frame2, relief=tk.RIDGE, borderwidth=1)
frame2c.grid(row=1, column=0)
tk.Label(frame2c, text="Email: ").grid(row=0, column=0)
combo = ttk.Combobox(frame2c, state="readonly", value=db.fetchEmails())
combo.grid(row=0, column=1)
button = tk.Button(frame2c, text="Usuń", command=lambda: updateCombo(combo))
button.grid(row=0, column=2)

frame3 = tk.Frame(root, bg=bgColor)
frame3.grid(row=0, column=1, sticky="nwse")

#DODAJ
imageNames=[]
def addImage(frame, button):
    i=4
    global imageNames
    imageNames=filedialog.askopenfilenames(initialdir="/", title="Wybierz zdjęcia", filetypes=[("Obrazy",".bmp .tif .tiff .png .gif .jpg .jpeg .jfif .pjpeg .pjp")])
    for name in imageNames:
        button.grid(row=i+1, column=1)
        label = tk.Label(frame, text=name)
        label.grid(row=i, column=2)
        deleteButton = tk.Button(frame, text="Usuń")
        deleteButton.grid(row=i, column=3)
        i+=1
def addProduct(product, title, price, desc, category):
    global imageNames
    db.insertP(product, title, price, desc, category)
    p = db.getP(product)[0]
    for name in imageNames:
        db.insertI(name, p)
frame3a = tk.Frame(frame3, relief=tk.RIDGE, borderwidth=1)
frame3a.grid(row=0, column=1)
tk.Label(frame3a, text="Produkt: ").grid(row=0, column=0)
product = tk.Entry(frame3a, textvariable=tk.StringVar())
product.grid(row=0, column=1)
tk.Label(frame3a, text="Tytuł: ").grid(row=1, column=0)
title = tk.Entry(frame3a, textvariable=tk.StringVar())
title.grid(row=1, column=1)
tk.Label(frame3a, text="Cena: ").grid(row=2, column=0)
price = tk.Entry(frame3a, textvariable=tk.IntVar())
price.grid(row=2, column=1)
tk.Label(frame3a, text="Opis: ").grid(row=3, column=0)
desc = tk.Entry(frame3a, textvariable=tk.StringVar())
desc.grid(row=3, column=1)
tk.Label(frame3a, text="Kategoria: ").grid(row=4, column=0)
l =[]
for i in db.fetchC():
    l.append(i[0])
combo = ttk.Combobox(frame3a, state="readonly", value=l)
combo.grid(row=4, column=1)
tk.Label(frame3a, text="Zdjęcia: ").grid(row=5, column=0)
images = tk.Button(frame3a, text="Wybierz", command=lambda: addImage(frame, button))
images.grid(row=5, column=1)
button = tk.Button(frame3a, text="Dodaj", command=lambda: addProduct(product.get(), title.get(), price.get(), desc.get(), db.getC(combo.get())))
button.grid(row=6, column=1)

#EDYTUJ
frame3b = tk.Frame(frame3, relief=tk.RIDGE, borderwidth=1)
frame3b.grid(row=0, column=2)
tk.Label(frame3b, text="Produkt: ").grid(row=0, column=0)
l = []
for i in db.fetchP():
    l.append(i[0])
combo = ttk.Combobox(frame3b, state="readonly", value=l)
combo.grid(row=0, column=1)
button = tk.Button(frame3b, text="Edytuj")
button.grid(row=0, column=2)

#USUŃ
def updateCombo(combo):
    db.deleteP(combo.get())
    products=db.fetchP()
    combo.config(value=products[0])
    combo.set(products)
frame3c = tk.Frame(frame3, relief=tk.RIDGE, borderwidth=1)
frame3c.grid(row=1, column=1)
tk.Label(frame3c, text="Produkt: ").grid(row=0, column=0)
combo = ttk.Combobox(frame3c, state="readonly", value=db.fetchP())
combo.grid(row=0, column=1)
button = tk.Button(frame3c, text="Usuń", command=lambda: updateCombo(combo))
button.grid(row=0, column=2)

frame4 = tk.Frame(root, bg=bgColor)
frame4.grid(row=0, column=1, sticky="nwse")

#DODAJ
def insertLocalization(location):
    db.insertL(location.get())
frame4a = tk.Frame(frame4, relief=tk.RIDGE, borderwidth=1)
frame4a.grid(row=0, column=1)
tk.Label(frame4a, text="Lokalizacja: ").grid(row=0, column=0)
location = tk.Entry(frame4a, textvariable=tk.StringVar())
location.grid(row=0, column=1)
button = tk.Button(frame4a, text="Dodaj", command=lambda: insertLocalization(location))
button.grid(row=0, column=2)

#EDYTUJ
frame4b = tk.Frame(frame4, relief=tk.RIDGE, borderwidth=1)
frame4b.grid(row=0, column=2)
tk.Label(frame4b, text="Lokalizacja: ").grid(row=0, column=0)
combo = ttk.Combobox(frame4b, state="readonly", value=db.fetchL())
combo.grid(row=0, column=1)
button = tk.Button(frame4b, text="Edytuj")
button.grid(row=0, column=2)

#USUŃ
def updateCombo(combo):
    db.deleteL(combo.get())
    locations=db.fetchL()
    combo.config(value=locations[0])
    combo.set(locations)
frame4c = tk.Frame(frame4, relief=tk.RIDGE, borderwidth=1)
frame4c.grid(row=1, column=1)
tk.Label(frame4c, text="Lokalizacja: ").grid(row=0, column=0)
combo = ttk.Combobox(frame4c, state="readonly", value=db.fetchL())
combo.grid(row=0, column=1)
button = tk.Button(frame4c, text="Usuń", command=lambda: updateCombo(combo))
button.grid(row=0, column=2)

frame1 = tk.Frame(root, bg=bgColor)
frame1.grid(row=0, column=1, sticky="nwse")
ttk.Label(frame1, text="Ukryj przed znajomymi: ").grid(row=0, column=0)
var1 = tk.IntVar()
ttk.Checkbutton(frame1, variable=var1).grid(row=0, column=1, sticky="w")
ttk.Label(frame1, text="Konto: ").grid(row=2, column=0)
combo1 = ttk.Combobox(frame1, state="readonly", value=db.fetchEmails())
#combo1.current(0)
combo1.grid(row=2, column=1, sticky="w")
ttk.Label(frame1, text="Ile ogłoszeń: ").grid(row=3, column=0)
iterrations = tk.Entry(frame1, textvariable=tk.IntVar(value=1))
iterrations.grid(row=3, column=1, sticky="w")
runButton = tk.Button(frame1, text="Uruchom", command=lambda: openChooseProducts(int(iterrations.get()), var1.get(), combo1.get()))
runButton.grid(row=4, column=1, sticky="w")

root.mainloop()