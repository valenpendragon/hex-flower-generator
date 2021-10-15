import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

class ControlPanel(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('400x400')
        self.title("Hex Flower Generator")

        ttk.Button(self,
                   text='File Open',
                   command=self.callback).grid(row=0, column=0)
        
    def callback(self):
        name = fd.askopenfilename()
        return name

class BoardWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("400x400+10+10")
        self.title("Hex Flower")
