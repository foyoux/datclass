from dataclasses import dataclass

from datclass import DatClass


@dataclass
class User(DatClass):
    name: str = None
