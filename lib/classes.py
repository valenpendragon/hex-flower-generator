from collections import OrderedDict

class Hex(OrderedDict):
    def __init__(self, dictionary):
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
        for k, v in dictionary.items():
            if type(k) == dict:
                # k is the adjacency subdictionary
                for subk, subv in dictionary['adjacency'].items():
                    setattr(self['adjacency'], subk, subv)
            else:
                setattr(self, k, v)
    print(self)

    def __str__(self):
        super().__str__(self)

    def __repr__(self):
        super().__repr__(self)
