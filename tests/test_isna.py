from tinytim.isna import (
    column_isnull,
    column_isnull_inplace,
    column_notnull,
    column_notnull_inplace,
    is_missing,
    isna,
    isnull,
    isnull_inplace,
    notna,
    notnull,
    notnull_inplace,
    row_isnull,
    row_isnull_inplace,
    row_notnull,
    row_notnull_inplace,
)


# Tests for is_missing helper function
def test_is_missing_with_none():
    assert is_missing(None, None) is True


def test_is_missing_with_value():
    assert is_missing(5, None) is False


def test_is_missing_custom_na_value():
    assert is_missing(-999, -999) is True
    assert is_missing(0, -999) is False


def test_is_missing_equality():
    assert is_missing("NA", "NA") is True
    assert is_missing("NA", "N/A") is False


# Tests for isnull / isna (they're the same)
def test_isnull_basic():
    data = {'x': [1, None, 3], 'y': [None, 5, 6]}
    result = isnull(data)
    assert result == {'x': [False, True, False], 'y': [True, False, False]}


def test_isna_basic():
    data = {'x': [1, None, 3], 'y': [None, 5, 6]}
    result = isna(data)
    assert result == {'x': [False, True, False], 'y': [True, False, False]}


def test_isnull_custom_na_value():
    data = {'x': [1, -999, 3], 'y': [-999, 5, 6]}
    result = isnull(data, na_value=-999)
    assert result == {'x': [False, True, False], 'y': [True, False, False]}


def test_isnull_no_nulls():
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    result = isnull(data)
    assert result == {'x': [False, False, False], 'y': [False, False, False]}


def test_isnull_all_nulls():
    data = {'x': [None, None], 'y': [None, None]}
    result = isnull(data)
    assert result == {'x': [True, True], 'y': [True, True]}


# Tests for notnull / notna
def test_notnull_basic():
    data = {'x': [1, None, 3], 'y': [None, 5, 6]}
    result = notnull(data)
    assert result == {'x': [True, False, True], 'y': [False, True, True]}


def test_notna_basic():
    data = {'x': [1, None, 3], 'y': [None, 5, 6]}
    result = notna(data)
    assert result == {'x': [True, False, True], 'y': [False, True, True]}


def test_notnull_custom_na_value():
    data = {'x': [1, -999, 3], 'y': [-999, 5, 6]}
    result = notnull(data, na_value=-999)
    assert result == {'x': [True, False, True], 'y': [False, True, True]}


# Tests for isnull_inplace
def test_isnull_inplace_basic():
    data = {'x': [1, None, 3], 'y': [None, 5, 6]}
    result = isnull_inplace(data)
    assert result is None  # Should return None
    assert data == {'x': [False, True, False], 'y': [True, False, False]}


def test_isnull_inplace_custom_na_value():
    data = {'x': [1, -999, 3], 'y': [-999, 5, 6]}
    isnull_inplace(data, na_value=-999)
    assert data == {'x': [False, True, False], 'y': [True, False, False]}


# Tests for notnull_inplace
def test_notnull_inplace_basic():
    data = {'x': [1, None, 3], 'y': [None, 5, 6]}
    result = notnull_inplace(data)
    assert result is None  # Should return None
    assert data == {'x': [True, False, True], 'y': [False, True, True]}


def test_notnull_inplace_custom_na_value():
    data = {'x': [1, -999, 3], 'y': [-999, 5, 6]}
    notnull_inplace(data, na_value=-999)
    assert data == {'x': [True, False, True], 'y': [False, True, True]}


# Tests for column_isnull
def test_column_isnull_basic():
    column = [1, None, 3, None, 5]
    result = column_isnull(column)
    assert result == [False, True, False, True, False]


def test_column_isnull_custom_na_value():
    column = [1, -999, 3, -999, 5]
    result = column_isnull(column, na_value=-999)
    assert result == [False, True, False, True, False]


def test_column_isnull_all_null():
    column = [None, None, None]
    result = column_isnull(column)
    assert result == [True, True, True]


def test_column_isnull_no_null():
    column = [1, 2, 3, 4]
    result = column_isnull(column)
    assert result == [False, False, False, False]


# Tests for column_notnull
def test_column_notnull_basic():
    column = [1, None, 3, None, 5]
    result = column_notnull(column)
    assert result == [True, False, True, False, True]


def test_column_notnull_custom_na_value():
    column = [1, -999, 3, -999, 5]
    result = column_notnull(column, na_value=-999)
    assert result == [True, False, True, False, True]


# Tests for column_isnull_inplace
def test_column_isnull_inplace_basic():
    column = [1, None, 3]
    result = column_isnull_inplace(column)
    assert result is None  # Should return None
    assert column == [False, True, False]


def test_column_isnull_inplace_custom_na_value():
    column = [1, -999, 3]
    column_isnull_inplace(column, na_value=-999)
    assert column == [False, True, False]


# Tests for column_notnull_inplace
def test_column_notnull_inplace_basic():
    column = [1, None, 3]
    result = column_notnull_inplace(column)
    assert result is None  # Should return None
    assert column == [True, False, True]


def test_column_notnull_inplace_custom_na_value():
    column = [1, -999, 3]
    column_notnull_inplace(column, na_value=-999)
    assert column == [True, False, True]


# Tests for row_isnull
def test_row_isnull_basic():
    row = {'x': 1, 'y': None, 'z': 3}
    result = row_isnull(row)
    assert result == {'x': False, 'y': True, 'z': False}


def test_row_isnull_custom_na_value():
    row = {'x': 1, 'y': -999, 'z': 3}
    result = row_isnull(row, na_value=-999)
    assert result == {'x': False, 'y': True, 'z': False}


def test_row_isnull_all_null():
    row = {'x': None, 'y': None}
    result = row_isnull(row)
    assert result == {'x': True, 'y': True}


# Tests for row_notnull
def test_row_notnull_basic():
    row = {'x': 1, 'y': None, 'z': 3}
    result = row_notnull(row)
    assert result == {'x': True, 'y': False, 'z': True}


def test_row_notnull_custom_na_value():
    row = {'x': 1, 'y': -999, 'z': 3}
    result = row_notnull(row, na_value=-999)
    assert result == {'x': True, 'y': False, 'z': True}


# Tests for row_isnull_inplace
def test_row_isnull_inplace_basic():
    row = {'x': 1, 'y': None, 'z': 3}
    result = row_isnull_inplace(row)
    assert result is None  # Should return None
    assert row == {'x': False, 'y': True, 'z': False}


def test_row_isnull_inplace_custom_na_value():
    row = {'x': 1, 'y': -999, 'z': 3}
    row_isnull_inplace(row, na_value=-999)
    assert row == {'x': False, 'y': True, 'z': False}


# Tests for row_notnull_inplace
def test_row_notnull_inplace_basic():
    row = {'x': 1, 'y': None, 'z': 3}
    result = row_notnull_inplace(row)
    assert result is None  # Should return None
    assert row == {'x': True, 'y': False, 'z': True}


def test_row_notnull_inplace_custom_na_value():
    row = {'x': 1, 'y': -999, 'z': 3}
    row_notnull_inplace(row, na_value=-999)
    assert row == {'x': True, 'y': False, 'z': True}


# Edge cases
def test_isnull_empty_data():
    data = {}
    result = isnull(data)
    assert result == {}


def test_column_isnull_empty_column():
    column = []
    result = column_isnull(column)
    assert result == []


def test_row_isnull_empty_row():
    row = {}
    result = row_isnull(row)
    assert result == {}

