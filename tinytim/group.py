from typing import Any, Callable, Dict, List, Mapping, Sequence, Tuple, Union
from statistics import mean, mode, stdev, pstdev

import tinytim.filter as filter_functions
import tinytim.utils as utils_functions
import tinytim.rows as rows_functions
from tinytim.types import DataDict, DataMapping, RowDict, RowMapping


RowNumDict = Dict[str, Union[int, float]]


def groupbycolumn(data: Mapping, column: Sequence) -> List[tuple]:
    keys = utils_functions.uniques(column)
    return [(k, filter_functions.filter_data(data,
                                             filter_functions.column_filter(column, lambda x: x == k)))
                for k in keys]


def groupbyone(data: Mapping, column_name: str) -> List[tuple]:
    return groupbycolumn(data, data[column_name])


def groupbymulti(data: Mapping, column_names: Sequence[str]) -> List[tuple]:
    return groupbycolumn(data, utils_functions.row_value_tuples(data, column_names))


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
    return labels, rows_functions.row_dicts_to_data(rows)


def sum_groups(groups: List[tuple]) -> Tuple[List, DataDict]:
    return aggregate_groups(groups, sum_data)


def count_groups(groups: List[tuple]) -> Tuple[List, DataDict]:
    return aggregate_groups(groups, count_data)


def mean_groups(groups: List[tuple]) -> Tuple[List, DataDict]:
    return aggregate_groups(groups, mean_data)


def min_groups(groups: List[tuple]) -> Tuple[List, DataDict]:
    return aggregate_groups(groups, min_data)


def max_groups(groups: List[tuple]) -> Tuple[List, DataDict]:
    return aggregate_groups(groups, max_data)


def mode_groups(groups: List[tuple]) -> Tuple[List, DataDict]:
    return aggregate_groups(groups, mode_data)


def stdev_groups(groups: List[tuple]) -> Tuple[List, DataDict]:
    return aggregate_groups(groups, stdev_data)


def pstdev_groups(groups: List[tuple]) -> Tuple[List, DataDict]:
    return aggregate_groups(groups, pstdev_data)


def nunique_groups(groups: List[tuple]) -> Tuple[List, DataDict]:
    return aggregate_groups(groups, nunique_data)


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


def mean_data(data: Mapping) -> RowNumDict:
    return aggregate_data(data, mean)


def min_data(data: Mapping) -> RowNumDict:
    return aggregate_data(data, min)


def max_data(data: Mapping) -> RowNumDict:
    return aggregate_data(data, max)


def mode_data(data: Mapping) -> RowNumDict:
    return aggregate_data(data, mode)


def stdev_data(data: Mapping) -> RowNumDict:
    return aggregate_data(data, stdev)


def pstdev_data(data: Mapping) -> RowNumDict:
    return aggregate_data(data, pstdev)


def nunique_data(data: Mapping) -> RowNumDict:
    return aggregate_data(data, utils_functions.nuniques)