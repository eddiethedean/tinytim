from typing import Any, Mapping, MutableSequence, Tuple


def column_count(data: Mapping) -> int:
    """Return the number of columns in data."""
    return len(data)


def row_count(data: Mapping) -> int:
    """Return the number of rows in data."""
    if column_count(data) == 0: return 0
    return len(data[first_column_name(data)])


def shape(data: Mapping) -> Tuple[int, int]:
    """Return data row count, column count tuple."""
    col_count = column_count(data)
    if col_count == 0: return 0, 0
    return row_count(data), col_count


def size(data: Mapping) -> int:
    """Return data row count multiplied by column count."""
    rows, columns = shape(data)
    return rows * columns


def first_column_name(data: Mapping) -> str:
    """Return the name of the first column.
       Raises StopIteration if data has zero columns.
    """
    return next(iter(data))


def column_names(data: Mapping[str, Any]) -> Tuple[str]:
    """Return data column names."""
    return tuple(data)


def head(data: Mapping, n: int = 5) -> dict:
    """Return the first n rows of data."""
    return {col: values[:n] for col, values in data.items()}


def tail(data: Mapping, n: int = 5) -> dict:
    """Return the last n rows of data."""
    return {col: values[-n:] for col, values in data.items()}


def index(data: Mapping) -> Tuple[int]:
    """Return tuple of data column indexes."""
    return tuple(range(row_count(data)))


def table_value(data: Mapping, column_name: str, index: int) -> Any:
    """Return one value from column at row index."""
    return data[column_name][index]


def column_values(data: Mapping[str, MutableSequence], column_name: str) -> MutableSequence:
    return data[column_name]