from base.gets import *
from base.generators import generate_value
from globals import *
from database.psqlconnection import is_value_in_database, retrieve_data


class OnePropTestCombination(object):
    """
    Object describing test combination for a property to be written to the test set of the .ini files
    """

    # Attributes:
    # none_value - the 0 length string
    # blank_value - the blank character
    # file_value - the valid file value
    # db_value - the value of a particular property already storing in the database

    def __init__(self, file_value, db_value):
        self.none_value = ""
        self.blank_value = " "
        self.file_value = file_value
        self.db_value = db_value


class DbDescription(object):
    """
    Table and column the database value of a property can be retrieved from
    """

    def __init__(self, one_prop_db_descr_d):
        self.table = one_prop_db_descr_d[TABLE]
        self.column = one_prop_db_descr_d[COLUMN]


class OneProp(object):
    # Attributes:
    # prop_d - dictionary of the elements describing one property of the initial json file
    # db_flag - flag showing is the database check is needed; False - no database check, True - database check should
    #                                                           be performed
    # db_description - database table and column to run the queries
    # test_combination - OnePropTestCombination object

    def __init__(self, prop_d):
        """
        :param prop_d: dictionary describing the property position and its sense in the future .ini file
        :return: OneProp object
        """
        self.prop_d = prop_d
        self.db_flag = False
        self.db_description = None
        self.test_combination = None

    def gen_test_combination(self):
        """
        OneProp object method
        :return: test combination for one property in the future .ini file
        """
        file_value = None
        db_value = None
        if POSSIBLE_VALUES in self.prop_d:
            file_value = self.prop_d[POSSIBLE_VALUES][0]
        else:
            file_value = generate_value(self.prop_d[TYPE])
        if self.db_flag:
            while is_value_in_database(file_value, self.db_description.table, self.db_description.column):
                file_value = generate_value(self.prop_d[TYPE])
            db_value = retrieve_data(self.db_description.table, self.db_description.column)
        self.test_combination = OnePropTestCombination(file_value, db_value)

    def check_dependency_type(self, prop1, prop2):
        if prop2 in self.prop_d[prop1][DEPENDENCIES]:
            if self.prop_d[prop1][DEPENDENCY_TYPE] == AND:
                return True
            if self.prop_d[prop1][DEPENDENCY_TYPE] == XOR:
                return False
            return None # trow an exception
        else:
            return None


class Section(object):
    """
    Corresponds to one section in the .ini file
    Should contain the section name, sorted list of the section properties and their dependencies
    """

    # Attributes:
    # name - section name in the .ini file
    # s_props_l - sorted list of properties in the section
    # deps_d - dict of dependencies of the properties in the section

    def __init__(self, name, props_d):
        """
        :param name: the name of one section in the .ini file, STRING
        :param props_d: dictionary, containing all properties of the .ini file, get directly from the .json file
        :return: Section object
        """
        self.name = name
        self.s_props_l = get_specific_properties(SECTION, props_d, True, self.name)
        self.deps_d = get_specific_properties(DEPENDENCIES, props_d, False, None)


class FileProps(object):
    # Attributes:
    # f_name_pattern_l - pattern of the file name used to create a test set
    #              [0] - name of the file
    #              [1] - extension
    # s_sections_l - sorted list of sections
    # sections_obj_l - list of Section objects
    # props_obj_d - dict of properties and their specifications
    # test_files_amount - amout of the test files of the given .ini to be created in the test bunch

    def __init__(self, file_props_d, db_descr_d):
        """
        :param file_props_d: dictionary of the future .ini file specifications and properties
        :param db_descr_d: dictionary of a database table-column pair to retrieve given property database value
        :return: a FileProps object
        """

        # forming the list of the .ini file's name and extension
        self.f_name_pattern_l = [file_props_d[FILE_NAME_PATTERN],
                                 file_props_d[FILE_EXTENSION]]

        # getting the dictionary of the .ini file sections to put them into a sorted list
        sections_d = file_props_d[FILE_PROPERTIES][SECTIONS]
        self.s_sections_l = [value for (key, value) in sorted(sections_d.items())]

        # getting the dictionary of the .ini file properties
        props_d = file_props_d[FILE_PROPERTIES][PROPERTIES]

        self.sections_obj_l = [Section(element, props_d) for element in self.s_sections_l]

        self.props_obj_d = {}
        for element in props_d:
            self.props_obj_d[element] = OneProp(props_d[element])
            if element in db_descr_d:
                self.props_obj_d[element].db_description = DbDescription(db_descr_d[element])
                self.props_obj_d[element].db_flag = True

        # initiating the test files amount as 4 by the default minimum: None, Blank, file value, db value
        self.test_files_amount = 4


    def gen_test_combination(self):
        """
        For each props_obj_d element calls function that generate test combination
        :return:
        """
        for element in self.props_obj_d:
            self.props_obj_d[element].gen_test_combination()


    def count_test_files_amount(self):
        # initiating the test files amount as 4 by the default minimum: None, Blank, file value, db value
        amount = 4
        depend_tuples_d = {}

        for dep_type in DEPENDENCY_TYPE_SET:
            depend_tuples_d[dep_type] = get_dependency_tuples(self.props_obj_d, dep_type)

        return amount