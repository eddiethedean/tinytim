import unittest

from tinytim.data import column_count, row_count, shape, size
from tinytim.data import first_column_name, column_names
from tinytim.data import head, tail, index, table_value, column_values


DATA = {'x': [1, 2, 3], 'y': [6, 7, 8]}


class TestColumnCount(unittest.TestCase):
    def test_basic(self):
        result = column_count(DATA)
        self.assertEqual(result, 2)