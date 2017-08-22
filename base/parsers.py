import json


# parses json file and returns a dict
def parse_json(json_file):
    json_stream_dict = {}
    for jf_line in json_file:
        json_stream_dict.update(json.loads(str(jf_line)))
    return json_stream_dict
