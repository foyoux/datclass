"""
File "/root/.pyenv/versions/3.8.5/lib/python3.8/site-packages/datclass/__init__.py", line 72, in __post_init__
    setattr(self, attr_name, [item_type(**i) for i in getattr(self, attr_name)])
  File "/root/.pyenv/versions/3.8.5/lib/python3.8/site-packages/datclass/__init__.py", line 72, in <listcomp>
    setattr(self, attr_name, [item_type(**i) for i in getattr(self, attr_name)])
TypeError: type object argument after ** must be a mapping, not int
"""
from dataclasses import dataclass, field
from typing import List

from datclass import DatClass
from datclass.__main__ import Generator

dat = {
    'name': 'foyou',
    'ranks': [89, 90, 67, 99, 120]
}


@dataclass
class Object(DatClass):
    name: str = None
    ranks: List[int] = field(default_factory=list)


def test_list_int():
    Object(**dat)


def test_gen_list_int():
    gen = Generator()
    gen.gen_datclass(dat)
    assert gen.imports.List == True
