__title__ = 'datclass'
__author__ = 'foyoux'
__version__ = '0.0.1'

__all__ = [
    'main',
    'DatGen',
    'DatClass',
    'get_datclass',
]

import argparse
import json
import logging
import os
from dataclasses import dataclass, is_dataclass
from pathlib import Path

try:
    from typing import get_origin, get_args
except ImportError:
    from typing_extensions import get_origin, get_args

from datclass.gens import DatGen
from datclass.utils import get_ok_identifier

_ORIGINAL_INIT = '__dataclass_init__'

_log = logging.getLogger('datclass')
_handler = logging.StreamHandler()
_handler.setFormatter(
    logging.Formatter(
        fmt=f'%(asctime)s datclass.%(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
)
_log.addHandler(_handler)


def get_datclass(nested: bool = True, extra: bool = True, log: bool = True):
    def __datclass_init__(obj, *args, **kwargs):
        # 字段映射为合法字段
        if kwargs:
            kwargs = {get_ok_identifier(k): v for k, v in kwargs.items()}
        # 调用原构造函数
        getattr(obj, _ORIGINAL_INIT)(*args, **{k: kwargs.pop(k) for k in obj.__dataclass_fields__ if k in kwargs})
        # 扩展字段或者打印缺失字段日志，并且有未定义的字段
        if (extra or log) and kwargs:
            cls = obj.__class__
            for attr, value in kwargs.items():
                if log:
                    _log.warning(f'{cls.__module__}.{cls.__name__}({attr} : {type(value).__name__} = {value!r})')
                if extra:
                    setattr(obj, attr, value)

    # noinspection PyPep8Naming
    @dataclass
    class __datclass__:
        def __new__(cls, *args, **kwargs):
            if not hasattr(cls, _ORIGINAL_INIT):
                setattr(cls, _ORIGINAL_INIT, cls.__init__)
                setattr(cls, '__init__', __datclass_init__)
            return super().__new__(cls)

        # noinspection PyUnusedLocal
        def __post_init__(self, *args, **kwargs):
            if not nested:
                return
            for attr_name, FIELD in self.__dataclass_fields__.items():  # type: ignore
                attr_type = FIELD.type
                origin = get_origin(attr_type)
                if origin is None and is_dataclass(attr_type):
                    attr = getattr(self, attr_name)
                    setattr(self, attr_name, attr if is_dataclass(attr) else attr_type(**attr) if attr else None)
                    continue
                for item_type in get_args(attr_type):
                    if is_dataclass(item_type):
                        setattr(self, attr_name,
                                [i if is_dataclass(i) else item_type(**i) for i in getattr(self, attr_name) or []])

    return __datclass__


DatClass = get_datclass()


def main():
    epilog = f'%(prog)s({__version__}) by foyoux(https://github.com/foyoux/datclass)'
    parser = argparse.ArgumentParser(prog='datclass', description='generate datclass & support nested and extra',
                                     epilog=epilog)
    parser.add_argument('-v', '--version', action='version', version=epilog)

    parser.add_argument('-n', '--name', help='main dat class name', default='Object')
    parser.add_argument('-o', '--output', help='output file - *.py')
    parser.add_argument('-d', '--dict', help='generate TypedDict class', action='store_true')
    parser.add_argument('-S', '--no-sort', help='sort attrs', action='store_false')
    parser.add_argument('-R', '--no-recursive', dest='recursive', help='not recursive generate dat class',
                        action='store_false')
    parser.add_argument('file', nargs='?', help='input file - likes-json')

    args = parser.parse_args()

    name = args.name
    recursive = args.recursive
    input_file = args.file
    output_file = args.output
    sort = args.no_sort

    if input_file:
        f = Path(input_file)
        if not f.exists():
            print(f'{f.absolute()} not exists')
            return
        text = f.read_text(encoding='utf8')
    else:
        print(f'Please paste the JSON/DICT string - {"Ctrl-Z" if os.name == "nt" else "Ctrl-D"} Return')
        data = []
        try:
            while True:
                data.append(input())
        except EOFError:
            text = '\n'.join(data)
        except KeyboardInterrupt:
            print('\n🎉 Bye-Bye')
            return

    try:
        body = json.loads(text)
    except json.JSONDecodeError:
        # noinspection PyBroadException
        try:
            body = eval(text)
        except Exception as e:
            print('\nInvalid JSON/DICT data', e)
            return

    gen = DatGen()

    if args.dict:
        codes = gen.gen_typed_dict(body, name, recursive, sort=sort).codes
    else:
        codes = gen.gen_datclass(body, name, recursive, sort=sort).codes

    dat = '\n'.join(gen.imports.codes + codes + [''])

    if output_file:
        f = Path(output_file)
        f.parent.mkdir(exist_ok=True, parents=True)
        f.write_text(dat, encoding='utf8')
    else:
        print()
        print(dat)

    print('🎉 Generate successful')
