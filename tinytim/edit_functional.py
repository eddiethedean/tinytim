from itertools import repeat
from numbers import Number
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Sized, Union, Callable

import tinytim.data as data_features
import tinytim.copy as copy
import tinytim.columns as columns
from tinytim.utils import set_values_to_many, set_values_to_one

DataMapping = Mapping[str, Sequence]
DataDict = Dict[str, list]


def to_datadict(data: DataMapping) -> DataDict:
    return {str(col): list(values) for col, values in data.items()}


def edit_row_items(
    data: DataMapping,
    index: int,
    items: Mapping[str, Any]
) -> DataDict:
    """
    Changes row index to mapping items values.

    Parameters
    ----------
    data : Mapping[str, Sequence]
        data mapping of {column name: column values}
    index : int
        index of row to edit
    items : Mapping[str, Any]
        {column names: value} of new values to edit in data

    Returns
    -------
    Dict[str, list]

    Example
    -------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> edit_row_items(data, 0, {'x': 11, 'y': 66})
    {'x': [11, 2, 3], 'y': [66, 7, 8]}
    >>> data
    {'x': [1, 2, 3], 'y': [6, 7, 8]}
    """
    data = to_datadict(data)
    for col in items:
        data[col][index] = items[col]
    return data


def edit_row_values(
    data: DataMapping,
    index: int,
    values: Sequence
) -> DataDict:
    """
    Changed row index to values.

    Parameters
    ----------
    data : Mapping[str, Sequence]
        data mapping of {column name: column values}
    index : int
        index of row to edit
    values : Sequence
        new values to replace in data row

    Returns
    -------
    Dict[str, list]

    Example
    -------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> edit_row_values(data, 1, (22, 77))
    {'x': [1, 22, 3], 'y': [6, 77, 8]}
    >>> data
    {'x': [1, 2, 3], 'y': [6, 7, 8]}
    """
    data = to_datadict(data)
    if len(values) != data_features.column_count(data):
        raise AttributeError('values length must match columns length.')
    for col, value in zip(data_features.column_names(data), values):
        data[col][index] = value
    return data


def edit_column(
    data: DataMapping,
    column_name: str,
    values: Union[Sequence, str]
) -> DataDict:
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
    Dict[str, list]

    Example
    -------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> edit_column(data, 'x', [11, 22, 33])
    {'x': [11, 22, 33], 'y': [6, 7, 8]}
    >>> data
    {'x': [1, 2, 3], 'y': [6, 7, 8]}
    """
    data = to_datadict(data)
    iterable_and_sized = isinstance(values, Iterable) and isinstance(values, Sized)
    if isinstance(values, str) or not iterable_and_sized:
        if column_name in data:
            set_values_to_one(data[column_name], values)
        else:
            data[column_name] = list(repeat(values, data_features.row_count(data)))
        return data
    if len(values) != data_features.row_count(data):
        raise ValueError('values length must match data rows count.')
    if column_name in data:
        set_values_to_many(data[column_name], values)
    else:
        data[column_name] = list(values)
    return data


def operator_column(
    data: DataMapping,
    column_name: str,
    values: Union[Sequence, str, Number],
    func: Callable[[Any, Any], Any]
) -> DataDict:
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
    Dict[str, list]

    Examples
    --------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> operator_column(data, 'x', 1, lambda x, y : x + y)
    {'x': [2, 3, 4], 'y': [6, 7, 8]}
    >>> data
    {'x': [1, 2, 3], 'y': [6, 7, 8]}

    >>> operator_column(data, 'x', [3, 4, 5], lambda x, y : x + y)
    {'x': [4, 6, 8], 'y': [6, 7, 8]}
    >>> data
    {'x': [1, 2, 3], 'y': [6, 7, 8]}
    """
    data = to_datadict(data)
    new_values = columns.operate_on_column(data[column_name], values, func)
    set_values_to_many(data[column_name], new_values)
    return data


def add_to_column(
    data: DataMapping,
    column_name: str,
    values: Union[Sequence, str, Number]
) -> DataDict:
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
    Dict[str, list]

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
    return operator_column(data, column_name, values, lambda x, y : x + y)


def subtract_from_column(
    data: DataMapping,
    column_name: str,
    values: Union[Sequence, Number]
) -> DataDict:
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
    Dict[str, list]

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
    return operator_column(data, column_name, values, lambda x, y : x - y)


def multiply_column_inplace(
    data: DataMapping,
    column_name: str,
    values: Union[Sequence, Number]
) -> DataDict:
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
    Dict[str, list]

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
    return operator_column(data, column_name, values, lambda x, y : x * y)


def divide_column(
    data: DataMapping,
    column_name: str,
    values: Union[Sequence, Number]
) -> DataDict:
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
    Dict[str, list]

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
    return operator_column(data, column_name, values, lambda x, y : x / y)


def drop_row(
    data: DataMapping,
    index: int
) -> DataDict:
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
    Dict[str, list]

    Example
    -------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> drop_row_inplace(data, 1)
    >>> data
    {'x': [1, 3], 'y': [6, 8]}
    """
    data = to_datadict(data)
    for col in data_features.column_names(data):
        data[col].pop(index)
    return data


def drop_label(
    labels: Union[None, Sequence],
    index: int
) -> Union[None, List]:
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
    None | list

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
        labels = list(labels)
        labels.pop(index)
    return labels


def drop_column(
    data: DataMapping,
    column_name: str
) -> DataDict:
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
    Dict[str, list]

    Example
    -------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> drop_column_inplace(data, 'y')
    >>> data
    {'x': [1, 2, 3]}
    """
    data = to_datadict(data)
    del data[column_name]
    return data


def edit_value(
    data: DataMapping,
    column_name: str,
    index: int,
    value: Any
) -> DataDict:
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
    Dict[str, list]

    Example
    -------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> edit_value_inplace(data, 'x', 0, 11)
    >>> data
    {'x': [11, 2, 3], 'y': [6, 7, 8]}
    """
    data = to_datadict(data)
    data[column_name][index] = value
    return data


def replace_column_names(
    data: DataMapping,
    new_names: Sequence[str]
) -> DataDict:
    """
    Return a new dict same column data but new column names.

    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}
    new_names : Sequence[str]
        new names of columns

    Returns
    -------
    Dict[str, list]
        copy of data with new column names

    Example
    -------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> replace_column_names(data, ('xx', 'yy'))
    >>> {'xx': [1, 2, 3], 'yy': [6, 7, 8]}
    >>> data
    {'x': [1, 2, 3], 'y': [6, 7, 8]}
    """
    old_names = data_features.column_names(data)
    if len(new_names) != len(old_names):
        raise ValueError('new_names must be same size as data column_count.')
    return {new_name: list(data[old_name]) for new_name, old_name in zip(new_names, old_names)}