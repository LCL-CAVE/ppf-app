import json


def parse_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


# if __name__ == "__main__":
#     output_json = parse_json('./params/category.json')
#     print(output_json)
