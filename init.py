import sys
from base.parsers import parse_json
from base.classes import FileProps


def main():
    try:
        with open(sys.argv[1]) as json_file:
            file_props_d = parse_json(json_file) # file_properties_dict

        with open(sys.argv[2]) as d_json_file:
            db_descr_d = parse_json(d_json_file)     # database_description_dict

        file_props_o = FileProps(file_props_d, db_descr_d)
        file_props_o.gen_test_combination()
        print('End')
        #for element in file_props_o.props_obj_d:
        #    if file_props_o.props_obj_d[element].db_flag:
        #        with DbConnection() as db_connection_obj:



        #key1 = KeyWords.fileProperties.value
        #key2 = KeyWords.properties.value
        #key3 = KeyWords.name.value

        #test_comb_d = {} # file_test_combination
        #props_d = file_props_d[key1][key2]

        #for prop in props_d:
        #    if props_d[prop][key3] not in db_descr_d:
        #        prop_db_table_d = None # one_property_database_table_dict
        #    else:
        #        key4 = props_d[prop][key3]
        #        prop_db_table_d = db_descr_d[key4]
        #    prop_test_comb_t = create_test_combinations(props_d[prop], prop_db_table_d)
        #    test_comb_d[prop] = prop_test_comb_t

        #print(test_comb_d)
        #create_test_file(file_props_d, test_comb_d)
    except KeyError:
        print('Error')


if __name__ == '__main__':
    main()