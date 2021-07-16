import json


def parse(json_file):
    with open(json_file, 'r') as output:
        results = json.load(output)
    return 0
