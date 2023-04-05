from datclass.utils import not_null


def test_not_null():
    assert not_null({}) is False
    assert not_null([]) is False
    assert not_null([{}]) is False
