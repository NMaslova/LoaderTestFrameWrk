from objects.enums import KeyWords
import random


def simple_generator():
    return random.randint(0, 1000000)


def generate_value(property_type):
    value = simple_generator()
    if property_type == KeyWords.number.value:
        return value
    return str(value)+"_string"
