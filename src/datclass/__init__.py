__title__ = 'datclass'
__author__ = 'foyoux'
__version__ = '0.0.1'
__all__ = ['main', 'DatClass']

import argparse

from dataclasses import dataclass, is_dataclass
from typing import get_origin, get_args

_ORIGIN_INIT = '__dataclass_init__'


def _datclass_init(self, *args, **kwargs):
    getattr(self, _ORIGIN_INIT)(
        *args, **{k: kwargs.pop(k) for k in self.__dataclass_fields__ if k in kwargs}
    )
    for attr, value in kwargs.items():
        setattr(self, attr, value)


@dataclass
class DatClass:

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        if not hasattr(cls, _ORIGIN_INIT):
            setattr(cls, _ORIGIN_INIT, cls.__init__)
            setattr(cls, '__init__', _datclass_init)
        return obj

    def __post_init__(self, *args, **kwargs):
        for attr_name, field in self.__dataclass_fields__.items():  # type: ignore
            attr_type = field.type
            origin = get_origin(attr_type)
            if origin is None and is_dataclass(attr_type):
                setattr(self, attr_name, attr_type(**getattr(self, attr_name)))
                continue
            for item_type in get_args(attr_type):
                setattr(self, attr_name, [item_type(**i) for i in getattr(self, attr_name)])


def main():
    epilog = f'%(prog)s({__version__}) by foyoux(https://github.com/foyoux/datclass)'
    parser = argparse.ArgumentParser(prog='datclass', description='', epilog=epilog)
    parser.add_argument('-v', '--version', action='version', version=epilog)

    parser.parse_args()
