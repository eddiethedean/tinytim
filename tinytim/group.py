from collections import namedtuple
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple, Union

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


def _keys(key, by) -> dict:
    keys = {}
    if isinstance(by, str):
        keys[by] = key
    else:
        for col, k in zip(by, key):
            keys[col] = k
    return keys


def aggregate_groups(
    groups: Sequence[Tuple[Any, DataMapping]],
    by: Sequence[str],
    func: Callable[[DataMapping], RowMapping],
    tuplename: Optional[str] = 'GroupbyKey'
) -> Tuple[List, DataDict]:
    labels = []
    rows = []
    for key, data in groups:
        row = func(data)
        if len(row):
            GroupbyKey = namedtuple(field_names=by, typename=tuplename)
            keys = _keys(key, by)
            labels.append(GroupbyKey(*keys.values()))
            rows.append(row)
    return labels, row_dicts_to_data(rows)


def sum_groups(
    groups: List[tuple],
    by: Sequence[str]
) -> Tuple[List, DataDict]:
    return aggregate_groups(groups, by, sum_data, 'Sums')


def count_groups(
    groups: List[tuple],
    by: Sequence[str]
) -> Tuple[List, DataDict]:
    return aggregate_groups(groups, by, count_data, 'Counts')


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