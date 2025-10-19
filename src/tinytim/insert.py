from typing import Iterable

import tinytim.data as data_features
from tinytim.custom_types import DataDict, DataMapping, RowMapping, data_dict


def insert_row(
    data: DataMapping,
    row: RowMapping
) -> DataDict:
    data = data_dict(data)
    insert_row_inplace(data, row)
    return data


def insert_rows(
    data: DataMapping,
    rows: Iterable[RowMapping]
) -> DataDict:
    data = data_dict(data)
    insert_rows_inplace(data, rows)
    return data


def insert_row_inplace(
    data: DataDict,
    row: RowMapping
) -> None:
    insert_rows_inplace(data, [row])


def insert_rows_inplace(
    data: DataDict,
    rows: Iterable[RowMapping],
    missing_value=None
) -> None:
    column_names = data_features.column_names(data)
    for row in rows:
        for column in column_names:
            value = row.get(column, missing_value)
            data[column].append(value)
