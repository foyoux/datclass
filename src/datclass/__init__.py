__title__ = 'datclass'
__author__ = 'foyoux'
__version__ = '0.0.1'
__all__ = [
    'main',
    'DatClass',
    'List',
    'Dict',
    'Union',
    'TypedDict',
    'get_origin',
    'get_args',
    'dataclass',
    'field',
    'is_dataclass',
    'set_debug',
]

import argparse
import hashlib
import json
import keyword
import os
import string
from dataclasses import dataclass, is_dataclass, field, asdict
from pathlib import Path
from typing import List, Dict, Union

try:
    from typing import get_origin, get_args, TypedDict
except ImportError:
    from typing_extensions import get_origin, get_args, TypedDict

_DEBUG = False
_NAME_MAP = {}
_ORIGINAL_INIT = '__dataclass_init__'


def set_debug(b):
    global _DEBUG
    _DEBUG = b


def _get_md5_identifier(name, length=8):
    s = hashlib.md5(name.encode()).hexdigest()
    return f'a_{s[:length]}'  # attribute


def get_ok_identifier(name: str):
    # 查询缓存
    if name in _NAME_MAP:
        return _NAME_MAP[name]

    # 如果是关键字，则加 '_' 后缀
    if keyword.iskeyword(name):
        s = f'{name}_'
    elif name.isidentifier():
        # 关键字是合法标识符，所以先判断关键字，再判断标识符
        s = name
    else:
        # 不是标准标识符，过滤掉除 下划线、大小写字母、数字 的其他字符
        s = ''.join(filter(lambda c: c in '_' + string.ascii_letters + string.digits, name))
        if s:
            if s[0] in string.digits:
                s = f'a_{s}'
            elif keyword.iskeyword(s):
                s = f'{s}_'
            elif not s.isidentifier():
                s = _get_md5_identifier(name)
        else:
            s = _get_md5_identifier(name)

    # 返回之前进行缓存
    _NAME_MAP[name] = s
    return s


def _datclass_init(self, *args, **kwargs):
    if kwargs:
        kwargs = {get_ok_identifier(k): v for k, v in kwargs.items()}

    if _DEBUG:
        getattr(self, _ORIGINAL_INIT)(*args, **kwargs)
    else:
        getattr(self, _ORIGINAL_INIT)(
            *args, **{k: kwargs.pop(k) for k in self.__dataclass_fields__ if k in kwargs}
        )
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
    return field_name.title().replace('_', '')


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
            elif d[k] and isinstance(v, dict):
                d[k] = merge_list_dict([d[k], v])
            elif not d[k] and v:
                d[k] = v
    return d


@dataclass
class Imports:
    dataclass: bool = False
    field: bool = False
    List: bool = False
    Dict: bool = False
    TypedDict: bool = False
    DatClass: bool = False

    def to_list(self):
        return [f'from datclass import {", ".join([k for k, v in asdict(self).items() if v])}', '', '']


imports = Imports()


def gen_datclass(dat: Union[list, dict], name='Object', recursive=False, dict_=False):
    """
    :param dat: list or dict data
    :param name: main dat class name
    :param recursive: recursive generate datclass
    :param dict_: generate TypedDict class
    """
    try:
        dat = merge_list_dict(dat)
    except TypeError:
        pass

    if dict_:
        imports.TypedDict = True
        codes = [f'class {name}(TypedDict):']
    else:
        imports.dataclass = True
        imports.DatClass = True
        codes = ['@dataclass', f'class {name}(DatClass):']

    for k_, v in dat.items():
        k = get_ok_identifier(k_)
        c = '' if k == k_ else f'  # rename from \'{k_}\''
        v_t = get_v_type(v)
        v_d = get_t_default(v_t)
        t_s = get_t_string(v_t)
        if recursive and v and (isinstance(v, dict) or t_s == 'List[dict]'):
            s = get_nice_cls_name(k)
            if isinstance(v, dict):
                t_s = s
            elif t_s == 'List[dict]':
                imports.List = True
                t_s = f'List[{s}]'
            codes = gen_datclass(v, s, recursive=True, dict_=dict_) + ['', ''] + codes
        if t_s == 'Dict':
            imports.Dict = True
        if dict_:
            codes.append(f'    {k}: {t_s}{c}')
        else:
            if v_d.startswith('field'):
                imports.field = True
            codes.append(f'    {k}: {t_s} = {v_d}{c}')

    return codes


def gen_typed_dict(dat: Union[list, dict], name='Object', recursive=False):
    try:
        dat = merge_list_dict(dat)
    except TypeError:
        pass
    imports.TypedDict = True
    codes = []
    n_t_dict = {}
    for k, v in dat.items():
        v_t = get_v_type(v)
        t_s = get_t_string(v_t)
        if recursive and v and (isinstance(v, dict) or t_s == 'List[dict]'):
            s = get_nice_cls_name(k)
            if isinstance(v, dict):
                t_s = s
            elif t_s == 'List[dict]':
                t_s = f'List[{s}]'
            codes = gen_typed_dict(v, s, recursive=True) + codes
        if t_s == 'Dict':
            imports.Dict = True
        if t_s.startswith('List'):
            imports.List = True
        n_t_dict[k] = t_s
    s = ', '.join([f'\'{k}\': {v}' for k, v in n_t_dict.items()])
    codes.append(f'{name} = TypedDict(\'{name}\', {{{s}}})')
    return codes


def main():
    epilog = f'%(prog)s({__version__}) by foyoux(https://github.com/foyoux/datclass)'
    parser = argparse.ArgumentParser(prog='datclass', description='generate datclass & support nested and extra',
                                     epilog=epilog)
    parser.add_argument('-v', '--version', action='version', version=epilog)

    parser.add_argument('-n', '--name', help='main dat class name', default='Object')
    parser.add_argument('-r', '--recursive', help='recursive generate dat class', action='store_true')
    parser.add_argument('-o', '--output', help='output file - *.py')
    parser.add_argument('-d', '--dict', help='generate TypedDict class', action='store_true')
    parser.add_argument('-i', '--inline', help='use inline model to generate TypedDict type', action='store_true')
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

    if args.dict and args.inline:
        dat = gen_typed_dict(body, name, recursive)
    else:
        dat = gen_datclass(body, name, recursive, args.dict)

    dat = '\n'.join(imports.to_list() + dat + [''])

    if output:
        f = Path(output)
        f.parent.mkdir(exist_ok=True, parents=True)
        f.write_text(dat)
    else:
        print()
        print(dat)

    print('🎉 Generate successful')
