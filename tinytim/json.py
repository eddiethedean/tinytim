"""
Module used for converting data format to json and json to data format.
"""

from typing import Dict, List, Mapping, Sequence
import json

from tinytim.rows import iterrows
from tinytim.utils import row_dicts_to_data


def data_to_json_list(data: Mapping[str, Sequence]) -> List[Dict]:
    """
    Example:
    data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    data_to_json_list(data) -> [{'x': 1, 'y': 6},
                                {'x': 2, 'y': 7},
                                {'x': 3, 'y': 8}]
    """
    return [row for _, row in iterrows(data)]


def json_list_to_data(l: List[Dict]) -> Dict[str, list]:
    """
    Example:
    json = [{'x': 1, 'y': 6},
            {'x': 2, 'y': 7},
            {'x': 3, 'y': 8}]
    json_list_to_data(json) -> {'x': [1, 2, 3],
                                'y': [6, 7, 8]}
    """
    return row_dicts_to_data(l)


def data_to_json(data: Mapping[str, Sequence]) -> str:
    """
    Example:
    data = {'x': [1, 2, 3], 'y': [6, 7, 8]}
    data_to_json(data) -> '''[{"x": 1, "y": 6},
                              {"x": 2, "y": 7},
                              {"x": 3, "y": 8}]'''
    """
    l: List[Dict] = data_to_json_list(data)
    return json.dumps(l)


def json_to_data(j: str) -> Dict[str, list]:
    """
    Example:
    j = '''[{"x": 1, "y": 6},
            {"x": 2, "y": 7},
            {"x": 3, "y": 8}]'''
    json_to_data(j) -> {'x': [1, 2, 3],
                        'y': [6, 7, 8]}
    """
    l = json.loads(j)
    return json_list_to_data(l)