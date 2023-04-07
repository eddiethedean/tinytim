import unittest

import tinytim.columns as columns_functions


DATA = {'x': [1, 2, 3], 'y': [6, 7, 8]}


class TestColumnDict(unittest.TestCase):
    def test_basic(self):
        x = columns_functions.column_mapping(DATA, 'x')
        y = columns_functions.column_mapping(DATA, 'y')
        self.assertDictEqual({'x': [1, 2, 3]}, x)
        self.assertDictEqual({'y': [6, 7, 8]}, y)


class TestItercolumns(unittest.TestCase):
    def test_basic(self):
        cols = list(columns_functions.itercolumns(DATA))
        self.assertTupleEqual(('x', [1, 2, 3]), cols[0])
        self.assertTupleEqual(('y', [6, 7, 8]), cols[1])


if __name__ == '__main__':
    unittest.main()