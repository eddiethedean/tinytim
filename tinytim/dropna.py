from typing import Any, Optional, Sequence, Union

import tinytim.data as data_features
from tinytim.edit import drop_row_inplace, drop_column_inplace
from tinytim.rows import iterrows
from tinytim.types import DataMapping, DataDict, RowMapping, data_dict


def dropna(
    data: DataDict,
    axis: Union[int, str] = 0,
    how: str = 'any',
    thresh: Optional[int] = None,
    subset: Optional[Sequence[str]] = None,
    inplace: bool = False,
    na_value: Optional[Any] = None
) -> Union[DataDict, None]:
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


def dropna_any_inplace(
    data: DataDict,
    axis: Union[int, str] = 0,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> None:
    if axis in [1, 'columns']:
        dropna_columns_any_inplace(data, subset, na_value)
    elif axis in [0, 'rows']:
        dropna_rows_any_inplace(data, subset, na_value)


def dropna_any(
    data: DataMapping,
    axis: Union[int, str] = 0,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> DataDict:
    data = data_dict(data)
    dropna_any_inplace(data, axis, subset, na_value)
    return data


def dropna_thresh_inplace(
    data: DataDict,
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
    data: DataMapping,
    thresh: int,
    axis: Union[int, str] = 0,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> DataDict:
    data = data_dict(data)
    dropna_thresh_inplace(data, thresh, axis, subset, na_value)
    return data


def dropna_columns_any_inplace(
    data: DataDict,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> None:
    for col in data_features.column_names(data):
        if subset is not None and col not in subset:
            continue
        dropna_column_any_inplace(data, col, na_value)


def dropna_column_any_inplace(
    data: DataDict,
    column_name: str,
    na_value: Optional[Any] = None
) -> None:
    if column_any_na(data[column_name], na_value):
        drop_column_inplace(data, column_name)


def dropna_column_any(
    data: DataMapping,
    column_name: str,
    na_value: Optional[Any] = None
) -> DataDict:
    data = data_dict(data)
    dropna_column_any_inplace(data, column_name, na_value)
    return data


def dropna_columns_any(
    data: DataMapping,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> DataDict:
    data = data_dict(data)
    dropna_columns_any_inplace(data, subset, na_value)
    return data


def dropna_rows_any_inplace(
    data: DataDict,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> None:
    for i, row in iterrows(data, reverse=True):
        if row_any_na(row, subset, na_value):
            drop_row_inplace(data, i)


def dropna_rows_any(
    data: DataMapping,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> DataDict:
    data = data_dict(data)
    dropna_rows_any_inplace(data, subset, na_value)
    return data


def column_any_na(
    column: Sequence,
    na_value: Optional[Any] = None
) -> bool:
    return any(val == na_value for val in column)


def subset_row_values(
    row: RowMapping,
    subset: Optional[Sequence[str]] = None
) -> list:
    return list(row.values()) if subset is None else [val for key, val in row.items() if key in subset]


def row_any_na(
    row: DataMapping,
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
    row: DataMapping,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> bool:
    values = subset_row_values(row, subset)
    return all(val == na_value for val in values)


def dropna_all_inplace(
    data: DataDict,
    axis: Union[int, str] = 0,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> None:
    if axis == 1:
        dropna_columns_all_inplace(data, subset, na_value)
    elif axis == 0:
        dropna_rows_all_inplace(data, subset, na_value)


def dropna_all(
    data: DataMapping,
    axis: Union[int, str] = 0,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> DataDict:
    data = data_dict(data)
    dropna_all_inplace(data, axis, subset, na_value)
    return data


def dropna_columns_all_inplace(
    data: DataDict,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> None:
    for col in data_features.column_names(data):
        if subset is not None and col not in subset:
            continue
        if column_all_na(data[col], na_value):
            drop_column_inplace(data, col)


def dropna_columns_all(
    data: DataMapping,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> DataDict:
    data = data_dict(data)
    dropna_columns_all_inplace(data, subset, na_value)
    return data


def dropna_rows_all_inplace(
    data: DataDict,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> None:
    for i, row in iterrows(data, reverse=True):
        if row_all_na(row, subset, na_value):
            drop_row_inplace(data, i)


def dropna_rows_all(
    data: DataMapping,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> DataDict:
    data = data_dict(data)
    dropna_rows_all_inplace(data, subset, na_value)
    return data


def dropna_columns_thresh_inplace(
    data: DataDict,
    thresh: int,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> None:
    for col in data_features.column_names(data):
        if subset is not None and col not in subset:
            continue
        dropna_column_thresh_inplace(data, col, thresh, na_value)


def dropna_column_thresh_inplace(
    data: DataDict,
    column_name: str,
    thresh: int,
    na_value: Optional[Any] = None
) -> None:
    if not column_na_thresh(data[column_name], thresh, na_value):
        drop_column_inplace(data, column_name)


def dropna_columns_thresh(
    data: DataMapping,
    thresh: int,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> DataDict:
    data = data_dict(data)
    dropna_columns_thresh_inplace(data, thresh, subset, na_value)
    return data


def dropna_rows_thresh_inplace(
    data: DataDict,
    thresh: int,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> None:
    for i, row in iterrows(data, reverse=True):
        if not row_na_thresh(row, thresh, subset, na_value):
            drop_row_inplace(data, i)


def dropna_rows_thresh(
    data: DataMapping,
    thresh: int,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] = None
) -> DataDict:
    data = data_dict(data)
    dropna_rows_thresh_inplace(data, thresh, subset, na_value)
    return data


def column_na_thresh(
    column: Sequence,
    thresh: int,
    na_value: Optional[Any] = None
) -> bool:
    return sum(val != na_value for val in column) >= thresh


def row_na_thresh(
    row: RowMapping,
    thresh: int,
    subset: Optional[Sequence[str]] = None,
    na_value: Optional[Any] =None
) -> bool:
    items = row.values() if subset is None else [val for key, val in row.items() if key in subset]
    return sum(val != na_value for val in items) >= thresh

