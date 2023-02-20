__title__ = 'datclass'
__author__ = 'foyoux'
__version__ = '0.0.1'
__all__ = ['main', 'DatClass']

import argparse
import json
from dataclasses import dataclass, is_dataclass
from pathlib import Path
from typing import get_origin, get_args

_ORIGINAL_INIT = '__dataclass_init__'


def _datclass_init(self, *args, **kwargs):
    getattr(self, _ORIGINAL_INIT)(
        *args, **{k: kwargs.pop(k) for k in self.__dataclass_fields__ if k in kwargs}
    )
    for attr, value in kwargs.items():
        setattr(self, attr, value)


@dataclass
class DatClass:

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        if not hasattr(cls, _ORIGINAL_INIT):
            setattr(cls, _ORIGINAL_INIT, cls.__init__)
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

    parser.add_argument('-n', '--name', help='main dat class name', default='Object')
    parser.add_argument('-r', '--recursive', help='recursive generate dat class', action='store_true')
    parser.add_argument('-f', '--input', help='input file - likes-json')
    parser.add_argument('-o', '--output', help='output file - *.py')

    args = parser.parse_args()

    name = args.name
    recursive = args.recursive
    input_ = args.input
    output = args.output

    if input_:
        f = Path(input_)
        if not f.exists():
            print(f'{f.absolute()} not exists')
            return
        text = f.read_text()
    else:
        print('请粘贴 JSON 字符串：CTRL + C 结束')
        data = []
        try:
            while True:
                data.append(input(str(len(data) + 1)))
        except KeyboardInterrupt:
            text = '\n'.join(data)

    try:
        body = json.loads(text)
    except json.JSONDecodeError:
        print('无效 JSON 数据')
        return

    # TODO
    dat = ''

    if output:
        f = Path(output)
        f.parent.mkdir(exist_ok=True, parents=True)
        f.write_text(dat)
    else:
        print(dat)

    print('🎉 Generate successful')
