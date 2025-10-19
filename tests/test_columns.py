import tinytim.columns as columns_functions

DATA = {'x': [1, 2, 3], 'y': [6, 7, 8]}


def test_column_dict():
    x = columns_functions.column_mapping(DATA, 'x')
    y = columns_functions.column_mapping(DATA, 'y')
    assert x == {'x': [1, 2, 3]}
    assert y == {'y': [6, 7, 8]}


def test_itercolumns():
    cols = list(columns_functions.itercolumns(DATA))
    assert cols[0] == ('x', [1, 2, 3])
    assert cols[1] == ('y', [6, 7, 8])
