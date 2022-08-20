from typing import Callable, Iterable, List, MutableMapping, Sequence


TableFilter = Iterable[bool]


def column_filter(column: Iterable, func: Callable) -> List[bool]:
    return [func(item) for item in column]


def indexes_from_filter(f: TableFilter) -> List[int]:
    return [i for i, b in enumerate(f) if b]


def filter_list_by_indexes(values: Sequence, indexes: Sequence[int]) -> List:
    """Return only values in indexes."""
    return [values[i] for i in indexes]


def filter_by_indexes(data: MutableMapping, indexes: Sequence[int]) -> dict:
    """Return only rows in indexes"""
    return {col: filter_list_by_indexes(values, indexes) for col, values in data.items()}


def filter_data(data: MutableMapping, f: TableFilter) -> dict:
    indexes = indexes_from_filter(f)
    return filter_by_indexes(data, indexes)


def filter_by_column_func(data: MutableMapping, column_name: str, func) -> dict:
    """Return only rows of data where named column equals value."""
    indexes = [i for i, val in enumerate(data[column_name]) if func(val)]
    return filter_by_indexes(data, indexes)


def filter_by_column_eq(data: MutableMapping, column_name: str, value) -> dict:
    """Return only rows of data where named column equals value."""
    return filter_by_column_func(data, column_name, lambda x: x == value)


def filter_by_column_ne(data: MutableMapping, column_name: str, value) -> dict:
    """Return only rows of data where named column does not equal value."""
    return filter_by_column_func(data, column_name, lambda x: x != value)


def filter_by_column_gt(data: MutableMapping, column_name: str, value) -> dict:
    """Return only rows of data where named column is greater than value."""
    return filter_by_column_func(data, column_name, lambda x: x > value)


def filter_by_column_lt(data: MutableMapping, column_name: str, value) -> dict:
    """Return only rows of data where named column is less than value."""
    return filter_by_column_func(data, column_name, lambda x: x < value)


def filter_by_column_ge(data: MutableMapping, column_name: str, value) -> dict:
    """Return only rows of data where named column is greater than or equal value."""
    return filter_by_column_func(data, column_name, lambda x: x >= value)


def filter_by_column_le(data: MutableMapping, column_name: str, value) -> dict:
    """Return only rows of data where named column is less than or equal value."""
    return filter_by_column_func(data, column_name, lambda x: x <= value)


def filter_by_column_isin(data: MutableMapping, column_name: str, values) -> dict:
    """Return only rows of data where named column is in values."""
    return filter_by_column_func(data, column_name, lambda x: x in values)


def filter_by_column_notin(data: MutableMapping, column_name: str, values) -> dict:
    """Return only rows of data where named column is not in values."""
    return filter_by_column_func(data, column_name, lambda x: x not in values)


