from typing import Dict, List

from datclass.utils import get_value_type


def test_get_v_type():
    assert get_value_type({}) == Dict
    assert get_value_type([]) == List
    assert get_value_type([111]) == List[int]
    assert get_value_type(['111']) == List[str]
    assert get_value_type(['111', 111]) == List
    assert get_value_type(1) == int
    assert get_value_type(1.1) == float
    assert get_value_type(True) == bool
    assert get_value_type({'a': 'b'}) == Dict
    assert get_value_type([{}]) == List[dict]
    assert get_value_type([123, 4354]) == List[int]
    assert get_value_type(None) == str
    assert get_value_type(None, int) == int
