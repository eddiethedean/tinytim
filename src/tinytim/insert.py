from typing import Any, Dict, Iterable, Mapping, Sequence
import tinytim.data as data_features

DataMapping = Mapping[str, Sequence]
DataDict = Dict[str, list]
RowMapping = Mapping[str, Any]


def data_dict(data) -> DataDict:
    return {col: list(values) for col, values in data.items()}


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
            value = missing_value if column not in row else row[column]
            data[column].append(value)