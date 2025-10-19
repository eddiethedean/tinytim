from typing import List

import tinytim.json as json_functions
from tinytim.custom_types import RowDict

DATA = {'x': [1, 2, 3], 'y': [6, 7, 8]}
JSON = '[{"x": 1, "y": 6}, {"x": 2, "y": 7}, {"x": 3, "y": 8}]'
JSON_LIST = [{'x': 1, 'y': 6},
             {'x': 2, 'y': 7},
             {'x': 3, 'y': 8}]


def test_data_to_json():
    result = json_functions.data_to_json(DATA)
    expected = JSON
    assert result == expected


def test_json_to_data():
    result = json_functions.json_to_data(JSON)
    expected = DATA
    assert result == expected


def test_data_to_json_list():
    result = json_functions.data_to_json_list(DATA)
    expected = JSON_LIST
    assert result == expected


def test_json_list_to_data():
    json: List[RowDict] = JSON_LIST
    result = json_functions.json_list_to_data(json)
    expected = DATA
    assert result == expected
