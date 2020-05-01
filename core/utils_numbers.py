"""
Some functions about numbers
"""
###############################################

def is_number(v):
    try:
        v = float(v)
        return True
    except ValueError:
        return False
    except TypeError:
        return False

###############################################

def get_number(v):
    defaultVal = None
    try:
        v = float(v)
        return v
    except ValueError:
        return defaultVal
    except TypeError:
        return defaultVal

###############################################

def represents_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

###############################################

def represents_float(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False