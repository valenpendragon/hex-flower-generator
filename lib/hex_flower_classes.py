import os
import math
import random
import csv
from collections import OrderedDict
from lib.colors import Color, Colors
from abc import ABC, abstractmethod, abstractproperty
from xmltodict import parse


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


class HexFlower(OrderedDict):
    """
    This class receives an OrderedDict produced by xmltodict and converts
    it into a HexFlower object. The XML format can be found in the sample
    hex flowers included in this project. The format for the data once it is
    imported fully is an OrderedDict with 19 keys, integers 1 through 19, with
    Hex objects as values. HF also has two attributes, type and dice, that
    are pulled from the XML file.

    Class Attributes:
        DICE: set, list of the tuples of dice acceptable for HexFlower.
        TYPES: set, list of str which are types of supported HexFlowers.
        ADJKEYS: set, list of str which are keys for adjacency dictionary

    Instance Attributes:
        type: str, required, specifies the usage of the Hex Flower.
        dice: tuple of str, required, specifies the dice rolls for the walks
            using this hex flower.
        diagnostic: bool, optional, defaults to False. Used to toggle on/off
            diagnostic messages to stdio.

    Class Methods:
        _extract_tuple: internal method that extracts tuples from string
            and returns the tuple.
        _extract_adjacency: internal that converts strings in the 
            OrderedDict adjacency data into integers and None type data.
            It returns a dict object after verifying that all movement
            references are eitehr integers between 1 and 19 or are None.
            Anything that cannot be converted into integers raises a
            ValueError. Any keys missing from ADJKEYS in the dictionary
            keys raises a KeyError.
    
    """
    DICE = {('d6', None), (None, 'd8'), ('d6','d6'), ('d4', 'd4', 'd4'), 
            ('d6', 'd8')}
    TYPES = {'normal', 'basic'}
    ADJKEYS = {'a', 'b', 'c', 'd', 'e', 'f'}

    def __init__(self, d: OrderedDict, diagnostic=False):
        """
        This method takes an OrderedDict produced by parsing a HexFlower XML
        file with xmltodict and imports it into a HexFlower object. HF is 
        based on OrderedDict. This method keeps the final step of conversion
        self-contained within the class.

        Note: If the XML structure does not match thet format used in the
        examples, __init__ is very likely to raise KeyError and ValueErrors.
        """
        self.type = d['hex_flower']['@type']
        if self.type not in self.TYPES:
            raise ValueError(f"Type value {self.type} is not a value options. Options are {self.TYPES}.")
    
        # Unfortunately, every data item is a string until we convert them.
        dice = self._extract_tuple(d['hex_flower']['@dice'])
        if not isinstance(dice, tuple):
            raise TypeError(f"Dice must be a tuple of strings or None type.")
        if dice not in self.DICE:
            raise ValueError(f"Hex Flower:Dice value {dice} is not a valid option. Options are {DICE}.")
        self.dice = dice
        self.diagnostic=diagnostic
        if diagnostic:
            print(f"HexFlower: Attritute initialized. Beginning population of Hex objects.")
        
        # Now, we need to extra the Hexes and import them into the HexFlower.
        # Again, if the format is wrong, this will explode quickly. As before
        # we need extra some of the strings and convert them to integer or
        # None type.
        for i in range(19):
            id = int(d['hex_flower']['hex'][i]['@id'])
            adjacency = self._extract_adjacency(id,
                d['hex_flower']['hex'][i]['adjacency'])
            self[i+1] = Hex(
                id=id,
                zone = Zone(
                    label=d['hex_flower']['hex'][i]['zone']['@label'],
                    z_type=d['hex_flower']['hex'][i]['zone']['@type'],
                    icon=d['hex_flower']['hex'][i]['zone']['@icon'],
                    color=d['hex_flower']['hex'][i]['zone']['@color'],
                    effect=d['hex_flower']['hex'][i]['zone']['@effect']),
                adjacency=adjacency,
                diagnostic=diagnostic
            )
        if diagnostic:
            print(f"HexFlower: Hexes loaded. Initialization completed.")
            print(f"Hex Flower is now {self}.")
    
    def _extract_tuple(self, s: str) -> tuple:
        """
        This method receives a string representation of a tuple and returns
        the tuple contained within it.
        """
        s = s.replace('(', '')
        s = s.replace(')', '')
        s = s.split(',')
        return tuple(s)
    
    def _extract_adjacency(self, id: int, d: OrderedDict) -> dict:
        """
        This method receives an OrderedDict of adjacency data. It also 
        receives the Hex id. That allows for an error message  that 
        specifies which Hex in the XML file contains bad data. It returns a
        dict, converting string of integers into integers and 'null' into
        None type. It also checks to make sure that the integers. If the
        conversion to integer fails or an invalid string is found, it raises
        a KeyErrors or ValueErrors as appropriate.
        """
        adjacency = {}
        if set(d.keys()) != self.ADJKEYS:
            raise KeyError(f"Keys for adjacency for Hex {id} are invalid. Must be {ADJKEYS}.")
        for k in self.ADJKEYS:
            val = d[k]
            # First, check for 'null'. If not, it must be a str(int).
            if val == 'null':
                adjacency[k] = None
            else:
                try:
                    val = int(val)
                    if 1 <= val <= 19:
                        adjacency[k] = val
                    else:
                        raise ValueError(f"HexFlower: Adjacency in Hex {id} for key {k} exceeds [1,19] range.")
                except ValueError:
                    raise ValueError(f"HexFlower: Adjacency is not an integer in Hex {id} for key {k}.")
        return adjacency

    def __str__(self) -> str:
        s1 = f"HexFlower (based on OrderedDict) with class attributes: "
        s2 = f"DICE: {self.DICE}, TYPES: {self.TYPES}, and instance attributes:"
        s3 = f" type: {self.type}, dice: {self.dice}, containing Hex objects: "
        s4 = f" {super(HexFlower, self).__str__()}"
        return s1 + s2 + s3

    def __repr__(self) -> str:
        #               (           ([(                         ([(         
        s1 = f"HexFlower(OrderedDict([('hex_flower', OrderedDict([('@type', "
        dice = str(self.dice).replace("'", "")
        #                  )  (                )
        s2 = f" {self.type}), ('@dice','{dice}'),"
        #         ( hex data opened
        h_str = " ('hex', "
        for i in range(1, 20):
            #      [           ([(                    )   (
            h1 = f"[OrderedDict([('@id', '{self[i].id}'), ('zone', "
            #                 ([(                              )
            h2 = f"OrderedDict([('@type', '{self[i].zone.type}'), "
            #      (                              )
            h3 = f"('@label', '{self[i].zone.label}'), "
            #      (                            )
            h4 = f"('@icon', '{self[i].zone.icon}'), "
            #      (                              )
            h5 = f"('@color', '{self[i].zone.color}'), "
            #      (                                )])) zone closed
            h6 = f"('@effect', '{self[i].zone.effect}')])), "
            #           (                        ([
            adj_str = f"('adjacency', OrderedDict(["
            for item in self.ADJKEYS:
                if self[i].adjacency[item]:
                    adj = self[i].adjacency[item]
                else:
                    adj = 'null'
                #                     (                 )
                adj_str = adj_str + f"('{item}', '{adj}'), "
            if i != 19:
                # hex & adjacency closed
                hc = "]))]), "
            else:
                # hex, adjacency, and hex flower closed
                hc = "])]))])"
            h_str = h_str + h1 + h2 + h3 + h4 + h5 + h6 + adj_str + hc
        return s1 + s2 + h_str
    
class Walk(ABC):
    pass

class NormalWalk(Walk):
    """
    Include Terrain and Weather here.
    """
    pass



class CourtWalk(Walk):
    pass

class MoraleWalk(Walk):
    pass

#123456789b123456789c123456789d123456789e123456789f123456789g123456789h123456789

