import tkinter as tk
from lib.classes import Hex


class HexFlower():
    """
    This class takes a list of 19 Hex objects and adds them in the
    order of the number value. They need to be numbered 1 through 19
    in the Hex['number'] attribute
    """
    def __init__(self, *args):
        self = []
        for i in range(1, 20):
            for hex in args:
                if type(hex) != Hex:
                    raise TypeError
                if hex['number'] == i:
                    self.extend(hex)

    def __str__(self) -> str:
        s = ''
        for i in range(19):
            s = s + 'Hex: {}'.format(self[i].__str__())
        return s
