import os
import math
import random
import csv
from collections import OrderedDict
from lib.colors import Color, Colors

class Zone:
    """
    Zone(label: str, type='normal', color=None, icon=None, effect=None)

    Arguments:
        label: str, required. Usually this is the corresponding Hex.id to
            the Hex object this zone belongs to.
        z_type: str, optional. Defaults to 'normal'. Only validates if this
            is a str.
        color: str, optional. If specified, it must be an actual string name
            of a color or the hexadecimal string for a color. Will raise a
            ValueError or TypeError as appropriate if not.
        icon: str, optional. If specified,  it must be the path to an icon
            the user wants to associate with Hexes that have this Zone
            attribute. Will raise an IOError if the file is not found.
        effect: str, optional. Short descriptive text of the severity of any
            Hex that has this Zone attribute.
    Icons allow for a Hex Flower to be displayed with appropriate icons 
    instead of labels.

    The arguments map to attributes as follows:
        label      --> z.label    must be str
        z_type     --> z.type     must be str (default: 'normal')
        color      --> z.color    str or None type
        icon       --> z.icon     pathtofile or None type
        effect     --> z.effect   str or None type
        diagnostic --> diagnostic bool (default: False)
    """
    def __init__(self, label: str, z_type='normal', color=None, icon=None,
                effect=None, diagnostic=False):
        # type and label must be str types.
        if isinstance(label, str):
            self.label = label
        else:
            raise TypeError(f"Zone: label attribute must be str type.")
        if isinstance(z_type, str):
            self.type = z_type
        else:
            raise TypeError(f"Zone: type attribute must be str type.")
        
        # We need to validate the color choice. First we check to see if it is
        # set to None.
        if color is None:
            self.color = 'black'
        else:
            if not isinstance(color, str):
                raise TypeError(f"Color value must be a str color name or a str hexadecimal for a color.")
            # So, color is a string. We need to initialize the color 
            # conversion OrderedDict.
            x = Colors()
            # First, we test to see if it is a valid hex name for a color.
            try:
                rgb = x.hex_to_color(color)
            except ValueError:
                # Now, we need to try to find the string in the dictionary keys.
                # This can raise a ValueError as well. At this point, we want
                # the program to fail with an error because the Hex and Zone
                # data are invalid.
                rgb = x.text_to_color(color)
            self.color = x.color_to_hex(rgb)
        if icon is None:
            self.icon = None
        else:
            # We need to make sure the file exists. If not, we need to fail.
            if os.path.isfile(icon):
                self.icon = icon
            else:
                raise IOError(f"{icon} icon file not found.")
        # Effect has to be a string or None as well.
        if effect is None:
            self.effect = None
        elif not isinstance(effect, str):
            raise TypeError(f"Zone: effect must be str or None type.")
        else:
            self.effect = effect
        self.diagnostic = diagnostic
        if self.diagnostic:
            print(f"Zone: {self} successfully initialized.")
    
    def __str__(self):
        s1 = f"Zone with attributes: label: {self.label}, type: {self.type}, "
        s2 = f"color: {self.color}, icon: {self.icon}, effect: {self.effect}, "
        s3 = f"diagnostic: {self.diagnostic}"
        return s1 + s2 + s3

    def __repr__(self):
        s1 = f"Zone(label='{self.label}', type='{self.type}', "
        s2 = f"color='{self.color}', icon='{self.icon}', "
        s3 = f"effect='{self.effect}', diagnostic={self.diagnostic})"
        return s1 + s2 + s3



class Hex:
    """
    Hex(id: int, zone: Zone, adjacency: dict)

    Arguments:
        id: int, required. Number of the hex, range 1-19.
        zone: Zone, required. Describes the threat level or outcome of landing
            on a Hex in this zone. Controls labeling and iconography for the
            Hex.
        adjacency: dict, required. Determines which other Hexes are adjacent
            to this Hex and whether movement into that Hex is possible. It is
            designateed by side of the hex using the following table:
                a : top hex    b: upper right hex   c: lower right hex
                d : bottom hex e: lover left hex    f: upper left hex         
            Each of these letters are adjacency keys and will be unique. A None
            value for one of these keys means that movement across that side of
            the Hex is not allowed.
        diagnostic: bool, optional. Defaults to False. This argument determines
            if the class will produce diagnostic messages while running.
    
    The arguments map to attributes as follows:
        id         --> h.label      must be int, range 1-19
        zone       --> h.zone       must be Zone type and initialized
        adjacency  --> h.adjacency  dict with keys {a, b, c, d, e, f}
        diagnostic --> diagnostic   bool (default: false)
    
    Class Attributes:
        ADJKEYS: a set of all the acceptable adjacency keys.
    """
    ADJKEYS = {'a', 'b', 'c', 'd', 'e', 'f'}

    def __init__(self, id: int, zone: Zone, adjacency: dict, diagnostic=False):
        if not isinstance(id, int) :
            raise TypeError(f"Hex: Hex id must be an integer. {id} is not an integer.")
        elif id < 1 or id > 19:
            raise TypeError(f"Hex: Hex id must be an integer from 1 to 19.")
        self.id = id
        if not isinstance(zone, Zone):
            raise TypeError(f"Hex: zone must be of type Zone. {zone} is type {type(zone)}.")
        self.zone = zone
        
        if isinstance(adjacency, dict):
            self.adjacency = {}
            # We do not know if this is properly configured data. That means
            # that we might not have the right keys in the dictionary.
            for k in self.ADJKEYS:
                try:
                    if not isinstance(adjacency[k], (int, type(None))):
                        raise TypeError(f"Hex: adjacency value {adjacency[k]} is not int or None type.")
                    elif (isinstance(adjacency[k], int) and 
                         not (1 <= adjacency[k] <= 19)):
                        raise ValueError(f"Hex: values for adjacency must from 1 to 19. {adjacency[k]} fails the criteria.")
                    else:
                        self.adjacency[k] = adjacency[k]                                            
                except KeyError:
                    raise ValueError(f"Hex: adjacency key {k} is not a memver of set {self.ADJKEYS}.")
        else:
            raise TypeError(f"Hex: adjacency must dict type. {adjacency} is type {type(adjacency)}.")
        
        self.diagnostic = diagnostic
        if self.diagnostic:
            print(f"Hex: {self} is fully initialized.")
    
    def __str__(self) -> str:
        s1 = f"Hex with attributes: id: {self.id}, zone: {self.zone}. "
        s2 = f"adjacency: {self.adjacency}, diagnostic: {self.diagnostic}."
        return s1 + s2
    
    def __repr__(self) -> str:
        s1 = f"Hex(id={self.id}, zone={self.zone.__repr__()}, "
        s2 = f"adjacency={self.adjacency}, diagnostic={self.diagnostic}"
        return s1 + s2

#123456789b123456789c123456789d123456789e123456789f123456789g123456789h123456789


class HexFlower():
    pass