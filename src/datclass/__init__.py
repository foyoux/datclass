__title__ = 'datclass'
__author__ = 'foyoux'
__version__ = '0.0.1'

__all__ = [
    'DatClass',
    'get_datclass',
]

import json
import logging
from dataclasses import dataclass, is_dataclass, asdict, astuple
from pathlib import Path
from typing import Dict, ClassVar, Callable

from datclass.__main__ import get_ok_identifier

try:
    from typing import get_origin, get_args
except ImportError:
    from typing_extensions import get_origin, get_args

# 常量
_ORIGINAL_INIT = '__datclass_init__'

# 日志
_log = logging.getLogger('datclass')
_handler = logging.StreamHandler()
_handler.setFormatter(
    logging.Formatter(
        fmt=f'%(asctime)s datclass.%(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
)
_log.addHandler(_handler)


def get_datclass(nested: bool = True, extra: bool = True, log: bool = True,
                 ok_identifier: Callable[[str], str] = get_ok_identifier):
    def __datclass_init__(obj, *args, **kwargs):
        cls = obj.__class__
        # 任意字段名映射为合法 Python 字段名
        if kwargs:
            kwargs = {cls.__rename_attrs__.get(k, k): v for k, v in kwargs.items()}
        # 调用原构造函数
        getattr(obj, _ORIGINAL_INIT)(*args, **{k: kwargs.pop(k) for k in obj.__dataclass_fields__ if k in kwargs})
        # 扩展字段或者打印缺失字段日志，并且有未定义的字段
        if (extra or log) and kwargs:
            for attr, value in kwargs.items():
                ok_attr = ok_identifier(attr)
                if log:
                    _log.warning(f'{cls.__module__}.{cls.__name__}({ok_attr}: {type(value).__name__} = {value!r})'
                                 f'{"" if ok_attr == attr else f"  # rename from {attr!r}"}')
                if extra:
                    setattr(obj, ok_attr, value)
                    if ok_attr != attr and ok_attr not in obj.__rename_attrs__:
                        obj.__rename_attrs__[attr] = ok_attr

    def __to_value__(v, ignore_none=False):
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
                vl.append(__to_value__(i, ignore_none=ignore_none))
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
            for attr_name, field in self.__dataclass_fields__.items():  # type: ignore
                origin = get_origin(field.type)
                if origin is None and is_dataclass(field.type):
                    attr = getattr(self, attr_name)
                    setattr(self, attr_name, attr if is_dataclass(attr) else field.type(**attr) if attr else None)
                    continue
                for item_type in get_args(field.type):
                    if is_dataclass(item_type):
                        setattr(self, attr_name,
                                [i if is_dataclass(i) else item_type(**i) for i in getattr(self, attr_name) or []])

        # 原始字段名 -> 重命名之后的合法 Python 字段名
        __rename_attrs__: ClassVar[Dict[str, str]] = {}

        @classmethod
        def from_str(cls, text: str):
            return cls(**json.loads(text))

        def to_str(self, ensure_ascii=True, indent=None, ignore_none=False, sort_keys=False) -> str:
            return json.dumps(self.to_dict(ignore_none=ignore_none), ensure_ascii=ensure_ascii, indent=indent,
                              sort_keys=sort_keys)

        def to_dict(self, ignore_none=False) -> dict:
            d = {}
            revert_rename_attrs = {v: k for k, v in self.__rename_attrs__.items()}
            for k, v in self.__dict__.items():
                if ignore_none and v is None:
                    continue
                d[revert_rename_attrs.get(k, k)] = __to_value__(v, ignore_none=ignore_none)
            return d

        def to_tuple(self) -> tuple:
            return astuple(self)

        @classmethod
        def from_file(cls, file_path: str, encoding: str = 'utf8'):
            text = Path(file_path).read_text(encoding=encoding)
            return cls.from_str(text)

        def to_file(self, file_path: str, encoding: str = 'utf8', ensure_ascii=True, indent=None, ignore_none=False,
                    sort_keys=False):
            Path(file_path).write_text(self.to_str(ensure_ascii=ensure_ascii, indent=indent, ignore_none=ignore_none,
                                                   sort_keys=sort_keys), encoding=encoding)

    return __datclass__


DatClass = get_datclass()
