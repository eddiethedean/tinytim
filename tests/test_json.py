import unittest

from tinytim.json import data_to_json, json_to_data, data_to_json_list, json_list_to_data


DATA = {'x': [1, 2, 3], 'y': [6, 7, 8]}
JSON = '[{"x": 1, "y": 6}, {"x": 2, "y": 7}, {"x": 3, "y": 8}]'
JSON_LIST = [{'x': 1, 'y': 6},
             {'x': 2, 'y': 7},
             {'x': 3, 'y': 8}]


class TestDataToJson(unittest.TestCase):
    def test_basic(self):
        result = data_to_json(DATA) 
        expected = JSON
        self.assertEqual(result, expected)


class TestJsonToData(unittest.TestCase):
    def test_basic(self):
        result = json_to_data(JSON)
        expected = DATA
        self.assertDictEqual(result, expected)


class TestDataToJsonList(unittest.TestCase):
    def test_basic(self):
        result = data_to_json_list(DATA)
        expected = JSON_LIST
        self.assertListEqual(result, expected)


class TestJsonListToData(unittest.TestCase):
    def test_basic(self):
        json = JSON_LIST
        result = json_list_to_data(json)
        expected = DATA
        self.assertDictEqual(result, expected)

