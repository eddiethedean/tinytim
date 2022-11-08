from typing import List
import unittest

import tinytim.json as json_functions
from tinytim.types import RowDict


DATA = {'x': [1, 2, 3], 'y': [6, 7, 8]}
JSON = '[{"x": 1, "y": 6}, {"x": 2, "y": 7}, {"x": 3, "y": 8}]'
JSON_LIST = [{'x': 1, 'y': 6},
             {'x': 2, 'y': 7},
             {'x': 3, 'y': 8}]


class TestDataToJson(unittest.TestCase):
    def test_basic(self):
        result = json_functions.data_to_json(DATA) 
        expected = JSON
        self.assertEqual(result, expected)


class TestJsonToData(unittest.TestCase):
    def test_basic(self):
        result = json_functions.json_to_data(JSON)
        expected = DATA
        self.assertDictEqual(result, expected)


class TestDataToJsonList(unittest.TestCase):
    def test_basic(self):
        result = json_functions.data_to_json_list(DATA)
        expected = JSON_LIST
        self.assertListEqual(result, expected)


class TestJsonListToData(unittest.TestCase):
    def test_basic(self):
        json: List[RowDict] = JSON_LIST
        result = json_functions.json_list_to_data(json)
        expected = DATA
        self.assertDictEqual(result, expected)

