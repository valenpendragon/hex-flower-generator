import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import sys

class ControlPanel(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('1020x600')
        self.title("Hex Flower Generator")
        self.frame = (self)
        menu=tk.Menu(self.frame)
        self.config(menu=menu)
        filemenu = tk.Menu(menu)
        menu.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label='Exit', command=sys.exit)
       
    def openfile(self):
        name = fd.askopenfilename(initialdir="./data", title="Select XML File")
        return name

class BoardWindow(tk.Toplevel):
    def __init__(self, parent, width, height):
        super().__init__(parent)
        self.geometry("400x400")
        self.title("Hex Flower")
        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.grid(row=0, column=0)
        self.canvas.labels = []