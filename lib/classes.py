import tkinter as tk
from Tools.pynche import ColorDB
import os
import colorsys
import math

class HexFlower():
    """
    This class takes a list of 19 Hex objects and adds them in the
    order of the Hex.number value. They need to be numbered 1 through 19
    in the Hex.number attribute.

    Class Attributes are:
        hexes: list, required, a list of 19 Hex objects
        type: str, required, indicates the type of Hex Flower
        dice: tuple of str, optional, default is ('d6', 'd6')
        side: integer, optional, the length of a side, default 20
        canvas_height: integer, optional, the tk.Canvas height, default=300
        canvas_width: integer, optional, the tk.Canvas width, default=300
     
    Methods:
        proximity: Cartesian distance between a point and the center of each
                   Hex object, returns a list of tuples sorted by proximity
                   tuples are (distance to Hex, Hex.number)
        drawHexFlower : this method draws the Hex Flower on the supplied 
                   canvas, using the attributes already designated in the
                   HF attributes and Hex attributes
    """
    def __init__(self, hexes, type: str, 
                 dice=('d6', 'd6'), side=20.0, 
                 height=300, width=300,                  
                 diagnostic=False):
        self.hexes = []
        for i in range(1, 20):
            for hex in hexes:
                if isinstance(hex, Hex):
                    raise TypeError("HexFlower cannot import lists of non-Hex objects.")
                if hex.number == i:
                    self.extend(hex)
                else:
                    continue
        self.type = type
        if len(dice) > 3 or len(dice) < 1 or dice is None:
            raise ValueError("Improper number of dice specified. Must 1, 2 or 3")
        else:
            # Checking to make sure the dice are specified correctly, They need
            # span 1-6 (d6), 1-8 (d8), 2-12 (2d6), 3-12 (3d4), or 2-14 (d6 + d8).
            dice_options = [
                ('d6'), ('d8'), ('d6', 'd6'), ('d4','d4', 'd4'), ('d6','d8')
            ]
            if dice not in dice_options:
                raise ValueError(f"{dice} is not a valid option. Dice must be {dice_options}.")
            else:
                self.dice = dice
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
        if diagnostic:
            print("HexFlower initialized")

    def __str__(self) -> str:
        s = ''
        for i in range(19):
            s = s + 'Hex: {}'.format(self[i].__str__())
        return s

    def __repr__(self) -> str:
        pass
    
    def proximity(self, point: tuple, diagnostic=False):
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
                if diagnostic:
                    print(f"close_hexes: {close_hexes}")
        if len(close_hexes ) == 0:
            return None
        elif len(close_hexes) == 1:
            return close_hexes[0].number
        else: # More than one are very close. Point is inside the HF.
            closest = close_hexes[0]
            counter = 0
            for hex in close_hexes:
                if diagnostic:
                    print(f"Begin loop: Closest: {closest}, counter: {counter}")
                if counter == 0: # first cycle
                    prox_closest = prox(point, hex.center())
                elif prox(point, hex.center()) < prox_closest:
                    closest = hex
                counter += 1
                if diagnostic:
                    print(f"End loop: Closest: {closest}, counter: {counter}")
            return closest.number

    def drawHexFlower(self, canvas: tk.Canvas,
                      width=3, diagnostic=False):
        """
        This method draws the HF on the canvas supplied to it. Start locations,
        color, and length of a side of each hex are supplied by Hex attributes.
        width has a default, but can be supplied. diagnostic determines how
        much text gets sent to stdio while it is runnin.
        """
        if diagnostic:
            print(f"drawHexFlower: Arguments received: {locals()}")
            print(f"Hex Flower status: {self}")
        # We need a list of labels.
        labels = []
        ctr = 0
        for hex in self.hexes:
            points = []
            x_c, y_c = hex.center(side=self.side, diagnostic=diagnostic)
            x, y = hex.vertex
            # Add the starting point.
            points.extend((x,         y))
            points.extend((x + s,     y))
            points.extend((x + b + s, y + h))
            points.extend((x + s,     y + 2 * h))
            points.extend((x,         y + 2 * h))
            points.extend((x - b,     y + h))
            if diagnostic:
                print(points)
            if hex.color:
                outline=hex.color
            else:
                outline="black"
            fill=None # I will probably change this later.
            canvas.create_polygon(points,
                                  outline=outline,
                                  fill=fill,
                                  width=width)
            if hex.icon:
                icon = tk.PhotoImage(file=hex.icon)
                labels[ctr].extend(tk.Label(canvas, image=icon))
            else:
                labels[ctr].extend(tk.Label(canvas, text=hex.label))
            labels[ctr].place(x=x_c, y=y_c, anchor=tk.CENTER)
            ctr += 1

class Hex():
    def __init__(self, number: int, vertex: tuple,
                 label: str, zone : str,
                 adjacency: dict,
                 color=None, icon=None, effect=None,
                 diagnostic=False):
        """
        This class requires a dictionary of values of the following form:
            number : int, , required, number of the hex (1-19)
            vertex : tuple (x, y), required, coordinates of the left lower corner
                        on the tk.Canvas for this hex to appear.
            label  : str, required, what should appear if the icon is None
            color  : str, optional, the value of the outline of the hex, it 
                        can indicate the severity of the outcome
            icon   : filename or None, optional. icon that will be displayed 
                        in the hex if specified
            zone   : str, required, describes threat level of this section
                        of the Hex Flower, may alter the color of the Hex fill
            effect : str or None, optional, this describes the outcome of 
                        landing here
            adjacency : dictionary storing the next hex in the flower to move
                        to by edge of the hex numbered a through f starting at
                        the top of the hex. Any adjacency that is None prevents
                        movement for this turn
                a : top hex    b: upper right hex   c: lower right hex
                d : bottom hex e: lover left hex    f: upper left hex 
                A None values means movement is blocked in that direction out
                of the hex and the walk stays here for the next effect/outcome.
        The diagnostic argument indicates if the program is running in diagnostic
        mode, which prints logs to stdio.

        Methods:
            center : returns that coordinates of the center of the hex, has an
                        has an optional side length for the side of the hex when
                        printed on the canvas
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
            self.color='black'
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
        self.zone = zone
        self.effect = effect
        if isinstance(adjacency, dict):
            for k in {'a', 'b', 'c', 'd', 'e', 'f'}:
                self.adjacency[k] = adjacency[k]
        else:
            raise ValueError("Adjacency must be a dictionary with a, b, c, d, e, and f adjacent hex numbers.")
        if diagnostic:
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

    def center(self, side=20, diagnostic=False):
        """
        This method returns a tuple (x,y) coordinates of the center of this
        Hex object. It requires a value of side, but allows for a default of 20.
        """
        c_x = round(side * math.cos(math.pi / 3) + self.vertex[0])
        c_y = round(side * math.sin(math.pi / 3) + self.vertex[1])
        if diagnostic:
            print(f"Center of hex is: ({c_x},{c_y})")
        return (c_x, c_y)