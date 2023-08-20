from dataclasses import dataclass
from typing import ClassVar, Dict

from datclass import DatClass


@dataclass
class User(DatClass):
    name: str
    age: int
    attr_123: str

    # Rename the field.
    __rename_attrs__: ClassVar[Dict[str, str]] = {
        'Name': 'name',
        'Age': 'age',
        '123#$^%^%*': 'attr_123'
    }

    # This way of writing is also acceptable.
    # __rename_attrs__ = {
    #     'Name': 'name',
    #     'Age': 'age',
    #     '123#$^%^%*': 'attr_123',
    # }


def test_rename_attrs():
    s = '{"Name": "foo", "Age": 18, "123#$^%^%*": "test rename attrs"}'
    user = User.from_str(s)
    assert user.to_str() == s


@dataclass
class User2(DatClass):
    name: str
    age: int
    attr_123: str

    # Rename the field.
    # __rename_attrs: ClassVar[Dict[str, str]] = {
    #     'Name': 'name',
    #     'Age': 'age',
    #     '123#$^%^%*': 'attr_123'
    # }

    # This way of writing is also acceptable.
    __rename_attrs__ = {
        'Name': 'name',
        'Age': 'age',
        '123#$^%^%*': 'attr_123',
    }


def test_rename_attrs2():
    s = '{"Name": "foo", "Age": 18, "123#$^%^%*": "test rename attrs"}'
    user = User.from_str(s)
    assert user.to_str() == s
