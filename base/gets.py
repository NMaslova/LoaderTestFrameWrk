from objects.enums import KeyWords


# returns list of properties that have desired description and its value
# if value is None then returns only those who have specified description regardless its value
def get_specific_properties(word, props_d, s=True, value=None):
    desired_props_d = {}

    # file property is described as a dictionary where the key is the property itself, the value
    # is a dictionary of descriptions
    for key in props_d:  # for each property in the dict

        for inter_key in props_d[key]:  # for each description of the property

            # checking if that description contains desired keyword and value if not None
            if (inter_key == word and value is None) or (
                            inter_key == word and props_d[key][inter_key] == value):
                desired_props_d[props_d[key][KeyWords.order.value]] = key  # adding the property to the list

    if s:
        # sorted list of desired properties
        s_desired_props_l = [value for (key, value) in sorted(desired_props_d.items())]
        return s_desired_props_l

    return desired_props_d
