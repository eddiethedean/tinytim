from tinytim.insert import insert_row, insert_row_inplace, insert_rows, insert_rows_inplace


def test_insert_row_basic():
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    row = {'x': 10, 'y': 20}
    result = insert_row(data, row)
    assert result == {'x': [1, 2, 3, 10], 'y': [4, 5, 6, 20]}
    # Original data should be unchanged
    assert data == {'x': [1, 2, 3], 'y': [4, 5, 6]}


def test_insert_row_missing_column():
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    row = {'x': 10}  # Missing 'y'
    result = insert_row(data, row)
    assert result == {'x': [1, 2, 3, 10], 'y': [4, 5, 6, None]}


def test_insert_row_extra_column_ignored():
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    row = {'x': 10, 'y': 20, 'z': 30}  # 'z' should be ignored
    result = insert_row(data, row)
    assert result == {'x': [1, 2, 3, 10], 'y': [4, 5, 6, 20]}


def test_insert_row_empty_data():
    data = {'x': [], 'y': []}
    row = {'x': 1, 'y': 2}
    result = insert_row(data, row)
    assert result == {'x': [1], 'y': [2]}


def test_insert_rows_multiple():
    data = {'x': [1, 2], 'y': [3, 4]}
    rows = [{'x': 10, 'y': 20}, {'x': 30, 'y': 40}]
    result = insert_rows(data, rows)
    assert result == {'x': [1, 2, 10, 30], 'y': [3, 4, 20, 40]}
    # Original should be unchanged
    assert data == {'x': [1, 2], 'y': [3, 4]}


def test_insert_rows_with_missing_columns():
    data = {'x': [1, 2], 'y': [3, 4]}
    rows = [{'x': 10}, {'x': 30, 'y': 40}]
    result = insert_rows(data, rows)
    assert result == {'x': [1, 2, 10, 30], 'y': [3, 4, None, 40]}


def test_insert_rows_empty_rows():
    data = {'x': [1, 2], 'y': [3, 4]}
    rows = []
    result = insert_rows(data, rows)
    assert result == {'x': [1, 2], 'y': [3, 4]}


def test_insert_row_inplace_basic():
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    row = {'x': 10, 'y': 20}
    result = insert_row_inplace(data, row)
    assert result is None  # Should return None
    assert data == {'x': [1, 2, 3, 10], 'y': [4, 5, 6, 20]}


def test_insert_row_inplace_missing_column():
    data = {'x': [1, 2], 'y': [3, 4]}
    row = {'x': 10}
    insert_row_inplace(data, row)
    assert data == {'x': [1, 2, 10], 'y': [3, 4, None]}


def test_insert_rows_inplace_basic():
    data = {'x': [1, 2], 'y': [3, 4]}
    rows = [{'x': 10, 'y': 20}, {'x': 30, 'y': 40}]
    result = insert_rows_inplace(data, rows)
    assert result is None  # Should return None
    assert data == {'x': [1, 2, 10, 30], 'y': [3, 4, 20, 40]}


def test_insert_rows_inplace_with_missing_values():
    data = {'x': [1], 'y': [2], 'z': [3]}
    rows = [{'x': 10}, {'y': 20, 'z': 30}]
    insert_rows_inplace(data, rows)
    assert data == {'x': [1, 10, None], 'y': [2, None, 20], 'z': [3, None, 30]}


def test_insert_rows_inplace_custom_missing_value():
    data = {'x': [1, 2], 'y': [3, 4]}
    rows = [{'x': 10}, {'y': 40}]
    insert_rows_inplace(data, rows, missing_value=-999)
    assert data == {'x': [1, 2, 10, -999], 'y': [3, 4, -999, 40]}


def test_insert_rows_inplace_empty_rows():
    data = {'x': [1, 2], 'y': [3, 4]}
    rows = []
    insert_rows_inplace(data, rows)
    assert data == {'x': [1, 2], 'y': [3, 4]}


def test_insert_row_single_column():
    data = {'x': [1, 2, 3]}
    row = {'x': 99}
    result = insert_row(data, row)
    assert result == {'x': [1, 2, 3, 99]}

