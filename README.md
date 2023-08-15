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

### 示例 1

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

### 示例 2

```py
from dataclasses import dataclass
from typing import ClassVar, Dict

from datclass import DatClass


@dataclass
class User(DatClass):
    Name: str
    Age: int

    # 重命名字段
    __rename_attrs: ClassVar[Dict[str, str]] = {
        'Name': 'name',
        'Age': 'age',
        '123#$^%^%*': 'attr_123'
    }

    # 这样写也是可以的
    # __rename_attrs = {
    #     'Name': 'name',
    #     'Age': 'age',
    #     '123#$^%^%*': 'attr_123',
    # }


if __name__ == '__main__':
    s = '{"Name": "foo", "Age": 18, "123#$^%^%*": "test rename attrs"}'
    user = User.from_str(s)
    assert user.to_str() == s

```

## 自动生成 `DatClass`

详见 `datclass` 命令

```sh
datclass -h
```

### 示例 1

输入 user.json

```json
{
  "Name": "foo",
  "Age": 18,
  "123#$^%^%*": "test rename attrs"
}
```

执行命令

```sh
$ datclass -o user.py user.json

```

输出 user.py

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