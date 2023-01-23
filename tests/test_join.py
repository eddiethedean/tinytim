import unittest

from tinytim.join import inner_join, full_join, left_join, right_join
from tinytim.join import locate
from tinytim.rows import records_equal


class TestJoin(unittest.TestCase):
    def test_inner_join(self):
        left =  {'id': ['a', 'c', 'd', 'f', 'g'], 'x': [33, 44, 55, 66, 77]}
        right = {'id': ['a', 'b', 'c', 'd'], 'y': [11, 22, 33, 44]}
        results = inner_join(left, right, 'id')
        expected = {'id': ['a', 'c', 'd'], 'x': [33, 44, 55], 'y': [11, 33, 44]}
        self.assertTrue(records_equal(results, expected))

    def test_full_join(self):
        left = {'id': ['a', 'c', 'd', 'f', 'g'], 'x': [33, 44, 55, 66, 77]}
        right = {'id': ['a', 'b', 'c', 'd'], 'y': [11, 22, 33, 44]}
        results = full_join(left, right, 'id')
        expected = {'id': ['a', 'c', 'd', 'f', 'g', 'b'],
                    'x': [33, 44, 55, 66, 77, None],
                    'y': [11, 33, 44, None, None, 22]}
        self.assertTrue(records_equal(results, expected))

    def test_left_join(self):
        left = {'id': ['a', 'c', 'd', 'f'], 'x': [33, 44, 55, 66]}
        right = {'id': ['a', 'b', 'c', 'd'], 'y': [11, 22, 33, 44]}
        results = left_join(left, right, 'id')
        expected = {'id': ['a', 'c', 'd', 'f'], 'x': [33, 44, 55, 66], 'y': [11, 33, 44, None]}
        self.assertTrue(records_equal(results, expected))

    def test_right_join(self):
        left = {'id': ['a', 'c', 'd', 'f'], 'x': [33, 44, 55, 66]}
        right = {'id': ['a', 'b', 'c', 'd'], 'y': [11, 22, 33, 44]}
        results = right_join(left, right, 'id')
        expected = {'id': ['a', 'b', 'c', 'd'], 'x': [33, None, 44, 55], 'y': [11, 22, 33, 44]}
        self.assertTrue(records_equal(results, expected))


class TestLocate(unittest.TestCase):
    def test_locate(self):
        l = [1, 2, 1, 2, 4, 5, 1]
        results = locate(l, 1)
        expected = [0, 2, 6]
        self.assertListEqual(results, expected)

    

    