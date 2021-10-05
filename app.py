import tkinter as tk
from lib.classes import Hex, HexFlower
from xml.etree import cElementTree as ElementTree
import sys
from lib.xml_to_dict import xml2dict, etree_to_dict

tree = ElementTree.parse("./data/basic_hex_flower.xml")
print(f"Printing ElementTree: {tree}")
root = tree.getroot()
print(f"Printing root: {root}")
flowerdata = xml2dict(root)
print(f"Printing xmldata: {flowerdata}")
# Now, we have a dictionary we can parse to pull our Hex and HF attributes
# and data from. All attributes have an @name to separate them from actual
# dictionaries as attributes.
