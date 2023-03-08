import keyword
from dataclasses import dataclass, asdict, field
from typing import Union, List

from datclass.utils import get_ok_identifier, get_value_type, get_type_default, merge_list_dict, get_type_string


@dataclass
class Imports:
    dataclass: bool = False
    field: bool = False
    List: bool = False
    Dict: bool = False
    TypedDict: bool = False
    DatClass: bool = False

    @property
    def codes(self):
        return [f'from datclass import {", ".join([k for k, v in asdict(self).items() if v])}', '', '']


@dataclass
class Attr:
    name: str = None
    type: str = None
    default: str = None
    comment: str = ''

    @property
    def code(self):
        return f'    {self.name}: {self.type} = {self.default}{self.comment}'


@dataclass
class Class:
    name: str = None
    attr_list: List[Attr] = field(default_factory=list)

    @property
    def codes(self, ):
        codes = [f'@datclass', f'class {self.name}(DatClass):']
        for attr in self.attr_list:
            codes.append(attr.code)
        return codes


class DatGen:

    def __init__(self):
        self.class_map = set()
        self.imports = Imports()

    def get_nice_cls_name(self, field_name: str, level=0):
        cls_name = field_name.title().replace('_', '')
        if cls_name in self.class_map:
            cls_name = f'{cls_name}{level}'
        if cls_name == field_name:
            cls_name = f'{cls_name}_'
        if keyword.iskeyword(cls_name):
            cls_name = f'{cls_name}_'
        self.class_map.add(cls_name)
        return cls_name

    def gen_datclass(self, dat: Union[list, dict], name='Object', recursive=False, dict_=False, level=0):
        """
        :param dat: list or dict data
        :param name: main dat class name
        :param recursive: recursive generate datclass
        :param dict_: generate TypedDict class
        :param level: 层级，用以解决 类名 冲突问题
        """
        try:
            dat = merge_list_dict(dat)
        except TypeError:
            pass

        if dict_:
            self.imports.TypedDict = True
            codes = [f'class {name}(TypedDict):']
        else:
            self.imports.dataclass = True
            self.imports.DatClass = True
            codes = ['@dataclass', f'class {name}(DatClass):']

        for k, value in dat.items():
            identifier = get_ok_identifier(k)
            comment = '' if identifier == k else f'  # rename from \'{k}\''
            value_type = get_value_type(value)
            value_default = get_type_default(value_type)
            type_string = get_type_string(value_type)
            if recursive and value and (isinstance(value, dict) or type_string == 'List[dict]'):
                nice_cls_name = self.get_nice_cls_name(identifier, level)
                if isinstance(value, dict):
                    type_string = nice_cls_name
                elif type_string == 'List[dict]':
                    self.imports.List = True
                    type_string = f'List[{nice_cls_name}]'
                codes = self.gen_datclass(
                    value, nice_cls_name, recursive=True, dict_=dict_, level=level + 1
                ) + ['', ''] + codes
            if type_string == 'Dict':
                self.imports.Dict = True
            if dict_:
                codes.append(f'    {identifier}: {type_string}{comment}')
            else:
                if value_default.startswith('field'):
                    self.imports.field = True
                codes.append(f'    {identifier}: {type_string} = {value_default}{comment}')

        return codes

    def gen_typed_dict(self, dat: Union[list, dict], name='Object', recursive=False, level=0):
        try:
            dat = merge_list_dict(dat)
        except TypeError:
            pass
        self.imports.TypedDict = True
        codes = []
        n_t_dict = {}
        for k, v in dat.items():
            v_t = get_value_type(v)
            t_s = get_type_string(v_t)
            if recursive and v and (isinstance(v, dict) or t_s == 'List[dict]'):
                s = self.get_nice_cls_name(get_ok_identifier(k), level)
                if isinstance(v, dict):
                    t_s = s
                elif t_s == 'List[dict]':
                    t_s = f'List[{s}]'
                codes = self.gen_typed_dict(v, s, recursive=True, level=level + 1) + codes
            if t_s == 'Dict':
                self.imports.Dict = True
            if t_s.startswith('List'):
                self.imports.List = True
            n_t_dict[k] = t_s
        s = ', '.join([f'\'{k}\': {v}' for k, v in n_t_dict.items()])
        codes.append(f'{name} = TypedDict(\'{name}\', {{{s}}})')
        return codes
