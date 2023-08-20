from dataclasses import dataclass

from datclass import get_datclass

DatClass = get_datclass()


@dataclass(frozen=True)
class User(DatClass):
    name: str
    age: int


def test_frozen():
    User(**{'name': 'John', 'age': 20, 'xxx': 1})


from datclass import DatClass

import sys

if sys.version_info >= (3, 10):
    @dataclass(slots=True)
    class User(DatClass):
        name: str
        age: int
else:
    @dataclass()
    class User(DatClass):
        name: str
        age: int


def test_slots():
    s = '{"name": "John", "age": 20, "xxx": 1}'
    user = User.from_str(s)
    assert user.to_dict() == {'name': 'John', 'age': 20, 'xxx': 1}
    assert user.to_str() == s
