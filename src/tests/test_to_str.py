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
