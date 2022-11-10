import unittest
from tinytim.na import fillna, dropna


class TestFillna(unittest.TestCase):
    def fillna_zeros(self):
        data = {'A': [None, 3, None, None],
                'B': [2, 4, None, 3],
                'C': [None, None, None, None],
                'D': [0, 1, None, 4]}
        results = fillna(data, 0)
        expected = {'A': [0, 3, 0, 0], 'B': [2, 4, 0, 3], 'C': [0, 0, 0, 0], 'D': [0, 1, 0, 4]}
        self.assertDictEqual(results, expected)  # type: ignore

    def fillna_ffill(self):
        data = {'A': [None, 3, None, None],
                'B': [2, 4, None, 3],
                'C': [None, None, None, None],
                'D': [0, 1, None, 4]}
        results = fillna(data, method="ffill")
        expected = {'A': [None, 3, 3, 3],
                    'B': [2, 4, 4, 3],
                    'C': [None, None, None, None],
                    'D': [0, 1, 1, 4]}
        self.assertDictEqual(results, expected)  # type: ignore

    def fillna_values(self):
        data = {'A': [None, 3, None, None],
                'B': [2, 4, None, 3],
                'C': [None, None, None, None],
                'D': [0, 1, None, 4]}
        values = {"A": 0, "B": 1, "C": 2, "D": 3}
        results = fillna(data, value=values)
        expected = {'A': [0, 3, 0, 0], 'B': [2, 4, 1, 3], 'C': [2, 2, 2, 2], 'D': [0, 1, 3, 4]}
        self.assertDictEqual(results, expected)  # type: ignore

    def fillna_first(self):
        data = {'A': [None, 3, None, None],
                'B': [2, 4, None, 3],
                'C': [None, None, None, None],
                'D': [0, 1, None, 4]}
        values = {"A": 0, "B": 1, "C": 2, "D": 3}
        results = fillna(data, value=values, limit=1)
        expected = {'A': [0, 3, None, None],
                    'B': [2, 4, 1, 3],
                    'C': [2, None, None, None],
                    'D': [0, 1, 3, 4]}
        self.assertDictEqual(results, expected)  # type: ignore

    def fillna_zeros_inplace(self):
        data = {'A': [None, 3, None, None],
                'B': [2, 4, None, 3],
                'C': [None, None, None, None],
                'D': [0, 1, None, 4]}
        results = fillna(data, 0, inplace=True)
        self.assertIsNone(results)
        expected = {'A': [0, 3, 0, 0], 'B': [2, 4, 0, 3], 'C': [0, 0, 0, 0], 'D': [0, 1, 0, 4]}
        self.assertDictEqual(data, expected)


class Dropna(unittest.TestCase):
    def no_params(self):
        data = {"name": ['Alfred', 'Batman', 'Catwoman'],
                "toy": [None, 'Batmobile', 'Bullwhip'],
                "born": [None, "1940-04-25", None]}
        results = dropna(data)
        expected = {'name': ['Batman'], 'toy': ['Batmobile'], 'born': ['1940-04-25']}
        self.assertDictEqual(results, expected)  # type: ignore

    def axis_column(self):
        data = {"name": ['Alfred', 'Batman', 'Catwoman'],
                "toy": [None, 'Batmobile', 'Bullwhip'],
                "born": [None, "1940-04-25", None]}
        results = dropna(data, axis='columns')
        expected = {'name': ['Alfred', 'Batman', 'Catwoman']}
        self.assertDictEqual(results, expected)  # type: ignore

    def how_all(self):
        data = {"name": ['Alfred', 'Batman', 'Catwoman'],
                "toy": [None, 'Batmobile', 'Bullwhip'],
                "born": [None, "1940-04-25", None]}
        results = dropna(data, how='all')
        expected = {'name': ['Alfred', 'Batman', 'Catwoman'],
                    'toy': [None, 'Batmobile', 'Bullwhip'],
                    'born': [None, '1940-04-25', None]}
        self.assertDictEqual(results, expected)  # type: ignore

    def thresh_two(self):
        data = {"name": ['Alfred', 'Batman', 'Catwoman'],
                "toy": [None, 'Batmobile', 'Bullwhip'],
                "born": [None, "1940-04-25", None]}
        results = dropna(data, thresh=2)
        expected = {'name': ['Batman', 'Catwoman'],
                    'toy': ['Batmobile', 'Bullwhip'],
                    'born': ['1940-04-25', None]}
        self.assertDictEqual(results, expected)  # type: ignore

    def subset(self):
        data = {"name": ['Alfred', 'Batman', 'Catwoman'],
                "toy": [None, 'Batmobile', 'Bullwhip'],
                "born": [None, "1940-04-25", None]}
        results = dropna(data, subset=['name', 'toy'])
        expected = {'name': ['Batman', 'Catwoman'],
                    'toy': ['Batmobile', 'Bullwhip'],
                    'born': ['1940-04-25', None]}
        self.assertDictEqual(results, expected)  # type: ignore

    def inplace_no_params(self):
        data = {"name": ['Alfred', 'Batman', 'Catwoman'],
                "toy": [None, 'Batmobile', 'Bullwhip'],
                "born": [None, "1940-04-25", None]}
        results = dropna(data, inplace=True)
        self.assertIsNone(results)
        expected = {'name': ['Batman'], 'toy': ['Batmobile'], 'born': ['1940-04-25']}
        self.assertDictEqual(data, expected)  # type: ignore