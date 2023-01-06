from copy import copy, deepcopy
from typing import Any, MutableMapping, MutableSequence

import tinytim.data as data_features


MutableDataMapping = MutableMapping[str, MutableSequence]
MutableRowMapping = MutableMapping[str, Any]


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