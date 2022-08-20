from typing import Any, Generator, Mapping



def row_values_generator(row: Mapping) -> Generator[Any, None, None]:
    for key in row:
        yield row[key]