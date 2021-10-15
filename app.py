import tkinter as tk
from tkinter import ttk
from lib.classes import Hex, HexFlower, Zone
from lib.tkinter_classes import ControlPanel as CP
from lib.tkinter_classes import BoardWindow as BW
from xml.etree import cElementTree as ElementTree
import sys
from lib.xml_to_dict import xml2dict, etree_to_dict

def process_xml_hex_flower(xmlfile, diagnostic=False, side=20,
                           canvas_width=300, canvas_height=300) -> HexFlower:
    """
    This function takes an xml file and returns a HexFlower object. The other
    arguments are optional. These are:
        side: float or int, length of a hex edge
        canvas_width: int, width of the tk.Canvas
        canvas_height: int, height of the tk.Canvas
        diagnostic: bool, whether or not to generate diagnostic messages while 
            running
    """
    def str_to_tuple(s: str, f):
        """
        This function takes a string, creates a tuple and applies the function
        to each element of the tuple to produce the correct data type for each
        element. Best options are str to create a tuple of strings, or int to 
        create a tuple of integers (like coordinates).
        """
        # Remove parentheses.
        s = s.replace('(','')
        s = s.replace(')','')
        t = tuple(map(f, s.split(',')))
        return t
    
    tree = ElementTree.parse(xmlfile)
    if diagnostic:
        print(f"Printing ElementTree: {tree}")
    root = tree.getroot()
    if diagnostic:
        print(f"Printing root: {root}")
    flowerdata = xml2dict(root)
    if diagnostic:
        print(f"Data type is {type(flowerdata)}")
        print("Top level pairs are:")
        for k in flowerdata.keys():
            print(f"\t{k} : {flowerdata[k]}")
        print("First level pairs are")
        for k in flowerdata['hex_flower']:
            print(f"\t{k} : {flowerdata['hex_flower'][k]}")
    # Now, we have a dictionary we can parse to pull our Hex and HF 
    # attributes and data from. All attributes have an @name to separate
    # them from actual dictionaries as attributes.
    # First, we pull out the HF attributes.
    hex_flower = flowerdata['hex_flower']
    hexdata = hex_flower['hex']
    hftype = hex_flower['@type']
    hfdice = str_to_tuple(hex_flower['@dice'], str)
    if diagnostic:
        print(f"Extracted Hex Flower type: {hftype}")
        print(f"Extracted hfdice as type {type(hfdice)}: {hfdice}")
        print(f"Extracted hexdata as type {type(hexdata)}: {hexdata}")
    
    # Now, we have a list of dictionaries of hex data that need to be converted.
    hexes = []
    for i in range(len(hexdata)):
        zonedata = hexdata[i]['zone']
        adjacencydata = hexdata[i]['adjacency']
        hex_id = int(hexdata[i]['@id'])
        hex_vertex = str_to_tuple(hexdata[i]['@vertex'], int)
        if diagnostic:
            print(f"Extracted zone data as type {type(zonedata)}: {zonedata}")
            print(f"Extracted adjacency data as type {type(adjacencydata)}: {adjacencydata}")
            print(f"Extracted hex id as type {type(hex_id)}: {hex_id}")
            print(f"Extracted hex vertex as type {type(hex_vertex)}: {hex_vertex}")
        # Now, we pull the zone attributes from the zone dictionary.
        zone_type = zonedata['@type']
        zone_label = zonedata['@label']
        if zonedata['@icon'] == 'null':
            zone_icon = None
        else:
            zone_icon = zonedata['@icon']
        zone_color = zonedata['@color']
        if zonedata['@effect'] == 'null':
            zone_effect = None
        else:
            zone_effect = zonedata['@effect']
        if diagnostic:
            print(f"Extracted zone type as type {type(zone_type)}: {zone_type}")
            print(f"Extracted zone label as type {type(zone_label)}: {zone_label}")
            print(f"Extracted zone icon as type {type(zone_icon)}: {zone_icon}")
            print(f"Extracted zone color as type {type(zone_color)}: {zone_color}")
            print(f"Extracted zone effect as type {type(zone_effect)}: {zone_effect}")
        
        # Final step before converting this into Hex objects is to convert the
        # adjacency data. Currently, the values are strings. They need to ids of
        # hexes (integers) or None if the move is not allowed.
        adjacency = {}
        for k,v in adjacencydata.items():
            if v == 'null':
                adjacency[k] = None
            else:
                adjacency[k] = int(v)
        if diagnostic:
            print(f"Converted adjacency data to: type {type(adjacency)}: {adjacency}")

        new_hex = Hex(id=hex_id, vertex=hex_vertex, label=zone_label,
                      type=zone_type, color=zone_color, icon=zone_icon,
                      effect=zone_effect, adjacency=adjacency,
                      diagnostic=diagnostic)
        hexes.append(new_hex)
        if diagnostic:
            print(f"Created new hex: type: {type(new_hex)}: {new_hex}")
            print(f"Hex list is now: {hexes}")
    # Hexes have been assembled. We are ready to make a Hex Flower.
    return HexFlower(hexes=hexes, type=hftype, dice=hfdice, side=side,
                     height=canvas_height, width=canvas_width,
                     diagnostic=diagnostic)

# Setting default values. This should be changed at some point to allow the
# user to decide what to use instead.
canvas_width = 400
canvas_height = 400
side = 40
diagnostic = True
xmlfile = "./data/basic_hex_flower.xml"
rows = 2
cols = 2

root = CP()
# This is a temporary declaration. It will be replaced by a menu
# system for picking the HexFlower xml file.
xmlfile = root.openfile()
hf = process_xml_hex_flower(xmlfile=xmlfile, canvas_width=canvas_width,
                            canvas_height=canvas_height, side=side,
                            diagnostic=diagnostic)
board = BW(root)
canvas = tk.Canvas(board, width=canvas_width, height=canvas_height)
canvas.grid(row=0, column=0)

ttk.Button(board,
           text='Close',
           command=board.destroy).place(x=0, y=375)
ttk.Button(board,
           text='Start Walk',
           command=print).place(x=100, y=375)
ttk.Button(board,
           text='Stop Walk',
           command=print).place(x=200, y=375)

hf.drawHexFlower(canvas, diagnostic=diagnostic, width=3)
tk.mainloop()