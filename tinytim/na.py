from copy import copy, deepcopy
from lib2to3.pgen2.token import OP
from telnetlib import SE
from typing import Any, Mapping, MutableMapping, MutableSequence, Optional, Sequence, Union

from pandas import value_counts

import tinytim.data as data_features
from hasattrs import has_mapping_attrs
from tinytim.edit import drop_row_inplace, edit_row_items_inplace, drop_column_inplace

from tinytim.rows import iterrows

MutableDataMapping = MutableMapping[str, MutableSequence]
MutableRowMapping = MutableMapping[str, Any]


def fillna(
    data: MutableDataMapping,
    value: Optional[Any] = None,
    method: Optional[str] = None,
    axis: Optional[Union[int, str]] = 0,
    inplace: bool = False,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> Union[MutableDataMapping, None]:
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


def isnull(data: MutableDataMapping, na_value=None) -> MutableDataMapping:
    data = deepcopy(data)
    isnull_inplace(data, na_value)
    return data


def notnull(data: MutableDataMapping, na_value=None) -> MutableDataMapping:
    data = deepcopy(data)
    notnull_inplace(data, na_value)
    return data

isna = isnull
notna = notnull


def dropna(
    data: MutableDataMapping,
    axis: Union[int, str] = 0,
    how: str = 'any',
    thresh: Optional[int] = None,
    subset: Optional[Sequence[str]] = None,
    inplace: bool = False,
    na_value: Optional[Any] = None
) -> Union[MutableDataMapping, None]:
    """
    Remove missing values.

    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}
    axis : int | str
        {0 or 'rows', 1 or 'columns'}
    how : str
        {'any', 'all'}
    thresh : int, optional
        Require that many not missing values. Cannot be combined with how.
    subset : Sequence[str]
        column names to consider when checking for row values
    inplace : bool, default False
        Whether to modify the original data rather than returning new data.

    Returns
    -------
    MutableDataMapping | None
        Object with missing values removed or None if inplace=True
    """
    if thresh is not None:
        if inplace:
            dropna_thresh_inplace(data, thresh, axis, subset, na_value)
        else:
            return dropna_thresh(data, thresh, axis, subset, na_value)
    elif how == 'any':
        if inplace:
            dropna_any_inplace(data, axis, subset, na_value)
        else:
            return dropna_any(data, axis, subset, na_value)
    elif how == 'all':
        if inplace:
            dropna_all_inplace(data, axis, subset, na_value)
        else:
            return dropna_all(data, axis, subset, na_value)

# ------------------------------------------------------------------------------------------ #
# ----------------------------Dropna Functions---------------------------------------------- #
# ------------------------------------------------------------------------------------------ #

def dropna_any_inplace(
    data: MutableDataMapping,
    axis: Union[int, str] = 0,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> None:
    if axis in [1, 'columns']:
        dropna_columns_any_inplace(data, subset, na_value)
    elif axis in [0, 'rows']:
        dropna_rows_any_inplace(data, subset, na_value)


def dropna_any(
    data: MutableDataMapping,
    axis: Union[int, str] = 0,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> MutableDataMapping:
    data = deepcopy(data)
    dropna_any_inplace(data, axis, subset, na_value)
    return data


def dropna_thresh_inplace(
    data: MutableDataMapping,
    thresh: int,
    axis: Union[int, str] = 0,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> None:
    if axis in [1, 'columns']:
        dropna_columns_thresh_inplace(data, thresh, subset, na_value)
    elif axis in [0, 'rows']:
        dropna_rows_thresh_inplace(data, thresh, subset, na_value)


def dropna_thresh(
    data: MutableDataMapping,
    thresh: int,
    axis: Union[int, str] = 0,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> MutableDataMapping:
    data = deepcopy(data)
    dropna_thresh_inplace(data, thresh, axis, subset, na_value)
    return data


def dropna_columns_any_inplace(
    data: MutableDataMapping,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> None:
    for col in data_features.column_names(data):
        if subset is not None and col not in subset:
            continue
        dropna_column_any_inplace(data, col, na_value)


def dropna_column_any_inplace(
    data: MutableDataMapping,
    column_name: str,
    na_value: Optional[Any] = None
) -> None:
    if column_any_na(data[column_name], na_value):
        drop_column_inplace(data, column_name)


def dropna_column_any(
    data: MutableDataMapping,
    column_name: str,
    na_value: Optional[Any] = None
) -> MutableDataMapping:
    data = deepcopy(data)
    dropna_column_any_inplace(data, column_name, na_value)
    return data


def dropna_columns_any(
    data: MutableDataMapping,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> MutableDataMapping:
    data = deepcopy(data)
    dropna_columns_any_inplace(data, subset, na_value)
    return data


def dropna_rows_any_inplace(
    data: MutableDataMapping,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> None:
    for i, row in iterrows(data, reverse=True):
        if row_any_na(row, subset, na_value):
            drop_row_inplace(data, i)


def dropna_rows_any(
    data: MutableDataMapping,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> MutableDataMapping:
    data = deepcopy(data)
    dropna_rows_any_inplace(data, subset, na_value)
    return data


def column_any_na(
    column: Sequence,
    na_value: Optional[Any] = None
) -> bool:
    return any(val == na_value for val in column)


def subset_row_values(
    row: Mapping[str, Any],
    subset: Optional[Sequence[str]] = None
) -> list:
    return list(row.values()) if subset is None else [val for key, val in row.items() if key in subset]


def row_any_na(
    row: MutableRowMapping,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> bool:
    values = subset_row_values(row, subset)
    return any(val == na_value for val in values)


def column_all_na(
    column: Sequence,
    na_value: Optional[Any] = None
) -> bool:
    return all(val == na_value for val in column)


def row_all_na(
    row: MutableRowMapping,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> bool:
    values = subset_row_values(row, subset)
    return all(val == na_value for val in values)


def dropna_all_inplace(
    data: MutableDataMapping,
    axis: Union[int, str] = 0,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> None:
    if axis == 1:
        dropna_columns_all_inplace(data, subset, na_value)
    elif axis == 0:
        dropna_rows_all_inplace(data, subset, na_value)


def dropna_all(
    data: MutableDataMapping,
    axis: Union[int, str] = 0,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> MutableDataMapping:
    data = deepcopy(data)
    dropna_all_inplace(data, axis, subset, na_value)
    return data


def dropna_columns_all_inplace(
    data: MutableDataMapping,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> None:
    for col in data_features.column_names(data):
        if subset is not None and col not in subset:
            continue
        if column_all_na(data[col], na_value):
            drop_column_inplace(data, col)


def dropna_columns_all(
    data: MutableDataMapping,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> MutableDataMapping:
    data = deepcopy(data)
    dropna_columns_all_inplace(data, subset, na_value)
    return data


def dropna_rows_all_inplace(
    data: MutableDataMapping,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> None:
    for i, row in iterrows(data, reverse=True):
        if row_all_na(row, subset, na_value):
            drop_row_inplace(data, i)


def dropna_rows_all(
    data: MutableDataMapping,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> MutableDataMapping:
    data = deepcopy(data)
    dropna_rows_all_inplace(data, subset, na_value)
    return data


def dropna_columns_thresh_inplace(
    data: MutableDataMapping,
    thresh: int,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> None:
    for col in data_features.column_names(data):
        if subset is not None and col not in subset:
            continue
        dropna_column_thresh_inplace(data, col, thresh, na_value)


def dropna_column_thresh_inplace(
    data: MutableDataMapping,
    column_name: str,
    thresh: int,
    na_value: Optional[Any] = None
) -> None:
    if not column_na_thresh(data[column_name], thresh, na_value):
        drop_column_inplace(data, column_name)


def dropna_columns_thresh(
    data: MutableDataMapping,
    thresh: int,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> MutableDataMapping:
    data = deepcopy(data)
    dropna_columns_thresh_inplace(data, thresh, subset, na_value)
    return data


def dropna_rows_thresh_inplace(
    data: MutableDataMapping,
    thresh: int,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> None:
    for i, row in iterrows(data, reverse=True):
        if not row_na_thresh(row, thresh, subset, na_value):
            drop_row_inplace(data, i)


def dropna_rows_thresh(
    data: MutableDataMapping,
    thresh: int,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> MutableDataMapping:
    data = deepcopy(data)
    dropna_rows_thresh_inplace(data, thresh, subset, na_value)
    return data


def column_na_thresh(
    column: Sequence,
    thresh: int,
    na_value: Optional[Any] = None
) -> bool:
    return sum(val != na_value for val in column) >= thresh


def row_na_thresh(
    row: Mapping[str, Any],
    thresh: int,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] =None
) -> bool:
    items = row.values() if subset is None else [val for key, val in row.items() if key in subset]
    return sum(val != na_value for val in items) >= thresh

# ------------------------------------------------------------------------------------------ #
# ----------------------------Is/Not Null Functions----------------------------------------- #
# ------------------------------------------------------------------------------------------ #

def isnull_inplace(data: MutableDataMapping, na_value=None) -> None:
    for col in data_features.column_names(data):
        column_isnull_inplace(data[col], na_value)


def notnull_inplace(data: MutableDataMapping, na_value=None) -> None:
    for col in data_features.column_names(data):
        column_notnull_inplace(data[col], na_value)


def column_isnull(column: MutableSequence, na_value=None) -> MutableSequence:
    column = copy(column)
    column_isnull_inplace(column, na_value)
    return column


def column_notnull(column: MutableSequence, na_value=None) -> MutableSequence:
    column = copy(column)
    column_notnull_inplace(column, na_value)
    return column


def column_isnull_inplace(column: MutableSequence, na_value=None) -> None:
    for i, item in enumerate(column):
        column[i] =  item == na_value


def column_notnull_inplace(column: MutableSequence, na_value=None) -> None:
    for i, item in enumerate(column):
        column[i] =  item != na_value


def row_isnull(row: MutableRowMapping, na_value=None) -> MutableRowMapping:
    row = deepcopy(row)
    row_isnull_inplace(row, na_value)
    return row


def row_notnull(row: MutableRowMapping, na_value=None) -> MutableRowMapping:
    row = deepcopy(row)
    row_notnull_inplace(row, na_value)
    return row


def row_isnull_inplace(row: MutableRowMapping, na_value=None) -> None:
    for key, item in row.items():
        row[key] = item == na_value


def row_notnull_inplace(row: MutableRowMapping, na_value=None) -> None:
    for key, item in row.items():
        row[key] = item != na_value

# ------------------------------------------------------------------------------------------ #
# ----------------------------Backfill Functions-------------------------------------------- #
# ------------------------------------------------------------------------------------------ #

def backfill_inplace(
    data: MutableDataMapping,
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
    data: MutableDataMapping,
    axis: Optional[Union[int, str]] = 0,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> MutableDataMapping:
    """
    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}

    Returns
    -------
    MutableMapping[str, MutableSequence]
    """
    data = deepcopy(data)
    backfill_inplace(data, axis, limit, na_value)
    return data


def backfill_columns_inplace(
    data: MutableDataMapping,
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
    data: MutableDataMapping,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> MutableDataMapping:
    """
    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}

    Returns
    -------
    MutableMapping[str, MutableSequence]
    """
    data = deepcopy(data)
    backfill_columns_inplace(data, limit, na_value)
    return data


def _back(values: Sequence, index: int, na_value=None) -> Any:
    """Return the next value after index."""
    if index >= len(values) - 1:
        return na_value
    return values[index + 1]


def backfill_column_inplace(
    column: MutableSequence,
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


def backfill_column(
    column: MutableSequence,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> MutableSequence:
    column = copy(column)
    backfill_column_inplace(column, limit, na_value)
    return column


def backfill_rows_inplace(
    data: MutableDataMapping,
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
    for i, row in iterrows(data):
        new_row = backfill_row(row, limit, na_value)
        edit_row_items_inplace(data, i, new_row)


def backfill_rows(
    data: MutableDataMapping,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> MutableDataMapping:
    """
    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}

    Returns
    -------
    MutableMapping[str, MutableSequence]
    """
    data = deepcopy(data)
    backfill_rows_inplace(data, limit, na_value)
    return data


def backfill_row_inplace(
    row: MutableRowMapping,
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
    row: MutableRowMapping,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> MutableRowMapping:
    row = deepcopy(row)
    backfill_row_inplace(row, limit, na_value)
    return row

# ------------------------------------------------------------------------------------------ #
# ----------------------------Forwardfill Functions----------------------------------------- #
# ------------------------------------------------------------------------------------------ #

def forwardfill_inplace(
    data: MutableDataMapping,
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
    if axis in [0, 'row']:
        forwardfill_columns_inplace(data, limit, na_value)
    elif axis in [1, 'column']:
        forwardfill_rows_inplace(data, limit, na_value)


def forwardfill(
    data: MutableDataMapping,
    axis: Optional[Union[int, str]] = 0,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> MutableDataMapping:
    """
    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}

    Returns
    -------
    MutableMapping[str, MutableSequence]
    """
    data = deepcopy(data)
    forwardfill_inplace(data, axis, limit, na_value)
    return data


def forwardfill_columns_inplace(
    data: MutableDataMapping,
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
    data: MutableDataMapping,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> MutableDataMapping:
    """
    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}

    Returns
    -------
    MutableMapping[str, MutableSequence]
    """
    data = deepcopy(data)
    forwardfill_columns_inplace(data, limit, na_value)
    return data


def _forward(values: Sequence, index: int, na_value=None) -> Any:
    """Return the previoud value before index."""
    if index < 1:
        return na_value
    return values[index - 1]


def forwardfill_column_inplace(
    column: MutableSequence,
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
    column: MutableSequence,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> MutableSequence:
    column = copy(column)
    forwardfill_column_inplace(column, limit, na_value)
    return column


def forwardfill_rows_inplace(
    data: MutableDataMapping,
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
    for i, row in iterrows(data):
        new_row = forwardfill_row(row, limit, na_value)
        edit_row_items_inplace(data, i, new_row)


def forwardfill_rows(
    data: MutableDataMapping,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> MutableDataMapping:
    """
    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}

    Returns
    -------
    MutableMapping[str, MutableSequence]
    """
    data = deepcopy(data)
    forwardfill_rows_inplace(data, limit, na_value)
    return data


def forwardfill_row_inplace(
    row: MutableRowMapping,
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
    row: MutableRowMapping,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> MutableRowMapping:
    row = deepcopy(row)
    forwardfill_row_inplace(row, limit, na_value)
    return row



# ------------------------------------------------------------------------------------------ #
# ----------------------------Fill With Value Functions------------------------------------- #
# ------------------------------------------------------------------------------------------ #

def fill_with_value(
    data: MutableDataMapping,
    value: Any,
    axis: Optional[Union[int, str]] = 0,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> MutableDataMapping:
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
    data = deepcopy(data)
    fill_with_value_inplace(data, value, axis, limit, na_value)
    return data


def fill_with_value_inplace(
    data: MutableDataMapping,
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
    if axis in [0, 'row']:
        fill_columns_with_value_inplace(data, value, limit, na_value)
    elif axis in [1, 'column']:
        fill_rows_with_value_inplace(data, value, limit, na_value)


def fill_columns_with_value(
    data: MutableDataMapping,
    value: Any,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> MutableDataMapping:
    """
    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}

    Returns
    -------
    MutableMapping[str, MutableSequence]
    """
    data = deepcopy(data)
    fill_columns_with_value_inplace(data, value, limit, na_value)
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


def fill_columns_with_value_inplace(
    data: MutableDataMapping,
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
    columns = data_features.column_names(data)
    for col in columns:
        try:
            fill_value = _get_fill_value(value, col)
        except Continue:
            continue
        fill_column_with_value_inplace(data[col], fill_value, limit, na_value)


def fill_rows_with_value(
    data: MutableDataMapping,
    value: Any,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> MutableDataMapping:
    """
    Parameters
    ----------
    data : MutableMapping[str, MutableSequence]
        data mapping of {column name: column values}

    Returns
    -------
    MutableMapping[str, MutableSequence]
    """
    data = deepcopy(data)
    fill_rows_with_value_inplace(data, value, limit, na_value)
    return data


def fill_rows_with_value_inplace(
    data: MutableDataMapping,
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
    for i, row in iterrows(data):
        new_row = fill_row_with_value(row, value, limit, na_value)
        edit_row_items_inplace(data, i, new_row)


def fill_column_with_value(
    column: MutableSequence,
    value: Optional[Any] = None,
    limit: Optional[int] = None,
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
    column = copy(column)
    fill_column_with_value_inplace(column, value, limit, na_value)
    return column


def fill_column_with_value_inplace(
    column: MutableSequence,
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
    row: MutableRowMapping,
    value: Optional[Any] = None,
    limit: Optional[int] = None,
    na_value: Optional[Any] = None
) -> MutableRowMapping:
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
    row = deepcopy(row)
    fill_row_with_value_inplace(row, value, limit, na_value)
    return row


def fill_row_with_value_inplace(
    row: MutableRowMapping,
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