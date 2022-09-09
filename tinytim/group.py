from typing import Any, Callable, Dict, List, Mapping, Sequence, Tuple, Union

from tinytim.filter import column_filter, filter_data
from tinytim.utils import row_dicts_to_data, row_value_tuples, uniques

DataMapping = Mapping[str, Sequence]
DataDict = Dict[str, list]
RowMapping = Mapping[str, Any]
RowDict = Dict[str, Any]
RowNumDict = Dict[str, Union[int, float]]


def groupbycolumn(data: Mapping, column: Sequence) -> List[tuple]:
    keys = uniques(column)
    return [(k, filter_data(data, column_filter(column, lambda x: x == k)))
                for k in keys]


def groupbyone(data: Mapping, column_name: str) -> List[tuple]:
    return groupbycolumn(data, data[column_name])


def groupbymulti(data: Mapping, column_names: Sequence[str]) -> List[tuple]:
    return groupbycolumn(data, row_value_tuples(data, column_names))


def groupby(data: Mapping, by: Union[str, Sequence[str]]) -> List[tuple]:
    if isinstance(by, str):
        return groupbyone(data, by)
    else:
        return groupbymulti(data, by)


def aggregate_groups(
    groups: Sequence[Tuple[Any, DataMapping]],
    func: Callable[[DataMapping], RowMapping]
) -> Tuple[List, DataDict]:
    labels = []
    rows = []
    for key, data in groups:
        row = func(data)
        if len(row):
            labels.append(key)
            rows.append(row)
    return labels, row_dicts_to_data(rows)


def sum_groups(groups: List[tuple]) -> Tuple[List, DataDict]:
    return aggregate_groups(groups, sum_data)


def count_groups(groups: List[tuple]) -> Tuple[List, DataDict]:
    return aggregate_groups(groups, count_data)


def aggregate_data(data: Mapping, func: Callable) -> RowDict:
    out = {}
    for column_name in data.keys():
        try:
            col_sum = func(data[column_name])
        except TypeError:
            continue
        out[column_name] = col_sum
    return out


def sum_data(data: Mapping) -> RowNumDict:
    return aggregate_data(data, sum)


def count_data(data: Mapping) -> RowNumDict:
    return aggregate_data(data, len)