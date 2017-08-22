from base.gets import get_specific_properties
from base.generators import generate_value
from objects.enums import KeyWords
from database.psqlconnection import is_value_in_database, retrieve_data


class TestCombination(object):

    def __init__(self, file_value, db_value):
        self.none_value = ""
        self.blanc_value = " "
        self.file_value = file_value
        self.db_value = db_value


class DbDescription(object):

    def __init__(self, one_prop_db_descr_d):
        self.table = one_prop_db_descr_d[KeyWords.table.value]
        self.column = one_prop_db_descr_d[KeyWords.column.value]


class OneProp(object):

    def __init__(self, prop_d):
        self.prop_d = prop_d
        self.db_flag = False
        self.db_description = None
        self.test_combination = None

    def gen_test_combination(self):
        file_value = None
        db_value = None
        if KeyWords.possibleValues.value in self.prop_d:
            file_value = self.prop_d[KeyWords.possibleValues.value][0]
        else:
            file_value = generate_value(self.prop_d[KeyWords.type.value])
        if self.db_flag:
            while is_value_in_database(file_value, self.db_description.table, self.db_description.column):
                file_value = generate_value(self.prop_d[KeyWords.type.value])
            db_value = retrieve_data(self.db_description.table, self.db_description.column)
        self.test_combination = TestCombination(file_value, db_value)


class Section(object):

    # Attributes:
    # name - section name in the ini file
    # s_props_l - list of sorted properties in the section
    # deps_d - dict of dependencies of the properties

    def __init__(self, name, props_d):
        self.name = name
        self.s_props_l = get_specific_properties(KeyWords.section.value, props_d, True, self.name)
        self.deps_d = get_specific_properties(KeyWords.dependencies.value, props_d, False, None)


class FileProps(object):

    # Attributes:
    # f_name_pattern_l - pattern of the file name used to create a test set
    #              [0] - name of the file
    #              [1] - extension
    # s_sections_l - sorted list of section
    # sections_obj_l - list of Section objects
    # props_obj_d - dict of properties and there specifications

    def __init__(self, file_props_d, db_descr_d):

        self.f_name_pattern_l = [file_props_d[KeyWords.fileNamePattern.value],
                                 file_props_d[KeyWords.fileExtension.value]]

        sections_d = file_props_d[KeyWords.fileProperties.value][KeyWords.sections.value]
        self.s_sections_l = [value for (key, value) in sorted(sections_d.items())]

        props_d = file_props_d[KeyWords.fileProperties.value][KeyWords.properties.value]
        self.sections_obj_l = []
        for element in self.s_sections_l:
            x_section = Section(element, props_d)
            self.sections_obj_l.append(x_section)

        self.props_obj_d = {}
        for element in props_d:
            self.props_obj_d[element] = OneProp(props_d[element])
            if element in db_descr_d:
                self.props_obj_d[element].db_description = DbDescription(db_descr_d[element])
                self.props_obj_d[element].db_flag = True


    def gen_test_combination(self):
        for element in self.props_obj_d:
            self.props_obj_d[element].gen_test_combination()