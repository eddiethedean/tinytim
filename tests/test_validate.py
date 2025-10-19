from tinytim.validate import data_columns_same_len, valid_table_mapping


def test_data_columns_same_len_empty_data():
    data = {}
    assert data_columns_same_len(data) is True


def test_data_columns_same_len_single_column():
    data = {'x': [1, 2, 3]}
    assert data_columns_same_len(data) is True


def test_data_columns_same_len_multiple_columns_same_length():
    data = {'x': [1, 2, 3], 'y': [4, 5, 6], 'z': [7, 8, 9]}
    assert data_columns_same_len(data) is True


def test_data_columns_same_len_mismatched_lengths():
    data = {'x': [1, 2, 3], 'y': [4, 5]}
    assert data_columns_same_len(data) is False


def test_data_columns_same_len_multiple_mismatched():
    data = {'x': [1, 2, 3], 'y': [4, 5], 'z': [6, 7, 8, 9]}
    assert data_columns_same_len(data) is False


def test_data_columns_same_len_empty_columns():
    data = {'x': [], 'y': [], 'z': []}
    assert data_columns_same_len(data) is True


def test_valid_table_mapping_valid_dict():
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    assert valid_table_mapping(data) is True


def test_valid_table_mapping_invalid_not_mapping():
    data = [1, 2, 3]  # List, not a mapping
    assert valid_table_mapping(data) is False


def test_valid_table_mapping_mismatched_lengths():
    data = {'x': [1, 2, 3], 'y': [4, 5]}
    assert valid_table_mapping(data) is False


def test_valid_table_mapping_empty_data():
    data = {}
    assert valid_table_mapping(data) is True


def test_valid_table_mapping_string_not_mapping():
    data = "not a mapping"
    assert valid_table_mapping(data) is False


def test_valid_table_mapping_none():
    data = None
    assert valid_table_mapping(data) is False


def test_valid_table_mapping_single_column():
    data = {'x': [1, 2, 3, 4, 5]}
    assert valid_table_mapping(data) is True

