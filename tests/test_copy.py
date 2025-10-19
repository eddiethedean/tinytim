from tinytim.copy import copy_sequence, copy_table, deepcopy_sequence, deepcopy_table


# Tests for copy_table
def test_copy_table_basic():
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    result = copy_table(data)
    assert result == {'x': [1, 2, 3], 'y': [4, 5, 6]}
    # Verify it's a deep copy
    result['x'][0] = 99
    assert data['x'][0] == 1  # Original unchanged


def test_copy_table_nested_lists():
    data = {'x': [[1, 2], [3, 4]], 'y': [[5, 6], [7, 8]]}
    result = copy_table(data)
    assert result == data
    # Verify deep copy of nested structures
    result['x'][0][0] = 99
    assert data['x'][0][0] == 1  # Original unchanged


def test_copy_table_empty():
    data = {}
    result = copy_table(data)
    assert result == {}


# Tests for deepcopy_table
def test_deepcopy_table_basic():
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    result = deepcopy_table(data)
    assert result == {'x': [1, 2, 3], 'y': [4, 5, 6]}
    # Verify it's a deep copy
    result['x'][0] = 99
    assert data['x'][0] == 1  # Original unchanged


def test_deepcopy_table_nested_lists():
    data = {'x': [[1, 2], [3, 4]], 'y': [[5, 6], [7, 8]]}
    result = deepcopy_table(data)
    assert result == data
    # Verify deep copy of nested structures
    result['x'][0][0] = 99
    assert data['x'][0][0] == 1  # Original unchanged


def test_deepcopy_table_preserves_type():
    # Test that deepcopy_table preserves the mapping type
    from collections import OrderedDict
    data = OrderedDict([('x', [1, 2, 3]), ('y', [4, 5, 6])])
    result = deepcopy_table(data)
    assert isinstance(result, OrderedDict)
    assert result == data


def test_deepcopy_table_empty():
    data = {}
    result = deepcopy_table(data)
    assert result == {}


# Tests for copy_sequence
def test_copy_sequence_list():
    values = [1, 2, 3, 4, 5]
    result = copy_sequence(values)
    assert result == [1, 2, 3, 4, 5]
    # Verify it's a copy
    result[0] = 99
    assert values[0] == 1  # Original unchanged


def test_copy_sequence_tuple():
    values = (1, 2, 3, 4, 5)
    result = copy_sequence(values)
    assert result == (1, 2, 3, 4, 5)
    assert isinstance(result, tuple)


def test_copy_sequence_empty():
    values = []
    result = copy_sequence(values)
    assert result == []


def test_copy_sequence_strings():
    values = ['a', 'b', 'c']
    result = copy_sequence(values)
    assert result == ['a', 'b', 'c']
    result[0] = 'x'
    assert values[0] == 'a'


# Tests for deepcopy_sequence
def test_deepcopy_sequence_list():
    values = [1, 2, 3, 4, 5]
    result = deepcopy_sequence(values)
    assert result == [1, 2, 3, 4, 5]
    # Verify it's a deep copy
    result[0] = 99
    assert values[0] == 1  # Original unchanged


def test_deepcopy_sequence_nested_lists():
    values = [[1, 2], [3, 4], [5, 6]]
    result = deepcopy_sequence(values)
    assert result == [[1, 2], [3, 4], [5, 6]]
    # Verify deep copy of nested structures
    result[0][0] = 99
    assert values[0][0] == 1  # Original unchanged


def test_deepcopy_sequence_tuple():
    values = (1, 2, 3)
    result = deepcopy_sequence(values)
    assert result == (1, 2, 3)
    assert isinstance(result, tuple)


def test_deepcopy_sequence_empty():
    values = []
    result = deepcopy_sequence(values)
    assert result == []


# Edge cases - verify independence
def test_copy_table_independence():
    data = {'x': [1, 2, 3]}
    result = copy_table(data)
    result['x'].append(4)
    assert len(data['x']) == 3  # Original has 3 elements
    assert len(result['x']) == 4  # Copy has 4 elements


def test_deepcopy_table_independence():
    data = {'x': [1, 2, 3]}
    result = deepcopy_table(data)
    result['x'].append(4)
    assert len(data['x']) == 3  # Original has 3 elements
    assert len(result['x']) == 4  # Copy has 4 elements

