from tinytim.filter import (
    column_filter,
    filter_by_column_eq,
    filter_by_column_func,
    filter_by_column_ge,
    filter_by_column_gt,
    filter_by_column_isin,
    filter_by_column_le,
    filter_by_column_lt,
    filter_by_column_ne,
    filter_by_column_notin,
    filter_by_columns,
    filter_by_columns_inplace,
    filter_by_indexes,
    filter_by_indexes_inplace,
    filter_data,
    filter_list_by_indexes,
    indexes_from_filter,
    only_columns,
    only_columns_inplace,
    sample,
    sample_indexes,
)

DATA = {'x': [1, 2, 3, 4, 5], 'y': [10, 20, 30, 40, 50], 'z': ['a', 'b', 'c', 'd', 'e']}


# Tests for column_filter
def test_column_filter():
    column = [1, 2, 3, 4, 5]
    result = column_filter(column, lambda x: x > 2)
    assert result == [False, False, True, True, True]


def test_column_filter_all_true():
    column = [1, 2, 3]
    result = column_filter(column, lambda x: x > 0)
    assert result == [True, True, True]


def test_column_filter_all_false():
    column = [1, 2, 3]
    result = column_filter(column, lambda x: x > 10)
    assert result == [False, False, False]


# Tests for indexes_from_filter
def test_indexes_from_filter():
    f = [False, True, False, True, True]
    result = indexes_from_filter(f)
    assert result == [1, 3, 4]


def test_indexes_from_filter_all_true():
    f = [True, True, True]
    result = indexes_from_filter(f)
    assert result == [0, 1, 2]


def test_indexes_from_filter_all_false():
    f = [False, False, False]
    result = indexes_from_filter(f)
    assert result == []


# Tests for filter_list_by_indexes
def test_filter_list_by_indexes():
    values = ['a', 'b', 'c', 'd', 'e']
    indexes = [0, 2, 4]
    result = filter_list_by_indexes(values, indexes)
    assert result == ['a', 'c', 'e']


def test_filter_list_by_indexes_empty():
    values = ['a', 'b', 'c']
    indexes = []
    result = filter_list_by_indexes(values, indexes)
    assert result == []


# Tests for filter_by_indexes
def test_filter_by_indexes():
    result = filter_by_indexes(DATA, [0, 2, 4])
    assert result == {'x': [1, 3, 5], 'y': [10, 30, 50], 'z': ['a', 'c', 'e']}


def test_filter_by_indexes_empty():
    result = filter_by_indexes(DATA, [])
    assert result == {'x': [], 'y': [], 'z': []}


def test_filter_by_indexes_single():
    result = filter_by_indexes(DATA, [2])
    assert result == {'x': [3], 'y': [30], 'z': ['c']}


# Tests for filter_by_indexes_inplace
def test_filter_by_indexes_inplace():
    data = {'x': [1, 2, 3, 4, 5], 'y': [10, 20, 30, 40, 50]}
    result = filter_by_indexes_inplace(data, [1, 3])
    assert result is None  # Should return None
    assert data == {'x': [2, 4], 'y': [20, 40]}


def test_filter_by_indexes_inplace_empty():
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    filter_by_indexes_inplace(data, [])
    assert data == {'x': [], 'y': []}


# Tests for filter_data
def test_filter_data():
    f = [True, False, True, False, True]
    result = filter_data(DATA, f)
    assert result == {'x': [1, 3, 5], 'y': [10, 30, 50], 'z': ['a', 'c', 'e']}


def test_filter_data_all_true():
    f = [True, True, True, True, True]
    result = filter_data(DATA, f)
    assert result == DATA


def test_filter_data_all_false():
    f = [False, False, False, False, False]
    result = filter_data(DATA, f)
    assert result == {'x': [], 'y': [], 'z': []}


# Tests for filter_by_column_func
def test_filter_by_column_func():
    result = filter_by_column_func(DATA, 'x', lambda v: v > 3)
    assert result == {'x': [4, 5], 'y': [40, 50], 'z': ['d', 'e']}


def test_filter_by_column_func_no_matches():
    result = filter_by_column_func(DATA, 'x', lambda v: v > 100)
    assert result == {'x': [], 'y': [], 'z': []}


# Tests for filter_by_column_eq
def test_filter_by_column_eq():
    result = filter_by_column_eq(DATA, 'x', 3)
    assert result == {'x': [3], 'y': [30], 'z': ['c']}


def test_filter_by_column_eq_no_match():
    result = filter_by_column_eq(DATA, 'x', 99)
    assert result == {'x': [], 'y': [], 'z': []}


# Tests for filter_by_column_ne
def test_filter_by_column_ne():
    data = {'x': [1, 2, 3, 2, 1], 'y': [10, 20, 30, 40, 50]}
    result = filter_by_column_ne(data, 'x', 2)
    assert result == {'x': [1, 3, 1], 'y': [10, 30, 50]}


def test_filter_by_column_ne_all_match():
    result = filter_by_column_ne(DATA, 'x', 99)
    assert len(result['x']) == 5  # All rows kept


# Tests for filter_by_column_gt
def test_filter_by_column_gt():
    result = filter_by_column_gt(DATA, 'x', 3)
    assert result == {'x': [4, 5], 'y': [40, 50], 'z': ['d', 'e']}


# Tests for filter_by_column_lt
def test_filter_by_column_lt():
    result = filter_by_column_lt(DATA, 'x', 3)
    assert result == {'x': [1, 2], 'y': [10, 20], 'z': ['a', 'b']}


# Tests for filter_by_column_ge
def test_filter_by_column_ge():
    result = filter_by_column_ge(DATA, 'x', 3)
    assert result == {'x': [3, 4, 5], 'y': [30, 40, 50], 'z': ['c', 'd', 'e']}


def test_filter_by_column_ge_equals():
    result = filter_by_column_ge(DATA, 'x', 5)
    assert result == {'x': [5], 'y': [50], 'z': ['e']}


# Tests for filter_by_column_le
def test_filter_by_column_le():
    result = filter_by_column_le(DATA, 'x', 3)
    assert result == {'x': [1, 2, 3], 'y': [10, 20, 30], 'z': ['a', 'b', 'c']}


def test_filter_by_column_le_equals():
    result = filter_by_column_le(DATA, 'x', 1)
    assert result == {'x': [1], 'y': [10], 'z': ['a']}


# Tests for filter_by_column_isin
def test_filter_by_column_isin():
    result = filter_by_column_isin(DATA, 'x', [1, 3, 5])
    assert result == {'x': [1, 3, 5], 'y': [10, 30, 50], 'z': ['a', 'c', 'e']}


def test_filter_by_column_isin_empty():
    result = filter_by_column_isin(DATA, 'x', [])
    assert result == {'x': [], 'y': [], 'z': []}


def test_filter_by_column_isin_strings():
    result = filter_by_column_isin(DATA, 'z', ['a', 'c'])
    assert result == {'x': [1, 3], 'y': [10, 30], 'z': ['a', 'c']}


# Tests for filter_by_column_notin
def test_filter_by_column_notin():
    result = filter_by_column_notin(DATA, 'x', [2, 4])
    assert result == {'x': [1, 3, 5], 'y': [10, 30, 50], 'z': ['a', 'c', 'e']}


def test_filter_by_column_notin_empty():
    result = filter_by_column_notin(DATA, 'x', [])
    assert len(result['x']) == 5  # All rows kept


# Tests for sample
def test_sample_with_seed():
    result = sample(DATA, 2, random_state=42)
    assert len(result['x']) == 2
    assert len(result['y']) == 2
    # Same seed should give same results
    result2 = sample(DATA, 2, random_state=42)
    assert result == result2


def test_sample_without_seed():
    result = sample(DATA, 3)
    assert len(result['x']) == 3
    assert len(result['y']) == 3


def test_sample_single():
    result = sample(DATA, 1, random_state=42)
    assert len(result['x']) == 1


# Tests for sample_indexes
def test_sample_indexes_with_seed():
    result = sample_indexes(DATA, 2, random_state=42)
    assert len(result) == 2
    assert all(0 <= idx < 5 for idx in result)
    # Same seed should give same results
    result2 = sample_indexes(DATA, 2, random_state=42)
    assert result == result2


def test_sample_indexes_without_seed():
    result = sample_indexes(DATA, 3)
    assert len(result) == 3
    assert all(0 <= idx < 5 for idx in result)


# Tests for filter_by_columns
def test_filter_by_columns():
    result = filter_by_columns(DATA, ['x', 'z'])
    assert result == {'x': [1, 2, 3, 4, 5], 'z': ['a', 'b', 'c', 'd', 'e']}
    assert 'y' not in result


def test_filter_by_columns_single_column():
    result = filter_by_columns(DATA, ['x'])
    assert result == {'x': [1, 2, 3, 4, 5]}


def test_filter_by_columns_all_columns():
    result = filter_by_columns(DATA, ['x', 'y', 'z'])
    assert result == DATA


# Tests for filter_by_columns_inplace
def test_filter_by_columns_inplace():
    data = {'x': [1, 2, 3], 'y': [4, 5, 6], 'z': [7, 8, 9]}
    result = filter_by_columns_inplace(data, ['x', 'z'])
    assert result is None  # Should return None
    assert data == {'x': [1, 2, 3], 'z': [7, 8, 9]}
    assert 'y' not in data


def test_filter_by_columns_inplace_single():
    data = {'x': [1, 2], 'y': [3, 4]}
    filter_by_columns_inplace(data, ['x'])
    assert data == {'x': [1, 2]}


def test_filter_by_columns_inplace_all_columns():
    data = {'x': [1, 2], 'y': [3, 4]}
    filter_by_columns_inplace(data, ['x', 'y'])
    assert data == {'x': [1, 2], 'y': [3, 4]}


# Tests for aliases
def test_only_columns_alias():
    result = only_columns(DATA, ['x'])
    assert result == {'x': [1, 2, 3, 4, 5]}


def test_only_columns_inplace_alias():
    data = {'x': [1, 2], 'y': [3, 4]}
    only_columns_inplace(data, ['x'])
    assert data == {'x': [1, 2]}


# Edge cases
def test_filter_empty_data():
    data = {'x': [], 'y': []}
    result = filter_by_column_gt(data, 'x', 0)
    assert result == {'x': [], 'y': []}


def test_sample_all_rows():
    result = sample(DATA, 5, random_state=42)
    assert len(result['x']) == 5

