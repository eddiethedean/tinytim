from os import unlink
import unittest

from tinytim.columns import column_dict, itercolumns


DATA = {'x': [1, 2, 3], 'y': [6, 7, 8]}


class TestColumnDict(unittest.TestCase):
    def test_basic(self):
        x = column_dict(DATA, 'x')
        y = column_dict(DATA, 'y')
        self.assertDictEqual({'x': [1, 2, 3]}, x)
        self.assertDictEqual({'y': [6, 7, 8]}, y)


class TestItercolumns(unittest.TestCase):
    def test_basic(self):
        cols = list(itercolumns(DATA))
        self.assertTupleEqual(('x', (1, 2, 3)), cols[0])
        self.assertTupleEqual(('y', (6, 7, 8)), cols[1])