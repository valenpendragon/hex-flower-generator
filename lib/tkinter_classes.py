import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import sys

class ControlPanel(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('400x400')
        self.title("Hex Flower Generator")
        menu=tk.Menu(self)
        self.config(menu=menu)
        filemenu = tk.Menu(menu)
        menu.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label="Open...", command=self.openfile)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=sys.exit)
        helpmenu = tk.Menu(menu)
        menu.add_cascade(label='Help', menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.about)
        
    def openfile(self):
        name = fd.askopenfilename()
        return name
    
    def about(self):
        print("Needs an about dialog")
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
