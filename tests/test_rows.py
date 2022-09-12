import unittest

from tinytim.rows import row_dict, row_value_counts, row_values, iterrows
from tinytim.rows import itertuples, itervalues, values


DATA = {'x': [1, 2, 3], 'y': [6, 7, 8]}


class TestRowDict(unittest.TestCase):
    def test_basic(self):
        results = row_dict(DATA, 1)
        self.assertDictEqual(results,  {'x': 2, 'y': 7})
        self.assertDictEqual(DATA, {'x': [1, 2, 3], 'y': [6, 7, 8]})


class TestRowValues(unittest.TestCase):
    def test_basic(self):
        results = row_values(DATA, 0)
        self.assertTupleEqual(results, (1, 6))
        self.assertDictEqual(DATA, {'x': [1, 2, 3], 'y': [6, 7, 8]})


class TestIterrows(unittest.TestCase):
    def test_basic(self):
        generator = iterrows(DATA)
        v1 = next(generator)
        self.assertTupleEqual(v1, (0, {'x': 1, 'y': 6}))
        v2 = next(generator)
        self.assertTupleEqual(v2, (1, {'x': 2, 'y': 7}))
        v3 = next(generator)
        self.assertTupleEqual(v3, (2, {'x': 3, 'y': 8}))
        with self.assertRaises(StopIteration):
            next(generator)
        self.assertDictEqual(DATA, {'x': [1, 2, 3], 'y': [6, 7, 8]})


class TestItertuples(unittest.TestCase):
    def test_basic(self):
        generator = itertuples(DATA)
        v1 = next(generator)
        self.assertTupleEqual(v1, (1, 6))
        v2 = next(generator)
        self.assertTupleEqual(v2, (2, 7))
        v3 = next(generator)
        self.assertTupleEqual(v3, (3, 8))
        with self.assertRaises(StopIteration):
            next(generator)
        self.assertDictEqual(DATA, {'x': [1, 2, 3], 'y': [6, 7, 8]})


class TestItervalues(unittest.TestCase):
    def test_basic(self):
        generator = itervalues(DATA)
        v1 = next(generator)
        self.assertTupleEqual(v1, (1, 6))
        v2 = next(generator)
        self.assertTupleEqual(v2, (2, 7))
        v3 = next(generator)
        self.assertTupleEqual(v3, (3, 8))
        with self.assertRaises(StopIteration):
            next(generator)
        self.assertDictEqual(DATA, {'x': [1, 2, 3], 'y': [6, 7, 8]})


class TestValues(unittest.TestCase):
    def test_basic(self):
        results = values(DATA)
        self.assertTupleEqual(results, ((1, 6), (2, 7), (3, 8)))
        self.assertDictEqual(DATA, {'x': [1, 2, 3], 'y': [6, 7, 8]})


class TestRowValueCounts(unittest.TestCase):
    def test_basic(self):
        data = {'x': [1, 2, 3, 3], 'y': [6, 7, 3, 3]}
        result = row_value_counts(data)
        expected = {(3, 3): 2, (1, 6): 1, (2, 7): 1}
        self.assertDictEqual(expected, result)
