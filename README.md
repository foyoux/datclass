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