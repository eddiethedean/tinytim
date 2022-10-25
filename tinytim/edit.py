from itertools import repeat
from numbers import Number
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, MutableSequence, Sequence, Sized, Union, Callable

import tinytim.data as data_features
import tinytim.copy as copy
import tinytim.columns as columns
from tinytim.utils import set_values_to_many, set_values_to_one

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
    values: Union[MutableSequence, str]
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
    values: Union[MutableSequence, str, Number],
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
    values: Union[MutableSequence, str, Number]
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
    values: Union[MutableSequence, Number]
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
    values: Union[MutableSequence, Number]
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
    values: Union[MutableSequence, Number]
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


def drop_label_inplace(labels: Union[None, List], index) -> None:
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


def replace_column_names(
    data: MutableDataMapping,
    new_names: Sequence[str]
) -> Dict[str, MutableSequence]:
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
    Dict[str, MutableSequence]
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
    return {new_name: data[old_name] for new_name, old_name in zip(new_names, old_names)}


def edit_row_items(
    data: MutableDataMapping,
    index: int,
    items: Mapping
) -> MutableDataMapping:
    """
    Return a new dict with row index changed to mapping items values.

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
    MutableMapping[str, MutableSequence]
        copy of data with edited row values

    Examples
    --------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> edit_row_items(data, 2, {'x': 33, 'y': 88})
    {'x': [1, 2, 33], 'y': [6, 7, 88]}
    >>> data
    {'x': [1, 2, 3], 'y': [6, 7, 8]}

    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> edit_row_items(data, 0, {'x': 55})
    {'x': [55, 2, 3], 'y': [6, 7, 8]}
    >>> data
    {'x': [1, 2, 3], 'y': [6, 7, 8]}
    """
    new_data = copy.copy_table(data)
    edit_row_items_inplace(new_data, index, items)
    return new_data


def edit_row_values(
    data: MutableDataMapping,
    index: int,
    values: Sequence
) -> MutableDataMapping:
    """
    Return a new dict with row index changed to values.

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
    MutableMapping[str, MutableSequence]
        copy of data with row at index changed to values

    Example
    -------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> edit_row_values(data, 1, (22, 77))
    {'x': [1, 22, 3], 'y': [6, 77, 8]}
    >>> data
    {'x': [1, 2, 3], 'y': [6, 7, 8]}
    """
    new_data = copy.copy_table(data)
    edit_row_values_inplace(new_data, index, values)
    return new_data


def edit_column(
    data: MutableDataMapping,
    column_name: str,
    values: MutableSequence
) -> MutableDataMapping:
    """
    Returns a new dict with values added to data in named column.
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
    MutableMapping[str, MutableSequence]
        copy of data with new column values

    Example
    -------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> edit_column(data, 'x', [4, 5, 6])
    {'x': [4, 5, 6], 'y': [6, 7, 8]}
    >>> data
     {'x': [1, 2, 3], 'y': [6, 7, 8]}
    """
    new_data = copy.copy_table(data)
    edit_column_inplace(new_data, column_name, values)
    return new_data


def add_to_column(
    data: MutableDataMapping,
    column_name: str,
    values: Union[MutableSequence, str, Number]
) -> MutableDataMapping:
    """
    Returns a new dict with values added to data in named column.

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
    MutableMapping[str, MutableSequence]
        copy of data with new column values

    Example
    -------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> edit_column(data, 'x', [4, 5, 6])
    {'x': [4, 5, 6], 'y': [6, 7, 8]}
    >>> data
     {'x': [1, 2, 3], 'y': [6, 7, 8]}
    """
    new_data = copy.copy_table(data)
    add_to_column_inplace(new_data, column_name, values)
    return new_data


def subtract_from_column(
    data: MutableDataMapping,
    column_name: str,
    values: Union[MutableSequence, Number]
) -> MutableDataMapping:
    """
    Returns a new dict with values subtracted from data in named column.

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
    MutableMapping[str, MutableSequence]
        copy of data with new column values

    Example
    -------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> subtract_from_column(data, 'x', [4, 5, 6])
    {'x': [-3, -3, -3], 'y': [6, 7, 8]}
    >>> data
     {'x': [1, 2, 3], 'y': [6, 7, 8]}
    """
    new_data = copy.copy_table(data)
    subtract_from_column_inplace(new_data, column_name, values)
    return new_data


def multiply_column(
    data: MutableDataMapping,
    column_name: str,
    values: Union[MutableSequence, Number]
) -> MutableDataMapping:
    """
    Returns a new dict with values multiplied with data in named column.

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
    MutableMapping[str, MutableSequence]
        copy of data with new column values

    Example
    -------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> multiply_column(data, 'x', [4, 5, 6])
    {'x': [4, 10, 18], 'y': [6, 7, 8]}
    >>> data
     {'x': [1, 2, 3], 'y': [6, 7, 8]}
    """
    new_data = copy.copy_table(data)
    multiply_column_inplace(new_data, column_name, values)
    return new_data


def divide_column(
    data: MutableDataMapping,
    column_name: str,
    values: Union[MutableSequence, Number]
) -> MutableDataMapping:
    """
    Returns a new dict with values divided from data in named column.

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
    MutableMapping[str, MutableSequence]
        copy of data with new column values

    Example
    -------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> divide_column(data, 'x', [4, 5, 6])
    {'x': [0.25, 0.4, 0.5], 'y': [6, 7, 8]}
    >>> data
     {'x': [1, 2, 3], 'y': [6, 7, 8]}
    """
    new_data = copy.copy_table(data)
    divide_column_inplace(new_data, column_name, values)
    return new_data


def edit_value(
    data: MutableDataMapping,
    column_name: str,
    index: int,
    value: Any
) -> MutableDataMapping:
    """
    Return a new table with the value in named column changed at row index.

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
    MutableMapping[str, MutableSequence]
        copy of data with new value changed

    Example
    -------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> edit_value(data, 'y', 2, 88)
    {'x': [1, 2, 3], 'y': [6, 7, 88]}
    >>> data
    {'x': [1, 2, 3], 'y': [6, 7, 8]}
    """
    new_data = copy.copy_table(data)
    edit_value_inplace(new_data, column_name, index, value)
    return new_data


def drop_row(
    data: MutableDataMapping,
    index: int
) -> MutableDataMapping:
    """
    Return a new dict with index row removed from data.

    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}
    index : int
        index of row to remove from data

    Returns
    -------
    MutableMapping[str, MutableSequence]
        copy of data with dropped row

    Example
    -------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> drop_row(data, 0)
    {'x': [2, 3], 'y': [7, 8]}
    >>> data
    {'x': [1, 2, 3], 'y': [6, 7, 8]}
    """
    new_data = copy.copy_table(data)
    drop_row_inplace(new_data, index)
    return new_data


def drop_label(
    labels: Union[None, List],
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
    list | None
        copy of labels with row dropped

    Examples
    --------
    >>> labels = [1, 2, 3, 4]
    >>> drop_label(labels, 1)
    [1, 3, 4]
    >>> labels
    [1, 3, 4, 5]

    >>> labels = None
    >>> drop_label(labels, 1)
    None
    >>> labels
    None
    """
    if labels is None: return
    new_labels = copy.copy_list(labels)
    drop_label_inplace(new_labels, index)
    return new_labels


def drop_column(
    data: MutableDataMapping,
    column_name: str
) -> MutableDataMapping:
    """
    Return a new dict with the named column removed from data.

    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}
    column_name : str
        name of column to remove from data

    Returns
    -------
    MutableMapping[str, MutableSequence]
        copy of data with column dropped

    Example
    -------
    >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    >>> drop_column(data, 'y')
    {'x': [1, 2, 3]}
    >>> data
    {'x': [1, 2, 3], 'y': [6, 7, 8]}
    """
    new_data = copy.copy_table(data)
    drop_column_inplace(new_data, column_name)
    return new_data