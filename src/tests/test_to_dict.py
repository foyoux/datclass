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


@dataclass
class Resource(DatClass):
    type: str = None
    id: str = None


@dataclass
class Users(DatClass):
    name: str = None
    email: str = None


@dataclass
class ExtraCls(DatClass):
    users: List[Users] = field(default_factory=list)
    action: str = None
    timestamp: str = None
    resource: Resource = None


def test_to_dict_extra():
    s = """{
  "users": [
    {
      "name": "John Doe",
      "email": "test@example.com"
    }
  ],
  "action": "create",
  "timestamp": "2016-01-01T00:00:00Z",
  "resource": {
    "type": "user",
    "id": "123"
  }
}"""
    s_none_1 = """{
  "users": [
    {
      "name": "John Doe",
      "email": null
    }
  ],
  "action": "create",
  "timestamp": "2016-01-01T00:00:00Z",
  "resource": {
    "type": "user",
    "id": "123"
  }
}"""
    s_none_2 = """{
  "users": [
    {
      "name": "John Doe"
    }
  ],
  "action": "create",
  "timestamp": "2016-01-01T00:00:00Z",
  "resource": {
    "type": "user",
    "id": "123"
  }
}"""
    s_extra = """{
  "users": [
    {
      "name": "John Doe"
    }
  ],
  "action": "create",
  "timestamp": "2016-01-01T00:00:00Z",
  "resource": {
    "type": "user",
    "id": "123"
  },
  "extra": {
    "type": "user",
    "id": "123"
  }
}"""
    obj = ExtraCls.from_str(s)
    assert obj.to_dict() == json.loads(s)
    assert obj.to_str(indent=2) == s
    assert obj.to_str(indent=2) == s
    assert obj.to_str(indent=2, ignore_none=True) == s
    obj = ExtraCls.from_str(s_none_1)
    assert obj.to_dict() == json.loads(s_none_1)
    assert obj.to_str(indent=2) == s_none_1
    assert obj.to_str(indent=2, ignore_none=True) == s_none_2
    obj = ExtraCls.from_str(s_extra)
    assert obj.to_dict(ignore_none=True) == json.loads(s_extra)
    assert obj.to_str(indent=2, ignore_none=True) == s_extra
    assert obj.to_str(indent=2, ignore_none=True) == s_extra
