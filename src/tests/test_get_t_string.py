from typing import List, Dict

from datclass import GenerateDatClass


def test_get_t_string():
    assert GenerateDatClass.get_t_string(List[int]) == 'List[int]'
    assert GenerateDatClass.get_t_string(List[str]) == 'List[str]'
    assert GenerateDatClass.get_t_string(List[float]) == 'List[float]'
    assert GenerateDatClass.get_t_string(List[bool]) == 'List[bool]'
    assert GenerateDatClass.get_t_string(List[Dict]) == 'List[Dict]'
    assert GenerateDatClass.get_t_string(List[dict]) == 'List[dict]'
