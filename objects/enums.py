import base
import enum


class Check(enum.Enum):
    existence = 'existence'
    duplication = 'duplication'


class KeyWords(enum.Enum):
    fileNamePattern = 'fileNamePattern'
    fileExtension = 'fileExtension'
    fileProperties = 'fileProperties'
    sections = 'sections'
    properties = 'properties'
    section = 'section'
    type = 'type'
    name = 'name'
    fileCheck = 'fileCheck'
    dbCheck = 'dbCheck'
    possibleValues = 'possibleValues'
    number = 'number'
    string = 'string'
    set = 'set'
    table = 'table'
    column = 'column'
    order = 'order'
    dependencies = 'dependencies'
    mysql = 'mysql'
    oracle = 'oracle'
    optional = 'optional'


class PTypes():
    number = 0
    string = ""
