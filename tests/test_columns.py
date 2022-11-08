import unittest

import tinytim.columns as columns


DATA = {'x': [1, 2, 3], 'y': [6, 7, 8]}


class TestColumnDict(unittest.TestCase):
    def test_basic(self):
        x = columns.column_dict(DATA, 'x')
        y = columns.column_dict(DATA, 'y')
        self.assertDictEqual({'x': [1, 2, 3]}, x)
        self.assertDictEqual({'y': [6, 7, 8]}, y)


class TestItercolumns(unittest.TestCase):
    def test_basic(self):
        cols = list(columns.itercolumns(DATA))
        self.assertTupleEqual(('x', (1, 2, 3)), cols[0])
        self.assertTupleEqual(('y', (6, 7, 8)), cols[1])


class TestValueCounts(unittest.TestCase):
    def test_basic(self):
        values = [4, 1, 1, 4, 5, 1]
        results = columns.value_counts(values)
        self.assertEqual({1: 3, 4: 2, 5: 1}, results)