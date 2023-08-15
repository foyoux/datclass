import hashlib
import keyword
import string

try:
    from typing import get_origin, get_args
except ImportError:
    from typing_extensions import get_origin, get_args
_NAME_MAP = {}


def get_md5_identifier(name, length=8):
    s = hashlib.md5(name.encode()).hexdigest()
    return f'a_{s[:length]}'  # attribute


def get_ok_identifier(name: str):
    # 查询缓存
    if name in _NAME_MAP:
        return _NAME_MAP[name]

    # 处理双(多)下划线开头字段，替换为一个
    if name.startswith('__'):
        name = '_' + name.lstrip('_')

    # 如果是关键字，则加 '_' 后缀
    if keyword.iskeyword(name):
        s = f'{name}_'
    elif name.isidentifier():
        # 关键字是合法标识符，所以先判断关键字，再判断标识符
        s = name
    else:
        # 先替换 "-" 为 "_"
        name = name.replace('-', '_')
        # 不是标准标识符，过滤掉除 下划线、大小写字母、数字 的其他字符
        s = ''.join(filter(lambda c: c in '_' + string.ascii_letters + string.digits, name))
        if s:
            if s[0] in string.digits:
                s = f'a_{s}'  # attribute
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
