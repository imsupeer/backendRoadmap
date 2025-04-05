import os
import json


def get_file_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)


def from_json(filename):
    path = get_file_path(filename)
    return json.load(open(path))
