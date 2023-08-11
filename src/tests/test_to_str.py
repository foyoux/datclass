import json
from dataclasses import dataclass, field
from typing import List

from datclass import DatClass


@dataclass
class A(DatClass):
    imToken: str = None
    retryTimes: int = None
    retryInterSec: int = None
    linkServers: List[str] = field(default_factory=list)


@dataclass
class B(DatClass):
    code: int = None
    desc: str = None
    data: A = None


def test_to_str():
    s = """{
    "code": 200,
    "desc": "success",
    "data": {
        "imToken": "321edfs",
        "retryTimes": 3,
        "retryInterSec": 5,
        "linkServers": [
            "fssdsf-fs"
        ]
    }
}"""
    t = B.from_str(s)
    assert t.to_str(indent=4) == s
    assert t.to_dict() == json.loads(s)


@dataclass
class Ids(DatClass):
    id: str = None
    type: str = None


@dataclass
class XXCls(DatClass):
    newSession: bool = None
    sessionID: str = None
    now: int = None
    ids: List[Ids] = field(default_factory=list)
    localData: str = None


def test_to_str_ignore_none():
    s = """{
    "newSession": true,
    "sessionID": "6763652d617321d369612d6561737431-1",
    "now": 1691737826,
    "ids": [
        {
            "id": null,
            "type": "pageview"
        }
    ],
    "localData": null
}"""
    s1 = """{
    "newSession": true,
    "sessionID": "6763652d617321d369612d6561737431-1",
    "now": 1691737826,
    "ids": [
        {
            "type": "pageview"
        }
    ]
}"""
    t = XXCls.from_str(s)
    assert t.to_str(indent=4) == s
    assert t.to_dict() == json.loads(s)
    assert t.to_str(ignore_none=True, indent=4) == s1
    assert t.to_dict(ignore_none=True) == json.loads(s1)
