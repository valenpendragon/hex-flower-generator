from lib.colors import Color, Colors

def darken_outline(fill, darken = 40, fill_type='str', result='hex'):
    """
    This functions receives a color in str name form, does a normalize to make
    certain it is a valed color string name. If so, it converts it to RGB and
    reduces all of the RGB indicators by the amount of integer darken. It uses
    The str result to determine what type value to return: 'hex' for hex color
    representation, 'rgb' for namedtuple, and 'str' for string represenation.
    
    Warning: Only a very small number of colors in the RGB framework have actual
    names. This may result is a ValueError. Also, color must be a valid str
    color value or a ValueError will be raised. This check is performed against
    CSS3 names.

    Arguments:
        fill: Color hex or str, determined by fill_type
        darken: int, optional, defaults to 40
        fill_type: str, vallid options: 'hex', 'rgb', 'str', optional, default
            'str'
        result: str, valid options: 'hex', 'rgb', 'str', optional, default 'hex'
    """
    # Check arguments
    x = Colors()
    if not isinstance(fill_type, str):
        raise ValueError(f"fill_type must be type str")
    elif fill_type not in ('hex', 'rgb', 'str'):
        raise ValueError(f"fill_type must be 'hex', 'rgb', or 'str'")
    try:
        darken = int(darken)
    except ValueError:
        raise ValueError(f"darken must be an integer. {darken} cannot be converted to integer.")
    if result not in ('hex', 'rgb', 'str'):
        raise ValueError(f"result must be type str matching 'hex', 'rgb',or'str'")
    
    # Colors.text_to_hex checks to make sure the text in color matches a value
    # for an actual HTML or Tkinter named color.
    if fill_type == 'str':
        color = x.text_to_color(fill)
    elif fill_type == 'rgb':
        color = fill
    else: # fill_type == 'hex'
        color = x.hex_to_color(fill)

    # Darken the values by the darken amount. None of these values can be less
    # than zero however.
    new_vals = []
    for i in color:
        new_val = i - darken
        if new_val < 0:
            new_val = 0
        new_vals.append(new_val)
    # Now, to convert the result into an rbg namedtuple
    result_rgb = Color(red=new_vals[0], green=new_vals[1], blue=new_vals[2])
    # We need a flag for a color with no string name assigned to it.
    bad_string = False
    try:
        result_str = x.color_to_text(result_rgb)
    except ValueError:
        bad_string = True
    result_hex = x.color_to_hex(result_rgb)
    # The bad_string flag is only acted on if the function has result='str'
    # as an argument. That is why this error is trapped her.
    if result == 'hex':
        return result_hex
    elif result == 'rgb':
        return result_rgb
    else:
        # Result is a string
        if bad_string:
            raise ValueError(f"{result_rgb} does not have a string representation.")
        else:
            return result_str