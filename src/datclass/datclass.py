from dataclasses import dataclass, is_dataclass
from typing import get_type_hints, get_origin, get_args


class MetaClass(type):
    @staticmethod
    def init(self, *args, **kwargs):
        for attr, value in zip(get_type_hints(self), args):
            setattr(self, attr, value)
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.__post_init__()

    def __new__(mcs, *args, **kwargs):
        cls = type(*args, **kwargs)
        cls.__init__ = MetaClass.init
        return cls


@dataclass
class DatClass:
    def __post_init__(self):
        attrs = get_type_hints(self)
        for attr_name, attr_type in attrs.items():
            origin = get_origin(attr_type)
            if origin is None and is_dataclass(attr_type):
                setattr(self, attr_name, attr_type(**getattr(self, attr_name)))
                continue
            for item_type in get_args(attr_type):
                setattr(self, attr_name, [item_type(**i) for i in getattr(self, attr_name)])
