from objects.enums import KeyWords


def create_test_file(file_props_d, test_comb_d):
    key1 = KeyWords.fileProperties.value
    key2 = KeyWords.properties.value
    key3 = KeyWords.sections.value

    sections_dict = {}

    for section_in_dict in props_d[key1][key3]:
        sections_dict[section_in_dict] = props_d[key1][key3][section_in_dict]
    sorted_sections_list = [value for (key, value) in sorted(sections_dict.items())]
    sorted_properties_in_section_dict = {}
    for order_number in sections_dict:
        sorted_properties_in_section_dict[sections_dict[order_number]] = get_sorted_properties_by_section(
                sections_dict[order_number],
                props_d[key1]
                [key2])
    for i in range(4):
        file_name = props_d[KeyWords.fileNamePattern.value] + str(i) + "." + props_d[KeyWords.
            fileExtension.value]
        with open(file_name, "w+") as test_file:
            for file_section in sorted_sections_list:
                test_file.write("[" + file_section + "]\n")
                for file_property in sorted_properties_in_section_dict[file_section]:
                    test_file.write(props_d[key1]
                                    [key2]
                                    [file_property]
                                    [KeyWords.name.value] +
                                    "=" + str(test_comb_d[file_property][i]) + "\n")


