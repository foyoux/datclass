from dataclasses import dataclass
from typing import Dict

from datclass import DatClass


@dataclass
class Log(DatClass):
    version: str = None
    creator: Dict = None


@dataclass
class Har(DatClass):
    log: Log = None


def test_xx_not_none():
    Har(**{
        'log': None
    })
