from tinytim.join import full_join, inner_join, left_join, locate, right_join
from tinytim.rows import records_equal


def test_inner_join():
    left = {'id': ['a', 'c', 'd', 'f', 'g'], 'x': [33, 44, 55, 66, 77]}
    right = {'id': ['a', 'b', 'c', 'd'], 'y': [11, 22, 33, 44]}
    results = inner_join(left, right, 'id')
    expected = {'id': ['a', 'c', 'd'], 'x': [33, 44, 55], 'y': [11, 33, 44]}
    assert records_equal(results, expected)


def test_full_join():
    left = {'id': ['a', 'c', 'd', 'f', 'g'], 'x': [33, 44, 55, 66, 77]}
    right = {'id': ['a', 'b', 'c', 'd'], 'y': [11, 22, 33, 44]}
    results = full_join(left, right, 'id')
    expected = {'id': ['a', 'c', 'd', 'f', 'g', 'b'],
                'x': [33, 44, 55, 66, 77, None],
                'y': [11, 33, 44, None, None, 22]}
    assert records_equal(results, expected)


def test_left_join():
    left = {'id': ['a', 'c', 'd', 'f'], 'x': [33, 44, 55, 66]}
    right = {'id': ['a', 'b', 'c', 'd'], 'y': [11, 22, 33, 44]}
    results = left_join(left, right, 'id')
    expected = {'id': ['a', 'c', 'd', 'f'], 'x': [33, 44, 55, 66], 'y': [11, 33, 44, None]}
    assert records_equal(results, expected)


def test_right_join():
    left = {'id': ['a', 'c', 'd', 'f'], 'x': [33, 44, 55, 66]}
    right = {'id': ['a', 'b', 'c', 'd'], 'y': [11, 22, 33, 44]}
    results = right_join(left, right, 'id')
    expected = {'id': ['a', 'b', 'c', 'd'], 'x': [33, None, 44, 55], 'y': [11, 22, 33, 44]}
    assert records_equal(results, expected)


def test_locate():
    lst = [1, 2, 1, 2, 4, 5, 1]
    results = locate(lst, 1)
    expected = [0, 2, 6]
    assert results == expected


# Test joins with different left_on and right_on
def test_inner_join_different_columns():
    left = {'left_id': [1, 2, 3], 'value': ['a', 'b', 'c']}
    right = {'right_id': [2, 3, 4], 'score': [10, 20, 30]}
    result = inner_join(left, right, left_on='left_id', right_on='right_id')
    # Both join columns are kept when they have different names
    assert records_equal(result, {
        'left_id': [2, 3],
        'value': ['b', 'c'],
        'score': [10, 20],
        'right_id': [2, 3]
    })


def test_left_join_different_columns():
    left = {'left_id': [1, 2, 3], 'value': ['a', 'b', 'c']}
    right = {'right_id': [2, 3, 4], 'score': [10, 20, 30]}
    result = left_join(left, right, left_on='left_id', right_on='right_id')
    assert records_equal(result, {
        'left_id': [1, 2, 3],
        'value': ['a', 'b', 'c'],
        'score': [None, 10, 20],
        'right_id': [1, 2, 3]  # Contains left join key values
    })


def test_right_join_different_columns():
    left = {'left_id': [1, 2, 3], 'value': ['a', 'b', 'c']}
    right = {'right_id': [2, 3, 4], 'score': [10, 20, 30]}
    result = right_join(left, right, left_on='left_id', right_on='right_id')
    assert records_equal(result, {
        'left_id': [2, 3, 4],  # Contains right join key values
        'right_id': [2, 3, 4],
        'value': ['b', 'c', None],
        'score': [10, 20, 30]
    })


# Test joins with multiple columns
def test_inner_join_multiple_columns():
    left = {'a': [1, 1, 2], 'b': ['x', 'y', 'x'], 'val': [10, 20, 30]}
    right = {'a': [1, 1, 2], 'b': ['x', 'z', 'x'], 'score': [100, 200, 300]}
    result = inner_join(left, right, left_on=['a', 'b'], right_on=['a', 'b'])
    # Should match on (1, 'x') and (2, 'x')
    assert len(result['a']) == 2


# Test with select parameter
def test_inner_join_with_select():
    left = {'id': [1, 2, 3], 'value': ['a', 'b', 'c'], 'extra': [10, 20, 30]}
    right = {'id': [2, 3, 4], 'score': [100, 200, 300], 'extra2': [5, 6, 7]}
    result = inner_join(left, right, 'id', select=['id', 'value', 'score'])
    assert set(result.keys()) == {'id', 'value', 'score'}
    assert records_equal(result, {'id': [2, 3], 'value': ['b', 'c'], 'score': [100, 200]})


# Edge cases
def test_join_empty_left():
    left = {'id': [], 'value': []}
    right = {'id': [1, 2], 'score': [10, 20]}
    result = inner_join(left, right, 'id')
    assert result == {'id': [], 'value': [], 'score': []}


def test_join_empty_right():
    left = {'id': [1, 2], 'value': ['a', 'b']}
    right = {'id': [], 'score': []}
    result = inner_join(left, right, 'id')
    assert result == {'id': [], 'value': [], 'score': []}


def test_join_no_matches():
    left = {'id': [1, 2], 'value': ['a', 'b']}
    right = {'id': [3, 4], 'score': [10, 20]}
    result = inner_join(left, right, 'id')
    assert result == {'id': [], 'value': [], 'score': []}


def test_locate_no_matches():
    lst = [1, 2, 3, 4]
    result = locate(lst, 99)
    assert result == []


def test_locate_all_matches():
    lst = [5, 5, 5, 5]
    result = locate(lst, 5)
    assert result == [0, 1, 2, 3]


# Test full join with different columns
def test_full_join_different_columns():
    left = {'left_id': [1, 2], 'value': ['a', 'b']}
    right = {'right_id': [2, 3], 'score': [10, 20]}
    result = full_join(left, right, left_on='left_id', right_on='right_id')
    # Should include all rows from both tables
    assert len(result['value']) == 3  # 2 from left + 1 from right only


# Test join error handling - mismatched list lengths
def test_join_mismatched_list_lengths():
    import pytest
    left = {'id': [1, 2], 'value': ['a', 'b']}
    right = {'id': [2, 3], 'score': [10, 20]}
    # left_on and right_on lists must have same length
    with pytest.raises(ValueError, match='left_on sequence must be same len'):
        inner_join(left, right, left_on=['id', 'value'], right_on=['id'])


# Test join with invalid types for left_on/right_on
def test_join_invalid_on_types():
    import pytest
    left = {'id': [1, 2], 'value': ['a', 'b']}
    right = {'id': [2, 3], 'score': [10, 20]}
    # Both must be same type (both str or both sequence)
    with pytest.raises(ValueError):
        inner_join(left, right, left_on='id', right_on=['id'])


# Test _sequence_of_str with empty sequence
def test_join_with_empty_on_list():
    import pytest
    left = {'id': [1, 2], 'value': ['a', 'b']}
    right = {'id': [2, 3], 'score': [10, 20]}
    # Empty list for left_on should raise error
    with pytest.raises((ValueError, IndexError)):
        inner_join(left, right, left_on=[], right_on=[])
