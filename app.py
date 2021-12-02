import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog as sd
from lib.classes import Hex, HexFlower, Zone, BasicWalk
from lib.tkinter_classes import ControlPanel as CP
from lib.tkinter_classes import BoardWindow as BW
import sys, random
from lib.xml_functions import process_xml_hex_flower

def initiate_walk():
    global start
    walk = BasicWalk(hf=hf, start=start, moves=walk_length, diagnostic=diagnostic)
    for i in range(walk_length):
        current_hex = walk.completeMove(root, diagnostic=diagnostic,
                          output_file=walk_output_file)
    msg = "All moves also written to output file: {}.".format(walk_output_file)
    label = tk.Label(root.frame, text=msg)
    label.grid(row=28, column=0, columnspan=2, sticky=tk.W)
    start = int(current_hex)


# Setting default values. This should be changed at some point to allow the
# user to decide what to use instead.
diagnostic = True
canvas_width = 400
canvas_height = 400
side = 40
logging = True
log_file = "./log/log"
walk_length = 15
walk_output_file = "./output/walk_resulfs.csv"
start = 1
walk_type = 'basic'

root = CP()

if logging:
    sys.stdout = open(log_file, "w")

# Next, we set the walk length for "infinite walks" (aka walks that do not have
# and imbedded self-termination).
w_answer = sd.askinteger("Walk Length",
    "How long do you want this walk to be (default is 15 steps)?",
    parent=root, minvalue=10, maxvalue=75, initialvalue=walk_length)
if w_answer != 15:
    walk_length = w_answer

# Next, we set the output file for the CSV output.
f_answer = sd.askstring("Output File",
    "Give a file name for output of this walk (writes to ./output):",
    parent=root, initialvalue=walk_output_file)
if f_answer != walk_output_file:
    walk_output_file = f_answer

# Next, we designate the starting hex.
s_answer = sd.askinteger("Starting Hex",
    "Which hex do want to start the walk?\n 1-10 is preferable, 1-19 is acceptable.",
    parent=root, minvalue=1, maxvalue=19, initialvalue=start)
if s_answer != start:
    start = s_answer

# Now, we get the desired xml file containing the Hex Flower data.
xmlfile = None
while xmlfile == '' or xmlfile is None:
    xmlfile = root.openfile()
if diagnostic:
    print(f"Information collected: Walk is {w_answer} steps, starting at {s_answer}.")
    print(f"Hex Flower file is {xmlfile} with output to {f_answer}.")
hf = process_xml_hex_flower(xmlfile=xmlfile, canvas_width=canvas_width,
                            canvas_height=canvas_height, side=side,
                            diagnostic=diagnostic)
board = BW(root, width=canvas_width, height=canvas_height)
# A canvas is needed for the window that we write the polygons that form the
# HexFlower. We add control buttons using the C.place() method to make the 
# run start easier for the User. BW Contains such buttons and canvas.
#canvas = tk.Canvas(board, width=canvas_width, height=canvas_height)
#canvas.grid(row=0, column=0)

ttk.Button(board,
           text='Close',
           command=board.destroy).place(x=0, y=375)
ttk.Button(board,
           text='Start Walk',
           command=initiate_walk).place(x=100, y=375)
hf.drawHexFlower(board, diagnostic=diagnostic, width=3)
tk.mainloop()