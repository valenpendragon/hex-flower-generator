import tkinter as tk
from lib.classes import Hex, HexFlower
from xml.etree import cElementTree as ElementTree
import sys
from lib.xml_to_dict import xml2dict, etree_to_dict

tree = ElementTree.parse("./data/basic_hex_flower.xml")
print(f"Printing ElementTree: {tree}")
root = tree.getroot()
print(f"Printing root: {root}")
xmldata = xml2dict(root)
print(f"Printing xmldata: {xmldata}")