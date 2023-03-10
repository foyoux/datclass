__title__ = 'datclass'
__author__ = 'foyoux'
__version__ = '0.0.1'

__all__ = [
    'main',
    'DatClass',
    'dataclass',
    'is_dataclass',
    'set_debug', 'set_extra',
    'DatGen',
]

import argparse
import json
import os
from dataclasses import dataclass, is_dataclass
from pathlib import Path
from typing import get_origin, get_args

from datclass.gens import DatGen
from datclass.utils import get_ok_identifier

_DEBUG = False
_EXTRA = True
_ORIGINAL_INIT = '__dataclass_init__'


def set_debug(b):
    global _DEBUG
    _DEBUG = b


def set_extra(b):
    global _EXTRA
    _EXTRA = b


def _datclass_init(self, *args, **kwargs):
    if kwargs:
        kwargs = {get_ok_identifier(k): v for k, v in kwargs.items()}

    if _DEBUG:
        getattr(self, _ORIGINAL_INIT)(*args, **kwargs)
    else:
        getattr(self, _ORIGINAL_INIT)(
            *args, **{k: kwargs.pop(k) for k in self.__dataclass_fields__ if k in kwargs}
        )
        if _EXTRA:
            for attr, value in kwargs.items():
                setattr(self, attr, value)


@dataclass
class DatClass:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, _ORIGINAL_INIT):
            setattr(cls, _ORIGINAL_INIT, cls.__init__)
            setattr(cls, '__init__', _datclass_init)
        return super().__new__(cls)

    def __post_init__(self, *args, **kwargs):
        for attr_name, FIELD in self.__dataclass_fields__.items():  # type: ignore
            attr_type = FIELD.type
            origin = get_origin(attr_type)
            if origin is None and is_dataclass(attr_type):
                attr = getattr(self, attr_name)
                setattr(self, attr_name, attr_type(**attr) if attr else None)
                continue
            for item_type in get_args(attr_type):
                setattr(self, attr_name, [item_type(**i) for i in getattr(self, attr_name)])


def main():
    epilog = f'%(prog)s({__version__}) by foyoux(https://github.com/foyoux/datclass)'
    parser = argparse.ArgumentParser(prog='datclass', description='generate datclass & support nested and extra',
                                     epilog=epilog)
    parser.add_argument('-v', '--version', action='version', version=epilog)

    parser.add_argument('-n', '--name', help='main dat class name', default='Object')
    parser.add_argument('-r', '--recursive', help='recursive generate dat class', action='store_true')
    parser.add_argument('-o', '--output', help='output file - *.py')
    parser.add_argument('-d', '--dict', help='generate TypedDict class', action='store_true')
    parser.add_argument('file', nargs='?', help='input file - likes-json')

    args = parser.parse_args()

    name = args.name
    recursive = args.recursive
    input_file = args.file
    output_file = args.output

    if input_file:
        f = Path(input_file)
        if not f.exists():
            print(f'{f.absolute()} not exists')
            return
        text = f.read_text()
    else:
        print(f'Please paste the JSON string - {"Ctrl-Z" if os.name == "nt" else "Ctrl-D"} Return')
        data = []
        try:
            while True:
                data.append(input())
        except EOFError:
            text = '\n'.join(data)
        except KeyboardInterrupt:
            print('\n???? Bye-Bye')
            return

    try:
        body = json.loads(text)
    except json.JSONDecodeError:
        print('\nInvalid JSON data')
        return

    datgen = DatGen()

    if args.dict:
        codes = datgen.gen_typed_dict(body, name, recursive).codes
    else:
        codes = datgen.gen_datclass(body, name, recursive).codes

    dat = '\n'.join(datgen.imports.codes + codes + [''])

    if output_file:
        f = Path(output_file)
        f.parent.mkdir(exist_ok=True, parents=True)
        f.write_text(dat)
    else:
        print()
        print(dat)

    print('???? Generate successful')
