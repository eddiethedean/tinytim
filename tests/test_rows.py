import pytest

import tinytim.rows as rows_functions

DATA = {'x': [1, 2, 3], 'y': [6, 7, 8]}


def test_row_dicts_to_data_basic():
    rows = [{'x': 1, 'y': 20}, {'x': 2, 'y': 21}, {'x': 3, 'y': 22}]
    results = rows_functions.row_dicts_to_data(rows)
    assert results == {'x': [1, 2, 3], 'y': [20, 21, 22]}
    assert rows == [{'x': 1, 'y': 20}, {'x': 2, 'y': 21}, {'x': 3, 'y': 22}]


def test_row_dicts_to_data_missing():
    rows = [{'x': 1, 'y': 20}, {'x': 2}, {'x': 3, 'y': 22}]
    results = rows_functions.row_dicts_to_data(rows)
    assert results == {'x': [1, 2, 3], 'y': [20, None, 22]}
    assert rows == [{'x': 1, 'y': 20}, {'x': 2}, {'x': 3, 'y': 22}]


def test_row_dict():
    results = rows_functions.row_dict(DATA, 1)
    assert results == {'x': 2, 'y': 7}
    assert DATA == {'x': [1, 2, 3], 'y': [6, 7, 8]}


def test_row_values():
    results = rows_functions.row_values(DATA, 0)
    assert results == (1, 6)
    assert DATA == {'x': [1, 2, 3], 'y': [6, 7, 8]}


def test_iterrows():
    generator = rows_functions.iterrows(DATA)
    v1 = next(generator)
    assert v1 == (0, {'x': 1, 'y': 6})
    v2 = next(generator)
    assert v2 == (1, {'x': 2, 'y': 7})
    v3 = next(generator)
    assert v3 == (2, {'x': 3, 'y': 8})
    with pytest.raises(StopIteration):
        next(generator)
    assert DATA == {'x': [1, 2, 3], 'y': [6, 7, 8]}


def test_itertuples():
    generator = rows_functions.itertuples(DATA)
    v1 = next(generator)
    assert v1 == (1, 6)
    v2 = next(generator)
    assert v2 == (2, 7)
    v3 = next(generator)
    assert v3 == (3, 8)
    with pytest.raises(StopIteration):
        next(generator)
    assert DATA == {'x': [1, 2, 3], 'y': [6, 7, 8]}


def test_itervalues():
    generator = rows_functions.itervalues(DATA)
    v1 = next(generator)
    assert v1 == (1, 6)
    v2 = next(generator)
    assert v2 == (2, 7)
    v3 = next(generator)
    assert v3 == (3, 8)
    with pytest.raises(StopIteration):
        next(generator)
    assert DATA == {'x': [1, 2, 3], 'y': [6, 7, 8]}


def test_values():
    results = rows_functions.values(DATA)
    assert results == ((1, 6), (2, 7), (3, 8))
    assert DATA == {'x': [1, 2, 3], 'y': [6, 7, 8]}


def test_row_value_counts():
    data = {'x': [1, 2, 3, 3], 'y': [6, 7, 3, 3]}
    result = rows_functions.row_value_counts(data)
    expected = {(3, 3): 2, (1, 6): 1, (2, 7): 1}
    assert result == expected


# Tests for records generator
def test_records():
    generator = rows_functions.records(DATA)
    r1 = next(generator)
    assert r1 == {'x': 1, 'y': 6}
    r2 = next(generator)
    assert r2 == {'x': 2, 'y': 7}
    r3 = next(generator)
    assert r3 == {'x': 3, 'y': 8}
    with pytest.raises(StopIteration):
        next(generator)


def test_records_list_conversion():
    result = list(rows_functions.records(DATA))
    expected = [{'x': 1, 'y': 6}, {'x': 2, 'y': 7}, {'x': 3, 'y': 8}]
    assert result == expected


# Tests for records_equal edge cases
def test_records_equal_different_column_order():
    d1 = {'x': [1, 2], 'y': [3, 4]}
    d2 = {'y': [3, 4], 'x': [1, 2]}  # Different order
    assert rows_functions.records_equal(d1, d2) is True


def test_records_equal_different_row_order():
    d1 = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    d2 = {'x': [2, 1, 3], 'y': [5, 4, 6]}  # Rows in different order
    assert rows_functions.records_equal(d1, d2) is True


def test_records_equal_different_columns():
    d1 = {'x': [1, 2], 'y': [3, 4]}
    d2 = {'x': [1, 2], 'z': [3, 4]}  # Different column name
    assert rows_functions.records_equal(d1, d2) is False


def test_records_equal_different_row_count():
    d1 = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    d2 = {'x': [1, 2], 'y': [4, 5]}
    assert rows_functions.records_equal(d1, d2) is False


def test_records_equal_missing_row():
    d1 = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    d2 = {'x': [1, 2], 'y': [4, 5]}  # Missing row
    assert rows_functions.records_equal(d1, d2) is False


# Tests for row_values_to_data
def test_row_values_to_data_basic():
    rows = [[1, 2], [3, 4], [5, 6]]
    columns = ['x', 'y']
    result = rows_functions.row_values_to_data(rows, columns)
    assert result == {'x': [1, 3, 5], 'y': [2, 4, 6]}


def test_row_values_to_data_missing_values():
    rows = [[1, 2], [3], [5, 6]]  # Second row missing a value
    columns = ['x', 'y']
    result = rows_functions.row_values_to_data(rows, columns)
    assert result == {'x': [1, 3, 5], 'y': [2, None, 6]}


def test_row_values_to_data_custom_missing_value():
    rows = [[1, 2], [3], [5, 6]]
    columns = ['x', 'y']
    result = rows_functions.row_values_to_data(rows, columns, missing_value=-999)
    assert result == {'x': [1, 3, 5], 'y': [2, -999, 6]}


def test_row_values_to_data_empty():
    rows = []
    columns = ['x', 'y']
    result = rows_functions.row_values_to_data(rows, columns)
    assert result == {}  # Empty rows produce empty dict


def test_row_values_to_data_single_column():
    rows = [[1], [2], [3]]
    columns = ['x']
    result = rows_functions.row_values_to_data(rows, columns)
    assert result == {'x': [1, 2, 3]}


# Test row_dicts_to_data with all missing values
def test_row_dicts_to_data_all_keys_present():
    rows = [{'x': 1, 'y': 2, 'z': 3}, {'x': 4, 'y': 5, 'z': 6}]
    result = rows_functions.row_dicts_to_data(rows)
    assert result == {'x': [1, 4], 'y': [2, 5], 'z': [3, 6]}


# Test records_equal with identical data
def test_records_equal_identical():
    d1 = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    d2 = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    assert rows_functions.records_equal(d1, d2) is True


# Edge case: single row
def test_row_dict_single_row_data():
    data = {'x': [99], 'y': [88]}
    result = rows_functions.row_dict(data, 0)
    assert result == {'x': 99, 'y': 88}


def test_row_values_single_row_data():
    data = {'x': [99], 'y': [88]}
    result = rows_functions.row_values(data, 0)
    assert result == (99, 88)


# Test records_equal with non-matching row
def test_records_equal_one_different_value():
    d1 = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    d2 = {'x': [1, 2, 3], 'y': [4, 5, 99]}  # Last value different
    assert rows_functions.records_equal(d1, d2) is False


# Test row_dicts_to_data with varying missing keys
def test_row_dicts_to_data_multiple_missing_keys():
    rows = [{'x': 1}, {'y': 2}, {'z': 3}]
    result = rows_functions.row_dicts_to_data(rows)
    # All keys should be present with None for missing values
    assert 'x' in result and 'y' in result and 'z' in result
    assert result['x'] == [1, None, None]
    assert result['y'] == [None, 2, None]
    assert result['z'] == [None, None, 3]
