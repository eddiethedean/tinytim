from tinytim.group import (
    aggregate_data,
    aggregate_groups,
    count_data,
    count_groups,
    groupby,
    groupbycolumn,
    groupbymulti,
    groupbyone,
    max_data,
    max_groups,
    mean_data,
    mean_groups,
    min_data,
    min_groups,
    mode_data,
    mode_groups,
    nunique_data,
    nunique_groups,
    pstdev_data,
    pstdev_groups,
    stdev_data,
    stdev_groups,
    sum_data,
    sum_groups,
)

# Test data
DATA = {
    'Animal': ['Falcon', 'Falcon', 'Parrot', 'Parrot'],
    'Color': ['Brown', 'Brown', 'Blue', 'Red'],
    'Max Speed': [380, 370, 24, 26]
}


# Tests for groupby
def test_groupby_single_column():
    groups = groupby(DATA, 'Animal')
    assert len(groups) == 2
    assert groups[0][0] == 'Falcon'
    assert groups[0][1] == {'Animal': ['Falcon', 'Falcon'],
                             'Color': ['Brown', 'Brown'],
                             'Max Speed': [380, 370]}
    assert groups[1][0] == 'Parrot'


def test_groupby_multiple_columns():
    groups = groupby(DATA, ['Animal', 'Color'])
    assert len(groups) == 3
    assert groups[0][0] == ('Falcon', 'Brown')
    assert groups[1][0] == ('Parrot', 'Blue')
    assert groups[2][0] == ('Parrot', 'Red')


# Tests for groupbyone
def test_groupbyone():
    groups = groupbyone(DATA, 'Animal')
    assert len(groups) == 2
    assert groups[0][0] == 'Falcon'
    assert groups[1][0] == 'Parrot'


# Tests for groupbymulti
def test_groupbymulti():
    groups = groupbymulti(DATA, ['Animal', 'Color'])
    assert len(groups) == 3


def test_groupbycolumn():
    column = ['A', 'B', 'A', 'B', 'C']
    data = {'key': ['A', 'B', 'A', 'B', 'C'], 'value': [1, 2, 3, 4, 5]}
    groups = groupbycolumn(data, column)
    assert len(groups) == 3
    assert groups[0][0] == 'A'
    assert groups[1][0] == 'B'
    assert groups[2][0] == 'C'


# Tests for sum_groups
def test_sum_groups():
    groups = groupby(DATA, 'Animal')
    labels, result = sum_groups(groups)
    assert labels == ['Falcon', 'Parrot']
    assert result == {'Max Speed': [750, 50]}


# Tests for count_groups
def test_count_groups():
    groups = groupby(DATA, 'Animal')
    labels, result = count_groups(groups)
    assert labels == ['Falcon', 'Parrot']
    assert result == {'Animal': [2, 2], 'Color': [2, 2], 'Max Speed': [2, 2]}


# Tests for mean_groups
def test_mean_groups():
    groups = groupby(DATA, 'Animal')
    labels, result = mean_groups(groups)
    assert labels == ['Falcon', 'Parrot']
    assert result == {'Max Speed': [375.0, 25.0]}


# Tests for min_groups
def test_min_groups():
    groups = groupby(DATA, 'Animal')
    labels, result = min_groups(groups)
    assert labels == ['Falcon', 'Parrot']
    assert result['Max Speed'] == [370, 24]
    assert 'Animal' in result  # String columns also included
    assert 'Color' in result


# Tests for max_groups
def test_max_groups():
    groups = groupby(DATA, 'Animal')
    labels, result = max_groups(groups)
    assert labels == ['Falcon', 'Parrot']
    assert result['Max Speed'] == [380, 26]
    assert 'Animal' in result  # String columns also included
    assert 'Color' in result


# Tests for mode_groups
def test_mode_groups():
    data = {'group': ['A', 'A', 'A', 'B', 'B', 'B'],
            'value': [1, 1, 2, 3, 3, 4]}
    groups = groupby(data, 'group')
    labels, result = mode_groups(groups)
    assert labels == ['A', 'B']
    assert result['value'] == [1, 3]
    assert 'group' in result  # Group column also included


# Tests for stdev_groups
def test_stdev_groups():
    data = {'group': ['A', 'A', 'A', 'B', 'B', 'B'],
            'value': [1, 2, 3, 4, 5, 6]}
    groups = groupby(data, 'group')
    labels, result = stdev_groups(groups)
    assert labels == ['A', 'B']
    # Standard deviation of [1,2,3] is 1.0, [4,5,6] is 1.0
    assert len(result['value']) == 2
    assert abs(result['value'][0] - 1.0) < 0.01
    assert abs(result['value'][1] - 1.0) < 0.01


# Tests for pstdev_groups
def test_pstdev_groups():
    data = {'group': ['A', 'A', 'A', 'B', 'B', 'B'],
            'value': [1, 2, 3, 4, 5, 6]}
    groups = groupby(data, 'group')
    labels, result = pstdev_groups(groups)
    assert labels == ['A', 'B']
    assert len(result['value']) == 2


# Tests for nunique_groups
def test_nunique_groups():
    data = {'group': ['A', 'A', 'A', 'B', 'B', 'B'],
            'value': [1, 1, 2, 3, 3, 3]}
    groups = groupby(data, 'group')
    labels, result = nunique_groups(groups)
    assert labels == ['A', 'B']
    assert result['value'] == [2, 1]
    assert 'group' in result  # Group column also included


# Tests for aggregate_data functions
def test_sum_data():
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    result = sum_data(data)
    assert result == {'x': 6, 'y': 15}


def test_sum_data_with_non_numeric():
    data = {'x': [1, 2, 3], 'name': ['a', 'b', 'c']}
    result = sum_data(data)
    assert result == {'x': 6}  # Only numeric column


def test_count_data():
    data = {'x': [1, 2, 3], 'y': [4, 5, 6], 'z': ['a', 'b', 'c']}
    result = count_data(data)
    assert result == {'x': 3, 'y': 3, 'z': 3}


def test_mean_data():
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    result = mean_data(data)
    assert result == {'x': 2.0, 'y': 5.0}


def test_min_data():
    data = {'x': [3, 1, 2], 'y': [6, 4, 5]}
    result = min_data(data)
    assert result == {'x': 1, 'y': 4}


def test_max_data():
    data = {'x': [1, 3, 2], 'y': [4, 6, 5]}
    result = max_data(data)
    assert result == {'x': 3, 'y': 6}


def test_mode_data():
    data = {'x': [1, 1, 2], 'y': [3, 3, 4]}
    result = mode_data(data)
    assert result == {'x': 1, 'y': 3}


def test_stdev_data():
    data = {'x': [1, 2, 3]}
    result = stdev_data(data)
    assert 'x' in result
    assert abs(result['x'] - 1.0) < 0.01


def test_pstdev_data():
    data = {'x': [1, 2, 3]}
    result = pstdev_data(data)
    assert 'x' in result
    # Population stdev is different from sample stdev


def test_nunique_data():
    data = {'x': [1, 1, 2, 3], 'y': [1, 1, 1, 1]}
    result = nunique_data(data)
    assert result == {'x': 3, 'y': 1}


# Tests for aggregate_groups
def test_aggregate_groups():
    groups = groupby(DATA, 'Animal')
    labels, result = aggregate_groups(groups, sum_data)
    assert labels == ['Falcon', 'Parrot']
    assert 'Max Speed' in result


# Tests for aggregate_data
def test_aggregate_data():
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    result = aggregate_data(data, sum)
    assert result == {'x': 6, 'y': 15}


# Edge cases
def test_groupby_single_value_per_group():
    data = {'group': ['A', 'B', 'C'], 'value': [1, 2, 3]}
    groups = groupby(data, 'group')
    assert len(groups) == 3


def test_groupby_all_same_group():
    data = {'group': ['A', 'A', 'A'], 'value': [1, 2, 3]}
    groups = groupby(data, 'group')
    assert len(groups) == 1
    assert groups[0][0] == 'A'


def test_sum_data_empty():
    data = {'x': []}
    result = sum_data(data)
    assert result == {'x': 0}  # Empty list sums to 0


def test_count_data_single_row():
    data = {'x': [1], 'y': [2]}
    result = count_data(data)
    assert result == {'x': 1, 'y': 1}


def test_aggregate_groups_empty_result():
    # Group with data that produces empty aggregation
    groups = [('A', {'x': [], 'y': []})]
    labels, result = aggregate_groups(groups, sum_data)
    # Even empty data produces a result (sums to 0), so not filtered
    assert len(labels) == 1

