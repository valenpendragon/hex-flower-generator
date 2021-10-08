import tkinter as tk
from Tools.pynche import ColorDB
import os
import colorsys
import math

class HexFlower():
    """
    This class takes a list of 19 Hex objects and adds them in the
    order of the Hex.id value. They need to be numbered 1 through 19
    in the Hex.id attribute.

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
                   tuples are (distance to Hex, Hex.id)
        drawHexFlower: this method draws the Hex Flower on the supplied 
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
                if hex.id == i:
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
            raise TypeError("Side length must be a number.")
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
        s = "HexFlower(hexes={}, type={}, ".format(self.hexes, self.type)
        s = s + "dice={}, side={}, ".format(self.dice, self.side)
        s = s + "canvas_height={}, ".format(self.canvas_height)
        s = s + "canvas_width={})".format(self.canvas_width)
        return s
    
    def proximity(self, point: tuple, diagnostic=False):
        """
        This method determines if a point is contained in any Hex object
        contained in this HexFlower. Returns either None or Hex.id.
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
            return close_hexes[0].id
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
            return closest.id

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
            if hex.zone.color:
                outline=hex.zone.color
            else:
                outline="black"
            fill=None # I will probably change this later based on zone.effect.
            canvas.create_polygon(points,
                                  outline=outline,
                                  fill=fill,
                                  width=width)
            if hex.zone.icon:
                icon = tk.PhotoImage(file=hex.zone.icon)
                labels[ctr].extend(tk.Label(canvas, image=icon))
            else:
                labels[ctr].extend(tk.Label(canvas, text=hex.zone.label))
            labels[ctr].place(x=x_c, y=y_c, anchor=tk.CENTER)
            ctr += 1

class Zone():
    """
    Zone have the following attributes: 
        type: str, required, default is 'normal',
        color: str, required, no default
        label: str, required, no default, but it is often str(Hex.id)
        icon: str, optional, str is the relative path and filename of the icon
               to be displayed in this Hex when the Hex Flower is drawn,
               default is None
        effect: str, optional, description of the severity of the zone in 
                this Hex will appear, default is None
    If the icon is None, the label will be displayed instead of an icon.
    """
    def __init__(self, color: str, label:str,
                 type='normal', icon=None, effect=None,
                 diagnostic=False):
        self.type = type
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
                if diagnostic:
                    print(f"Colors are {colors}")
                if color not in colors:
                    raise ValueError(f"String '{color}' is not a valid color for Python or tkinter")
                else:
                    self.color = color
            else:
                raise ValueError("color must be a string for a valid color for Python or tkinter")
        self.icon = icon
        self.effect = effect
    
    def __str__(self) -> str:
        s = "Zone with attributes: type: {}, color: {}, label: {}, icon: {}, effect: {}. ".format(
            self.type, self.color, self.label, self.icon, self.effect
        )
        return s
    
    def __repr__(self) -> str:
        s = "Zone(color={}. label={}, type={}, ".format(self.color, self.label, self.type)
        s = s + "icon={}, effect={})".format(self.icon, self.effect)
        return s

class Hex():
    """
    This class requires a dictionary of values of the following form:
        id: int, required, number of the hex (1-19)
        vertex: tuple (x, y), required, coordinates of the left lower corner
                    on the tk.Canvas for this hex to appear.
        zone: Zone, required, describes threat level of this section
                    of the Hex Flower, may alter the color of the Hex fill,
                    also has its own attributes:
            type: str, required, it is severity of this zone in a word,
                    default is normal
            label: str, required, what should appear if the icon is None
            color: str, optional, the value of the outline of the hex, it 
                    can indicate the severity of the outcome
            icon: filename or None, optional. icon that will be displayed 
                    in the hex if specified
            effect: str or None, optional, this describes the outcome of 
                    landing here
        adjacency: dictionary storing the next hex in the flower to move
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
    def __init__(self, id: int, vertex: tuple, label: str,
                 adjacency: dict,  type='normal',
                 color=None, icon=None, effect=None,
                 diagnostic=False):
        self.id = id
        x,y = vertex
        if (isinstance(x, int) or isinstance(x, float)) and \
            (isinstance(y, int) or isinstance(y, float)):
            self.vertex = vertex
        else:
            raise TypeError("Vertex coordinates must be a ids")
        if label is None:
            label = str(self.id)
        self.zone = Zone(color=color, label=label, type=type, 
                         icon=icon, effect=effect, diagnostic=diagnostic)
        if isinstance(adjacency, dict):
            self.adjacency = {}
            for k in {'a', 'b', 'c', 'd', 'e', 'f'}:
                if isinstance(adjacency[k], int) or adjacency[k] is None:
                    self.adjacency[k] = adjacency[k]
                else:
                    raise ValueError("Adjacency values must be a Hex ID (int) or None.")
        else:
            raise ValueError("Adjacency keys must be a, b, c, d, e, or f.")
        if diagnostic:
            print(f"Initialized Hex: {self}")

    def __str__(self):
        s = "Hex with attributes: id = {}, vertex = {}\n".format(self.id, self.vertex)
        s = s + self.zone.__str__() + "\n"
        s = s + "Adjacency: {}".format(self.adjacency)
        return s

    def __repr__(self):
        s = "Hex(id={}, vertex={}, label={}, ".format(self.id, self.vertex, self.zone.label)
        s = s + "type={}, color={}, icon={}, ".format(self.zone.type, self.zone.color, self.zone.icon)
        s = s + "effect={}, adjacency={})".format(self.zone.effect, self.adjacency)
        return s

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