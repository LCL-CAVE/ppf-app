import os
import json


def serve_api_login():
    with open(os.path.join(
            os.getcwd(),
            'power_api/credential.json'), 'r') as file:
        credential = json.load(file)

    username = credential[0]['username']
    password = credential[0]['password']
    url = 'http://127.0.0.1:5000/v1/table'

    return url, username, password
