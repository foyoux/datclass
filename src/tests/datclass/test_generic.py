from dataclasses import dataclass
from typing import List, TypeVar, Generic

from datclass import DatClass

T = TypeVar('T', bound=DatClass)


@dataclass
class ResponseList(DatClass, Generic[T]):
    status: int
    message: str
    data: List[T]


@dataclass
class File(DatClass):
    name: str
    path: str
    size: int
    type: str
    url: str


@dataclass
class Share(DatClass):
    id: int
    name: str
    path: str
    size: int
    type: str
    url: str
    created_at: str
    updated_at: str


def test_generic():
    a = ResponseList[File](status=200, message='success',
                           data=[{'name': 'name', 'path': 'path', 'size': 1, 'type': 'type', 'url': 'url'}])
    print(a.data[0].name)
    b = ResponseList[Share](status=200, message='success', data=[
        {'id': 1, 'name': 'name', 'path': 'path', 'size': 1, 'type': 'type', 'url': 'url', 'created_at': 'created_at',
         'updated_at': 'updated_at'}])
    print(b.data[0].updated_at)
