import tkinter as tk
from tkinter import ttk


class EditProduct:
    def __init__(self, product, db):
        self.db = db
        root = tk.Tk()
        root.configure(background="white")
        root.title("Edytuj produkt")
        self.product = product
        wholeProduct = db.getP(self.product)
        style = ttk.Style()

        def updateProduct():
            self.db.update("product", "productName", entry1.get(), "productName", self.product)
            self.product = entry1.get()

        def addCategory():
            addButton.grid_forget()
            label1 = tk.Label(frame1, text="Kategoria " + str(self.counter) + ":", background="white",
                              foreground="black", font=('Verdana', 12))
            label1.grid(row=3 + self.counter, column=0)
            l1 = []
            for i in db.fetch("categories", "category"):
                l1.append(i[0])
            entry5 = ttk.Combobox(frame1, state="readonly", value=l1)
            entry5.grid(row=3 + self.counter, column=2)
            button1 = tk.Button(frame1, text="Dodaj")
            button1.configure(command=lambda: executeAdding(button1, entry5, label1))
            button1.grid(row=3 + self.counter, column=3)
            self.counter += 1

        def executeAdding(button2, entry6, label2):
            addButton.grid_configure(row=4 + self.counter, column=3)
            db.insertC(productId, db.getC(entry6.get()))
            g = db.getC(entry6.get())
            button2.configure(text="Edytuj", command=lambda: db.updateC(db.getC(entry6.get()), str(productId), str(g)))
            button3 = tk.Button(frame1, text="Usuń")
            button3.configure(
                command=lambda c=entry6.get(), b=button2, e=entry6, b1=button3, l=label2: executeDelete(db.getC(c), b,
                                                                                                        e, b1, l))
            button3.grid(row=3 + self.counter - 1, column=4)

        def executeDelete(categoryToDelete, buttonTD, entryTD, button1TD, labelTD):
            db.removeC(str(productId), str(categoryToDelete))
            buttonTD.destroy()
            entryTD.destroy()
            button1TD.destroy()
            labelTD.destroy()

        frame1 = tk.Frame(root, relief=tk.RIDGE, borderwidth=1, background="white")
        frame1.grid(row=0, column=1)

        ttk.Label(frame1, text="Nazwa: ", background="white", foreground="black", font=('Verdana', 12)).grid(row=0,
                                                                                                             column=0)
        ttk.Label(frame1, text=wholeProduct[1], background="white", foreground="black", font=('Verdana', 12)).grid(
            row=0, column=1)
        entry1 = ttk.Entry(frame1)
        entry1.grid(row=0, column=2)
        button = tk.Button(frame1, text="Edytuj", command=lambda: updateProduct())
        button.grid(row=0, column=3)

        ttk.Label(frame1, text="Tytuł: ", background="white", foreground="black", font=('Verdana', 12)).grid(row=1,
                                                                                                             column=0)
        ttk.Label(frame1, text=wholeProduct[2][0: 15] + "...", background="white", foreground="black",
                  font=('Verdana', 12)).grid(row=1, column=1)
        entry2 = ttk.Entry(frame1)
        entry2.grid(row=1, column=2)
        button = tk.Button(frame1, text="Edytuj",
                           command=lambda: db.update("product", "title", entry2.get(), "productName", self.product))
        button.grid(row=1, column=3)

        ttk.Label(frame1, text="Cena: ", background="white", foreground="black", font=('Verdana', 12)).grid(row=2,
                                                                                                            column=0)
        ttk.Label(frame1, text=wholeProduct[3], background="white", foreground="black", font=('Verdana', 12)).grid(
            row=2, column=1)
        entry3 = ttk.Entry(frame1)
        entry3.grid(row=2, column=2)
        button = tk.Button(frame1, text="Edytuj",
                           command=lambda: db.update("product", "price", entry3.get(), "productName", self.product))
        button.grid(row=2, column=3)

        ttk.Label(frame1, text="Opis: ", background="white", foreground="black", font=('Verdana', 12)).grid(row=3,
                                                                                                            column=0)
        ttk.Label(frame1, text=wholeProduct[4][0: 15] + "...", background="white", foreground="black",
                  font=('Verdana', 12)).grid(row=3, column=1)
        entry4 = ttk.Entry(frame1)
        entry4.grid(row=3, column=2)
        button = tk.Button(frame1, text="Edytuj",
                           command=lambda: db.update("product", "description", entry4.get(), "productName",
                                                     self.product))
        button.grid(row=3, column=3)

        productId = wholeProduct[0]
        categories = db.getPC(productId)
        self.counter = 1
        for category in categories:
            label = ttk.Label(frame1, text="Kategoria " + str(self.counter) + ":", background="white",
                              foreground="black", font=('Verdana', 12))
            label.grid(row=3 + self.counter, column=0)
            l1 = []
            for i in db.fetch("categories", "category"):
                l1.append(i[0])
            entry4 = ttk.Combobox(frame1, state="readonly", value=l1)
            entry4.grid(row=3 + self.counter, column=2)
            button = tk.Button(frame1, text="Edytuj",
                               command=lambda c=category[0], e=entry4: db.updateC(db.getC(e.get()),
                                                                                  str(productId), str(c)))
            button.grid(row=3 + self.counter, column=3)
            if self.counter != 1:
                button1 = tk.Button(frame1, text="Usuń")
                button1.configure(
                    command=lambda c=category[0], b=button, e=entry4, b1=button1, l=label: executeDelete(c, b, e, b1,
                                                                                                         l))
                button1.grid(row=3 + self.counter, column=4)
            self.counter += 1
        addButton = tk.Button(frame1, text="Dodaj kategorię",
                              command=lambda: addCategory())
        addButton.grid(row=3 + self.counter, column=3)

        root.mainloop()
