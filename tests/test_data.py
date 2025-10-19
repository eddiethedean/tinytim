import tinytim.data as data_functions

DATA = {'x': [1, 2, 3], 'y': [6, 7, 8]}


def test_column_count():
    result = data_functions.column_count(DATA)
    assert result == 2


def test_row_count():
    result = data_functions.row_count(DATA)
    assert result == 3


def test_shape():
    result = data_functions.shape(DATA)
    assert result == (3, 2)


def test_size():
    result = data_functions.size(DATA)
    assert result == 6


def test_first_column_name():
    result = data_functions.first_column_name(DATA)
    assert result == 'x'


def test_column_names():
    result = data_functions.column_names(DATA)
    assert result == ['x', 'y']


def test_head():
    result = data_functions.head(DATA, 2)
    assert result == {'x': [1, 2], 'y': [6, 7]}


def test_tail():
    result = data_functions.tail(DATA, 2)
    assert result == {'x': [2, 3], 'y': [7, 8]}


def test_index():
    result = data_functions.index(DATA)
    assert result == (0, 1, 2)


def test_table_value():
    result = data_functions.table_value(DATA, 'x', 1)
    assert result == 2


def test_column_values():
    result = data_functions.column_values(DATA, 'y')
    assert result == [6, 7, 8]


# Edge cases
def test_first_column_name_empty_data():
    import pytest
    data = {}
    with pytest.raises(StopIteration):
        data_functions.first_column_name(data)


def test_shape_empty_data():
    data = {}
    result = data_functions.shape(data)
    assert result == (0, 0)


def test_head_empty_data():
    data = {'x': [], 'y': []}
    result = data_functions.head(data, 5)
    assert result == {'x': [], 'y': []}


def test_tail_empty_data():
    data = {'x': [], 'y': []}
    result = data_functions.tail(data, 5)
    assert result == {'x': [], 'y': []}


# More edge cases
def test_head_n_greater_than_rows():
    result = data_functions.head(DATA, 10)
    assert result == DATA


def test_tail_n_greater_than_rows():
    result = data_functions.tail(DATA, 10)
    assert result == DATA


def test_size_empty():
    data = {}
    result = data_functions.size(data)
    assert result == 0


def test_column_count_single_column():
    data = {'x': [1, 2, 3]}
    result = data_functions.column_count(data)
    assert result == 1


# Test head/tail with specific n values
def test_head_with_zero():
    result = data_functions.head(DATA, 0)
    assert result == {'x': [], 'y': []}  # n=0 returns empty


def test_tail_with_zero():
    result = data_functions.tail(DATA, 0)
    assert result == DATA  # n=0 for tail returns all data


def test_head_with_one():
    result = data_functions.head(DATA, 1)
    assert result == {'x': [1], 'y': [6]}


def test_tail_with_one():
    result = data_functions.tail(DATA, 1)
    assert result == {'x': [3], 'y': [8]}


# Test row_count exception handling
def test_row_count_empty_data():
    data = {}
    result = data_functions.row_count(data)
    assert result == 0  # Empty data has 0 rows
