import json


def parse_json_keys(file_path, entry, key):
    with open(file_path, 'r') as file:
        loaded_file = json.load(file)
        return loaded_file[entry][key]


if __name__ == "__main__":
    output_value = parse_json_keys('./params/demand_renew.json', 0, 'value')
    print(type(output_value))
