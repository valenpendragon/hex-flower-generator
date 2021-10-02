import tkinter as tk
from lib.classes import Hex
import math


class HexFlower():
    """
    This class takes a list of 19 Hex objects and adds them in the
    order of the Hex.number value. They need to be numbered 1 through 19
    in the Hex.number attribute.

    Class Attributes are:
        hexes: a list of 19 Hex objects
        side: the length of a side, default 20
        canvas_height: the tk.Canvas height, default=300
        canvas_width: the tk.Canvas width, default=300
     
    Methods:
        proximity: Cartesian distance between a point and the center of each
                   Hex object, returns a list of tuples sorted by proximity
                   tuples are (distance to Hex, Hex.number)

    """
    def __init__(self, hexes, side=20.0, height=300, width=300):
        self.hexes = []
        for i in range(1, 20):
            for hex in hexes:
                if isinstance(hex, Hex):
                    raise TypeError("HexFlower cannot import lists of non-Hex objects.")
                if hex.number == i:
                    self.extend(hex)
                else:
                    continue
        if isinstance(side, int) or isinstance(side, float):
            self.side = side
        else:
            raise TypeError("Side lenght must be a number.")
        if isinstance(height, int):
            self.canvas_height = height
        else:
            raise TypeError("Height must be an integer for tk.Canvas objects.")
        if isinstance(width, int):
            self.canvas_width = width
        else:
            raise TypeError("Height must be an integer for tk.Canvas objects.")
        print("HexFlower initialized")

    def __str__(self) -> str:
        s = ''
        for i in range(19):
            s = s + 'Hex: {}'.format(self[i].__str__())
        return s

    def __repr__(self) -> str:
        pass
    
    def proximity(self, point: tuple):
        """
        This method determines if a point is contained in any Hex object
        contained in this HexFlower. Returns either None or Hex.number.
        """
        def prox(point, center):
            x1, x2 = point
            y1, y2 = center
            return math.sqrt( (x2 - x1) ** 2 + (y2 - y1) ** 2 )

        # First we eliminate hexes further out than HF.side since they
        # cannot contain the point.
        close_hexes = []
        for hex in self.hexes:
            if prox(point, hex.center(self.side)) < self.side:
                close_hexes.extend(hex)
        if len(close_hexes ) == 0:
            return None
        elif len(close_hexes) == 1:
            return close_hexes[0].number
        else: # More than one are very close. Point is inside the HF.
            closest = close_hexes[0]
            counter = 0
            for hex in close_hexes:
                if counter == 0: # first cycle
                    prox_closest = prox(point, hex.center())
                elif prox(point, hex.center()) < prox_closest:
                    closest = hex
                counter += 1
            return closest.number
