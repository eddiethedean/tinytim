import pytest

from tinytim.sequences import (
    add_to_sequence,
    divide_sequence,
    exponent_sequence,
    floor_sequence,
    mod_sequence,
    multiply_sequence,
    operate_on_sequence,
    subtract_from_sequence,
)


# Tests for operate_on_sequence (the base function)
def test_operate_on_sequence_with_scalar():
    column = [1, 2, 3, 4]
    result = operate_on_sequence(column, 10, lambda x, y: x + y)
    assert result == [11, 12, 13, 14]


def test_operate_on_sequence_with_sequence():
    column = [1, 2, 3, 4]
    values = [10, 20, 30, 40]
    result = operate_on_sequence(column, values, lambda x, y: x + y)
    assert result == [11, 22, 33, 44]


def test_operate_on_sequence_with_string():
    column = ['a', 'b', 'c']
    result = operate_on_sequence(column, 'X', lambda x, y: x + y)
    assert result == ['aX', 'bX', 'cX']


def test_operate_on_sequence_mismatched_length():
    column = [1, 2, 3, 4]
    values = [10, 20]  # Wrong length
    with pytest.raises(ValueError, match='values length must match data rows count'):
        operate_on_sequence(column, values, lambda x, y: x + y)


def test_operate_on_sequence_invalid_type():
    column = [1, 2, 3, 4]
    values = 5.5  # Number is valid but testing the type error path
    # Numbers should work fine
    result = operate_on_sequence(column, values, lambda x, y: x + y)
    assert result == [6.5, 7.5, 8.5, 9.5]


# Tests for add_to_sequence
def test_add_to_sequence_scalar():
    column = [1, 2, 3, 4]
    result = add_to_sequence(column, 10)
    assert result == [11, 12, 13, 14]


def test_add_to_sequence_sequence():
    column = [1, 2, 3, 4]
    values = [10, 20, 30, 40]
    result = add_to_sequence(column, values)
    assert result == [11, 22, 33, 44]


def test_add_to_sequence_strings():
    column = ['a', 'b', 'c']
    result = add_to_sequence(column, 'X')
    assert result == ['aX', 'bX', 'cX']


def test_add_to_sequence_string_sequences():
    column = ['a', 'b', 'c']
    values = ['X', 'Y', 'Z']
    result = add_to_sequence(column, values)
    assert result == ['aX', 'bY', 'cZ']


# Tests for subtract_from_sequence
def test_subtract_from_sequence_scalar():
    column = [10, 20, 30, 40]
    result = subtract_from_sequence(column, 5)
    assert result == [5, 15, 25, 35]


def test_subtract_from_sequence_sequence():
    column = [10, 20, 30, 40]
    values = [1, 2, 3, 4]
    result = subtract_from_sequence(column, values)
    assert result == [9, 18, 27, 36]


def test_subtract_from_sequence_negative_results():
    column = [1, 2, 3, 4]
    result = subtract_from_sequence(column, 10)
    assert result == [-9, -8, -7, -6]


# Tests for multiply_sequence
def test_multiply_sequence_scalar():
    column = [1, 2, 3, 4]
    result = multiply_sequence(column, 3)
    assert result == [3, 6, 9, 12]


def test_multiply_sequence_sequence():
    column = [1, 2, 3, 4]
    values = [2, 3, 4, 5]
    result = multiply_sequence(column, values)
    assert result == [2, 6, 12, 20]


def test_multiply_sequence_strings():
    column = ['a', 'b', 'c']
    result = multiply_sequence(column, 3)
    assert result == ['aaa', 'bbb', 'ccc']


def test_multiply_sequence_zero():
    column = [1, 2, 3, 4]
    result = multiply_sequence(column, 0)
    assert result == [0, 0, 0, 0]


# Tests for divide_sequence
def test_divide_sequence_scalar():
    column = [10, 20, 30, 40]
    result = divide_sequence(column, 2)
    assert result == [5.0, 10.0, 15.0, 20.0]


def test_divide_sequence_sequence():
    column = [10, 20, 30, 40]
    values = [2, 4, 5, 8]
    result = divide_sequence(column, values)
    assert result == [5.0, 5.0, 6.0, 5.0]


def test_divide_sequence_float_result():
    column = [1, 2, 3, 4]
    result = divide_sequence(column, 2)
    assert result == [0.5, 1.0, 1.5, 2.0]


# Tests for mod_sequence
def test_mod_sequence_scalar():
    column = [10, 11, 12, 13]
    result = mod_sequence(column, 3)
    assert result == [1, 2, 0, 1]


def test_mod_sequence_sequence():
    column = [10, 11, 12, 13]
    values = [3, 4, 5, 6]
    result = mod_sequence(column, values)
    assert result == [1, 3, 2, 1]


def test_mod_sequence_larger_divisor():
    column = [1, 2, 3, 4]
    result = mod_sequence(column, 10)
    assert result == [1, 2, 3, 4]


# Tests for exponent_sequence
def test_exponent_sequence_scalar():
    column = [1, 2, 3, 4]
    result = exponent_sequence(column, 2)
    assert result == [1, 4, 9, 16]


def test_exponent_sequence_sequence():
    column = [2, 3, 4, 5]
    values = [1, 2, 3, 4]
    result = exponent_sequence(column, values)
    assert result == [2, 9, 64, 625]


def test_exponent_sequence_zero():
    column = [1, 2, 3, 4]
    result = exponent_sequence(column, 0)
    assert result == [1, 1, 1, 1]


def test_exponent_sequence_one():
    column = [1, 2, 3, 4]
    result = exponent_sequence(column, 1)
    assert result == [1, 2, 3, 4]


# Tests for floor_sequence
def test_floor_sequence_scalar():
    column = [10, 11, 12, 13]
    result = floor_sequence(column, 3)
    assert result == [3, 3, 4, 4]


def test_floor_sequence_sequence():
    column = [10, 20, 30, 40]
    values = [3, 6, 7, 9]
    result = floor_sequence(column, values)
    assert result == [3, 3, 4, 4]


def test_floor_sequence_exact_division():
    column = [10, 20, 30, 40]
    result = floor_sequence(column, 10)
    assert result == [1, 2, 3, 4]


# Edge cases
def test_sequences_with_tuples():
    column = (1, 2, 3, 4)
    result = add_to_sequence(column, 10)
    assert result == [11, 12, 13, 14]


def test_sequences_with_negative_numbers():
    column = [-5, -3, -1, 1, 3]
    result = multiply_sequence(column, -2)
    assert result == [10, 6, 2, -2, -6]


def test_sequences_empty_should_work():
    column = []
    result = add_to_sequence(column, 10)
    assert result == []

