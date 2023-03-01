from dataclasses import dataclass, is_dataclass

from datclass import DatClass


@dataclass
class Info(DatClass):
    age: int = None
    sex: str = None


@dataclass
class User1(DatClass):
    name: str = None
    info: Info = None

    def __post_init__(self):
        pass


def test_not_super_post_init():
    u1 = User1(**{
        'name': 'foyou',
        'info': {}
    })
    assert is_dataclass(u1)
    assert isinstance(u1, DatClass)
    assert u1.name == 'foyou'
    assert isinstance(u1.info, dict)


@dataclass
class User2(DatClass):
    name: str = None
    info: Info = None

    def __post_init__(self):
        super().__post_init__()


def test_post_init():
    u1 = User2(**{
        'name': 'foyou',
        'info': {}
    })
    assert is_dataclass(u1)
    assert isinstance(u1, DatClass)
    assert u1.name == 'foyou'
    assert isinstance(u1.info, Info)
