import keyword
from dataclasses import dataclass, asdict
from typing import Union

from datclass.utils import get_ok_identifier, get_v_type, get_t_default, merge_list_dict, get_t_string


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


class DatclassGenerator:

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

        for k_, v in dat.items():
            k = get_ok_identifier(k_)
            c = '' if k == k_ else f'  # rename from \'{k_}\''
            v_t = get_v_type(v)
            v_d = get_t_default(v_t)
            t_s = get_t_string(v_t)
            if recursive and v and (isinstance(v, dict) or t_s == 'List[dict]'):
                s = self.get_nice_cls_name(k, level)
                if isinstance(v, dict):
                    t_s = s
                elif t_s == 'List[dict]':
                    self.imports.List = True
                    t_s = f'List[{s}]'
                codes = self.gen_datclass(v, s, recursive=True, dict_=dict_, level=level + 1) + ['', ''] + codes
            if t_s == 'Dict':
                self.imports.Dict = True
            if dict_:
                codes.append(f'    {k}: {t_s}{c}')
            else:
                if v_d.startswith('field'):
                    self.imports.field = True
                codes.append(f'    {k}: {t_s} = {v_d}{c}')

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
            v_t = get_v_type(v)
            t_s = get_t_string(v_t)
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
