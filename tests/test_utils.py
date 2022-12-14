import unittest

from hasattrs import has_mapping_attrs

import tinytim.utils as utils_functions


class TestUniques(unittest.TestCase):
    def test_basic(self):
        values = [1, 1, 2, 4, 5, 2, 0, 6, 1]
        results = utils_functions.uniques(values)
        self.assertListEqual(results, [1, 2, 4, 5, 0, 6])
        self.assertListEqual(values, [1, 1, 2, 4, 5, 2, 0, 6, 1])


class TestRowValueTuples(unittest.TestCase):
    def test_basic(self):
        data = {'x': [1, 2, 3], 'y': [6, 7, 8], 'z': [9, 10, 11]}
        results = utils_functions.row_value_tuples(data, ['x', 'z'])
        self.assertTupleEqual(results, ((1, 9), (2, 10), (3, 11)))
        self.assertDictEqual(data, {'x': [1, 2, 3], 'y': [6, 7, 8], 'z': [9, 10, 11]})





class TestAllBool(unittest.TestCase):
    def test_int(self):
        values = [1, True, False, True]
        result = utils_functions.all_bool(values)
        self.assertFalse(result)
        self.assertListEqual(values, [1, True, False, True])

    def test_bools(self):
        values = [True, True, False, True]
        result = utils_functions.all_bool(values)
        self.assertTrue(result)
        self.assertListEqual(values, [True, True, False, True])


class TestHasMappingAttrs(unittest.TestCase):
    def test_dict(self):
        obj = dict()
        result = has_mapping_attrs(obj)
        self.assertTrue(result)

    def test_list(self):
        obj = list()
        result = has_mapping_attrs(obj)
        self.assertFalse(result)


class TestAllKeys(unittest.TestCase):
    def test_basic(self):
        dicts = [{'x': 1, 'y': 2}, {'x': 4, 'z': 7}]
        results = utils_functions.all_keys(dicts)
        self.assertListEqual(results, ['x', 'y', 'z'])
        self.assertListEqual(dicts, [{'x': 1, 'y': 2}, {'x': 4, 'z': 7}])


class TestRowValuesGenerator(unittest.TestCase):
    def test_basic(self):
        row = {'x': 1, 'y': 4, 'z': 8}
        generator = utils_functions.row_values_generator(row)
        v1 = next(generator)
        self.assertEqual(v1, 1)
        v2 = next(generator)
        self.assertEqual(v2, 4)
        v3 = next(generator)
        self.assertEqual(v3, 8)
        with self.assertRaises(StopIteration):
            next(generator)


class TestSliceToRange(unittest.TestCase):
    def test_basic(self):
        s = slice(0, 3, 1)
        r = utils_functions.slice_to_range(s)
        self.assertEqual(r, range(0, 3, 1))

    def test_zero_step(self):
        s = slice(1, 4, 0)
        with self.assertRaises(ValueError):
            utils_functions.slice_to_range(s)


class TestCombineNamesRows(unittest.TestCase):
    def test_basic(self):
        column_names = ['x', 'y']
        rows = ((1, 2), (4, 5), (8, 10))
        results = utils_functions.combine_names_rows(column_names, rows)
        self.assertDictEqual(results, {'x': [1, 4, 8], 'y': [2, 5, 10]})
        

class TestNunique(unittest.TestCase):
    def test_basic(self):
        data = {'x': [1, 2, 2], 'y': [6, 7, 8], 'z': [9, 9, 9]}
        results = utils_functions.nunique(data)
        self.assertDictEqual(results, {'x': 2, 'y': 3, 'z': 1})


if __name__ == '__main__':
    unittest.main()