from collections import namedtuple
from typing import Callable, Collection, Iterable, List, MutableMapping, Union

from tinytim.functional.filter import column_filter, filter_data
from tinytim.functional.utils import row_dicts_to_data, uniques


TableFilter = Iterable[bool]


def groupbycolumn(data: MutableMapping, column: Collection) -> List[tuple]:
    keys = uniques(column)
    return [(k, filter_data(data, column_filter(column, lambda x: x == k)))
                for k in keys]


def groupbyone(data: MutableMapping, column_name: str) -> List[tuple]:
    return groupbycolumn(data, data[column_name])


def row_value_tuples(data: MutableMapping, column_names: Collection[str]) -> List[tuple]:
    return list(zip(*[data[col] for col in column_names]))


def groupbymulti(data: MutableMapping, column_names: Collection[str]) -> List[tuple]:
    return groupbycolumn(data, row_value_tuples(data, column_names))


def groupby(data: MutableMapping, by: Union[str, Collection[str]]) -> List[tuple]:
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


def aggregate_groups(groups: List[tuple], by: Collection[str], func: Callable, tuplename: str) -> tuple[List, dict]:
    labels = []
    rows = []
    for key, data in groups:
        row = func(data)
        if len(row):
            GroupbyKey = namedtuple(field_names=by, typename='GroupbyKey')
            keys = _keys(key, by)
            labels.append(GroupbyKey(*keys.values()))
            rows.append(row)
    return labels, row_dicts_to_data(rows)


def sum_groups(groups: List[tuple], by: Collection[str]) -> tuple[List, dict]:
    return aggregate_groups(groups, by, sum_data, 'Sums')


def count_groups(groups: List[tuple], by: Collection[str]) -> tuple[List, dict]:
    return aggregate_groups(groups, by, count_data, 'Counts')


def aggregate_data(data: MutableMapping, func: Callable) -> dict:
    out = {}
    for column_name in data.keys():
        try:
            col_sum = func(data[column_name])
        except TypeError:
            continue
        out[column_name] = col_sum
    return out


def sum_data(data: MutableMapping) -> dict:
    return aggregate_data(data, sum)


def count_data(data: MutableMapping) -> dict:
    return aggregate_data(data, len)


