from typing import Any, Optional, Sequence, Union

from hasattrs import has_mapping_attrs

import tinytim.data as data_functions
import tinytim.edit as edit_functions
import tinytim.rows as rows_functions
from tinytim.types import DataDict, DataMapping, RowDict, RowMapping, data_dict, row_dict


def fillna(
    data: DataDict,
    value: Optional[Any] = None,
    method: Optional[str] = None,
    axis: Optional[Union[int, str]] = 0,
    inplace: bool = False,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> Union[DataDict, None]:
    """
    Fill missing values using the specified method.

    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}
    value : Any
        value to use to fill missing values
    method : {'backfill', 'bfill', 'pad', 'ffill', None}
        method to use for filling holes in reindexed
        Series.
        pad/ffill: propagate last valid observation
        forward to next valid
        backfill/bfill: use next valid observation to fill gap.

    Returns
    -------
    Mapping or None
        Object with missing values filled or None if inplace=True
    """
    if method is None:
        if inplace:
            fill_with_value_inplace(data, value, axis, limit, na_value)
        else:
            return fill_with_value(data, value, axis, limit, na_value)
    elif method in ['backfill', 'bfill']:
        if value is not None:
            raise ValueError("Cannot specify both 'value' and 'method'.")
        if inplace:
            backfill_inplace(data, axis, limit, na_value)
        else:
            return backfill(data, axis, limit, na_value)
    elif method in ['pad', 'ffill']:
        if value is not None:
            raise ValueError("Cannot specify both 'value' and 'method'.")
        if inplace:
            forwardfill_inplace(data, axis, limit, na_value)
        else:
            return forwardfill(data, axis, limit, na_value)


def fill_with_value_inplace(
    data: DataDict,
    value: Any,
    axis: Optional[Union[int, str]] = 0,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> None:
    """
    Fill data columns with given value.

    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}
    value : Any
        value to use to fill missing values
        If value is Mapping: {column_name: value},
        fill missing values in each column with each value.
    """
    if axis in [0, 'rows']:
        fill_columns_with_value_inplace(data, value, limit, na_value)
    elif axis in [1, 'columns']:
        fill_rows_with_value_inplace(data, value, limit, na_value)


def fill_with_value(
    data: DataMapping,
    value: Any,
    axis: Optional[Union[int, str]] = 0,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> DataDict:
    """
    Fill data columns with given value.

    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}
    value : Any
        value to use to fill missing values
        If value is Mapping: {column_name: value},
        fill missing values in each column with each value.
    """
    data =  data_dict(data)
    fill_with_value_inplace(data, value, axis, limit, na_value)
    return data


def backfill_inplace(
    data: DataDict,
    axis: Optional[Union[int, str]] = 0,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> None:
    """
    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}
    """
    if axis in [0, 'row']:
        backfill_columns_inplace(data, limit, na_value)
    elif axis in [1, 'column']:
        backfill_rows_inplace(data, limit, na_value)


def backfill(
    data: DataMapping,
    axis: Optional[Union[int, str]] = 0,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> DataDict:
    """
    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}

    Returns
    -------
    MutableMapping[str, MutableSequence]
    """
    data = data_dict(data)
    backfill_inplace(data, axis, limit, na_value)
    return data


def forwardfill_inplace(
    data: DataDict,
    axis: Optional[Union[int, str]] = 0,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> None:
    """
    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}

    Returns
    -------
    None
    """
    if axis in [0, 'rows']:
        forwardfill_columns_inplace(data, limit, na_value)
    elif axis in [1, 'columns']:
        forwardfill_rows_inplace(data, limit, na_value)


def forwardfill(
    data: DataMapping,
    axis: Optional[Union[int, str]] = 0,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> DataDict:
    """
    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}

    Returns
    -------
    MutableMapping[str, MutableSequence]
    """
    data = data_dict(data)
    forwardfill_inplace(data, axis, limit, na_value)
    return data


def fill_columns_with_value_inplace(
    data: DataDict,
    value: Any,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> None:
    """
    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}

    Returns
    -------
    None
    """
    columns = data_functions.column_names(data)
    for col in columns:
        try:
            fill_value = _get_fill_value(value, col)
        except Continue:
            continue
        fill_column_with_value_inplace(data[col], fill_value, limit, na_value)


def fill_rows_with_value_inplace(
    data: DataDict,
    value: Any,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> None:
    """
    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}

    Returns
    -------
    None
    """
    for i, row in rows_functions.iterrows(data):
        new_row = fill_row_with_value(row, value, limit, na_value)
        edit_functions.edit_row_items_inplace(data, i, new_row)


def backfill_columns_inplace(
    data: DataDict,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> None:
    """
    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}

    Returns
    -------
    None
    """
    for col in data:
        backfill_column_inplace(data[col], limit, na_value)


def backfill_columns(
    data: DataMapping,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> DataDict:
    """
    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}

    Returns
    -------
    MutableMapping[str, MutableSequence]
    """
    data = data_dict(data)
    backfill_columns_inplace(data, limit, na_value)
    return data


def backfill_column(
    column: Sequence,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> list:
    column = list(column)
    backfill_column_inplace(column, limit, na_value)
    return column


def backfill_rows_inplace(
    data: DataDict,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> None:
    """
    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}

    Returns
    -------
    None
    """
    for i, row in rows_functions.iterrows(data):
        new_row = backfill_row(row, limit, na_value)
        edit_functions.edit_row_items_inplace(data, i, new_row)


def forwardfill_columns_inplace(
    data: DataDict,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> None:
    """
    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}

    Returns
    -------
    None
    """
    for col in data:
        forwardfill_column_inplace(data[col], limit, na_value)


def forwardfill_columns(
    data: DataMapping,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> DataDict:
    """
    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}

    Returns
    -------
    MutableMapping[str, MutableSequence]
    """
    data = data_dict(data)
    forwardfill_columns_inplace(data, limit, na_value)
    return data


def forwardfill_rows_inplace(
    data: DataDict,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> None:
    """
    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}

    Returns
    -------
    None
    """
    for i, row in rows_functions.iterrows(data):
        new_row = forwardfill_row(row, limit, na_value)
        edit_functions.edit_row_items_inplace(data, i, new_row)


def forwardfill_rows(
    data: DataMapping,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> DataDict:
    """
    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}

    Returns
    -------
    MutableMapping[str, MutableSequence]
    """
    data = data_dict(data)
    forwardfill_rows_inplace(data, limit, na_value)
    return data


class Continue(Exception):
    pass


def _get_fill_value(value, column):
    if has_mapping_attrs(value):
        if column not in value:
            raise Continue()
        return value[column]
    else:
        return value


def fill_column_with_value(
    column: Sequence,
    value: Optional[Any] = None,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> list:
    """
    Fill missing values in column with given value.

    Parameters
    ----------
    column : MutableSequence
        column of values
    value : Any
        value to use to fill missing values
    limit : int, default None
        max number of values to fill, fill all if None
    na_value : Any, default None
        value to replace, use np.nan for pandas DataFrame
    
    Returns
    -------
    MutableSequence

    Examples
    --------
    >>> col = [1, None, 3, None, 5]
    >>> fill_column_with_value(col, 0)
    [1, 0, 3, 0, 5]
    >>> col
    [1, None, 3, None, 5]
    """
    column = list(column)
    fill_column_with_value_inplace(column, value, limit, na_value)
    return column


def fill_column_with_value_inplace(
    column: list,
    value: Optional[Any] = None,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> None:
    """
    Fill missing values in column with given value.

    Parameters
    ----------
    column : MutableSequence
        column of values
    value : Any
        value to use to fill missing values
    inplace : bool, default False
        return MutableSequence if False,
        return None if True and change column inplace
    limit : int, default None
        max number of values to fill, fill all if None
    na_value : Any, default None
        value to replace, use np.nan for pandas DataFrame
    
    Returns
    -------
    MutableSequence | None

    Example
    -------
    >>> col = [1, None, 3, None, 5]
    >>> fill_column_with_value_inplace(col, 0)
    >>> col
    [1, 0, 3, 0, 5]
    """
    fill_count = 0
    for i, item in enumerate(column):
        if limit is not None:
            if fill_count >= limit:
                return
        if item == na_value:
            column[i] = value
            fill_count += 1


def fill_row_with_value(
    row: RowMapping,
    value: Optional[Any] = None,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> RowDict:
    """
    Fill missing values in row with given value.

    Parameters
    ----------
    row : MutableMapping[str, Any]
        row of values: {column_name: row_value}
    value : Any
        value to use to fill missing values
    inplace : bool, default False
        return MutableMapping if False,
        return None if True and change row inplace
    limit : int, default None
        max number of values to fill, fill all if None
    na_value : Any, default None
        value to replace, use np.nan for pandas DataFrame
    
    Returns
    -------
    MutableMapping | None

    Examples
    --------
    >>> row = {'a': 1, 'b': None, 'c': 3, 'd': None, 'e': 5}
    >>> fill_row_with_value(row, 0)
    {'a': 1, 'b': 0, 'c': 3, 'd': 0, 'e': 5}
    >>> row
    {'a': 1, 'b': None, 'c': 3, 'd': None, 'e': 5}
    """
    row = row_dict(row)
    fill_row_with_value_inplace(row, value, limit, na_value)
    return row


def fill_row_with_value_inplace(
    row: RowDict,
    value: Any,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> None:
    """
    Fill missing values in row with given value.

    Parameters
    ----------
    row : MutableMapping[str, MutableSequence]
        row of values: {column_name: row_value}
    value : Any
        value to use to fill missing values
    limit : int, default None
        max number of values to fill, fill all if None
    na_value : Any, default None
        value to replace, use np.nan for pandas DataFrame
    
    Returns
    -------
    None

    Examples
    --------
    >>> row = {'a': 1, 'b': None, 'c': 3, 'd': None, 'e': 5}
    >>> fill_row_with_value_inplace(col, 0)
    >>> row
    {'a': 1, 'b': 0, 'c': 3, 'd': 0, 'e': 5}

    >>> row = {'a': 1, 'b': None, 'c': 3, 'd': None, 'e': 5}
    >>> values = {'a': 11, 'b': 22, 'c': 33, 'd': 44, 'e': 55}
    >>> fill_row_with_value_inplace(col, values)
    >>> row
    {'a': 1, 'b': 22, 'c': 3, 'd': 44, 'e': 5}
    """
    fill_count = 0
    for key, item in row.items():
        if limit is not None:
            if fill_count >= limit:
                return
        if item == na_value:
            try:
                fill_value = _get_fill_value(value, key)
            except Continue:
                continue
            row[key] = fill_value
            fill_count += 1


def backfill_column_inplace(
    column: list,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> None:
    fill_count = 0
    for i, item in reversed(list(enumerate(column))):
        if limit is not None:
            if fill_count >= limit:
                return
        if item == na_value:
            b = _back(column, i, na_value)
            if b == na_value:
                continue
            column[i] = b
            fill_count += 1


def _back(values: Sequence, index: int, na_value=None) -> Any:
    """Return the next value after index."""
    if index >= len(values) - 1:
        return na_value
    return values[index + 1]


def backfill_rows(
    data: DataMapping,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> DataDict:
    """
    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}

    Returns
    -------
    MutableMapping[str, MutableSequence]
    """
    data = data_dict(data)
    backfill_rows_inplace(data, limit, na_value)
    return data


def backfill_row_inplace(
    row: RowDict,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> None:
    fill_count = 0
    for i, (key, item) in reversed(list(enumerate(row.items()))):
        if limit is not None:
            if fill_count >= limit:
                return
        if item == na_value:
            b = _back(list(row.values()), i, na_value)
            if b == na_value:
                continue
            row[key] = b
            fill_count += 1


def backfill_row(
    row: RowMapping,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> RowDict:
    row = row_dict(row)
    backfill_row_inplace(row, limit, na_value)
    return row


def forwardfill_column_inplace(
    column: list,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> None:
    fill_count = 0
    for i, item in enumerate(column):
        if limit is not None:
            if fill_count >= limit:
                return
        if item == na_value:
            f = _forward(column, i, na_value)
            if f == na_value:
                continue
            column[i] = f
            fill_count += 1


def forwardfill_column(
    column: Sequence,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> list:
    column = list(column)
    forwardfill_column_inplace(column, limit, na_value)
    return column


def _forward(values: Sequence, index: int, na_value=None) -> Any:
    """Return the previoud value before index."""
    if index < 1:
        return na_value
    return values[index - 1]


def forwardfill_row_inplace(
    row: RowDict,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> None:
    fill_count = 0
    for i, (key, value) in enumerate(row.items()):
        if limit is not None:
            if fill_count >= limit:
                return
        if value == na_value:
            f = _forward(list(row.values()), i, na_value)
            if f == na_value:
                continue
            row[key] = f
            fill_count += 1


def forwardfill_row(
    row: RowMapping,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> RowDict:
    row = row_dict(row)
    forwardfill_row_inplace(row, limit, na_value)
    return row


def fill_columns_with_value(
    data: DataMapping,
    value: Any,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> DataDict:
    """
    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}

    Returns
    -------
    MutableMapping[str, MutableSequence]
    """
    data = data_dict(data)
    fill_columns_with_value_inplace(data, value, limit, na_value)
    return data


def fill_rows_with_value(
    data: DataMapping,
    value: Any,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> DataDict:
    """
    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}

    Returns
    -------
    MutableMapping[str, MutableSequence]
    """
    data = data_dict(data)
    fill_rows_with_value_inplace(data, value, limit, na_value)
    return data