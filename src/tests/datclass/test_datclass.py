import dataclasses


def test_datclass():
    from datclass import DatClass

    c1 = DatClass.from_str('{}')
    d1 = c1.to_dict()
    assert d1 == {}

    c2 = DatClass.from_str('{"a": 1, "b": {}}')
    d2 = c2.to_dict()
    assert d2 == {'a': 1, 'b': {}}

    @dataclasses.dataclass()
    class A0(DatClass):
        pass

    @dataclasses.dataclass
    class A(A0):
        a1: int = None
        b1: int = None

    a1 = A(a1=100, b1=200)
    a2 = A.from_str('{"a1": 101, "b1": 201}')
    a3 = A.from_str('{"a1": 101, "b1": 201, "c1": 998}')


def test_get_datclass():
    from datclass import get_datclass

    DatClass = get_datclass(empty_dict_as_none=True)

    c1 = DatClass.from_str('{"a": {}}')
    assert c1.a is None
    d1 = c1.to_dict()
    assert d1['a'] is None
    d1 = c1.to_dict(ignore_none=True)
    assert d1 == {}
