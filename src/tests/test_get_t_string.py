from typing import List, Dict

from datclass.utils import get_type_string


def test_get_t_string():
    assert get_type_string(List[int]) == 'List[int]'
    assert get_type_string(List[str]) == 'List[str]'
    assert get_type_string(List[float]) == 'List[float]'
    assert get_type_string(List[bool]) == 'List[bool]'
    assert get_type_string(List[Dict]) == 'List[Dict]'
    assert get_type_string(List[dict]) == 'List[dict]'
