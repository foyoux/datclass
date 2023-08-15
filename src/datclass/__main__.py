import keyword
from dataclasses import dataclass, field
from typing import Dict, List, Union

from datclass import main
from datclass.utils import get_ok_identifier

try:
    from typing import get_origin, get_args
except ImportError:
    from typing_extensions import get_origin, get_args


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


def not_null(value):
    """[{}] [] {}"""
    if value:
        if isinstance(value, list) and not any(value):
            return False
        return True
    return False


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
                continue
            if d[k] is None:
                d[k] = v
                continue
            if isinstance(v, dict):
                d[k] = merge_list_dict([d[k], v])
                continue
            if isinstance(d[k], list) and isinstance(v, list):
                try:
                    ld = d[k] + v
                    d[k] = [merge_list_dict(ld)]
                except TypeError as e:
                    pass
    return d


@dataclass
class Imports:
    dataclass: bool = False
    field: bool = False
    List: bool = False
    Dict: bool = False
    TypedDict: bool = False
    DatClass: bool = False

    def get_dataclasses_imports(self):
        # from dataclasses import dataclass, field
        tl = []
        if self.dataclass:
            tl.append('dataclass')
        if self.field:
            tl.append('field')
        if tl:
            return [f'from dataclasses import {", ".join(tl)}']
        return []

    def get_typing_imports(self):
        # from typing import List, Dict, TypedDict
        tl = []
        if self.List:
            tl.append('List')
        if self.Dict:
            tl.append('Dict')
        if self.TypedDict:
            tl.append('TypedDict')
        if tl:
            return [f'from typing import {", ".join(tl)}']
        return []

    def get_datclass_imports(self):
        # from datclass import DatClass
        if self.DatClass:
            return ['from datclass import DatClass']
        return []

    @property
    def codes(self):
        dataclasses_imports = self.get_dataclasses_imports()
        typing_imports = self.get_typing_imports()
        datclass_imports = self.get_datclass_imports()
        tl = []
        if dataclasses_imports:
            tl += dataclasses_imports
        if typing_imports:
            tl += typing_imports
        if datclass_imports:
            if tl:
                tl += [''] + datclass_imports
            else:
                tl += datclass_imports
        return tl + ['', '']


@dataclass(order=True)
class Attr:
    name: str  # attr name
    value: object  # attr value
    # 值类型
    value_type: type = None
    # 缓存
    ok_name: str = None
    comment: str = None
    type_string: str = None
    default_string: str = None

    def __post_init__(self):
        self.ok_name = get_ok_identifier(self.name)
        self.comment = '' if self.name == self.ok_name else f'  # rename from {self.name!r}'
        self.value_type = get_value_type(self.value)
        self.default_string = get_type_default(self.value_type)
        self.type_string = get_type_string(self.value_type)

    @property
    def code(self):
        return f'    {self.ok_name}: {self.type_string} = {self.default_string}{self.comment}'


@dataclass
class Class:
    name: str = None
    sort: bool = None
    attrs: List[Attr] = field(default_factory=list)
    classes: List['Class'] = field(default_factory=list)

    @property
    def codes(self):
        codes = [f'@dataclass', f'class {self.name}(DatClass):']
        for attr in sorted(self.attrs) if self.sort else self.attrs:  # type: ignore
            codes.append(attr.code)
        # 处理 __rename_attrs__
        rename_attrs = [attr for attr in self.attrs if attr.name != attr.ok_name]
        if rename_attrs:
            codes.append('')
            codes.append('    __rename_attrs__ = {')
            codes.extend([f'        {attr.name!r}: {attr.ok_name!r},' for attr in rename_attrs])
            codes.append('    }')
        for cls in self.classes:
            codes = cls.codes + ['', ''] + codes
        return codes


@dataclass(order=True)
class DictAttr:
    name: str
    value: object
    # 值类型
    value_type: type = None
    type_string: str = None

    def __post_init__(self):
        self.value_type = get_value_type(self.value)
        self.type_string = get_type_string(self.value_type)

    @property
    def code(self):
        return f'{self.name!r}: {self.type_string}'


@dataclass
class DictClass:
    name: str = None
    sort: bool = None
    attr_list: List[DictAttr] = field(default_factory=list)
    classes: List['DictClass'] = field(default_factory=list)

    @property
    def codes(self):
        attr_string = ', '.join(
            [attr.code for attr in (sorted(self.attr_list) if self.sort else self.attr_list)])  # type: ignore
        codes = [f'{self.name} = TypedDict({self.name!r}, {{{attr_string}}})']
        for cls in self.classes:
            codes = cls.codes + codes
        return codes


class DatGen:

    def __init__(self):
        # 记录导入，当重复时，根据层级 level 重命名
        self.class_map = []
        # 记录导入
        self.imports = Imports()

    def get_nice_cls_name(self, attr_name: str, level=0) -> str:
        """根据属性名获取一个合适的类名"""
        cls_name = attr_name.title().replace('_', '')
        if cls_name in self.class_map:
            # 重复则重命名，尾加 level
            cls_name = f'{cls_name}{level}'
        if cls_name == attr_name:
            # 类名与属性名重名，则尾加下划线（此种情况现已不存在，因为属性名的首字母会置为小写）
            cls_name = f'{cls_name}_'
        if keyword.iskeyword(cls_name):
            # 是关键字（eg: None），则加下划线
            cls_name = f'{cls_name}_'
        # 返回之前先记录
        return cls_name

    def gen_datclass(self, dat: Union[list, dict], name='Object', recursive=True, sort=True, level=0) -> Class:
        """
        :param dat: 列表 或者 字典
        :param name: 主类名称
        :param recursive: 是否递归生成
        :param sort: 是否对属性列表进行排序
        :param level: 层级，用以解决 类名 冲突问题
        """
        assert dat
        self.class_map.append(name)
        try:
            dat = merge_list_dict(dat)
        except TypeError as e:
            pass
        # 这些针对模块
        self.imports.dataclass = True
        self.imports.DatClass = True
        # 存储类信息
        obj = Class(name=name, sort=sort)
        for name, value in dat.items():
            # 存储属性信息
            attr = Attr(name, value)
            # 如果是 列表 或者 字典，且递归为真，则递归处理
            if recursive and not_null(value) and (isinstance(value, dict) or attr.type_string == 'List[dict]'):
                nice_cls_name = self.get_nice_cls_name(attr.ok_name, level)
                if isinstance(value, dict):
                    attr.type_string = nice_cls_name
                elif attr.type_string == 'List[dict]':
                    self.imports.List = True
                    attr.type_string = f'List[{nice_cls_name}]'
                # 递归处理
                obj.classes.append(self.gen_datclass(value, nice_cls_name, recursive=True, sort=sort, level=level + 1))
            # 如果类型是 Dict，则导入 Dict
            if attr.type_string == 'Dict':
                self.imports.Dict = True
            if attr.type_string.startswith('List'):
                self.imports.List = True
            # 如果默认值有 field，则导入 field
            if attr.default_string.startswith('field'):
                self.imports.field = True
            obj.attrs.append(attr)
        return obj

    def gen_typed_dict(self, dat: Union[list, dict], name='Object', recursive=True, sort=True, level=0) -> DictClass:
        """生成 "Response = TypedDict('Response', {'update_id': int, 'message': Message})" 形式的字典约束（代码提示）类"""
        assert dat
        try:
            dat = merge_list_dict(dat)
        except TypeError as e:
            pass
        self.imports.TypedDict = True
        obj = DictClass(name=name, sort=sort)
        for name, value in dat.items():
            attr = DictAttr(name, value)
            if recursive and not_null(value) and (isinstance(value, dict) or attr.type_string == 'List[dict]'):
                nice_cls_name = self.get_nice_cls_name(get_ok_identifier(name), level)
                if isinstance(value, dict):
                    attr.type_string = nice_cls_name
                elif attr.type_string == 'List[dict]':
                    attr.type_string = f'List[{nice_cls_name}]'
                obj.classes.append(
                    self.gen_typed_dict(value, nice_cls_name, recursive=True, sort=sort, level=level + 1))
            if attr.type_string == 'Dict':
                self.imports.Dict = True
            if attr.type_string.startswith('List'):
                self.imports.List = True
            obj.attr_list.append(attr)
        return obj


if __name__ == '__main__':
    main()
