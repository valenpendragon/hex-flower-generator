import os
import math
import random
import csv
from collections import OrderedDict, namedtuple
from lib.colors import Color, Colors
from abc import ABC, abstractmethod
from xmltodict import parse


class Zone:
    """
    Zone(label: str, type='normal', color=None, icon=None, effect=None,
         diagnostic=False)

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
    Hex(id: int, zone: Zone, adjacency: dict, diagnostic=False)

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
    # Constant Class Attributes
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
    HexFlower(data: OrderedDict, diagnostic=False)

    Arguments:
        data: OrderedDict, HexFlower data extracted via xmltodict
        diagnostic: bool, optional, determines if the Class prints out
            diagnostic data to stdio

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
    # Constant Class Attributes
    DICE = {('d6', None), (None, 'd8'), ('d6','d6'), ('d4', 'd4', 'd4'), 
            ('d6', 'd8')}
    TYPES = {'normal', 'basic', 'terrain', 'weather'}
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


Step = namedtuple('Step', ['step_num', 'hex', 'effect'])

class Walk(ABC):
    """
    Walk(hf: HexFlower, length: int, diagnostic=False)

    Arguments:
        hf: HexFlower, required
        length: int, required in most subclasses, 0 indicates infinite
        diagnostic: bool, determines whether or not the method print
            diagnostic messages to stdio

    Walks use standard tables to determine the next possible most in any
    walk. The HexFlower data determines which of these moves are possible
    from the current Hex as well as which table and 'dice' to use when rolling
    the move. The dice options can be found in the HexFlower.DICE class constant
    while the HexFlower.TYPES class constant lists all of the types of walks
    that have been implemented thus far. Remember as well that the
    HexFlower.ADJKEYS class constant are the edges of the Hex, designated by
    'a' for the top edge and working clockwise around the Hex to 'f' in the
    upper left edge.

    Walk tables include uniform and non-uniform options for movement. These
    tables are incorporated into dictionaries to make them easier to code.
    All of the tables are class constants.

    Note: In addition to blocked movement with some of these distributions,
    the HexFlower in its original definition blocked movement south ouf of
    Hex 1 into Hex 19 (the most severe outcome). It also blocked some moves
    from Hexes 17-19 (very severe outcomes) into the lowest ranks of Hexes to
    simulate the low probabilities of dire outcomes disappearing quickly.

    Note: This class assumes that HexFlower, Hex, and Zone classes did their
    full data checks of the HexFlower data during importation. This class
    and its subclasses will only perform checks of the types of HexFlowers
    considered acceptable to the type of Walk in question.

    This cleas requires a HexFlower to initiaze the Walk and a walk length,
    an integer. Each subcless will implement its own restrictions on the
    walk length, some of which will not require one.

    Class Attributes (constants):
        UNIFORMBIAS: dict, handles a uniform distribution around the Hex edges
        NUNIFORMBIAS: dict, also a uniform bias distribution, but 2 options
            produce None automatically
        STANDARDBIAS: dict, handles the original bias table created for this
            determination method which biases toward the lower left Hexes,
            uses 2d6
        SOUTHBIAS: dict, a "bell curve" bias the focuses movement toward the
            lower hexes, uses 3d4
        SPECIAL: dict, this provides a wider distribution across lower
            hexes, uses d6+d8 to produce the distribution
        TYPES: set of strings, an empty list for this base class, since it
            cannot instantiate anything, used to identify which types of
            HexFlower a walk subclass supports

        Note: Most of these bias tables can be found in the Hex Flower
        Cookbook by Goblin's Henchman. This is an implementation of the 
        Navigation Hexes.

        Note: Each subclass is required to use the class attribute, types,
        to control the supported HexFlower types. W.TYPES is a set containing
        strings listing said types. Here are a couple examples:
            types = {'normal', 'basic'}
            types = {'terrain', 'weather'}
    
    Instance Attributes:
        type: str, the type of Walk being performed
        length: int, the lenght of the Walk, 0 indicates infinite
        start: int, optional, defaults to 1
        count: int, starts at 0, counter for the steps
        hf: HexFlower, the actual data used during the Walk
        steps: list, contains namedtuples in the form Step(step_num: int,
            hex: int, effect: str or None)
        diagnostic: bool, optional (default: False), determines if the
            program will print diagnostic messages to stdio
        Note: The length of the Walk is the number of steps taken after the
        start position is added. So, len(w.steps) = w.length + 1.
    
    Class Methods:
        None

    Internal Class Methods:
        _check_walk_length: used by __init__ to validate walk length before
            setting the attribute
        _check_type: used by __init__ to validate that the HexFlower is a
            compatible type for the Walk being run before setting the
            attribute
        _check_walk_start: validate that the start is an integer, and is
            usable for this subclass of Walk.
        Note: _check_walk_start is NOT an abstract method. It is coded here
        because most subclasses of Walk can use it unchanged.

    """
    # Class Attributes Constants
    UNIFORMBIAS = {
        1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f'}
    NUNIFORMBIAS = {
        1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: None, 8: None}
    STANDARDBIAS = {
        2: 'b', 3: 'b',  4: 'c',  5: 'c',  6: 'd', 7: 'd',
        8: 'e', 9: 'e', 10: 'f', 11: 'f', 12: 'a'}
    SOUTHBIAS = {
        3: 'b', 4: 'b',  5: 'c',  6: 'c', 7: 'd',
        8: 'e', 9: 'e', 10: 'f', 11: 'f', 12: 'a'}
    SPECIAL = {
        2: 'a',   3: 'b',  4: 'b',  5: 'c',  6: 'c', 7: 'd', 8: 'd',
        9: None, 10: 'e', 11: 'e', 12: 'f', 13: 'f', 14: 'a'}
    # This class attribute is empty in the abstract base class because it
    # cannot support instantiation.
    TYPES = set()
    
    def __init__(self, hf: HexFlower, length: int, start=1,
                 diagnostic=False):
        """
        This class requires a HexFlower object that has been properly
        imported and validated by its class constructor. It also requires
        an integer walk length that is greater than zero. Data validation
        during construction will be handled by internal methods that will
        overwritten by the subclasses.

        When implementing subclasses to this abstract class, make every
        effort to focus overrides on the internal methods instead of the
        dunder methods.

        __init__ calls the follogin internal methods:
            _check_walk_length: validate walk length before setting the
                attribute
            _check_walk_type: validate that the HexFlower is the correct type
                for the Walk being run before setting the attribute
            _check_walk_start: validate that the start is an integer, and is
                usable for this subclass of Walk.
            Note: _check_walk_start is NOT an abstract method. It is coded
            here because most subclasses of Walk can use it unchanged.
        """
        if self._check_walk_length(length):
            self.length = length
        else:
            raise ValueError(f"{length} is not a valid walk length for this type of Walk.")
        if self._check_walk_type(hf.type):
            self.type = hf.type
            self.hf = hf
        else:
            raise ValueError(f"{hf.type} is not compatible with this Walk class.")
        self.steps = []
        self.count = 0
        if self._check_walk_start(start):
            self.start = start
            # Add start to steps.
            self.steps.append(Step(0, start, self.hf[start].zone.effect))
        else:
            raise ValueError(f"{start} is not a valid starting hex for any 19 Hex Hex Flower.")
        self.diagnostic = diagnostic
        if self.diagnostic:
            print(f"{self.__class__.__name__} has been initialized successfully.")
            print(f"Walk object is now {self}.")

    @abstractmethod
    def _check_walk_length(self, length: int) -> bool:
        """
        This internal method makes certain the wwlk length, if used, is set
        correctly for the tyhpe of walk. Returns True if the walk length is
        a usable value, False otherwise.
        """
        pass

    def _check_walk_type(self, walk_type: str) -> bool:
        """
        This internal method makes certain the wwlk type for the HexFlower is
        compatible with the Walk subclass requested. Returns True if the walk
        type is compatible, False otherwise.
        """
        if walk_type in self.TYPES:
            return True
        else:
            return False

    def _check_walk_start(self, start: int) -> bool:
        """
        This internal method makes certain that the starting Hex is set to an
        integer between 1 and 19 (the only values valid for a 19 Hex
        HexFlower). It returns True if so, False otherwise.

        If other restrictions apply (such as starting at 10 only or a specific
        Zone or small group of values), override this method.
        """
        if isinstance(start, int):
            if 1 <= start <=19:
                return True
        return False

    def __str__(self):
        """
        This method is fully defined here to avoid duplicating code in the
        subclasses.
        """
        s1 = f"{self.__class__.__name__} with attributes: type: {self.type}, "
        s2 = f"length: {self.length}, start: {self.start}, "
        s3 = f"count: {self.count}, hf: {self.hf}, steps: {self.steps}, "
        s4 = f"diagnostic: {self.diagnostic}."
        return s1 + s2 + s3 + s4

    def __repr__(self):
        """
        This method is fully defined here to avoid duplicating code in the
        subclasses.
        """
        s1 = f"{self.__class__.__name__}(hf={repr(self.hf)}, length="
        s2 = f"{self.length}, start={self.start}, diagnostic="
        s3 = f"{self.diagnostic})"
        return s1 + s2 + s3


class BasicWalk(Walk):
    """
    BasicWalk(hf: HexFlower, length: int, diagnostic=False)

    Arguments:
        hf: HexFlower, required
        length: int, required in most subclasses, 0 indicates infinite
        diagnostic: bool, determines whether or not the method print
            diagnostic messages to stdio

    This is an implementation of the "infinite" walk designed by Goblin's
    Henchman. This type is used for most HexFlowers. The types supported by
    this class include basic, normal, terrain, and weather. To control
    this type and keep it from running forever, it requires a fixed walk
    length. The range of acceptable values for walk length are integers
    between 10 and 75. So, there is a minimum and a maximem.

    It inherits the Walk tables which as class constants and adds a new
    class attribute, types. As with Walk, it relies on the HexFlower class to
    ensure that a valid HexFlower object has been provided as an argument. It
    also inherits all of the attributes from Walk. It also inherits all of the
    methods from Walk, only overriding one internal validator method.

    Overriden Class Attributes:
        TYPES: set of strings, contains all supported types of HexFlower as
            strings
    
    Overriden Instance Methods:
        _check_walk_length: used by __init__ to validate walk length before
            setting the attribute, must be an integer from 10 to 75

    New Instance Methods:
        None
    """
    TYPES = {'normal', 'basic', 'terrain', 'weather'}

    def _check_walk_length(self, length: int) -> bool:
        """
        This internal method makes certain the wwlk length, if used, is set
        correctly for the tyhpe of walk. Returns True if the walk length is
        a usable value, False otherwise. For this Basic Walks, walk length
        needs to be between 10 and 75.
        """
        if isinstance(length, int):
            if 10 <= length <= 75:
                return True
        return False


class TerminalEventWalk(Walk):
    pass

class CourtWalk(Walk):
    pass

class MoraleWalk(Walk):
    pass

#123456789b123456789c123456789d123456789e123456789f123456789g123456789h123456789

