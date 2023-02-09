# datclass

python package datclass

## install

```sh
pip install -U datclass
pip install git+ssh://git@github.com/foyoux/datclass.git
pip install git+https://github.com/foyoux/datclass.git
```

## basic usage

<details>
<summary>Example 1</summary>

```py
from dataclasses import dataclass, field
from typing import Dict, List

from datclass import DatClass


@dataclass
class User(DatClass):
    name: str = None
    age: int = None


@dataclass
class Group(DatClass):
    name: str = None
    users: List[User] = field(default_factory=list)
    meta: Dict = field(default_factory=dict)


if __name__ == '__main__':
    dat = {
        'name': 'foyoux',
        'users': [
            {'name': 'foyou', 'age': 18}
        ],
        'meta': {
            'field1': 'value1',
            'field2': 'value2',
            'field3': 'value3',
        },
    }

    group = Group(**dat)

    print(group.name, group.meta)
    for user in group.users:
        print(user.name, user.age)

```

</details>

<details>
<summary>Example 2</summary>

在 **Example 1** 中，如果将修改 `dat` 为
```py
dat = {
    'name': 'foyoux',
    'users': [
        {'name': 'foyou', 'age': 18, 'sex': 'female'}
    ],
    'meta': {
        'field1': 'value1',
        'field2': 'value2',
        'field3': 'value3',
    },
}
```

程序将会抛出 `TypeError: User.__init__() got an unexpected keyword argument 'sex'` 错误，原因就是定义的字段少于实际给出的

解决这个问题的办法设置 metaclass，新代码如下

```py
from dataclasses import dataclass, field
from typing import Dict, List

from datclass import DatClass, MetaClass


@dataclass
class User(DatClass, metaclass=MetaClass):
    name: str = None
    age: int = None


@dataclass
class Group(DatClass, metaclass=MetaClass):
    name: str = None
    users: List[User] = field(default_factory=list)
    meta: Dict = field(default_factory=dict)


if __name__ == '__main__':
    dat = {
        'name': 'foyoux',
        'users': [
            {'name': 'foyou', 'age': 18, 'sex': 'male'},
            # {'name': 'foyou', 'age': 18},
        ],
        'meta': {
            'field1': 'value1',
            'field2': 'value2',
            'field3': 'value3',
        },
    }

    group = Group(**dat)

    print(group.name, group.meta)
    for user in group.users:
        print(user.name, user.age)

```

</details>