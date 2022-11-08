import unittest

import tinytim.data as data_features


DATA = {'x': [1, 2, 3], 'y': [6, 7, 8]}


class TestColumnCount(unittest.TestCase):
    def test_basic(self):
        result = data_features.column_count(DATA)
        self.assertEqual(result, 2)


class TestRowCount(unittest.TestCase):
    def test_basic(self):
        result = data_features.row_count(DATA)
        self.assertEqual(result, 3)


class TestShape(unittest.TestCase):
    def test_basic(self):
        result = data_features.shape(DATA)
        self.assertEqual(result, (3, 2))


class TestSize(unittest.TestCase):
    def test_basic(self):
        result = data_features.size(DATA)
        self.assertEqual(result, 6)


class TestFirstColumnName(unittest.TestCase):
    def test_basic(self):
        result = data_features.first_column_name(DATA)
        self.assertEqual(result, 'x')


class TestColumnNames(unittest.TestCase):
    def test_basic(self):
        result = data_features.column_names(DATA)
        self.assertEqual(result, ('x', 'y'))


class TestHead(unittest.TestCase):
    def test_basic(self):
        result = data_features.head(DATA, 2)
        self.assertEqual(result, {'x': [1, 2], 'y': [6, 7]})


class TestTail(unittest.TestCase):
    def test_basic(self):
        result = data_features.tail(DATA, 2)
        self.assertEqual(result, {'x': [2, 3], 'y': [7, 8]})


class TestIndex(unittest.TestCase):
    def test_basic(self):
        result = data_features.index(DATA)
        self.assertEqual(result, (0, 1, 2))


class TestTableValue(unittest.TestCase):
    def test_basic(self):
        result = data_features.table_value(DATA, 'x', 1)
        self.assertEqual(result, 2)


class TestColumnValues(unittest.TestCase):
    def test_basic(self):
        result = data_features.column_values(DATA, 'y')
        self.assertEqual(result, [6, 7, 8])