import tkinter as tk
from tkinter import ttk
from Tools.pynche import ColorDB
import os, colorsys, math, random, csv, copy

class HexFlower():
    """
    This class takes a list of 19 Hex objects and adds them in the
    order of the Hex.id value. They need to be numbered 1 through 19
    in the Hex.id attribute.

    Class Attributes:
        hfcols: 5, the number of columns of Hexes in the HF
        hfcolumns: dict, placement of Hexes by Hex.id in the HF,
            None indicates an empty spot
    
    Instance Attributes:
        hexes: list, required, a list of 19 Hex objects
        type: str, required, indicates the type of Hex Flower
        dice: tuple of str, optional, default is ('d6', 'd6')
        side: integer, optional, the length of a side, default 20
        canvas_height: integer, optional, the tk.Canvas height, default=300
        canvas_width: integer, optional, the tk.Canvas width, default=300
     
    Methods:
        proximity: finds the hex.id for the Hex containing the coordinates
            supplies as a argument, returns hex.id or None if outside the
            HF.
        drawHexFlower: this method draws the Hex Flower on the supplied 
            canvas, using the attributes already designated in the HF attributes
            and Hex attributes. A tkinter.Canvas object is needed because we
            need the C.create_polygon method for the Hexes.
    """
    # Here are the constants for every Hex Flower. The dictionary lays
    # out the Hexes stacked in each column. Note, this is tkinter. So, the
    # order has to be reversed because the y-axis is increased as it moves
    # down.
    hfcols = 5
    hfcolumns = {
        0: [None, 14, 9, 4, None],
        1: [17, 12, 7, 2],
        2: [19, 15, 10, 5, 1],
        3: [18, 13, 8, 3],
        4: [None, 16, 11, 6, None]
    }

    def __init__(self, hexes, type: str, 
                 dice=('d6', 'd6'), side=20.0, 
                 height=300, width=300,                  
                 diagnostic=False):
        self.hexes = []
        for i in range(1, 20):
            for hex in hexes:
                if not isinstance(hex, Hex):
                    raise TypeError("HexFlower cannot import lists of non-Hex objects.")
                if hex.id == i:
                    self.hexes.append(hex)
                else:
                    continue
        self.type = type
        if len(dice) > 3 or len(dice) <= 1 or dice is None:
            raise ValueError("Improper number of dice specified. Must 1, 2 or 3")
        else:
            # Checking to make sure the dice are specified correctly, They need
            # span 1-6 (d6), 1-8 (d8), 2-12 (2d6), 3-12 (3d4), or 2-14 (d6 + d8).
            dice_options = [('d6', None), (None, 'd8'), ('d6','d6'),
                            ('d4', 'd4', 'd4'), ('d6', 'd8')]
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
        # Building the correct vertices.
        h = round(self.side * math.sin(math.pi / 3), 2)
        b = round(self.side * math.cos(math.pi / 3), 2)
        for i in range(self.hfcols):
            x = round(((i + 1) * b) + (i * self.side), 2)
            h_adj = h * (i % 2)
            stack_height = len(self.hfcolumns[i])
            for n in range(stack_height):
                hex_id = self.hfcolumns[i][n] 
                y = round((h_adj + (n * 2 * h)), 2)          
                if hex_id is not None:
                    self.hexes[hex_id - 1].vertex = (x, y)
                    if diagnostic:
                        print(f"New Hex is {self.hexes[hex_id - 1]}")
        if diagnostic:
            print("HexFlower initialized")
            print(self)

    def __str__(self) -> str:
        s = "HexFlower with attributes: type = {}, dice = {},\n".format(self.type, self.dice)
        s = s + "side = {}, canvas height = {}, ".format(self.side, self.canvas_height)
        s = s + "canvas width = {},\nand hexes = {}.".format(self.canvas_width, self.hexes)
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
        This method draws the HF on the canvas supplied to it. A tkinter.Canvas
        is required because we leverage the C.create_polygon method to draw the 
        hexagons for each Hex object in the HexFlower. Start locations, color,
        and length of a side of each hex are supplied by Hex attributes. width
        has a default, but is optional. diagnostic determines how much text gets
        sent to stdio while it is running.
        """
        if diagnostic:
            print(f"drawHexFlower: Arguments received: {locals()}")
            print(f"Hex Flower status: {self}")
        # Initializing the variables we need.
        s = self.side
        b = s * math.cos(math.pi / 3)
        h = s * math.sin(math.pi / 3)
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
                labels.append(tk.Label(canvas, image=icon))
            else:
                labels.append(tk.Label(canvas, text=hex.zone.label))
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

class BasicWalk():
    """
    This class is contains three types of standard walks. They depend on the dice
    types required. The 'standardbias' type uses 2d6, the 'southbias' 3d4, and the 
    'special' d6+d8. The choice is determined by the dice the Hex Flower object
    requires. The result 'tables' are dictionaries.

    It will make a move every 3 seconds until the walk ends. This is not a the
    class for walks that have to find an ending hex. Hitting the stop walk button
    will also stop the walk.

    Note: Self-terminating walks are not basic walks. Technically, Basic Walks
    are infinite walks that we stop after several iterations.

    Class Attributes:
        uniformbias: dict, specifies moves for a 1d6 uniform bias situation.
        nuniformbias: dict, specifies moves for a 1d8 uniform bias that uses 7
            8 as blocked moves.
        standardbias: dict, specific moves for 2d6 bias (most moves are b-e).
        southbias: dict, specific moves for 3d4 bias (most move are c, d, or e).
        special: dict, specific moves for d6+d8 (most moves are stay or c, d, e).
        correct_dice: list, tuples of dice combinations usable for this Walk
        correct_types: list, the types of Hex Flowers that this walk will accept
    
    Instance Attributes:
        hf: HexFlower, the HF supplied in the arguments
        last_move: int, number of the final move
        current_move: int, move counter for the walk, since it can be paused
        current_hex: int, hex_id of the current move
        moves: list of tuples of the form (hex_id, zone.type, zone.effect)
        outcomes: dict, picked from the Class Attributes based on hf.dice
    
    Methods:
        completeMove: executes a move and updates the TopLevel window supplied
            as an argument.
    """
    uniformbias = {
        1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f'}
    nuniformbias = {
        1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: None, 8: None}
    standardbias = {
        2: 'b', 3: 'b',  4: 'c',  5: 'c',  6: 'd', 7: 'd',
        8: 'e', 9: 'e', 10: 'f', 11: 'f', 12: 'a'}
    southbias = {
        3: 'b', 4: 'b',  5: 'c',  6: 'c', 7: 'd',
        8: 'e', 9: 'e', 10: 'f', 11: 'f', 12: 'a'}
    special = {
        2: 'a',   3: 'b',  4: 'b',  5: 'c',  6: 'c', 7: 'd', 8: '8',
        9: None, 10: 'e', 11: 'e', 12: 'f', 13: 'f', 14: 'a'}
    correct_dice = [('d6', None), (None, 'd8'), ('d6','d6'),
                    ('d4', 'd4', 'd4'), ('d6', 'd8')]
    correct_types = ['normal', 'basic']
    
    def __init__(self, hf, start: int, moves: int, diagnostic=False):
        """
        Each walk requires hex id (int) of the starting hex and number of moves for
        this walk. There must be a finite number for this type of walk. It also
        requires a hex flower object, which it uses to gather information. The
        type of Hex Flower must be basic or normal to use this Walk.
        """
        # Checking the arguments provided.
        if not isinstance(hf, HexFlower):
            raise ValueError("You must supply a Hex Flower object")
        if not isinstance(start, int):
            raise ValueError("Starting hex id must be an integer")
        elif start not in range(1, 20):
            raise ValueError("Start must a valid hex id (integer [1, 19])")
        if not isinstance(moves, int):
            raise ValueError("The nubmer of moves must be an integer")
        if hf.dice in self.correct_dice:
            self.outcomes = self._init_dice(hf)
        else:
            raise ValueError(f"Dice of type {hf.dice} are not valid for Basic Walks")
        if hf.type not in self.correct_types:
            raise ValueError(f"Basic walks are not valid for {hf.type} of hex flower")
        # Setting attributes for this basic walk.
        self.hf = copy.deepcopy(hf)
        self.last_move = moves
        self.current_move = 0
        self.current_hex = start
        self.moves = []
        zone = self.hf.hexes[start - 1].zone.type
        effect = self.hf.hexes[start - 1].zone.effect
        self.moves.append((start, zone, effect))
        if diagnostic:
            print(f"Basic Walk initialized as {self}")
    
    def _init_dice(self, hf) -> dict:
        """
        This internal method returns the dictionary corresponding to the dice
        specified by the HF.dice attribute.
        """
        if hf.dice == ('d6', None):
            return self.uniformbias
        elif hf.dice == (None, 'd8'):
            return self.nuniformbias
        elif hf.dice == ('d6','d6'):
            return self.standardbias
        elif hf.dice == ('d4', 'd4', 'd4'):
            return self.southbias
        elif hf.dice == ('d6', 'd8'):
            return self.special
        else:
            raise ValueError(f"{hf.dice} is not a valid type for Basic Walks.")
         
    def __repr__(self) -> str:
        return f"BasicWalk(hf={self.hf}, start={self.moves[0]}, moves={self.last_move})"
    
    def __str__(self):
        s = "Basic Walk using Hex Flower {}\n".format(self.hf)
        s = s + "Total Moves: {}, Current Move: {}, ".format(self.last_move, self.current_move)
        s = s + "Current Hex: {}\n".format(self.current_hex)
        s = s + "Moves thus far: {}".format(self.moves)
        return s

    def completeMove(self, window: tk.Toplevel, 
                     diagnostic=False,
                     output_file="./output/basic_walk_output.csv") -> None:
        """
        This method performs a move and updates that WalkOutputWindow with the
        outcome. It requires a tkinter.Toplevel to write the data to.
        """
        self.current_move += 1
        if diagnostic:
            print(f"Current move is #{self.current_move} from hex {self.current_hex}.")
        if self.current_move > self.last_move:
            print("Moves are already complete")
            return
        if len(self.moves) == 1:
            msg = "Start: Hex: {}, Zone: {}, Effect: {}".format(
                self.moves[0][0], self.moves[0][1], self.moves[0][2])
            with open(output_file, 'a+') as myfile:
                writer = csv.writer(myfile, delimiter=",")
                writer.writerow(self.moves[-1])
                if diagnostic:
                    print(f"Start written to {output_file}")
            label = tk.Label(window.frame, text=msg)
            label.grid(row=0, column=0, sticky=tk.W)
        
        roll = 0
        for i in range(len(self.hf.dice)):
            if self.hf.dice[i] == 'd4':
                roll += random.randint(1,4)
            elif self.hf.dice[i] == 'd6':
                roll += random.randint(1,6)
            elif self.hf.dice[i] == 'd8':
                roll += random.randint(1,8)
        if diagnostic:
            print(f"Rolled {roll} using {self.hf.dice}.")
            
        adjacency = self.hf.hexes[self.current_hex - 1].adjacency
        if diagnostic:
            print(f"Checking adjacency for {self.current_hex}.")
            print(f"Adjacency is {adjacency}.")
    
        if self.outcomes[roll] is None:
            new_hex = None
        else:
            new_hex = adjacency[self.outcomes[roll]]
        if new_hex is None:
            if diagnostic:
                print(f"New move is blocked. Staying in hex {self.current_hex}")
            new_hex = self.current_hex
        else:
            self.current_hex = new_hex
        zone = self.hf.hexes[new_hex - 1].zone.type
        effect = self.hf.hexes[new_hex - 1].zone.effect
        self.moves.append((new_hex, zone, effect))
        if diagnostic:
            if self.outcomes[roll] is not None:
                print(f"Roll produced {self.outcomes[roll]} result")
            print(f"Move is to ({new_hex}, {zone}, {effect})")
            
        # Now, we write the move to the TopLevel window.
        i = self.current_move
        msg = "Move #{}: Hex: {}, Zone: {}, Effect: {}".format(
            i, self.moves[i][0], self.moves[i][1], self.moves[i][2])
        # The index has to the start of an empty line in the text widget.
        label = tk.Label(window.frame, text=msg)
        label.grid(row=i, column=0, sticky=tk.W)
        if diagnostic:
            print(f"Move in moves is {self.moves[i]}")
            
        
        # This stanza writes the data to a CSV file that can be opened in a
        # spreadsheet program, like Excel.
        with open(output_file, 'a+') as myfile:
            writer = csv.writer(myfile, delimiter=",")
            writer.writerow(self.moves[-1])
            if diagnostic:
                print(f"Move written to {output_file}")
