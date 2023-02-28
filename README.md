# datclass

python package datclass

## 安装

```sh
pip install -U datclass
pip install git+ssh://git@github.com/foyoux/datclass.git
pip install git+https://github.com/foyoux/datclass.git
```

## 基本用法

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
    users: List[User] = field(default_factory=list)  # 允许嵌套
    meta: Dict = field(default_factory=dict)


if __name__ == '__main__':
    dat = {
        'name': 'foyoux',
        'users': [
            {'name': 'foyou', 'age': 18},
            {'name': 'hello', 'age': 8, 'sex': 'male'},  # 允许扩展字段
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

## `datclass` 命令行工具

通过 JSON 生成 dataclass or TypedDict

```sh
usage: datclass [-h] [-v] [-n NAME] [-r] [-o OUTPUT] [-d] [-i] [file]

generate datclass & support nested and extra

positional arguments:
  file                  input file - likes-json

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -n NAME, --name NAME  main dat class name
  -r, --recursive       recursive generate dat class
  -o OUTPUT, --output OUTPUT
                        output file - *.py
  -d, --dict            generate TypedDict class
  -i, --inline          use inline model to generate TypedDict type
```

<details>
<summary>data.json</summary>

```json
{
  "update_id": 1,
  "message": {
    "message_id": 5,
    "chat": {
      "id": 1,
      "first_name": "first_name",
      "last_name": "last_name",
      "username": "username",
      "type": "private"
    },
    "date": 1,
    "forward_from": {
      "id": 1,
      "is_bot": true,
      "first_name": "first_name",
      "username": "username"
    },
    "forward_date": 1,
    "video": {
      "duration": 29,
      "width": 1280,
      "height": 720,
      "mime_type": "video/mp4",
      "thumb": {
        "file_id": "file_id",
        "file_unique_id": "file_unique_id",
        "file_size": 7420,
        "width": 320,
        "height": 180
      },
      "file_id": "file_id",
      "file_unique_id": "file_unique_id",
      "file_size": 3905756
    },
    "caption": "caption",
    "caption_entities": [
      {
        "offset": 0,
        "length": 47,
        "type": "text_link",
        "url": "https://github.com/foyoux/datclass"
      }
    ]
  }
}
```

</details>

<details>
<summary>Example 1</summary>

```sh
datclass -r -o data.py data.json
```

### data.py

```py
from datclass import dataclass, field, List, DatClass


@dataclass
class CaptionEntities(DatClass):
    offset: int = None
    length: int = None
    type: str = None
    url: str = None


@dataclass
class Thumb(DatClass):
    file_id: str = None
    file_unique_id: str = None
    file_size: int = None
    width: int = None
    height: int = None


@dataclass
class Video(DatClass):
    duration: int = None
    width: int = None
    height: int = None
    mime_type: str = None
    thumb: Thumb = None
    file_id: str = None
    file_unique_id: str = None
    file_size: int = None


@dataclass
class ForwardFrom(DatClass):
    id: int = None
    is_bot: bool = None
    first_name: str = None
    username: str = None


@dataclass
class Chat(DatClass):
    id: int = None
    first_name: str = None
    last_name: str = None
    username: str = None
    type: str = None


@dataclass
class Message(DatClass):
    message_id: int = None
    chat: Chat = None
    date: int = None
    forward_from: ForwardFrom = None
    forward_date: int = None
    video: Video = None
    caption: str = None
    caption_entities: List[CaptionEntities] = field(default_factory=list)


@dataclass
class Object(DatClass):
    update_id: int = None
    message: Message = None

```

</details>


<details>
<summary>Example 2</summary>

```sh
datclass -r -o data.py data.json -n Response
```

### data.py

```py
from datclass import dataclass, field, List, DatClass


@dataclass
class CaptionEntities(DatClass):
    offset: int = None
    length: int = None
    type: str = None
    url: str = None


@dataclass
class Thumb(DatClass):
    file_id: str = None
    file_unique_id: str = None
    file_size: int = None
    width: int = None
    height: int = None


@dataclass
class Video(DatClass):
    duration: int = None
    width: int = None
    height: int = None
    mime_type: str = None
    thumb: Thumb = None
    file_id: str = None
    file_unique_id: str = None
    file_size: int = None


@dataclass
class ForwardFrom(DatClass):
    id: int = None
    is_bot: bool = None
    first_name: str = None
    username: str = None


@dataclass
class Chat(DatClass):
    id: int = None
    first_name: str = None
    last_name: str = None
    username: str = None
    type: str = None


@dataclass
class Message(DatClass):
    message_id: int = None
    chat: Chat = None
    date: int = None
    forward_from: ForwardFrom = None
    forward_date: int = None
    video: Video = None
    caption: str = None
    caption_entities: List[CaptionEntities] = field(default_factory=list)


@dataclass
class Response(DatClass):
    update_id: int = None
    message: Message = None

```

</details>

<details>
<summary>Example 3</summary>

```sh
datclass -r -o data.py data.json -n Response -d
```

### data.py

> 如果提示警告，没有代码提示，则从 `typing` 中导入 `TypedDict`
>
> 为了兼容 Python 3.7，datclass 引入了 `typing_extensions`，但是它并没有真正实现 `TypedDict`

```py
from datclass import List, TypedDict


class CaptionEntities(TypedDict):
    offset: int
    length: int
    type: str
    url: str


class Thumb(TypedDict):
    file_id: str
    file_unique_id: str
    file_size: int
    width: int
    height: int


class Video(TypedDict):
    duration: int
    width: int
    height: int
    mime_type: str
    thumb: Thumb
    file_id: str
    file_unique_id: str
    file_size: int


class ForwardFrom(TypedDict):
    id: int
    is_bot: bool
    first_name: str
    username: str


class Chat(TypedDict):
    id: int
    first_name: str
    last_name: str
    username: str
    type: str


class Message(TypedDict):
    message_id: int
    chat: Chat
    date: int
    forward_from: ForwardFrom
    forward_date: int
    video: Video
    caption: str
    caption_entities: List[CaptionEntities]


class Response(TypedDict):
    update_id: int
    message: Message

```

</details>

<details>
<summary>Example 4</summary>

```sh
datclass -r -o data.py data.json -n Response -d -i
```

### data.py

```py
from datclass import List, TypedDict


CaptionEntities = TypedDict('CaptionEntities', {'offset': int, 'length': int, 'type': str, 'url': str})
Thumb = TypedDict('Thumb', {'file_id': str, 'file_unique_id': str, 'file_size': int, 'width': int, 'height': int})
Video = TypedDict('Video', {'duration': int, 'width': int, 'height': int, 'mime_type': str, 'thumb': Thumb, 'file_id': str, 'file_unique_id': str, 'file_size': int})
ForwardFrom = TypedDict('ForwardFrom', {'id': int, 'is_bot': bool, 'first_name': str, 'username': str})
Chat = TypedDict('Chat', {'id': int, 'first_name': str, 'last_name': str, 'username': str, 'type': str})
Message = TypedDict('Message', {'message_id': int, 'chat': Chat, 'date': int, 'forward_from': ForwardFrom, 'forward_date': int, 'video': Video, 'caption': str, 'caption_entities': List[CaptionEntities]})
Response = TypedDict('Response', {'update_id': int, 'message': Message})
```

> 如果提示警告，没有代码提示，则从 `typing` 中导入 `TypedDict`
>
> 为了兼容 Python 3.7，datclass 引入了 `typing_extensions`，但是它并没有真正实现 `TypedDict`


```py
from typing import TypedDict
from datclass import List


CaptionEntities = TypedDict('CaptionEntities', {'offset': int, 'length': int, 'type': str, 'url': str})
Thumb = TypedDict('Thumb', {'file_id': str, 'file_unique_id': str, 'file_size': int, 'width': int, 'height': int})
Video = TypedDict('Video', {'duration': int, 'width': int, 'height': int, 'mime_type': str, 'thumb': Thumb, 'file_id': str, 'file_unique_id': str, 'file_size': int})
ForwardFrom = TypedDict('ForwardFrom', {'id': int, 'is_bot': bool, 'first_name': str, 'username': str})
Chat = TypedDict('Chat', {'id': int, 'first_name': str, 'last_name': str, 'username': str, 'type': str})
Message = TypedDict('Message', {'message_id': int, 'chat': Chat, 'date': int, 'forward_from': ForwardFrom, 'forward_date': int, 'video': Video, 'caption': str, 'caption_entities': List[CaptionEntities]})
Response = TypedDict('Response', {'update_id': int, 'message': Message})
```

</details>
