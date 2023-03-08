import hashlib
import keyword
import string
from typing import Dict, List

try:
    from typing import get_origin, get_args, TypedDict
except ImportError:
    from typing_extensions import get_origin, get_args, TypedDict

_NAME_MAP = {}


def get_md5_identifier(name, length=8):
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
                s = get_md5_identifier(name)
        else:
            s = get_md5_identifier(name)

    # 将首字母转为小写
    if s[0] in string.ascii_uppercase:
        s = s[0].lower() + s[1:]

    # 返回之前进行缓存
    _NAME_MAP[name] = s
    return s


def get_value_type(v, none_type=str):
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


def get_type_default(t):
    t = get_origin(t)
    if t is list:
        return 'field(default_factory=list)'
    return 'None'


def get_type_string(t):
    if t is Dict:
        return 'Dict'
    if get_origin(t) is list:
        st = get_args(t)
        return f'List[{get_type_string(st[0])}]' if st and not isinstance(None, st) else 'List'
    return t.__name__


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
