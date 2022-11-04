from itertools import repeat
from numbers import Number
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Sized, Union, Callable, MutableMapping, MutableSequence

import tinytim.data as data_features
import tinytim.copy as copy
import tinytim.columns as columns
from tinytim.utils import set_values_to_many, set_values_to_one

DataMapping = Mapping[str, Sequence]
DataDict = Dict[str, list]
MutableDataMapping = MutableMapping[str, MutableSequence]


def edit_row_items_inplace(
    data: MutableDataMapping,
    index: int,
    items: Mapping[str, Any]
) -> None:
    """
    Changes row index to mapping items values.

    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}
    index : int
        index of row to edit
    items : Mapping[str, Any]
        {column names: value} of new values to edit in data

    Returns
    -------
    None

    Example
    -------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> edit_row_items_inplace(data, 0, {'x': 11, 'y': 66})
    >>> data
    {'x': [11, 2, 3], 'y': [66, 7, 8]}
    """
    for col in items:
        data[col][index] = items[col]


def edit_row_values_inplace(
    data: MutableDataMapping,
    index: int,
    values: Sequence
) -> None:
    """
    Changed row index to values.

    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}
    index : int
        index of row to edit
    values : Sequence
        new values to replace in data row

    Returns
    -------
    None

    Example
    -------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> edit_row_values_inplace(data, 1, (22, 77))
    >>> data
    {'x': [1, 22, 3], 'y': [6, 77, 8]}
    """
    if len(values) != data_features.column_count(data):
        raise AttributeError('values length must match columns length.')
    for col, value in zip(data_features.column_names(data), values):
        data[col][index] = value


def edit_column_inplace(
    data: MutableDataMapping,
    column_name: str,
    values: Union[Sequence, str]
) -> None:
    """
    Edit values in named column.
    Overrides existing values if column exists,
    Created new column with values if column does not exist.

    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}
    column_name : str
        column name to edit in data
    values : Sequence
        new values to replace in data column

    Returns
    -------
    None

    Example
    -------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> edit_column_inplace(data, 'x', [11, 22, 33])
    >>> data
    {'x': [11, 22, 33], 'y': [6, 7, 8]}
    """
    iterable_and_sized = isinstance(values, Iterable) and isinstance(values, Sized)
    if isinstance(values, str) or not iterable_and_sized:
        if column_name in data:
            set_values_to_one(data[column_name], values)
        else:
            data[column_name] = list(repeat(values, data_features.row_count(data)))
        return
    if len(values) != data_features.row_count(data):
        raise ValueError('values length must match data rows count.')
    if column_name in data:
        set_values_to_many(data[column_name], values)
    else:
        data[column_name] = list(values)


def operator_column_inplace(
    data: MutableDataMapping,
    column_name: str,
    values: Union[Sequence, str, Number],
    func: Callable[[Any, Any], Any]
) -> None:
    """
    Uses func operator on values from existing named column.
    If values is a Sequence, operate each value from each existing value.
    Must be same len as column.
    If not a Sequence, operate value from all existing values.

    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}
    column_name : str
        column name to edit in data
    values : Sequence
        values to subtract from data column
    func : Callable[[Any, Any], Any]
        operator function to use to use values on existing column values

    Returns
    -------
    None
    """
    new_values = columns.operate_on_column(data[column_name], values, func)
    set_values_to_many(data[column_name], new_values)


def add_to_column_inplace(
    data: MutableDataMapping,
    column_name: str,
    values: Union[Sequence, str, Number]
) -> None:
    """
    Add values to existing named column.
    If values is a Sequence, add each value to each existing value.
    Must be same len as column.
    If not a Sequence, adds value to all existing values.

    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}
    column_name : str
        column name to edit in data
    values : Sequence
        values to add to data column

    Returns
    -------
    None

    Examples
    --------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> add_to_column_inplace(data, 'x', [11, 22, 33])
    >>> data
    {'x': [12, 24, 36], 'y': [6, 7, 8]}

    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> add_to_column_inplace(data, 'x', 1)
    >>> data
    {'x': [2, 3, 4], 'y': [6, 7, 8]}
    """
    operator_column_inplace(data, column_name, values, lambda x, y : x + y)


def subtract_from_column_inplace(
    data: MutableDataMapping,
    column_name: str,
    values: Union[Sequence, Number]
) -> None:
    """
    Subtract values from existing named column.
    If values is a Sequence, subtract each value from each existing value.
    Must be same len as column.
    If not a Sequence, subtracts value from all existing values.

    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}
    column_name : str
        column name to edit in data
    values : Sequence
        values to subtract from data column

    Returns
    -------
    None

    Examples
    --------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> subtract_from_column_inplace(data, 'x', [11, 22, 33])
    >>> data
    {'x': [-10, -20, -30], 'y': [6, 7, 8]}

    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> subtract_from_column_inplace(data, 'x', 1)
    >>> data
    {'x': [0, 1, 2], 'y': [6, 7, 8]}
    """
    operator_column_inplace(data, column_name, values, lambda x, y : x - y)


def multiply_column_inplace(
    data: MutableDataMapping,
    column_name: str,
    values: Union[Sequence, Number]
) -> None:
    """
    Multiply values with existing named column.
    If values is a Sequence, multiply each value with each existing value.
    Must be same len as column.
    If not a Sequence, multiply value with all existing values.

    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}
    column_name : str
        column name to edit in data
    values : Sequence
        values to multiply with data column

    Returns
    -------
    None

    Examples
    --------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> subtract_from_column_inplace(data, 'x', [11, 22, 33])
    >>> data
    {'x': [66, 44, 99], 'y': [6, 7, 8]}

    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> subtract_from_column_inplace(data, 'x', 2)
    >>> data
    {'x': [2, 4, 6], 'y': [6, 7, 8]}
    """
    operator_column_inplace(data, column_name, values, lambda x, y : x * y)


def divide_column_inplace(
    data: MutableDataMapping,
    column_name: str,
    values: Union[Sequence, Number]
) -> None:
    """
    Divide values from existing named column.
    If values is a Sequence, Divide each value from each existing value.
    Must be same len as column.
    If not a Sequence, divide value from all existing values.

    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}
    column_name : str
        column name to edit in data
    values : Sequence
        values to divide from data column

    Returns
    -------
    None

    Raises
    ------
    ZeroDivisionError
        if values is 0 or contains 0

    Examples
    --------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> divide_column_inplace(data, 'x', [2, 3, 4])
    >>> data
    {'x': [0.5, 0.6666666666666666, 0.75], 'y': [6, 7, 8]}

    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> divide_column_inplace(data, 'x', 2)
    >>> data
    {'x': [0.5, 1.0, 1.5], 'y': [6, 7, 8]}
    """
    operator_column_inplace(data, column_name, values, lambda x, y : x / y)


def drop_row_inplace(
    data: MutableDataMapping,
    index: int
) -> None:
    """
    Remove index row from data.

    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}
    index : int
        index of row to remove from data

    Returns
    -------
    None

    Example
    -------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> drop_row_inplace(data, 1)
    >>> data
    {'x': [1, 3], 'y': [6, 8]}
    """
    for col in data_features.column_names(data):
        data[col].pop(index)


def drop_label_inplace(labels: Union[None, List], index: int) -> None:
    """
    If labels exists, drop item at index.

    Parameters
    ----------
    labels : list, optional
        list of values used as labels
    index : int
        index of value to remove from labels list

    Returns
    -------
    None

    Examples
    --------
    >>> labels = [1, 2, 3, 4, 5]
    >>> drop_label_inplace(labels, 1)
    >>> labels
    [1, 3, 4, 5]

    >>> labels = None
    >>> drop_label_inplace(labels, 1)
    >>> labels
    None
    """
    if labels is not None:
        labels.pop(index)


def drop_column_inplace(
    data: MutableDataMapping,
    column_name: str
) -> None:
    """
    Remove named column from data.

    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}
    column_name : str
        name of column to remove from data

    Returns
    -------
    None

    Example
    -------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> drop_column_inplace(data, 'y')
    >>> data
    {'x': [1, 2, 3]}
    """
    del data[column_name]


def edit_value_inplace(
    data: MutableDataMapping,
    column_name: str,
    index: int,
    value: Any
) -> None:
    """
    Edit the value in named column as row index.

    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}
    column_name : str
        name of column to remove from data
    index : int
        row index of column to edit
    value : Any
        new value to change to

    Returns
    -------
    None

    Example
    -------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> edit_value_inplace(data, 'x', 0, 11)
    >>> data
    {'x': [11, 2, 3], 'y': [6, 7, 8]}
    """
    data[column_name][index] = value