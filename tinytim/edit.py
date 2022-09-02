from typing import Any, List, Mapping, MutableMapping, MutableSequence, Sequence, Union

import tinytim.data as data_features
import tinytim.copy as copy


def edit_row_items_inplace(data: MutableMapping, index: int, items: Mapping) -> None:
    """Changes row index to mapping items values.
    
       Example:
       data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
       edit_row_items_inplace(data, 0, {'x': 11, 'y': 66}) -> None
       data -> {'x': [11, 2, 3], 'y': [66, 7, 8]}
    """
    for col in items:
        data[col][index] = items[col]


def edit_row_values_inplace(data: MutableMapping, index: int, values: Sequence) -> None:
    """Changed row index to values.
    
       Example:
       data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
       edit_row_values_inplace(data, 1, (22, 77)) -> None
       data -> {'x': [1, 22, 3], 'y': [6, 77, 8]}
    """
    if len(values) != data_features.column_count(data):
        raise AttributeError('values length must match columns length.')
    for col, value in zip(data_features.column_names(data), values):
        data[col][index] = value


def edit_column_inplace(data: MutableMapping, column_name: str, values: MutableSequence) -> None:
    """Add values to data in named column.
       Overrides existing values if column exists,
       Created new column with values if column does not exist.

       Example:
       data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
       edit_column_inplace(data, 'x', [11, 22, 33]) -> None
       data -> {'x': [11, 22, 33], 'y': [6, 7, 8]}
    """
    if len(values) != data_features.row_count(data):
        raise ValueError('values length must match data rows count.')
    data[column_name] = values


def drop_row_inplace(data: MutableMapping, index: int) -> None:
    """Remove index row from data.
    
       Example:
       data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
       drop_row_inplace(data, 1) -> None
       data -> {'x': [1, 3], 'y': [6, 8]}
    """
    for col in data_features.column_names(data):
        data[col].pop(index)


def drop_label_inplace(labels: Union[None, List], index) -> None:
    """If labels exists, drop item at index.

       Examples:
       labels = [1, 2, 3, 4, 5]
       drop_label_inplace(labels, 1) -> None
       labels -> [1, 3, 4, 5]

       labels = None
       drop_label_inplace(labels, 1) -> None
       labels -> None
    """
    if labels is not None:
        labels.pop(index)


def drop_column_inplace(data: MutableMapping, column_name: str) -> None:
    """Return a new dict with the named column removed from data.
    
       Example:
       data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
       drop_column_inplace(data, 'y') -> None
       data -> {'x': [1, 2, 3]}
    """
    del data[column_name]


def edit_value_inplace(data: MutableMapping, column_name: str, index: int, value: Any) -> None:
    """Edit the value in named column as row index.
    
       Example:
       data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
       edit_value_inplace(data, 'x', 0, 11) -> None
       data -> {'x': [11, 2, 3], 'y': [6, 7, 8]}
    """
    data[column_name][index] = value


def replace_column_names(data: MutableMapping, new_names: Sequence[str]) -> dict:
    """Return a new dict same column data but new column names.
    
       Example:
       data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
       replace_column_names(data, ('xx', 'yy')) -> {'xx': [1, 2, 3], 'yy': [6, 7, 8]}
       data -> {'x': [1, 2, 3], 'y': [6, 7, 8]}
    """
    old_names = data_features.column_names(data)
    if len(new_names) != len(old_names):
        raise ValueError('new_names must be same size as data column_count.')
    return {new_name: data[old_name] for new_name, old_name in zip(new_names, old_names)}


def edit_row_items(data: MutableMapping, index: int, items: Mapping) -> MutableMapping:
    """Return a new dict with row index changed to mapping items values.
    
       Examples:
       data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
       edit_row_items(data, 2, {'x': 33, 'y': 88}) -> {'x': [1, 2, 33], 'y': [6, 7, 88]}
       data -> {'x': [1, 2, 3], 'y': [6, 7, 8]}

       data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
       edit_row_items(data, 0, {'x': 55}) -> {'x': [55, 2, 3], 'y': [6, 7, 8]}
       data -> {'x': [1, 2, 3], 'y': [6, 7, 8]}
    """
    new_data = copy.copy_table(data)
    edit_row_items_inplace(new_data, index, items)
    return new_data


def edit_row_values(data: MutableMapping, index: int, values: Sequence) -> MutableMapping:
    """Return a new dict with row index changed to values.
    
       Example:
       data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
       edit_row_values(data, 1, (22, 77)) -> {'x': [1, 22, 3], 'y': [6, 77, 8]}
       data -> {'x': [1, 2, 3], 'y': [6, 7, 8]}
    """
    new_data = copy.copy_table(data)
    edit_row_values_inplace(new_data, index, values)
    return new_data


def edit_column(data: MutableMapping, column_name: str, values: MutableSequence) -> MutableMapping:
    """Returns a new dict with values added to data in named column.
       Overrides existing values if column exists,
       Created new column with values if column does not exist.

       Example:
       data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
       edit_column(data, 'x', [4, 5, 6]) -> {'x': [4, 5, 6], 'y': [6, 7, 8]}
       data -> {'x': [1, 2, 3], 'y': [6, 7, 8]}
    """
    new_data = copy.copy_table(data)
    edit_column_inplace(new_data, column_name, values)
    return new_data


def edit_value(data: MutableMapping, column_name: str, index: int, value: Any) -> MutableMapping:
    """Return a new table with the value in named column changed at row index.
    
       Example:
       data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
       edit_value(data, 'y', 2, 88) -> {'x': [1, 2, 3], 'y': [6, 7, 88]}
       data -> {'x': [1, 2, 3], 'y': [6, 7, 8]}
    """
    new_data = copy.copy_table(data)
    edit_value_inplace(new_data, column_name, index, value)
    return new_data


def drop_row(data: MutableMapping, index: int) -> MutableMapping:
    """Return a new dict with index row removed from data.
    
       Example:
       data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
       drop_row(data, 0) -> {'x': [2, 3], 'y': [7, 8]}
       data -> {'x': [1, 2, 3], 'y': [6, 7, 8]}
    """
    new_data = copy.copy_table(data)
    drop_row_inplace(new_data, index)
    return new_data


def drop_label(labels: Union[None, List], index: int) -> Union[None, List]:
    """If labels exists, drop item at index.
    
       Examples:
       labels = [1, 2, 3, 4]
       drop_label(labels, 1) -> [1, 3, 4]
       labels -> [1, 2, 3, 4]

       labels = None
       drop_label(labels, 1) -> None
       labels -> None
    """
    if labels is None: return
    new_labels = copy.copy_list(labels)
    drop_label_inplace(new_labels, index)
    return new_labels


def drop_column(data: MutableMapping, column_name: str) -> MutableMapping:
    """Return a new dict with the named column removed from data.
    
       Example:
       data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
       drop_column(data, 'y') -> {'x': [1, 2, 3]}
       data -> {'x': [1, 2, 3], 'y': [6, 7, 8]}
    """
    new_data = copy.copy_table(data)
    drop_column_inplace(new_data, column_name)
    return new_data