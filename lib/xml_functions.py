from collections import defaultdict
from xml.etree import cElementTree as ElementTree
from lib.classes import HexFlower, Hex, Zone

def xml2dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v
                     for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v)
                        for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
              d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d

def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
              d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d

def str_to_tuple(s: str, f):
    """
    This function takes a string, creates a tuple and applies the function
    to each element of the tuple to produce the correct data type for each
    element. Best options are str to create a tuple of strings, or int to 
    create a tuple of integers (like coordinates).
    """
    # Remove parentheses.
    s = s.replace('(','')
    s = s.replace(')','')
    t = tuple(map(f, s.split(',')))
    return t
    
def process_xml_hex_flower(xmlfile, diagnostic=False, side=20,
                           canvas_width=300, canvas_height=300) -> HexFlower:
    """
    This function takes an xml file and returns a HexFlower object. The other
    arguments are optional. These are:
        side: float or int, length of a hex edge
        canvas_width: int, width of the tk.Canvas
        canvas_height: int, height of the tk.Canvas
        diagnostic: bool, whether or not to generate diagnostic messages while 
            running
    """
    tree = ElementTree.parse(xmlfile)
    if diagnostic:
        print(f"Printing ElementTree: {tree}")
    root = tree.getroot()
    if diagnostic:
        print(f"Printing root: {root}")
    flowerdata = xml2dict(root)
    if diagnostic:
        print(f"Data type is {type(flowerdata)}")
        print("Top level pairs are:")
        for k in flowerdata.keys():
            print(f"\t{k} : {flowerdata[k]}")
        print("First level pairs are")
        for k in flowerdata['hex_flower']:
            print(f"\t{k} : {flowerdata['hex_flower'][k]}")
    # Now, we have a dictionary we can parse to pull our Hex and HF 
    # attributes and data from. All attributes have an @name to separate
    # them from actual dictionaries as attributes.
    # First, we pull out the HF attributes.
    hex_flower = flowerdata['hex_flower']
    hexdata = hex_flower['hex']
    hftype = hex_flower['@type']
    hfdice = str_to_tuple(hex_flower['@dice'], str)
    # We need to check hfdice for nulls in the tuple.
    for i in range(len(hfdice)):
        chk_dice = list(hfdice)
        if hfdice[i] == 'null':
            chk_dice[i] = None
        hfdice = tuple(chk_dice)
    if diagnostic:
        print(f"Extracted Hex Flower type: {hftype}")
        print(f"Extracted hfdice as type {type(hfdice)}: {hfdice}")
        print(f"Extracted hexdata as type {type(hexdata)}: {hexdata}")
    
    # Now, we have a list of dictionaries of hex data that need to be converted.
    hexes = []
    for i in range(len(hexdata)):
        zonedata = hexdata[i]['zone']
        adjacencydata = hexdata[i]['adjacency']
        hex_id = int(hexdata[i]['@id'])
        hex_vertex = str_to_tuple(hexdata[i]['@vertex'], int)
        if diagnostic:
            print(f"Extracted zone data as type {type(zonedata)}: {zonedata}")
            print(f"Extracted adjacency data as type {type(adjacencydata)}: {adjacencydata}")
            print(f"Extracted hex id as type {type(hex_id)}: {hex_id}")
            print(f"Extracted hex vertex as type {type(hex_vertex)}: {hex_vertex}")
        # Now, we pull the zone attributes from the zone dictionary.
        zone_type = zonedata['@type']
        zone_label = zonedata['@label']
        if zonedata['@icon'] == 'null':
            zone_icon = None
        else:
            zone_icon = zonedata['@icon']
        zone_color = zonedata['@color']
        if zonedata['@effect'] == 'null':
            zone_effect = None
        else:
            zone_effect = zonedata['@effect']
        if diagnostic:
            print(f"Extracted zone type as type {type(zone_type)}: {zone_type}")
            print(f"Extracted zone label as type {type(zone_label)}: {zone_label}")
            print(f"Extracted zone icon as type {type(zone_icon)}: {zone_icon}")
            print(f"Extracted zone color as type {type(zone_color)}: {zone_color}")
            print(f"Extracted zone effect as type {type(zone_effect)}: {zone_effect}")
        
        # Final step before converting this into Hex objects is to convert the
        # adjacency data. Currently, the values are strings. They need to ids of
        # hexes (integers) or None if the move is not allowed.
        adjacency = {}
        for k,v in adjacencydata.items():
            if v == 'null':
                adjacency[k] = None
            else:
                adjacency[k] = int(v)
        if diagnostic:
            print(f"Converted adjacency data to: type {type(adjacency)}: {adjacency}")

        new_hex = Hex(id=hex_id, vertex=hex_vertex, label=zone_label,
                      type=zone_type, color=zone_color, icon=zone_icon,
                      effect=zone_effect, adjacency=adjacency,
                      diagnostic=diagnostic)
        hexes.append(new_hex)
        if diagnostic:
            print(f"Created new hex: type: {type(new_hex)}: {new_hex}")
            print(f"Hex list is now: {hexes}")
    # Hexes have been assembled. We are ready to make a Hex Flower.
    return HexFlower(hexes=hexes, type=hftype, dice=hfdice, side=side,
                     height=canvas_height, width=canvas_width,
                     diagnostic=diagnostic)
