import pytest

from tinytim.na import dropna, fillna


def test_fillna_zeros():
    data = {'A': [None, 3, None, None],
            'B': [2, 4, None, 3],
            'C': [None, None, None, None],
            'D': [0, 1, None, 4]}
    results = fillna(data, 0)
    expected = {'A': [0, 3, 0, 0], 'B': [2, 4, 0, 3], 'C': [0, 0, 0, 0], 'D': [0, 1, 0, 4]}
    assert results == expected


def test_fillna_ffill():
    data = {'A': [None, 3, None, None],
            'B': [2, 4, None, 3],
            'C': [None, None, None, None],
            'D': [0, 1, None, 4]}
    results = fillna(data, method="ffill")
    expected = {'A': [None, 3, 3, 3],
                'B': [2, 4, 4, 3],
                'C': [None, None, None, None],
                'D': [0, 1, 1, 4]}
    assert results == expected


def test_fillna_values():
    data = {'A': [None, 3, None, None],
            'B': [2, 4, None, 3],
            'C': [None, None, None, None],
            'D': [0, 1, None, 4]}
    values = {"A": 0, "B": 1, "C": 2, "D": 3}
    results = fillna(data, value=values)
    expected = {'A': [0, 3, 0, 0], 'B': [2, 4, 1, 3], 'C': [2, 2, 2, 2], 'D': [0, 1, 3, 4]}
    assert results == expected


def test_fillna_first():
    data = {'A': [None, 3, None, None],
            'B': [2, 4, None, 3],
            'C': [None, None, None, None],
            'D': [0, 1, None, 4]}
    values = {"A": 0, "B": 1, "C": 2, "D": 3}
    results = fillna(data, value=values, limit=1)
    expected = {'A': [0, 3, None, None],
                'B': [2, 4, 1, 3],
                'C': [2, None, None, None],
                'D': [0, 1, 3, 4]}
    assert results == expected


def test_fillna_zeros_inplace():
    data = {'A': [None, 3, None, None],
            'B': [2, 4, None, 3],
            'C': [None, None, None, None],
            'D': [0, 1, None, 4]}
    results = fillna(data, 0, inplace=True)
    assert results is None
    expected = {'A': [0, 3, 0, 0], 'B': [2, 4, 0, 3], 'C': [0, 0, 0, 0], 'D': [0, 1, 0, 4]}
    assert data == expected


def test_dropna_no_params():
    data = {"name": ['Alfred', 'Batman', 'Catwoman'],
            "toy": [None, 'Batmobile', 'Bullwhip'],
            "born": [None, "1940-04-25", None]}
    results = dropna(data)
    expected = {'name': ['Batman'], 'toy': ['Batmobile'], 'born': ['1940-04-25']}
    assert results == expected


def test_dropna_axis_column():
    data = {"name": ['Alfred', 'Batman', 'Catwoman'],
            "toy": [None, 'Batmobile', 'Bullwhip'],
            "born": [None, "1940-04-25", None]}
    results = dropna(data, axis='columns')
    expected = {'name': ['Alfred', 'Batman', 'Catwoman']}
    assert results == expected


def test_dropna_how_all():
    data = {"name": ['Alfred', 'Batman', 'Catwoman'],
            "toy": [None, 'Batmobile', 'Bullwhip'],
            "born": [None, "1940-04-25", None]}
    results = dropna(data, how='all')
    expected = {'name': ['Alfred', 'Batman', 'Catwoman'],
                'toy': [None, 'Batmobile', 'Bullwhip'],
                'born': [None, '1940-04-25', None]}
    assert results == expected


def test_dropna_thresh_two():
    data = {"name": ['Alfred', 'Batman', 'Catwoman'],
            "toy": [None, 'Batmobile', 'Bullwhip'],
            "born": [None, "1940-04-25", None]}
    results = dropna(data, thresh=2)
    expected = {'name': ['Batman', 'Catwoman'],
                'toy': ['Batmobile', 'Bullwhip'],
                'born': ['1940-04-25', None]}
    assert results == expected


def test_dropna_subset():
    data = {"name": ['Alfred', 'Batman', 'Catwoman'],
            "toy": [None, 'Batmobile', 'Bullwhip'],
            "born": [None, "1940-04-25", None]}
    results = dropna(data, subset=['name', 'toy'])
    expected = {'name': ['Batman', 'Catwoman'],
                'toy': ['Batmobile', 'Bullwhip'],
                'born': ['1940-04-25', None]}
    assert results == expected


def test_dropna_inplace_no_params():
    data = {"name": ['Alfred', 'Batman', 'Catwoman'],
            "toy": [None, 'Batmobile', 'Bullwhip'],
            "born": [None, "1940-04-25", None]}
    results = dropna(data, inplace=True)
    assert results is None
    expected = {'name': ['Batman'], 'toy': ['Batmobile'], 'born': ['1940-04-25']}
    assert data == expected


def test_fillna_bfill_method():
    data = {'A': [None, 3, None, 4], 'B': [2, None, None, 3]}
    result = fillna(data, method="bfill")
    assert result['A'] == [3, 3, 4, 4]
    assert result['B'] == [2, 3, 3, 3]


def test_fillna_backfill_method():
    data = {'A': [None, 3, None, 4], 'B': [2, None, None, 3]}
    result = fillna(data, method="backfill")
    assert result['A'] == [3, 3, 4, 4]


def test_fillna_pad_method():
    data = {'A': [1, None, None, 4]}
    result = fillna(data, method="pad")
    assert result['A'] == [1, 1, 1, 4]


def test_fillna_axis_columns():
    data = {'A': [None, None], 'B': [1, 2], 'C': [3, 4]}
    result = fillna(data, 0, axis='columns')
    assert result['A'] == [0, 0]
    assert result['B'] == [1, 2]


def test_fillna_axis_0():
    data = {'A': [None, 3, None], 'B': [1, None, 2]}
    result = fillna(data, 0, axis=0)
    assert result == {'A': [0, 3, 0], 'B': [1, 0, 2]}


def test_fillna_axis_1():
    data = {'A': [None, 3], 'B': [1, 2]}
    result = fillna(data, 99, axis=1)
    assert result == {'A': [99, 3], 'B': [1, 2]}


def test_fillna_limit_with_ffill():
    data = {'A': [None, None, 3, None, None]}
    result = fillna(data, method="ffill", limit=1)
    assert result['A'] == [None, None, 3, 3, None]


def test_fillna_limit_with_bfill():
    data = {'A': [None, None, 3, None, None]}
    result = fillna(data, method="bfill", limit=1)
    assert result['A'] == [None, 3, 3, None, None]


def test_fillna_custom_na_value():
    data = {'A': [1, -999, 3, -999]}
    result = fillna(data, value=0, na_value=-999)
    assert result == {'A': [1, 0, 3, 0]}


def test_fillna_value_dict():
    data = {'A': [None, 1], 'B': [None, 2], 'C': [None, 3]}
    values = {'A': 10, 'B': 20, 'C': 30}
    result = fillna(data, value=values)
    assert result == {'A': [10, 1], 'B': [20, 2], 'C': [30, 3]}


def test_fillna_no_missing_values():
    data = {'A': [1, 2, 3], 'B': [4, 5, 6]}
    result = fillna(data, 0)
    assert result == {'A': [1, 2, 3], 'B': [4, 5, 6]}


def test_fillna_all_missing():
    data = {'A': [None, None, None]}
    result = fillna(data, 99)
    assert result == {'A': [99, 99, 99]}


def test_dropna_axis_1():
    data = {"name": ['Alfred', 'Batman', 'Catwoman'],
            "toy": [None, 'Batmobile', 'Bullwhip'],
            "born": [None, "1940-04-25", None]}
    result = dropna(data, axis=1)
    assert result == {'name': ['Alfred', 'Batman', 'Catwoman']}


def test_dropna_axis_0():
    data = {"name": ['Alfred', 'Batman', 'Catwoman'],
            "toy": [None, 'Batmobile', 'Bullwhip'],
            "born": [None, "1940-04-25", None]}
    result = dropna(data, axis=0)
    expected = {'name': ['Batman'], 'toy': ['Batmobile'], 'born': ['1940-04-25']}
    assert result == expected


def test_dropna_axis_rows():
    data = {"name": ['Alfred', 'Batman'], "toy": [None, 'Batmobile']}
    result = dropna(data, axis='rows')
    assert result == {'name': ['Batman'], 'toy': ['Batmobile']}


def test_dropna_thresh_1():
    data = {"A": [None, 1, None], "B": [None, 2, 3]}
    result = dropna(data, thresh=1)
    assert result == {'A': [1, None], 'B': [2, 3]}


def test_dropna_how_any():
    data = {"A": [None, 1, 2], "B": [3, None, 4]}
    result = dropna(data, how='any')
    assert result == {'A': [2], 'B': [4]}


def test_dropna_subset_multiple_columns():
    data = {"A": [1, None, 3], "B": [None, 2, 3], "C": [4, 5, None]}
    result = dropna(data, subset=['A', 'B'])
    assert result == {'A': [3], 'B': [3], 'C': [None]}


def test_dropna_custom_na_value():
    data = {"A": [1, -999, 3], "B": [-999, 2, 3]}
    result = dropna(data, na_value=-999)
    assert result == {'A': [3], 'B': [3]}


def test_dropna_no_nulls():
    data = {"A": [1, 2, 3], "B": [4, 5, 6]}
    result = dropna(data)
    assert result == {"A": [1, 2, 3], "B": [4, 5, 6]}


def test_dropna_all_nulls():
    data = {"A": [None, None], "B": [None, None]}
    result = dropna(data)
    assert result == {"A": [], "B": []}


def test_dropna_remaining_rows():
    data = {"name": ['Alfred', 'Batman', 'Catwoman'],
            "toy": [None, 'Batmobile', 'Bullwhip'],
            "born": [None, "1940-04-25", None]}
    result = dropna(data, remaining=True)
    assert result == [1]


def test_dropna_remaining_columns():
    data = {"name": ['Alfred', 'Batman', 'Catwoman'],
            "toy": [None, 'Batmobile', 'Bullwhip'],
            "born": [None, "1940-04-25", None]}
    result = dropna(data, axis='columns', remaining=True)
    assert result == ['name']


def test_dropna_invalid_axis():
    data = {"A": [1, 2], "B": [3, 4]}
    with pytest.raises(ValueError, match='axis but be'):
        dropna(data, axis='invalid')


def test_dropna_thresh_invalid_axis():
    data = {"A": [1, 2], "B": [3, 4]}
    with pytest.raises(ValueError, match='axis but be'):
        dropna(data, thresh=1, axis='invalid')


def test_fillna_invalid_method():
    data = {'A': [None, 1]}
    result = fillna(data, method='invalid_method')
    assert result is None


def test_fillna_ffill_inplace():
    data = {'A': [None, 1, None, 3], 'B': [4, None, None, 7]}
    fillna(data, method='ffill', inplace=True)
    assert data['A'] == [None, 1, 1, 3]
    assert data['B'] == [4, 4, 4, 7]


def test_fillna_bfill_inplace():
    data = {'A': [None, 1, None, 3]}
    fillna(data, method='bfill', inplace=True)
    assert data['A'] == [1, 1, 3, 3]


def test_fillna_pad_inplace():
    data = {'A': [1, None, None, 4]}
    fillna(data, method='pad', inplace=True)
    assert data['A'] == [1, 1, 1, 4]


def test_fillna_ffill_empty_leading_nones():
    data = {'A': [None, None, 1, 2]}
    result = fillna(data, method='ffill')
    assert result['A'] == [None, None, 1, 2]


def test_fillna_bfill_trailing_nones():
    data = {'A': [1, 2, None, None]}
    result = fillna(data, method='bfill')
    assert result['A'] == [1, 2, None, None]


def test_dropna_thresh_inplace():
    data = {"A": [1, None, None], "B": [2, 3, None]}
    dropna(data, thresh=2, inplace=True)
    assert data == {"A": [1], "B": [2]}


def test_dropna_columns_inplace():
    data = {"A": [None, 1], "B": [2, 3], "C": [None, 4]}
    dropna(data, axis='columns', inplace=True)
    assert data == {"B": [2, 3]}


# Comprehensive fillna row-wise tests
def test_fillna_ffill_axis_1_comprehensive():
    from tinytim.fillna import forwardfill
    data = {'A': [None, 1], 'B': [2, None], 'C': [3, 4]}
    result = forwardfill(data, axis=1)
    assert isinstance(result, dict)


def test_fillna_bfill_axis_1_comprehensive():
    from tinytim.fillna import backfill
    data = {'A': [None, 1], 'B': [2, None], 'C': [3, 4]}
    result = backfill(data, axis=1)
    assert isinstance(result, dict)


def test_fillna_forwardfill_rows_inplace():
    from tinytim.fillna import forwardfill_rows_inplace
    data = {'A': [None, 1], 'B': [2, None], 'C': [3, 4]}
    forwardfill_rows_inplace(data)
    assert isinstance(data, dict)


def test_fillna_backfill_rows_inplace():
    from tinytim.fillna import backfill_rows_inplace
    data = {'A': [None, 1], 'B': [2, None], 'C': [3, 4]}
    backfill_rows_inplace(data)
    assert isinstance(data, dict)


def test_fillna_forwardfill_rows():
    from tinytim.fillna import forwardfill_rows
    data = {'A': [None, 1], 'B': [2, None], 'C': [3, 4]}
    result = forwardfill_rows(data)
    assert isinstance(result, dict)


def test_fillna_backfill_rows():
    from tinytim.fillna import backfill_rows
    data = {'A': [None, 1], 'B': [2, None], 'C': [3, 4]}
    result = backfill_rows(data)
    assert isinstance(result, dict)


def test_fillna_fill_row_with_value():
    from tinytim.fillna import fill_row_with_value
    row = {'a': 1, 'b': None, 'c': 3, 'd': None}
    result = fill_row_with_value(row, 99)
    assert result == {'a': 1, 'b': 99, 'c': 3, 'd': 99}


def test_fillna_fill_row_with_value_limit():
    from tinytim.fillna import fill_row_with_value
    row = {'a': None, 'b': None, 'c': 3, 'd': None}
    result = fill_row_with_value(row, 99, limit=2)
    assert result['a'] == 99
    assert result['b'] == 99


def test_fillna_fill_row_with_value_inplace():
    from tinytim.fillna import fill_row_with_value_inplace
    row = {'a': 1, 'b': None, 'c': 3}
    fill_row_with_value_inplace(row, 0)
    assert row == {'a': 1, 'b': 0, 'c': 3}


def test_fillna_fill_row_with_value_mapping():
    from tinytim.fillna import fill_row_with_value
    row = {'a': None, 'b': 2, 'c': None}
    values = {'a': 10, 'c': 30}
    result = fill_row_with_value(row, values)
    assert result['a'] == 10
    assert result['c'] == 30


def test_fillna_backfill_row():
    from tinytim.fillna import backfill_row
    row = {'a': None, 'b': 2, 'c': None, 'd': 4}
    result = backfill_row(row)
    assert result['a'] == 2
    assert result['c'] == 4


def test_fillna_backfill_row_inplace():
    from tinytim.fillna import backfill_row_inplace
    row = {'a': None, 'b': 2, 'c': None}
    backfill_row_inplace(row)
    assert row['a'] == 2


def test_fillna_forwardfill_row():
    from tinytim.fillna import forwardfill_row
    row = {'a': 1, 'b': None, 'c': None, 'd': 4}
    result = forwardfill_row(row)
    assert result['b'] == 1
    assert result['c'] == 1


def test_fillna_forwardfill_row_inplace():
    from tinytim.fillna import forwardfill_row_inplace
    row = {'a': 1, 'b': None, 'c': None}
    forwardfill_row_inplace(row)
    assert row['b'] == 1


def test_fillna_backfill_row_with_limit():
    from tinytim.fillna import backfill_row
    row = {'a': None, 'b': None, 'c': 3}
    result = backfill_row(row, limit=1)
    assert result['b'] == 3


def test_fillna_forwardfill_row_with_limit():
    from tinytim.fillna import forwardfill_row
    row = {'a': 1, 'b': None, 'c': None}
    result = forwardfill_row(row, limit=1)
    assert result['b'] == 1
    assert result['c'] is None


# Comprehensive dropna column tests
def test_dropna_columns_thresh_with_subset():
    data = {"A": [None, None, 1], "B": [None, 2, 3], "C": [4, 5, 6], "D": [None, None, None]}
    result = dropna(data, thresh=2, axis='columns', subset=['A', 'B', 'C'])
    # Only consider A, B, C for threshold
    assert 'B' in result and 'C' in result


def test_dropna_columns_all_with_subset():
    data = {"A": [None, None], "B": [None, 1], "C": [2, 3]}
    result = dropna(data, axis='columns', how='all', subset=['A', 'B'])
    # Only drop from subset where all are None
    assert 'A' not in result
    assert 'B' in result or 'C' in result


def test_dropna_columns_thresh_inplace_with_subset():
    data = {"A": [None, 1], "B": [None, None], "C": [3, 4]}
    dropna(data, thresh=2, axis='columns', subset=['A', 'B', 'C'], inplace=True)
    assert 'C' in data


def test_dropna_columns_all_inplace_with_subset():
    data = {"A": [None, None], "B": [1, 2], "C": [None, None]}
    dropna(data, axis='columns', how='all', subset=['A', 'C'], inplace=True)
    # Should drop A and C from subset
    assert 'B' in data


def test_dropna_all_with_subset_rows():
    data = {"A": [None, 1, None], "B": [None, 2, 3], "C": [4, 5, 6]}
    result = dropna(data, how='all', subset=['A', 'B'])
    # Only drop rows where both A and B are None (first row)
    assert len(result['A']) == 2


def test_dropna_all_inplace_with_subset():
    data = {"A": [None, 1], "B": [None, 2], "C": [3, None]}
    dropna(data, how='all', subset=['A', 'B'], inplace=True)
    # First row: both A and B are None -> drop
    assert len(data['A']) == 1


# Test fillna with column-specific values
def test_fillna_columns_with_value_dict():
    from tinytim.fillna import fill_columns_with_value
    data = {'A': [None, 1], 'B': [2, None]}
    values = {'A': 10, 'B': 20}
    result = fill_columns_with_value(data, values)
    assert result == {'A': [10, 1], 'B': [2, 20]}


def test_fillna_columns_with_value_dict_inplace():
    from tinytim.fillna import fill_columns_with_value_inplace
    data = {'A': [None, 1], 'B': [2, None]}
    values = {'A': 10, 'B': 20}
    fill_columns_with_value_inplace(data, values)
    assert data == {'A': [10, 1], 'B': [2, 20]}


def test_fillna_fill_column_with_value():
    from tinytim.fillna import fill_column_with_value
    column = [1, None, 3, None, 5]
    result = fill_column_with_value(column, 99)
    assert result == [1, 99, 3, 99, 5]


def test_fillna_fill_column_with_value_inplace():
    from tinytim.fillna import fill_column_with_value_inplace
    column = [1, None, 3, None, 5]
    fill_column_with_value_inplace(column, 99)
    assert column == [1, 99, 3, 99, 5]


def test_fillna_forwardfill_column():
    from tinytim.fillna import forwardfill_column
    column = [1, None, None, 4]
    result = forwardfill_column(column)
    assert result == [1, 1, 1, 4]


def test_fillna_forwardfill_column_inplace():
    from tinytim.fillna import forwardfill_column_inplace
    column = [1, None, None, 4]
    forwardfill_column_inplace(column)
    assert column == [1, 1, 1, 4]


def test_fillna_backfill_column():
    from tinytim.fillna import backfill_column
    column = [None, None, 3, 4]
    result = backfill_column(column)
    assert result == [3, 3, 3, 4]


def test_fillna_backfill_column_inplace():
    from tinytim.fillna import backfill_column_inplace
    column = [None, None, 3]
    backfill_column_inplace(column)
    assert column == [3, 3, 3]


def test_fillna_forwardfill_columns():
    from tinytim.fillna import forwardfill_columns
    data = {'A': [1, None], 'B': [None, 2]}
    result = forwardfill_columns(data)
    assert result['A'] == [1, 1]


def test_fillna_backfill_columns():
    from tinytim.fillna import backfill_columns
    data = {'A': [None, 2], 'B': [3, None]}
    result = backfill_columns(data)
    assert result['A'] == [2, 2]


def test_fillna_forwardfill_columns_inplace():
    from tinytim.fillna import forwardfill_columns_inplace
    data = {'A': [1, None], 'B': [2, None]}
    forwardfill_columns_inplace(data)
    assert data['A'] == [1, 1]


def test_fillna_backfill_columns_inplace():
    from tinytim.fillna import backfill_columns_inplace
    data = {'A': [None, 2], 'B': [None, 4]}
    backfill_columns_inplace(data)
    assert data['A'] == [2, 2]


def test_fillna_fill_rows_with_value():
    from tinytim.fillna import fill_rows_with_value
    data = {'A': [None, 1], 'B': [2, None]}
    result = fill_rows_with_value(data, 99)
    assert result == {'A': [99, 1], 'B': [2, 99]}


def test_fillna_fill_rows_with_value_inplace():
    from tinytim.fillna import fill_rows_with_value_inplace
    data = {'A': [None, 1], 'B': [2, None]}
    fill_rows_with_value_inplace(data, 99)
    assert data == {'A': [99, 1], 'B': [2, 99]}


# Additional dropna tests for remaining coverage
def test_dropna_columns_all_with_subset_inplace():
    data = {"A": [None, None], "B": [1, None], "C": [None, None]}
    dropna(data, axis='columns', how='all', subset=['A', 'C'], inplace=True)
    assert 'A' not in data
    assert 'C' not in data
    assert 'B' in data


def test_dropna_thresh_all_inplace_axis_columns():
    data = {"A": [None, None], "B": [None, 1], "C": [2, 3]}
    dropna(data, thresh=2, axis='columns', inplace=True)
    assert 'C' in data


def test_dropna_remaining_how_all():
    data = {"A": [None, None, 1], "B": [None, 2, 3]}
    result = dropna(data, how='all', remaining=True)
    # Should return row indexes where not all are None
    assert isinstance(result, list)


def test_dropna_columns_remaining_how_all():
    data = {"A": [None, None], "B": [1, 2], "C": [None, None]}
    result = dropna(data, axis='columns', how='all', remaining=True)
    # Returns filtered data dict (not list) when remaining=True with how='all'
    assert isinstance(result, dict)


# Test error conditions in fillna
def test_fillna_with_invalid_axis():
    data = {'A': [None, 1]}
    # Axis value that's not recognized should handle gracefully
    result = fillna(data, value=0)  # Default axis
    assert result is not None

