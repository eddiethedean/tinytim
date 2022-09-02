import unittest

from tinytim.edit import edit_row_items_inplace, edit_row_values_inplace
from tinytim.edit import edit_column_inplace, drop_row_inplace
from tinytim.edit import drop_label_inplace, drop_column_inplace
from tinytim.edit import edit_value_inplace
from tinytim.edit import replace_column_names
from tinytim.edit import edit_row_items, edit_row_values, edit_column
from tinytim.edit import edit_value, drop_row, drop_label, drop_column


class TestEditRowItemsInplace(unittest.TestCase):
    def test_basic(self):
        data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
        null = edit_row_items_inplace(data, 0, {'x': 11, 'y': 66})
        self.assertIsNone(null)
        self.assertDictEqual(data, {'x': [11, 2, 3], 'y': [66, 7, 8]})


class TestEditRowValuesInplace(unittest.TestCase):
    def test_basic(self):
        data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
        null = edit_row_values_inplace(data, 1, (22, 77))
        self.assertIsNone(null)
        self.assertDictEqual(data, {'x': [1, 22, 3], 'y': [6, 77, 8]})


class TestEditColumnInplace(unittest.TestCase):
    def test_basic(self):
        data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
        null = edit_column_inplace(data, 'x', [11, 22, 33])
        self.assertIsNone(null)
        self.assertDictEqual(data, {'x': [11, 22, 33], 'y': [6, 7, 8]})


class TestDropRowInplace(unittest.TestCase):
    def test_basic(self):
        data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
        null = drop_row_inplace(data, 1)
        self.assertIsNone(null)
        self.assertDictEqual(data, {'x': [1, 3], 'y': [6, 8]})


class TestDropLabelInplace(unittest.TestCase):
    def test_not_none(self):
        labels = [1, 2, 3, 4, 5]
        null = drop_label_inplace(labels, 1)
        self.assertIsNone(null)
        self.assertListEqual(labels, [1, 3, 4, 5])

    def test_is_none(self):
        labels = None
        null = drop_label_inplace(labels, 1)
        self.assertIsNone(null)
        self.assertIsNone(labels)


class TestDropColumnInplace(unittest.TestCase):
    def test_basic(self):
        data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
        null = drop_column_inplace(data, 'y')
        self.assertIsNone(null)
        self.assertDictEqual(data, {'x': [1, 2, 3]})


class TestEditValueInplace(unittest.TestCase):
    def test_basic(self):
        data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
        null = edit_value_inplace(data, 'x', 0, 11)
        self.assertIsNone(null)
        self.assertDictEqual(data, {'x': [11, 2, 3], 'y': [6, 7, 8]})


class TestReplaceColumnNames(unittest.TestCase):
    def test_basic(self):
        data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
        results = replace_column_names(data, ('xx', 'yy'))
        self.assertDictEqual(results, {'xx': [1, 2, 3], 'yy': [6, 7, 8]})
        self.assertDictEqual(data, {'x': [1, 2, 3], 'y': [6, 7, 8]})


class TestEditRowItems(unittest.TestCase):
    def test_all_keys(self):
        data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
        results = edit_row_items(data, 2, {'x': 33, 'y': 88})
        self.assertDictEqual(results, {'x': [1, 2, 33], 'y': [6, 7, 88]})
        self.assertDictEqual(data, {'x': [1, 2, 3], 'y': [6, 7, 8]})

    def test_one_key(self):
        data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
        results = edit_row_items(data, 0, {'x': 55})
        self.assertDictEqual(results, {'x': [55, 2, 3], 'y': [6, 7, 8]})
        self.assertDictEqual(data, {'x': [1, 2, 3], 'y': [6, 7, 8]})


class TestEditRowValues(unittest.TestCase):
    def test_basic(self):
        data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
        results = edit_row_values(data, 1, (22, 77))
        self.assertDictEqual(results, {'x': [1, 22, 3], 'y': [6, 77, 8]})
        self.assertDictEqual(data, {'x': [1, 2, 3], 'y': [6, 7, 8]})


class TestEditColumn(unittest.TestCase):
    def test_basic(self):
        data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
        results = edit_column(data, 'x', [4, 5, 6])
        self.assertDictEqual(results, {'x': [4, 5, 6], 'y': [6, 7, 8]})
        self.assertDictEqual(data, {'x': [1, 2, 3], 'y': [6, 7, 8]})


class TestEditValue(unittest.TestCase):
    def test_basic(self):
        data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
        results = edit_value(data, 'y', 2, 88)
        self.assertDictEqual(results, {'x': [1, 2, 3], 'y': [6, 7, 88]})
        self.assertDictEqual(data, {'x': [1, 2, 3], 'y': [6, 7, 8]})


class TestDropRow(unittest.TestCase):
    def test_basic(self):
        data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
        results = drop_row(data, 0)
        self.assertDictEqual(results, {'x': [2, 3], 'y': [7, 8]})
        self.assertDictEqual(data, {'x': [1, 2, 3], 'y': [6, 7, 8]})


class TestDropLabel(unittest.TestCase):
    def test_not_none(self):
        labels = [1, 2, 3, 4]
        results = drop_label(labels, 1)
        self.assertEqual(results, [1, 3, 4])
        self.assertEqual(labels, [1, 2, 3, 4])

    def test_is_none(self):
        labels = None
        results = drop_label(labels, 1)
        self.assertIsNone(results)
        self.assertIsNone(labels)


class TestDropColumn(unittest.TestCase):
    def test_basic(self):
        data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
        results = drop_column(data, 'y')
        self.assertDictEqual(results, {'x': [1, 2, 3]})
        self.assertDictEqual(data, {'x': [1, 2, 3], 'y': [6, 7, 8]})
