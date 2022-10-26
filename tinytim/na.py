from copy import copy, deepcopy
from typing import Any, Mapping, MutableMapping, MutableSequence, Optional, Union

import tinytim.data as data_features
from hasattrs import has_mapping_attrs
from tinytim.edit import edit_row_items_inplace

from tinytim.rows import iterrows, row_dict


def fillna(
    data: Mapping,
    value: Optional[Any] = None,
    method: Optional[str] = None,
    axis: Optional[int] = None,
    inplace: bool = False,
    limit: Optional[int] = None,
    downcast: Optional[dict] = None,
    na_value: Optional[Any] = None
) -> Union[Mapping, None]:
    """
    Fill missing values using the specified method.

    Parameters
    ----------
    data : Mapping[str, Sequence]
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
    ...


def fill_with_value(
    data: MutableMapping,
    value: Any,
    axis: Optional[Union[int, str]] = 1,
    inplace: bool = False,
    limit: Optional[int] = None,
    downcast: Optional[dict] = None,
    na_value: Optional[Any] = None
) -> Union[Mapping, None]:
    """
    Fill data columns with given value.

    Parameters
    ----------
    data : Mapping[str, Sequence]
        data mapping of {column name: column values}
    value : Any
        value to use to fill missing values
        If value is Mapping: {column_name: value},
        fill missing values in each column with each value.
    """
    if not inplace:
        data = deepcopy(data)

    if axis in [1, 'column']:
        columns = data_features.column_names(data)
        for col in columns:
            if has_mapping_attrs(value):
                fill_value = value[col]
            else:
                fill_value = value
            fill_column_with_value_inplace(data[col], fill_value)
    elif axis in [0, 'row']:
        for i, row in iterrows(data):
            new_row = fill_row_with_value(row, value)
            edit_row_items_inplace(data, i, new_row)

    if not inplace:
        return data


def fill_with_value_inplace(
    data: MutableMapping,
    value: Any,
    axis: Optional[Union[int, str]] = 1,
    limit: Optional[int] = None,
    downcast: Optional[dict] = None,
    na_value: Optional[Any] = None
) -> None:
    """
    Fill data columns with given value.

    Parameters
    ----------
    data : Mapping[str, Sequence]
        data mapping of {column name: column values}
    value : Any
        value to use to fill missing values
        If value is Mapping: {column_name: value},
        fill missing values in each column with each value.
    """
    if axis in [1, 'column']:
        columns = data_features.column_names(data)
        for col in columns:
            if has_mapping_attrs(value):
                if col not in value:
                    continue
                fill_value = value[col]
            else:
                fill_value = value
            fill_column_with_value_inplace(data[col], fill_value)
    elif axis in [0, 'row']:
        for i, row in iterrows(data):
            new_row = fill_row_with_value(row, value)
            edit_row_items_inplace(data, i, new_row)


def fill_column_with_value(
    column: MutableSequence,
    value: Optional[Any] = None,
    limit: Optional[int] = None,
    downcast: Optional[dict] = None,
    na_value: Optional[Any] = None
) -> MutableSequence:
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

    Examples
    --------
    >>> col = [1, None, 3, None, 5]
    >>> fill_column_with_value(col, 0)
    [1, 0, 3, 0, 5]
    >>> col
    [1, None, 3, None, 5]
    """
    column = copy(column)
    fill_column_with_value_inplace(column, value, limit, downcast, na_value)
    return column


def fill_column_with_value_inplace(
    column: MutableSequence,
    value: Optional[Any] = None,
    limit: Optional[int] = None,
    downcast: Optional[dict] = None,
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
    for i, value in enumerate(column):
        if limit is not None:
            if fill_count >= limit:
                return
        if value == na_value:
            column[i] = value
            fill_count += 1
            


def fill_row_with_value(
    row: MutableMapping[str, Any],
    value: Optional[Any] = None,
    limit: Optional[int] = None,
    downcast: Optional[dict] = None,
    na_value: Optional[Any] = None
) -> MutableMapping[str, Any]:
    """
    Fill missing values in row with given value.

    Parameters
    ----------
    row : MutableMapping
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
    >>> fill_row_with_value(col, 0)
    {'a': 1, 'b': 0, 'c': 3, 'd': 0, 'e': 5}
    >>> col
    row = {'a': 1, 'b': None, 'c': 3, 'd': None, 'e': 5}

    >>> row = {'a': 1, 'b': None, 'c': 3, 'd': None, 'e': 5}
    >>> fill_row_with_value(col, 0, inplace=True)
    >>> col
    {'a': 1, 'b': 0, 'c': 3, 'd': 0, 'e': 5}
    """
    return row


def fill_row_with_value_inplace(
    row: MutableMapping[str, Any],
    value: Any,
    limit: Optional[int] = None,
    downcast: Optional[dict] = None,
    na_value: Optional[Any] = None
) -> None:
    """
    Fill missing values in row with given value.

    Parameters
    ----------
    row : MutableMapping
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
    >>> col
    {'a': 1, 'b': 0, 'c': 3, 'd': 0, 'e': 5}

    >>> row = {'a': 1, 'b': None, 'c': 3, 'd': None, 'e': 5}
    >>> values = {'a': 11, 'b': 22, 'c': 33, 'd': 44, 'e': 55}
    >>> fill_row_with_value_inplace(col, values)
    >>> col
    {'a': 1, 'b': 22, 'c': 3, 'd': 44, 'e': 5}
    """
    fill_count = 0
    for key, item in row.items():
        if limit is not None:
            if fill_count >= limit:
                return
        if item == na_value:
            if has_mapping_attrs(value):
                if key not in value:
                    continue
                fill_value = value[key]
            else:
                fill_value = value
            row[key] = fill_value