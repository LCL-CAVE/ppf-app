import json


def parse_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
