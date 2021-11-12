import tkinter as tk
from tkinter import ttk
from db import Database
from tkinter import filedialog

db = Database("store.db")

class AddProduct:
    def __init__(self):
        def addImage(frame, button):
            i=4
            imageNames=filedialog.askopenfilenames(initialdir="/", title="Wybierz zdjęcia", filetypes=[("Obrazy",".bmp .tif .tiff .png .gif .jpg .jpeg .jfif .pjpeg .pjp")])
            for name in imageNames:
                button.grid(row=i+1, column=1)
                label = tk.Label(frame, text=name)
                label.grid(row=i, column=2)
                deleteButton = tk.Button(frame, text="Usuń")
                deleteButton.grid(row=i, column=3)
                i+=1

        root = tk.Tk()
        canvas = tk.Canvas(root, height=700, width=700)
        canvas.pack()

        frame = tk.Frame(root)
        frame.place(relwidth=1, relheight=1)

        tk.Label(frame, text="Produkt: ").grid(row=0, column=0)
        product = tk.Entry(frame, textvariable=tk.StringVar())
        product.grid(row=0, column=1)

        tk.Label(frame, text="Tytuł: ").grid(row=1, column=0)
        title = tk.Entry(frame, textvariable=tk.StringVar())
        title.grid(row=1, column=1)

        tk.Label(frame, text="Cena: ").grid(row=2, column=0)
        price = tk.Entry(frame, textvariable=tk.IntVar())
        price.grid(row=2, column=1)

        tk.Label(frame, text="Opis: ").grid(row=3, column=0)
        desc = tk.Entry(frame, textvariable=tk.StringVar())
        desc.grid(row=3, column=1)

        tk.Label(frame, text="Kategoria: ").grid(row=4, column=0)

        l =[]
        for i in db.fetchC():
            l.append(i[0])

        combo = ttk.Combobox(frame, state="readonly", value=l)
        combo.grid(row=4, column=1)

        tk.Label(frame, text="Zdjęcia: ").grid(row=5, column=0)
        images = tk.Button(frame, text="Wybierz", command=lambda: addImage(frame, button))
        images.grid(row=5, column=1)

        button = tk.Button(frame, text="Dodaj", command=lambda: db.insertP(product.get(), title.get(), price.get(), desc.get(), db.getC(combo.get())))
        button.grid(row=6, column=1)



        root.mainloop()