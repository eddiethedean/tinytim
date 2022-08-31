from typing import Dict, Generator, Mapping, Sequence, Tuple

import tinytim.data as data_features


def column_dict(data: Mapping[str, Sequence], col: str) -> Dict[str, Sequence]:
    """Return a dict of {col_name, col_values} from data.

       Example:
       data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
       column_dict(data, 'x') -> {'x': [1, 2, 3]}
       column_dict(data, 'y') -> {'y': [6, 7, 8]}
    """
    return {col: data[col]}


def itercolumns(data: Mapping) -> Generator[Tuple[str, tuple], None, None]:
    """Return a generator of tuple column name, column values.
       
       Example:
       data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
       cols = list(itercolumns(data))
       cols[0] -> ('x', (1, 2, 3)) 
       cols[1] -> ('y', (6, 7, 8))
    """
    for col in data_features.column_names(data):
        yield col, tuple(data[col])