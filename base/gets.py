from globals import *


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#        Check the s and value params!!!! they cannot be True and None at the same time

def get_specific_properties(specification, props_d, s=True, value=None):
    """
    gets either sorted list (value is not None) or dictionary (value in None) of properties that have desired
     specification

    :param specification: given specification of a property to be found in the dictionary
    :param props_d: dictionary of the .ini file properties taken from the .json file
    :param s: return flag; if True the function returns sorted list of the properties; default True
    :param value: value the specification must have; if the value is None the function pays no attention to the param;
                    default None

    :return:  either a sorted list of properties which contain given specification and value
                or a dictionary
    """
    specific_props_d = {}

    # file property is described as a dictionary where the key is the property itself, the value
    # is a dictionary of specifications
    for key in props_d:  # for each property in the dict

        for inter_key in props_d[key]:  # for each specification of the property

            # checking if that specification contains desired keyword and value if not None
            if (inter_key == specification):
                if value is None:
                    specific_props_d[key] = props_d[key][inter_key]
                if (props_d[key][inter_key] == value) and (value is not None):
                    specific_props_d[props_d[key][ORDER]] = key  # adding the property to the dict

    if s:
        # sorted list of desired properties
        s_desired_props_l = [value for (key, value) in sorted(specific_props_d.items())]
        return s_desired_props_l

    return specific_props_d
