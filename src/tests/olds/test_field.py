from dataclasses import dataclass, field, is_dataclass
from typing import List, Dict

from datclass import DatClass


@dataclass
class Person(DatClass):
    name: str = None
    friends: List['Person'] = field(default_factory=list)


def test_field_default_factory_list():
    dat = {
        'name': 'foyou',
    }
    p = Person(**dat)
    assert p.name == 'foyou'
    assert isinstance(p.friends, list) and len(p.friends) == 0


@dataclass
class User(DatClass):
    name: str
    info: Dict = field(default_factory=dict)


def test_field_default_factory_dict():
    dat = {
        'name': 'foyou',
    }
    user = User(**dat)
    assert user.name == 'foyou'
    assert isinstance(user.info, dict) and len(user.info) == 0


@dataclass()
class Student(DatClass):
    name: str = 'foyou'


def test_is_dataclass():
    s = Student(name='hello')
    assert is_dataclass(s)
    assert isinstance(s, Student)
    assert s.name == 'hello'
