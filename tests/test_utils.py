import pytest
from hasattrs import has_mapping_attrs

import tinytim.utils as utils_functions


def test_uniques():
    values = [1, 1, 2, 4, 5, 2, 0, 6, 1]
    results = utils_functions.uniques(values)
    assert results == [1, 2, 4, 5, 0, 6]
    assert values == [1, 1, 2, 4, 5, 2, 0, 6, 1]


def test_row_value_tuples():
    data = {'x': [1, 2, 3], 'y': [6, 7, 8], 'z': [9, 10, 11]}
    results = utils_functions.row_value_tuples(data, ['x', 'z'])
    assert results == ((1, 9), (2, 10), (3, 11))
    assert data == {'x': [1, 2, 3], 'y': [6, 7, 8], 'z': [9, 10, 11]}


def test_all_bool_int():
    values = [1, True, False, True]
    result = utils_functions.all_bool(values)
    assert not result
    assert values == [1, True, False, True]


def test_all_bool_bools():
    values = [True, True, False, True]
    result = utils_functions.all_bool(values)
    assert result
    assert values == [True, True, False, True]


def test_has_mapping_attrs_dict():
    obj = {}
    result = has_mapping_attrs(obj)
    assert result


def test_has_mapping_attrs_list():
    obj = []
    result = has_mapping_attrs(obj)
    assert not result


def test_all_keys():
    dicts = [{'x': 1, 'y': 2}, {'x': 4, 'z': 7}]
    results = utils_functions.all_keys(dicts)
    assert results == ['x', 'y', 'z']
    assert dicts == [{'x': 1, 'y': 2}, {'x': 4, 'z': 7}]


def test_row_values_generator():
    row = {'x': 1, 'y': 4, 'z': 8}
    generator = utils_functions.row_values_generator(row)
    v1 = next(generator)
    assert v1 == 1
    v2 = next(generator)
    assert v2 == 4
    v3 = next(generator)
    assert v3 == 8
    with pytest.raises(StopIteration):
        next(generator)


def test_slice_to_range_basic():
    s = slice(0, 3, 1)
    r = utils_functions.slice_to_range(s)
    assert r == range(0, 3, 1)


def test_slice_to_range_zero_step():
    s = slice(1, 4, 0)
    with pytest.raises(ValueError):
        utils_functions.slice_to_range(s)


def test_combine_names_rows():
    column_names = ['x', 'y']
    rows = ((1, 2), (4, 5), (8, 10))
    results = utils_functions.combine_names_rows(column_names, rows)
    assert results == {'x': [1, 4, 8], 'y': [2, 5, 10]}


def test_nunique():
    data = {'x': [1, 2, 2], 'y': [6, 7, 8], 'z': [9, 9, 9]}
    results = utils_functions.nunique(data)
    assert results == {'x': 2, 'y': 3, 'z': 1}


def test_nuniques():
    values = [1, 1, 2, 4, 5, 2, 0, 6, 1]
    result = utils_functions.nuniques(values)
    assert result == 6


def test_nuniques_all_unique():
    values = [1, 2, 3, 4, 5]
    result = utils_functions.nuniques(values)
    assert result == 5


def test_nuniques_all_same():
    values = [1, 1, 1, 1]
    result = utils_functions.nuniques(values)
    assert result == 1


# Tests for slice_to_range edge cases
def test_slice_to_range_negative_step():
    s = slice(10, 0, -1)
    r = utils_functions.slice_to_range(s)
    assert r == range(9, 0, -1)


def test_slice_to_range_with_stop_parameter():
    s = slice(None, None, 1)
    r = utils_functions.slice_to_range(s, stop=10)
    assert r == range(0, 10, 1)


def test_slice_to_range_negative_step_with_none_start():
    s = slice(None, 0, -1)
    r = utils_functions.slice_to_range(s, stop=10)
    assert r == range(9, 0, -1)  # start becomes stop-1


def test_slice_to_range_none_stop_raises():
    s = slice(0, None, 1)
    with pytest.raises(ValueError, match='stop cannot be None'):
        utils_functions.slice_to_range(s)


# Tests for set_values_to_one
def test_set_values_to_one():
    s = [1, 2, 3, 4, 5]
    utils_functions.set_values_to_one(s, 99)
    assert s == [99, 99, 99, 99, 99]


def test_set_values_to_one_empty():
    s = []
    utils_functions.set_values_to_one(s, 99)
    assert s == []


def test_set_values_to_one_single():
    s = [1]
    utils_functions.set_values_to_one(s, 'x')
    assert s == ['x']


# Tests for set_values_to_many
def test_set_values_to_many():
    s = [1, 2, 3, 4]
    values = [10, 20, 30, 40]
    utils_functions.set_values_to_many(s, values)
    assert s == [10, 20, 30, 40]


def test_set_values_to_many_mismatched_length():
    s = [1, 2, 3]
    values = [10, 20]  # Wrong length
    with pytest.raises(AttributeError, match='s and values must be same len'):
        utils_functions.set_values_to_many(s, values)


def test_set_values_to_many_empty():
    s = []
    values = []
    utils_functions.set_values_to_many(s, values)
    assert s == []


# Tests for combine_names_rows edge cases
def test_combine_names_rows_empty():
    column_names = ['x', 'y']
    rows = []
    result = utils_functions.combine_names_rows(column_names, rows)
    assert result == {}  # Empty rows produce empty dict


def test_combine_names_rows_single_row():
    column_names = ['x', 'y']
    rows = [(1, 2)]
    result = utils_functions.combine_names_rows(column_names, rows)
    assert result == {'x': [1], 'y': [2]}


# Tests for all_bool edge cases
def test_all_bool_empty():
    values = []
    result = utils_functions.all_bool(values)
    assert result is True  # all() of empty is True


def test_all_bool_mixed():
    values = [True, 1, False]
    result = utils_functions.all_bool(values)
    assert result is False


# Tests for all_keys edge cases
def test_all_keys_empty():
    dicts = []
    result = utils_functions.all_keys(dicts)
    assert result == []


def test_all_keys_single_dict():
    dicts = [{'x': 1, 'y': 2}]
    result = utils_functions.all_keys(dicts)
    assert result == ['x', 'y']


def test_all_keys_no_overlap():
    dicts = [{'x': 1}, {'y': 2}, {'z': 3}]
    result = utils_functions.all_keys(dicts)
    assert result == ['x', 'y', 'z']


# Additional slice_to_range tests for complete coverage
def test_slice_to_range_negative_step_with_start():
    s = slice(5, 0, -1)
    r = utils_functions.slice_to_range(s)
    assert r == range(4, 0, -1)
