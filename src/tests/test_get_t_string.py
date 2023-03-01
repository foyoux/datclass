from typing import List, Dict

from datclass import get_t_string


def test_get_t_string():
    assert get_t_string(List[int]) == 'List[int]'
    assert get_t_string(List[str]) == 'List[str]'
    assert get_t_string(List[float]) == 'List[float]'
    assert get_t_string(List[bool]) == 'List[bool]'
    assert get_t_string(List[Dict]) == 'List[Dict]'
    assert get_t_string(List[dict]) == 'List[dict]'
