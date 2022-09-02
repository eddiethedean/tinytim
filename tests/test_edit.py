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


