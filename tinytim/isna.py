from typing import Sequence

import tinytim.data as data_features
from tinytim.types import DataDict, DataMapping, data_dict, RowDict, RowMapping, row_dict


def isnull(data: DataMapping, na_value=None) -> DataDict:
    data = data_dict(data)
    isnull_inplace(data, na_value)
    return data


def notnull(data: DataMapping, na_value=None) -> DataDict:
    data = data_dict(data)
    notnull_inplace(data, na_value)
    return data


isna = isnull
notna = notnull


def isnull_inplace(data: DataDict, na_value=None) -> None:
    for col in data_features.column_names(data):
        column_isnull_inplace(data[col], na_value)


def notnull_inplace(data: DataDict, na_value=None) -> None:
    for col in data_features.column_names(data):
        column_notnull_inplace(data[col], na_value)


def column_isnull(column: Sequence, na_value=None) -> list:
    column = list(column)
    column_isnull_inplace(column, na_value)
    return column


def column_notnull(column: Sequence, na_value=None) -> list:
    column = list(column)
    column_notnull_inplace(column, na_value)
    return column


def column_isnull_inplace(column: list, na_value=None) -> None:
    for i, item in enumerate(column):
        column[i] =  item == na_value


def column_notnull_inplace(column: list, na_value=None) -> None:
    for i, item in enumerate(column):
        column[i] =  item != na_value


def row_isnull(row: RowMapping, na_value=None) -> RowDict:
    row = row_dict(row)
    row_isnull_inplace(row, na_value)
    return row


def row_notnull(row: DataMapping, na_value=None) -> RowDict:
    row = row_dict(row)
    row_notnull_inplace(row, na_value)
    return row


def row_isnull_inplace(row: RowDict, na_value=None) -> None:
    for key, item in row.items():
        row[key] = item == na_value


def row_notnull_inplace(row: RowDict, na_value=None) -> None:
    for key, item in row.items():
        row[key] = item != na_value