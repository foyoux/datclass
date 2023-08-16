# datclass

python dataclass nested & extra attrs

Extending the official [dataclass](https://docs.python.org/zh-cn/3/library/dataclasses.html) to support nested and extended fields.

## Install

[![PyPI](https://img.shields.io/pypi/v/datclass)](https://pypi.org/project/datclass/) [![python version](https://img.shields.io/pypi/pyversions/datclass)](https://pypi.org/project/datclass/)  [![Downloads](https://static.pepy.tech/personalized-badge/datclass?period=total&units=international_system&left_color=black&right_color=orange&left_text=Downloads)](https://pepy.tech/project/datclass)

```sh
pip install -U datclass
pip install git+ssh://git@github.com/foyoux/datclass.git
pip install git+https://github.com/foyoux/datclass.git
```

## Usage example

### Example 1

```py
from dataclasses import dataclass
from typing import List

# Default `dataclass` supports nested and extended fields. Missing fields will be logged.
from datclass import DatClass


# Custom `DatClass`
# from datclass import get_datclass
# Missing fields will not be logged.
# DatClass = get_datclass(log=False)


@dataclass
class User(DatClass):
    name: str
    age: int


@dataclass
class Group(DatClass):
    name: str
    users: List[User]


if __name__ == '__main__':
    user1 = User(name='foo', age=18)
    # Saving a data class to a file.
    user1.to_file('user.json')
    # Adding some control parameters.
    user1.to_file('user.json', indent=4, ignore_none=True, sort_keys=True)

    # Creating a data class from a dict.
    user2 = User(**{'name': 'bar', 'age': 20})
    # To convert a data class to a dictionary, you can support extended fields.
    # You can also use the official asdict function, but it cannot export extended fields.
    dict1 = user2.to_dict()
    # 'ignore_none' is used to ignore values that are None.
    dict2 = user2.to_dict(ignore_none=True)

    # Creating a data class from a string.
    user3 = User.from_str('{"name": "baz", "age": 22}')
    # Convert the data class to a JSON string.
    dict3 = user3.to_str()
    dict4 = user3.to_str(indent=4, ignore_none=True)

    # Creating a data class from a file.
    user4 = User.from_file('user.json')

    # Nested data classes
    grp = Group(name='group1', users=[user1, user2, user3, user4])
    grp.to_file('group.json', indent=4, ignore_none=True, sort_keys=True)

    for user in grp.users:
        print(user.name, user.age)

    # Extending fields
    user = {'name': 'foo', 'age': 18, 'sex': 1}
    user5 = User(**user)
    assert user5.to_dict() == user

```

### Example 2

```py
from dataclasses import dataclass
from typing import ClassVar, Dict

from datclass import DatClass


@dataclass
class User(DatClass):
    name: str
    age: int
    attr_123: str

    # Renaming fields.
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


if __name__ == '__main__':
    s = '{"Name": "foo", "Age": 18, "123#$^%^%*": "test rename attrs"}'
    user = User.from_str(s)
    assert user.to_str() == s

```

## Automatically generate `DataClass`

See the `datclass` command for details.

```sh
$ datclass -h

```

### Example 1

Input user.json

```json
{
  "Name": "foo",
  "Age": 18,
  "123#$^%^%*": "test rename attrs"
}
```

Execute the command

```sh
$ datclass -o user.py user.json

```

Output user.py

```py
from dataclasses import dataclass

from datclass import DatClass


@dataclass
class Object(DatClass):
    a_123: str = None  # rename from '123#$^%^%*'
    age: int = None  # rename from 'Age'
    name: str = None  # rename from 'Name'

    __rename_attrs__ = {
        'Name': 'name',
        'Age': 'age',
        '123#$^%^%*': 'a_123',
    }

```