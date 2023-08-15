from dataclasses import dataclass
from typing import ClassVar, Dict

from datclass import DatClass


@dataclass
class User(DatClass):
    name: str
    age: int
    attr_123: str

    # 重命名字段
    __rename_attrs__: ClassVar[Dict[str, str]] = {
        'Name': 'name',
        'Age': 'age',
        '123#$^%^%*': 'attr_123'
    }

    # 这样写也是可以的
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

    # 重命名字段
    # __rename_attrs: ClassVar[Dict[str, str]] = {
    #     'Name': 'name',
    #     'Age': 'age',
    #     '123#$^%^%*': 'attr_123'
    # }

    # 这样写也是可以的
    __rename_attrs__ = {
        'Name': 'name',
        'Age': 'age',
        '123#$^%^%*': 'attr_123',
    }


def test_rename_attrs2():
    s = '{"Name": "foo", "Age": 18, "123#$^%^%*": "test rename attrs"}'
    user = User.from_str(s)
    assert user.to_str() == s
