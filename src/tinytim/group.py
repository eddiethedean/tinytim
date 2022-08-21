from typing import Collection, List, MutableMapping, Union

import tinytim.filter as filter
import tinytim.utils as utils


def groupbycolumn(data: MutableMapping, column: Collection) -> List[tuple]:
    keys = utils.uniques(column)
    return [(k, filter.filter_data(data, filter.column_filter(column, lambda x: x == k)))
                for k in keys]


def groupbyone(data: MutableMapping, column_name: str) -> List[tuple]:
    return groupbycolumn(data, data[column_name])


def groupbymulti(data: MutableMapping, column_names: Collection[str]) -> List[tuple]:
    return groupbycolumn(data, utils.row_value_tuples(data, column_names))


def groupby(data: MutableMapping, by: Union[str, Collection[str]]) -> List[tuple]:
    if isinstance(by, str):
        return groupbyone(data, by)
    else:
        return groupbymulti(data, by)