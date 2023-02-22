__title__ = 'datclass'
__author__ = 'foyoux'
__version__ = '0.0.1'
__all__ = ['main', 'DatClass', 'List', 'Dict', 'Union', 'get_origin', 'get_args', 'dataclass', 'field', 'is_dataclass']

import argparse
import json
import os
from dataclasses import dataclass, is_dataclass, field
from pathlib import Path
from typing import List, Dict, Union

try:
    from typing import get_origin, get_args
except ImportError:
    from typing_extensions import get_origin, get_args

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


def get_v_type(v, none_type=str):
    if v is None:
        return none_type
    if isinstance(v, dict):
        return Dict
    if isinstance(v, list):
        t_set = set()
        for i in v:
            if isinstance(i, dict):
                t_set.add(dict)
            elif isinstance(i, list):
                t_set.add(list)
            else:
                t_set.add(type(i))
        if len(t_set) == 1:
            return List[t_set.pop()]
        else:
            return List
    return type(v)


def get_t_default(t):
    o_t = get_origin(t)
    if o_t is list:
        return 'field(default_factory=list)'
    return 'None'


def get_t_string(t):
    if t is Dict:
        return 'Dict'
    if get_origin(t) is list:
        st = get_args(t)
        return f'List[{get_t_string(st[0])}]' if st else 'List'
    return t.__name__


def get_nice_cls_name(field_name: str):
    return field_name.title()


def merge_list_dict(list_dict: List[dict]) -> Dict:
    if not isinstance(list_dict, list):
        raise TypeError(f'({list_dict}) is not list_dict')
    d = {}
    for i in list_dict:
        if not isinstance(i, dict):
            raise TypeError(f'element({i}) of list_dict is not dict')
        for k, v in i.items():
            if k not in d:
                d[k] = v
            elif not d[k] and v:
                d[k] = v
    return d


imports = [
    'from datclass import dataclass, field, List, Dict, DatClass', '', '',
]


def gen_datclass(dat: Union[list, dict], name='Object', recursive=False):
    """
    :param dat: list or dict data
    :param name: main dat class name
    :param recursive: recursive generate dat class
    """
    try:
        dat = merge_list_dict(dat)
    except TypeError:
        pass
    codes = ['@dataclass', f'class {name}(DatClass):']

    for k, v in dat.items():
        v_t = get_v_type(v)
        v_d = get_t_default(v_t)
        t_s = get_t_string(v_t)
        if recursive and v and (isinstance(v, dict) or t_s == 'List[dict]'):
            s = get_nice_cls_name(k)
            if isinstance(v, dict):
                t_s = s
            elif t_s == 'List[dict]':
                t_s = f'List[{s}]'
            codes = gen_datclass(v, s, recursive=True) + ['', ''] + codes
        codes.append(f'    {k}: {t_s} = {v_d}')

    return codes


def main():
    epilog = f'%(prog)s({__version__}) by foyoux(https://github.com/foyoux/datclass)'
    parser = argparse.ArgumentParser(prog='datclass', description='', epilog=epilog)
    parser.add_argument('-v', '--version', action='version', version=epilog)

    parser.add_argument('-n', '--name', help='main dat class name', default='Object')
    parser.add_argument('-r', '--recursive', help='recursive generate dat class', action='store_true')
    parser.add_argument('-o', '--output', help='output file - *.py')
    parser.add_argument('file', nargs='?', help='input file - likes-json')

    args = parser.parse_args()

    name = args.name
    recursive = args.recursive
    file = args.file
    output = args.output

    if file:
        f = Path(file)
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
            print('\n🎉 Bye-Bye')
            return

    try:
        body = json.loads(text)
    except json.JSONDecodeError:
        print('\nInvalid JSON data')
        return

    dat = gen_datclass(body, name, recursive)
    dat = '\n'.join(imports + dat + [''])

    if output:
        f = Path(output)
        f.parent.mkdir(exist_ok=True, parents=True)
        f.write_text(dat)
    else:
        print()
        print(dat)

    print('🎉 Generate successful')
