from typing import Any, Dict, Mapping, Sequence, Tuple

DataMapping = Mapping[str, Sequence]


def column_count(data: DataMapping) -> int:
    """ Return the number of columns in data.

        :param data: data mapping of {column name: column values}
        :return: number of columns in data
    
        :Example:
        >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
        >>> column_count(data)
        2
    """
    return len(data)


def first_column_name(data: DataMapping) -> str:
    """ Return the name of the first column.
        Raises StopIteration if data has zero columns.

        :param data: data mapping of {column name: column values}
        :return: name of first column

        :Example:
        >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
        >>> first_column_name(data)
        'x'
    """
    return next(iter(data))


def row_count(data: DataMapping) -> int:
    """ Return the number of rows in data.
        
        :param data: data mapping of {column name: column values}
        :return: number of rows in data
    
        :Example:
        >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
        >>> row_count(data)
        3
    """
    if column_count(data) == 0: return 0
    return len(data[first_column_name(data)])


def shape(data: DataMapping) -> Tuple[int, int]:
    """ Return data row count, column count tuple.

        :param data: data mapping of {column name: column values}
        :return: tuple(row count, column count)
    
        :Example:
        >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
        >>> shape(data)
        (3, 2)
    """
    col_count = column_count(data)
    if col_count == 0: return 0, 0
    return row_count(data), col_count


def size(data: DataMapping) -> int:
    """ Return data row count multiplied by column count.
        
        :param data: data mapping of {column name: column values}
        :return: row count * column count
    
        :Example:
        >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
        >>> size(data)
        6
    """
    rows, columns = shape(data)
    return rows * columns


def column_names(data: DataMapping) -> Tuple[str]:
    """ Return data column names.

        :param data: data mapping of {column name: column values}
        :return: tuple of data column names
    
        :Example:
        >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
        >>> column_names(data)
        ('x', 'y')
    """
    return tuple(data)


def head(data: DataMapping, n: int = 5) -> Dict[str, Sequence]:
    """ Return the first n rows of data.

        :param data: data mapping of {column name: column values}
        :param n: default 5, number of rows to return from top of data
        :return: dict of column name: top n column values
    
        :Example:
        >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
        >>> head(data, 2)
        {'x': [1, 2], 'y': [6, 7]}
    """
    return {col: values[:n] for col, values in data.items()}


def tail(data: DataMapping, n: int = 5) -> Dict[str, Sequence]:
    """ Return the last n rows of data.

        :param data: data mapping of {column name: column values}
        :param n: default 5, number of rows to return from bottom of data
        :return: dict of column name: bottom n column values
    
        :Example:
        >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
        >>> tail(data, 2)
        {'x': [2, 3], 'y': [7, 8]}
    """
    return {col: values[-n:] for col, values in data.items()}


def index(data: DataMapping) -> Tuple[int]:
    """ Return tuple of data column indexes.

        :param data: data mapping of {column name: column values}
        :return: tuple of row indexes
    
        :Example:
        >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
        >>> index(data)
        (0, 1, 2)
    """
    return tuple(range(row_count(data)))


def table_value(data: DataMapping, column_name: str, index: int) -> Any:
    """ Return one value from column at row index.

        :param data: data mapping of {column name: column values}
        :column_name: name of column
        :index: index of column value
        :return: value of column at index
    
        :Example:
        >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
        >>> table_value(data, 'x', 1)
        2
    """
    return data[column_name][index]


def column_values(data: DataMapping, column_name: str) -> Sequence:
    """ Return all the values from one column.
        
        :param data: data mapping of {column name: column values}
        :return: column values

        :Example:
        >>> data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
        >>> column_values(data, 'y')
        [6, 7, 8]
    """
    return data[column_name]