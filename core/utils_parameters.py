from utils_numbers import is_number


###########################################################

def set_key_order(ONTOLOGY_PARAMETERS):
    KEY_ORDER = {}
    order = 0
    for key, val in ONTOLOGY_PARAMETERS["QI"].items():
        KEY_ORDER[key] = order
        order = order+1

    ONTOLOGY_PARAMETERS["KEY_ORDER"] = KEY_ORDER
    return ONTOLOGY_PARAMETERS

###########################################################

def get_key_from_order(ONTOLOGY_PARAMETERS, order):
    key_order = ONTOLOGY_PARAMETERS["KEY_ORDER"]
    for key, val in key_order.items():
        if val == order:
            return key 

###########################################################

def get_attributes(dlist):
    global ATT_NAME
    att_names = []
    for (count, d) in enumerate(dlist):
        if (count>0):
            break
        for key,val in d.items():
            att_names.append(key)
    ATT_NAME = att_names

###########################################################

def set_categories(datum):
    IS_CAT = {}
    for key,d in datum.items():
        if is_number(d):
            IS_CAT[key] = False
        else:
            IS_CAT[key] = True
    return IS_CAT
