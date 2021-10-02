from collections import OrderedDict
import tkinter as tk
from Tools.pynche import ColorDB
import os
import colorsys
import math

class Hex():
    def __init__(self, number: int, vertex: tuple,
                 label: str, adjacency: dict,
                 color=None, icon=None):
        """
        This class requires a dictionary of values of the following form:
            number : int, number of the hex (1-19)
            vertex : tuple (x, y), coordinates of the left lower corner
                        on the tk.Canvas for this hex to appear.
            label  : str, what should appear if the icon is None
            color  : str, the value of the outline and/or fill of the hex,
                        it is also the severity of the outcome
            icon   : filename or None, icon that will be displayed in the hex
            adjacency : dictionary storing the next hex in the flower to move
                        to by edge of the hex numbered a through f starting at
                        the top of the hex. Any adjacency that is None prevents
                        movement for this turn
                a : top hex    b: upper right hex   c: lower right hex
                d : bottom hex e: lover left hex    f: upper left hex          
        """
        self.number = number
        x,y = vertex
        if (isinstance(x, int) or isinstance(x, float)) and \
            (isinstance(y, int) or isinstance(y, float)):
            self.vertex = vertex
        else:
            raise TypeError("Vertex coordinates must be a numbers")
        self.label = str(label)
        # Checking to see if color value set is valid.
        if color is None:
            self.color='white'
        else:
            if isinstance(color, str):
                rgb_file = os.path.join(os.path.dirname(ColorDB.__file__),
                                        'X', 'rgb.txt')
                rgb_db = ColorDB.get_colordb(rgb_file)
                colors = [x.lower().replace(' ', '') for x in rgb_db.unique_names()]
                if color not in colors:
                    raise ValueError("String is not a valid color for Python or tkinter")
                else:
                    self.color = color
            else:
                raise ValueError("color must be a string for a valid color for Python or tkinter")
        self.icon = icon
        if isinstance(adjacency, dict):
            for k in {'a', 'b', 'c', 'd', 'e', 'f'}:
                self.adjacency[k] = adjacency[k]
        else:
            raise ValueError("Adjacency must be a dictionary with a, b, c, d, e, and f adjacent hex nubmers.")
        print(self)

    def __str__(self):
        s = "Hex with attributes: number = {}, vertex = {}\n".format(self.number, 
                                                                     self.vertex)
        s = s + "label = {}, color = {}, icon = {}\n".format(self.label,
                                                             self.color,
                                                             self.icon)
        s = s + "Adjency: {" + ",".join() + "}"
        return s

    def __repr__(self):
        pass

    def center(self, side=20):
        """
        This method returns a tuple (x,y) coordinates of the center of this
        Hex object. It requires a value of side, but allows for a default of 20.
        """
        c_x = round(side * math.cos(math.pi / 3) + self.vertex[0])
        c_y = round(side * math.sin(math.pi / 3) + self.vertex[1])
        return (c_x, c_y)