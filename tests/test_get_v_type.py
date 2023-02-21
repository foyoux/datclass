from typing import Dict, List

from datclass import get_v_type


def test_get_v_type():
    assert get_v_type({}) == Dict
    assert get_v_type([]) == List
    assert get_v_type([111]) == List[int]
    assert get_v_type(['111']) == List[str]
    assert get_v_type(['111', 111]) == List
    assert get_v_type(1) == int
    assert get_v_type(1.1) == float
    assert get_v_type(True) == bool
    assert get_v_type({'a': 'b'}) == Dict
    assert get_v_type([{}]) == List[dict]
    assert get_v_type([123, 4354]) == List[int]
