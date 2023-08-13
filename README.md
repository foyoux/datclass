# datclass

python dataclass nested & extra

扩展官方 dataclass，支持嵌套和额外字段

## 安装

```sh
pip install -U datclass
pip install git+ssh://git@github.com/foyoux/datclass.git
pip install git+https://github.com/foyoux/datclass.git
```

## 用法示例

```py
from dataclasses import dataclass
from typing import List

# 默认 DatClass 支持嵌套、扩展字段，缺失字段会打印日志
from datclass import DatClass


# 自定义
# from datclass import get_datclass
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
    user1.to_file('user.json')
    user1.to_file('user.json', indent=4, ignore_none=True, sort_keys=True)

    user2 = User(**{'name': 'bar', 'age': 20})
    dict1 = user2.to_dict()
    dict2 = user2.to_dict(ignore_none=True)

    user3 = User.from_str('{"name": "baz", "age": 22}')
    dict3 = user3.to_str()
    dict4 = user3.to_str(indent=4, ignore_none=True)

    user4 = User.from_file('user.json')
    tuple4 = user4.to_tuple()

    grp = Group(name='group1', users=[user1, user2, user3, user4])
    grp.to_file('group.json', indent=4, ignore_none=True, sort_keys=True)

    for user in grp.users:
        print(user.name, user.age)

    user = {'name': 'foo', 'age': 18, 'sex': 1}
    user5 = User(**user)
    assert user5.to_dict() == user

```