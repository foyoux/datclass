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
from dataclasses import dataclass, is_dataclass, asdict, astuple
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
        # 任意字段名映射为合法 Python 字段名
        if kwargs:
            kwargs = {get_ok_identifier(k): v for k, v in kwargs.items()}
        # 调用原构造函数
        getattr(obj, _ORIGINAL_INIT)(*args, **{k: kwargs.pop(k) for k in obj.__dataclass_fields__ if k in kwargs})
        # 扩展字段或者打印缺失字段日志，并且有未定义的字段
        if (extra or log) and kwargs:
            cls = obj.__class__
            for attr, value in kwargs.items():
                if log:
                    _log.warning(f'{cls.__module__}.{cls.__name__}({attr}: {type(value).__name__} = {value!r})')
                if extra:
                    setattr(obj, attr, value)

    def __value_to_dict__(v, ignore_none=False):
        if is_dataclass(v):
            if isinstance(v, __datclass__):
                v = v.to_dict(ignore_none=ignore_none)
            else:
                if ignore_none:
                    v = asdict(v, dict_factory=lambda d1: {k1: v1 for k1, v1 in d1 if v1 is not None})
                else:
                    v = asdict(v)
        elif isinstance(v, list):
            vl = []
            for i in v:
                vl.append(__value_to_dict__(i, ignore_none=ignore_none))
            return vl
        return v

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

        @classmethod
        def from_str(cls, text: str):
            return cls(**json.loads(text))

        def to_str(self, ensure_ascii=True, indent=None, ignore_none=False) -> str:
            return json.dumps(self.to_dict(ignore_none=ignore_none), ensure_ascii=ensure_ascii, indent=indent)

        def to_dict(self, ignore_none=False) -> dict:
            d = {}
            for k, v in self.__dict__.items():
                if ignore_none and v is None:
                    continue
                d[k] = __value_to_dict__(v, ignore_none=ignore_none)
            return d

        def to_tuple(self) -> tuple:
            return astuple(self)

        @classmethod
        def from_file(cls, file_path: str, encoding: str = 'utf8'):
            text = Path(file_path).read_text(encoding=encoding)
            return cls.from_str(text)

        def to_file(self, file_path: str, encoding: str = 'utf8', ensure_ascii=True, indent=None, ignore_none=False):
            Path(file_path).write_text(self.to_str(ensure_ascii=ensure_ascii, indent=indent, ignore_none=ignore_none),
                                       encoding=encoding)

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
