from typing import Any, List, Mapping, MutableMapping, MutableSequence, Union

import tinytim.features as features
import tinytim.copy as copy


def edit_row_items_inplace(data: MutableMapping, index: int, items: Mapping) -> None:
    """Changes row index to mapping items values."""
    for col in items:
        data[col][index] = items[col]


def edit_row_values_inplace(data: MutableMapping, index: int, values: MutableSequence) -> None:
    """Changed row index to values."""
    if len(values) != features.column_count(data):
        raise AttributeError('values length must match columns length.')
    for col, value in zip(features.column_names(data), values):
        data[col][index] = value


def edit_column_inplace(data: MutableMapping, column_name: str, values: MutableSequence) -> None:
    """Add values to data in named column.
       Overrides existing values if column exists,
       Created new column with values if column does not exist.
    """
    if len(values) != features.row_count(data):
        raise ValueError('values length must match data rows count.')
    data[column_name] = values


def drop_row_inplace(data: MutableMapping, index: int) -> None:
    """Remove index row from data."""
    for col in features.column_names(data):
        data[col].pop(index)


def drop_label_inplace(labels: Union[None, List], index) -> None:
    if labels is not None:
        labels.pop(index)


def drop_column_inplace(data: MutableMapping, column_name: str) -> None:
    """Return a new dict with the named column removed from data."""
    del data[column_name]


def edit_value_inplace(data: MutableMapping, column_name: str, index: int, value: Any) -> None:
    """Edit the value in named column as row index."""
    data[column_name][index] = value


def replace_column_names(data: MutableMapping, new_names: MutableSequence[str]) -> dict:
    """Return a new dict same column data but new column names."""
    old_names = features.column_names(data)
    if len(new_names) != len(old_names):
        raise ValueError('new_names must be same size as data column_count.')
    return {new_name: data[old_name] for new_name, old_name in zip(new_names, old_names)}


def edit_row_items(data: MutableMapping, index: int, items: Mapping) -> MutableMapping:
    """Return a new dict with row index changed to mapping items values."""
    new_data = copy.copy_table(data)
    edit_row_items_inplace(new_data, index, items)
    return new_data


def edit_row_values(data: MutableMapping, index: int, values: MutableSequence) -> MutableMapping:
    """Return a new dict with row index changed to values."""
    new_data = copy.copy_table(data)
    edit_row_values_inplace(new_data, index, values)
    return new_data


def edit_column(data: MutableMapping, column_name: str, values: MutableSequence) -> MutableMapping:
    """Returns a new dict with values added to data in named column.
       Overrides existing values if column exists,
       Created new column with values if column does not exist.
    """
    new_data = copy.copy_table(data)
    edit_column_inplace(data, column_name, values)
    return new_data


def edit_value(data: MutableMapping, column_name: str, index: int, value: Any) -> MutableMapping:
    """Return a new table with the value in named column changed at row index."""
    new_data = copy.copy_table(data)
    edit_value_inplace(data, column_name, index, value)
    return new_data


def drop_row(data: MutableMapping, index: int) -> MutableMapping:
    """Return a new dict with index row removed from data."""
    new_data = copy.copy_table(data)
    drop_row_inplace(data, index)
    return new_data


def drop_label(labels: Union[None, List], index: int) -> Union[None, List]:
    if labels is None: return
    new_labels = copy.copy_list(labels)
    drop_label_inplace(new_labels, index)
    return new_labels


def drop_column(data: MutableMapping, column_name: str) -> MutableMapping:
    """Return a new dict with the named column removed from data."""
    new_data = copy.copy_table(data)
    drop_column_inplace(data, column_name)
    return new_data