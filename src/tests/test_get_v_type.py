from typing import Dict, List

from datclass import GenerateDatClass


def test_get_v_type():
    assert GenerateDatClass.get_v_type({}) == Dict
    assert GenerateDatClass.get_v_type([]) == List
    assert GenerateDatClass.get_v_type([111]) == List[int]
    assert GenerateDatClass.get_v_type(['111']) == List[str]
    assert GenerateDatClass.get_v_type(['111', 111]) == List
    assert GenerateDatClass.get_v_type(1) == int
    assert GenerateDatClass.get_v_type(1.1) == float
    assert GenerateDatClass.get_v_type(True) == bool
    assert GenerateDatClass.get_v_type({'a': 'b'}) == Dict
    assert GenerateDatClass.get_v_type([{}]) == List[dict]
    assert GenerateDatClass.get_v_type([123, 4354]) == List[int]
    assert GenerateDatClass.get_v_type(None) == str
    assert GenerateDatClass.get_v_type(None, int) == int
