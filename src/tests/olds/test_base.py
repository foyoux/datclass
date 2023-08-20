"""
Test basic usage.
1. Nested data classes
2. Field extension

"""
from dataclasses import dataclass

from datclass import DatClass


@dataclass
class Sex(DatClass):
    male: bool = None
    female: bool = None


@dataclass
class Info(DatClass):
    age: int = None
    sex: Sex = None


@dataclass
class Person(DatClass):
    name: str = None
    info: Info = None


def test_nested():
    dat = {
        'name': 'foyou',
        'info': {
            'age': 19,
            'sex': {
                'male': False,
                'female': True
            }
        },
    }
    p = Person(**dat)
    assert p.name == 'foyou'
    assert isinstance(p.info, Info)
    assert p.info.age == 19
    assert isinstance(p.info.sex, Sex)


def test_extra():
    dat = {
        'name': 'foyou',
        'info': {
            'age': 19,
            'sex': {
                'male': False,
                'female': True,
                'hello': 'world'
            },
            'no': 1001
        },
    }
    p = Person(**dat)
    assert p.name == 'foyou'
    assert isinstance(p.info, Info)
    assert p.info.age == 19
    assert isinstance(p.info.sex, Sex)
    assert p.info.sex.hello == 'world'
    assert p.info.no == 1001
