from itertools import repeat
from numbers import Number
from typing import Any, Callable, Iterable, List, Sequence, Sized, Union


def operate_on_sequence(
    column: Sequence[Any],
    values: Union[Iterable[Any], str, Number],
    func: Callable[[Any, Any], Any]
) -> List[Any]:
    """
    Uses func operator on values in column.
    If values is a sequence, operate on each column value with values.
    values sequence must be same len as column.
    If values is not a sequence, operate on each column value with the single value.

    Parameters
    ----------
    column : MutableSequence
        sequence of values in column
    values : Sequence | str | Number
        values to operate on column values
    func : Callable[[Any, Any], Any]
        operator function to use to use values on column values

    Returns
    -------
    list

    Examples
    --------
    >>> column = [1, 2, 3, 4]
    >>> operate_on_columns(column, 1, lamda x, y : x + y)
    [2, 3, 4, 5]

    >>> column = [1, 2, 3, 4]
    >>> operate_on_columns(column, [2, 3, 4, 5], lamda x, y : x + y)
    [3, 5, 7, 9]
    """
    iterable_and_sized = isinstance(values, Iterable) and isinstance(values, Sized)
    if isinstance(values, str) or not iterable_and_sized:
        return [func(x, y) for x, y in zip(column, repeat(values, len(column)))] # type: ignore

    if iterable_and_sized and not isinstance(values, Number):
        if len(values) != len(column):  # type: ignore
            raise ValueError('values length must match data rows count.')
        return [func(x, y) for x, y in zip(column, values)]
    else:
        raise TypeError('values must either be a sequence or number to operate on column')


def add_to_sequence(
    column: Sequence[Any],
    values: Union[Sequence[Any], str, Number]
) -> List[Any]:
    """
    Add a value or values to a sequence of column values.

    Parameters
    ----------
    column : Sequence
    values : Sequence | str | Number

    Returns
    -------
    list

    Examples
    --------
    Add a number to each value in a sequence.

    >>> column = (1, 2, 3, 4)
    >>> add_to_column(column, 1)
    [2, 3, 4, 5]

    Add a sequence of numbers to a sequence.

    >>> column = (1, 2, 3, 4)
    >>> add_to_column(column, (4, 5, 6, 7))
    [5, 7, 9, 11]

    Concatenate a string to each value in a sequence of strings.

    >>> column = ('a', 'b', 'c', 'd')
    >>> add_to_column(column, 'A')
    ['aA', 'bA', 'cA', 'dA']

    Concatenate a string to each value in a sequence of strings.

    >>> column = ('a', 'b', 'c', 'd')
    >>> add_to_column(column, ('A', 'B', 'C', 'D'))

    See Also
    --------
    tinytim.columns.subtract_from_column
    tinytim.columns.multiply_column
    tinytim.columns.divide_column
    """
    return operate_on_sequence(column, values, lambda x, y : x + y)


def subtract_from_sequence(
    column: Sequence[Any],
    values: Union[Sequence[Any], Number]
) -> List[Any]:
    """
    Subtract a value or values from a sequence of column values.

    Parameters
    ----------
    column : Sequence
    values : Sequence | str | Number

    Returns
    -------
    list

    Examples
    --------
    Subtract a number from each value in a sequence of numbers.

    >>> column = (1, 2, 3, 4)
    >>> subtract_from_column(column, 1)
    [0, 1, 2, 3]

    Subtract a sequence of numbers from a sequence of numbers.

    >>> column = (1, 2, 3, 4)
    >>> subtract_from_column(column, (4, 5, 6, 7))
    [-3, -3, -3, -3]

    See Also
    --------
    tinytim.columns.add_to_column
    tinytim.columns.multiply_column
    tinytim.columns.divide_column
    """
    return operate_on_sequence(column, values, lambda x, y : x - y)


def multiply_sequence(
    column: Sequence[Any],
    values: Union[Sequence[Any], Number]
) -> List[Any]:
    """
    Multiply a value or values with a sequence of column values.

    Parameters
    ----------
    column : Sequence
    values : Sequence | str | Number

    Returns
    -------
    list

    Examples
    --------
    Multiply a number with each value in a sequence of numbers.

    >>> column = (1, 2, 3, 4)
    >>> multiply_column(column, 2)
    [2, 4, 6, 8]

    Mutiply a sequence of numbers with a sequence of numbers.

    >>> column = (1, 2, 3, 4)
    >>> multiply_column(column, (4, 5, 6, 7))
    [4, 10, 18, 28]

    Multiply a sequence of strings with a sequence of numbers.
    >>> column = ['a', 'b', 'c', 'd']
    >>> multiply_column(column, 3)
    ['aaa', 'bbb', 'ccc', 'ddd']

    Multiply a sequence of numbers with a sequence of strings.
    >>> column = [1, 2, 3, 4]
    >>> multiply_column(column, ('z', 'q', 'y', 'q'))

    See Also
    --------
    tinytim.columns.add_to_column
    tinytim.columns.subtract_from_column
    tinytim.columns.divide_column
    """
    return operate_on_sequence(column, values, lambda x, y : x * y)


def divide_sequence(
    column: Sequence[Any],
    values: Union[Sequence[Any], Number]
) -> List[Any]:
    """
    Divide a value or values from a sequence of column values.

    Parameters
    ----------
    column : Sequence
    values : Sequence | str | Number

    Returns
    -------
    list

    Examples
    --------
    Divide a number from each value in a sequence of numbers.

    >>> column = (1, 2, 3, 4)
    >>> divide_column(column, 2)
    [0.5, 1.0, 1.5, 2.0]

    Divide a sequence of numbers from a sequence of numbers.

    >>> column = (1, 2, 3, 4)
    >>> divide_column(column, (4, 5, 6, 7))
    [0.25, 0.4, 0.5, 0.5714285714285714]

    See Also
    --------
    tinytim.columns.add_to_column
    tinytim.columns.subtract_from_column
    tinytim.columns.multiply_column
    """
    return operate_on_sequence(column, values, lambda x, y : x / y)


def mod_sequence(
    column: Sequence[Any],
    values: Union[Sequence[Any], Number]
) -> List[Any]:
    """
    Modulo a value or values from a sequence of column values.

    Parameters
    ----------
    column : Sequence
    values : Sequence | Number

    Returns
    -------
    list

    Examples
    --------
    Modulo a number from each value in a sequence of numbers.

    >>> column = (1, 2, 3, 4)
    >>> mod_column(column, 2)
    [1, 0, 1, 0]

    Modulo a sequence of numbers from a sequence of numbers.

    >>> column = (4, 67, 87, 65)
    >>> mod_column(column, (2, 3, 4, 5))
    [0, 1, 3, 0]

    See Also
    --------
    tinytim.columns.add_to_column
    tinytim.columns.subtract_from_column
    tinytim.columns.divide_column
    """
    return operate_on_sequence(column, values, lambda x, y : x % y)


def exponent_sequence(
    column: Sequence[Any],
    values: Union[Sequence[Any], Number]
) -> List[Any]:
    """
    Exponent a value or values with a sequence of column values.

    Parameters
    ----------
    column : Sequence
    values : Sequence | Number

    Returns
    -------
    list

    Examples
    --------
    Exponent a number with each value in a sequence of numbers.

    >>> column = (1, 2, 3, 4)
    >>> exponent_column(column, 2)
    [1, 4, 9, 16]

    Exponent a sequence of numbers with a sequence of numbers.

    >>> column = (2, 3, 4, 5)
    >>> exponent_column(column, (2, 3, 4, 5))
    [4, 27, 256, 3125]

    See Also
    --------
    tinytim.columns.add_to_column
    tinytim.columns.subtract_from_column
    tinytim.columns.divide_column
    """
    return operate_on_sequence(column, values, lambda x, y : x ** y)


def floor_sequence(
    column: Sequence[Any],
    values: Union[Sequence[Any], Number]
) -> List[Any]:
    """
    Floor divide a value or values from a sequence of column values.

    Parameters
    ----------
    column : Sequence
    values : Sequence | Number

    Returns
    -------
    list

    Examples
    --------
    Floor divide a number from each value in a sequence of numbers.

    >>> column = (1, 2, 3, 4)
    >>> floor_column(column, 2)
    [0, 1, 1, 2]

    Floor divide a sequence of numbers from a sequence of numbers.

    >>> column = (56, 77, 88, 55)
    >>> floor_column(column, (5, 6, 7, 8))
    [11, 12, 12, 6]

    See Also
    --------
    tinytim.columns.add_to_column
    tinytim.columns.subtract_from_column
    tinytim.columns.divide_column
    """
    return operate_on_sequence(column, values, lambda x, y : x // y)
