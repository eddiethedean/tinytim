import tinytim.edit as edit_functions


def test_edit_row_items_inplace():
    data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    result = edit_functions.edit_row_items_inplace(data, 0, {'x': 11, 'y': 66})
    assert result is None
    assert data == {'x': [11, 2, 3], 'y': [66, 7, 8]}


def test_edit_row_values_inplace():
    data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    result = edit_functions.edit_row_values_inplace(data, 1, (22, 77))
    assert result is None
    assert data == {'x': [1, 22, 3], 'y': [6, 77, 8]}


def test_edit_column_inplace():
    data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    result = edit_functions.edit_column_inplace(data, 'x', [11, 22, 33])
    assert result is None
    assert data == {'x': [11, 22, 33], 'y': [6, 7, 8]}


def test_drop_row_inplace():
    data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    result = edit_functions.drop_row_inplace(data, 1)
    assert result is None
    assert data == {'x': [1, 3], 'y': [6, 8]}


def test_drop_label_inplace_not_none():
    labels = [1, 2, 3, 4, 5]
    result = edit_functions.drop_label_inplace(labels, 1)
    assert result is None
    assert labels == [1, 3, 4, 5]


def test_drop_label_inplace_is_none():
    labels = None
    result = edit_functions.drop_label_inplace(labels, 1)
    assert result is None
    assert labels is None


def test_drop_column_inplace():
    data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    result = edit_functions.drop_column_inplace(data, 'y')
    assert result is None
    assert data == {'x': [1, 2, 3]}


def test_edit_value_inplace():
    data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    result = edit_functions.edit_value_inplace(data, 'x', 0, 11)
    assert result is None
    assert data == {'x': [11, 2, 3], 'y': [6, 7, 8]}


def test_replace_column_names():
    data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    results = edit_functions.replace_column_names(data, ('xx', 'yy'))
    assert results == {'xx': [1, 2, 3], 'yy': [6, 7, 8]}
    assert data == {'x': [1, 2, 3], 'y': [6, 7, 8]}


def test_edit_row_items_all_keys():
    data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    results = edit_functions.edit_row_items(data, 2, {'x': 33, 'y': 88})
    assert results == {'x': [1, 2, 33], 'y': [6, 7, 88]}
    assert data == {'x': [1, 2, 3], 'y': [6, 7, 8]}


def test_edit_row_items_one_key():
    data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    results = edit_functions.edit_row_items(data, 0, {'x': 55})
    assert results == {'x': [55, 2, 3], 'y': [6, 7, 8]}
    assert data == {'x': [1, 2, 3], 'y': [6, 7, 8]}


def test_edit_row_values():
    data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    results = edit_functions.edit_row_values(data, 1, (22, 77))
    assert results == {'x': [1, 22, 3], 'y': [6, 77, 8]}
    assert data == {'x': [1, 2, 3], 'y': [6, 7, 8]}


def test_edit_column():
    data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    results = edit_functions.edit_column(data, 'x', [4, 5, 6])
    assert results == {'x': [4, 5, 6], 'y': [6, 7, 8]}
    assert data == {'x': [1, 2, 3], 'y': [6, 7, 8]}


def test_edit_value():
    data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    results = edit_functions.edit_value(data, 'y', 2, 88)
    assert results == {'x': [1, 2, 3], 'y': [6, 7, 88]}
    assert data == {'x': [1, 2, 3], 'y': [6, 7, 8]}


def test_drop_row():
    data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    results = edit_functions.drop_row(data, 0)
    assert results == {'x': [2, 3], 'y': [7, 8]}
    assert data == {'x': [1, 2, 3], 'y': [6, 7, 8]}


def test_drop_label_not_none():
    labels = [1, 2, 3, 4]
    results = edit_functions.drop_label(labels, 1)
    assert results == [1, 3, 4]
    assert labels == [1, 2, 3, 4]


def test_drop_label_is_none():
    labels = None
    results = edit_functions.drop_label(labels, 1)
    assert results is None
    assert labels is None


def test_drop_column():
    data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    results = edit_functions.drop_column(data, 'y')
    assert results == {'x': [1, 2, 3]}
    assert data == {'x': [1, 2, 3], 'y': [6, 7, 8]}


# Tests for operator_column and operator_column_inplace
def test_add_to_column_inplace_scalar():
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    result = edit_functions.add_to_column_inplace(data, 'x', 10)
    assert result is None
    assert data == {'x': [11, 12, 13], 'y': [4, 5, 6]}


def test_add_to_column_inplace_sequence():
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    edit_functions.add_to_column_inplace(data, 'x', [10, 20, 30])
    assert data == {'x': [11, 22, 33], 'y': [4, 5, 6]}


def test_add_to_column_scalar():
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    result = edit_functions.add_to_column(data, 'x', 10)
    assert result == {'x': [11, 12, 13], 'y': [4, 5, 6]}
    assert data == {'x': [1, 2, 3], 'y': [4, 5, 6]}


def test_add_to_column_sequence():
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    result = edit_functions.add_to_column(data, 'x', [10, 20, 30])
    assert result == {'x': [11, 22, 33], 'y': [4, 5, 6]}


def test_subtract_from_column_inplace():
    data = {'x': [10, 20, 30], 'y': [4, 5, 6]}
    edit_functions.subtract_from_column_inplace(data, 'x', 5)
    assert data == {'x': [5, 15, 25], 'y': [4, 5, 6]}


def test_subtract_from_column():
    data = {'x': [10, 20, 30], 'y': [4, 5, 6]}
    result = edit_functions.subtract_from_column(data, 'x', 5)
    assert result == {'x': [5, 15, 25], 'y': [4, 5, 6]}
    assert data == {'x': [10, 20, 30], 'y': [4, 5, 6]}


def test_multiply_column_inplace():
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    edit_functions.multiply_column_inplace(data, 'x', 10)
    assert data == {'x': [10, 20, 30], 'y': [4, 5, 6]}


def test_multiply_column():
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    result = edit_functions.multiply_column(data, 'x', 10)
    assert result == {'x': [10, 20, 30], 'y': [4, 5, 6]}
    assert data == {'x': [1, 2, 3], 'y': [4, 5, 6]}


def test_divide_column_inplace():
    data = {'x': [10, 20, 30], 'y': [4, 5, 6]}
    edit_functions.divide_column_inplace(data, 'x', 2)
    assert data == {'x': [5.0, 10.0, 15.0], 'y': [4, 5, 6]}


def test_divide_column():
    data = {'x': [10, 20, 30], 'y': [4, 5, 6]}
    result = edit_functions.divide_column(data, 'x', 2)
    assert result == {'x': [5.0, 10.0, 15.0], 'y': [4, 5, 6]}
    assert data == {'x': [10, 20, 30], 'y': [4, 5, 6]}


# Test operator functions with sequences
def test_operator_column_inplace():
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    edit_functions.operator_column_inplace(data, 'x', 10, lambda a, b: a * b)
    assert data == {'x': [10, 20, 30], 'y': [4, 5, 6]}


def test_operator_column():
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    result = edit_functions.operator_column(data, 'x', 2, lambda a, b: a ** b)
    assert result == {'x': [1, 4, 9], 'y': [4, 5, 6]}
    assert data == {'x': [1, 2, 3], 'y': [4, 5, 6]}


# Edge cases
def test_edit_column_inplace_empty_data():
    data = {'x': [], 'y': []}
    edit_functions.edit_column_inplace(data, 'x', [])
    assert data == {'x': [], 'y': []}


def test_drop_row_inplace_first():
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    edit_functions.drop_row_inplace(data, 0)
    assert data == {'x': [2, 3], 'y': [5, 6]}


def test_drop_row_inplace_last():
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    edit_functions.drop_row_inplace(data, 2)
    assert data == {'x': [1, 2], 'y': [4, 5]}


def test_edit_value_first_position():
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    result = edit_functions.edit_value(data, 'x', 0, 99)
    assert result == {'x': [99, 2, 3], 'y': [4, 5, 6]}


def test_edit_value_last_position():
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    result = edit_functions.edit_value(data, 'x', 2, 99)
    assert result == {'x': [1, 2, 99], 'y': [4, 5, 6]}


# Test edit_column with string values
def test_edit_column_strings():
    data = {'x': ['a', 'b', 'c'], 'y': [1, 2, 3]}
    result = edit_functions.edit_column(data, 'x', ['X', 'Y', 'Z'])
    assert result == {'x': ['X', 'Y', 'Z'], 'y': [1, 2, 3]}
    assert data == {'x': ['a', 'b', 'c'], 'y': [1, 2, 3]}


# Test operator_column with mismatched lengths
def test_operator_column_inplace_mismatched_length():
    import pytest
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    with pytest.raises(ValueError, match='values length must match'):
        edit_functions.operator_column_inplace(data, 'x', [10, 20], lambda a, b: a + b)


def test_operator_column_mismatched_length():
    import pytest
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    with pytest.raises(ValueError, match='values length must match'):
        edit_functions.operator_column(data, 'x', [10, 20], lambda a, b: a + b)


# Test replace_column_names edge cases
def test_replace_column_names_mismatched_length():
    import pytest
    data = {'x': [1, 2], 'y': [3, 4]}
    with pytest.raises(ValueError, match='new_names must be same size'):
        edit_functions.replace_column_names(data, ('a',))  # Only 1 name for 2 columns


def test_replace_column_names_single_column():
    data = {'x': [1, 2, 3]}
    result = edit_functions.replace_column_names(data, ('new_x',))
    assert result == {'new_x': [1, 2, 3]}


def test_edit_column_inplace_with_string_value():
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    # Edit column with a single string value (repeats for all rows)
    edit_functions.edit_column_inplace(data, 'y', 'same')
    assert data == {'x': [1, 2, 3], 'y': ['same', 'same', 'same']}


def test_edit_column_with_string_value():
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    result = edit_functions.edit_column(data, 'y', 'same')
    assert result == {'x': [1, 2, 3], 'y': ['same', 'same', 'same']}


# Test edit_row_items with partial row update
def test_edit_row_items_inplace_partial():
    data = {'x': [1, 2, 3], 'y': [4, 5, 6], 'z': [7, 8, 9]}
    edit_functions.edit_row_items_inplace(data, 1, {'x': 99})
    assert data == {'x': [1, 99, 3], 'y': [4, 5, 6], 'z': [7, 8, 9]}


# Test operator_column_inplace with empty data
def test_operator_column_inplace_empty():
    data = {'x': [], 'y': []}
    edit_functions.operator_column_inplace(data, 'x', 10, lambda a, b: a + b)
    assert data == {'x': [], 'y': []}


# Test operator_column with empty data
def test_operator_column_empty():
    data = {'x': [], 'y': []}
    result = edit_functions.operator_column(data, 'x', 10, lambda a, b: a + b)
    assert result == {'x': [], 'y': []}
