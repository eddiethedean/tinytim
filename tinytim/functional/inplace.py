from typing import Any, List, Mapping, MutableMapping, MutableSequence, Union

from tinytim.functional.table import column_count, column_names, row_count


def edit_row_items(data: MutableMapping, index: int, items: Mapping) -> None:
    """Changes row index to mapping items values."""
    for col in items:
        data[col][index] = items[col]


def edit_row_values(data: MutableMapping, index: int, values: MutableSequence) -> None:
    """Changed row index to values."""
    if len(values) != column_count(data):
        raise AttributeError('values length must match columns length.')
    for col, value in zip(column_names(data), values):
        data[col][index] = value


def edit_column(data: MutableMapping, column_name: str, values: MutableSequence) -> None:
    """Add values to data in named column.
       Overrides existing values if column exists,
       Created new column with values if column does not exist.
    """
    if len(values) != row_count(data):
        raise ValueError('values length must match data rows count.')
    data[column_name] = values


def drop_row(data: MutableMapping, index: int) -> None:
    """Remove index row from data."""
    for col in column_names(data):
        data[col].pop(index)


def drop_label(labels: Union[None, List], index) -> None:
    if labels is not None:
        labels.pop(index)


def drop_column(data: MutableMapping, column_name: str) -> None:
    """Return a new dict with the named column removed from data."""
    del data[column_name]


def edit_value(data: MutableMapping, column_name: str, index: int, value: Any) -> None:
    """Edit the value in named column as row index."""
    data[column_name][index] = value
