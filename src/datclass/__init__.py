"""
`datclass` addresses two main issues:
1. `dataclasses.dataclass` cannot recursively convert nested dataclasses.
2. It raises an exception when undefined fields are encountered.
"""

__title__ = 'datclass'
__author__ = 'foyoux'
__version__ = '0.0.1'

__all__ = [
    'DatClass',
    'get_datclass',
    'main',
]

import argparse
import json
import logging
import os
from dataclasses import is_dataclass
from pathlib import Path
from typing import Dict, ClassVar, Callable

from datclass.utils import get_ok_identifier

try:
    from typing import get_origin, get_args
except ImportError:
    from typing_extensions import get_origin, get_args

# Original Constructor Name
# Naming should follow the conventions in `dataclasses.dataclass`, such as `_FIELDS`, `_PARAMS`, etc.
_ORIGINAL_INIT_NAME = '__datclass_init__'

# Internal logs
_log = logging.getLogger('datclass')
_handler = logging.StreamHandler()
_handler.setFormatter(
    logging.Formatter(
        fmt=f'%(asctime)s datclass.%(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
)
_log.addHandler(_handler)


def get_datclass(
        nested: bool = True, extra: bool = True, log: bool = True,
        ok_identifier: Callable[[str], str] = get_ok_identifier,
):
    """Get a decorator that can be used to convert a dataclass to a datclass.

    :param nested: Whether to recursively convert nested dataclasses.
    :param extra: Whether to extend fields.
    :param log: Whether to log missing fields, including undefined fields.
    :param ok_identifier: A function that maps any field name to a valid Python field name.
    :return: A class that extends a dataclass.
    """

    def __datclass_init__(obj, *args, **kwargs):
        """A new constructor that extends the original constructor.

        :param obj: Instances of a class that inherits from __dataclass__.
        :param args:
        :param kwargs:
        :return:
        """
        cls = obj.__class__
        # All code assumes that "cls" is a dataclass and a subclass of "__dataclass__",
        # eliminating the need for further checks.
        frozen = cls.__dataclass_params__.frozen
        # Map any field name to a valid Python field name.
        if kwargs:
            kwargs = {cls.__rename_attrs__.get(k, k): v for k, v in kwargs.items()}
        # Call the original constructor.
        getattr(obj, _ORIGINAL_INIT_NAME)(*args, **{k: kwargs.pop(k) for k in obj.__dataclass_fields__ if k in kwargs})
        # Extend fields or log missing fields, including undefined fields.
        if (extra or log) and kwargs:
            for attr, value in kwargs.items():
                ok_attr = ok_identifier(attr)
                if log:
                    _log.warning(f'{cls.__module__}.{cls.__name__}({ok_attr}: {type(value).__name__} = {value!r})'
                                 f'{"" if ok_attr == attr else f"  # rename from {attr!r}"}')
                if not frozen and extra:
                    setattr(obj, ok_attr, value)
                    if ok_attr != attr and ok_attr not in obj.__rename_attrs__:
                        obj.__rename_attrs__[attr] = ok_attr

    def __to_item__(v, ignore_none=False):
        """Convert v to a dictionary or a list.

        :param v:
        :param ignore_none: Ignore values that are None.
        :return:
        """
        if isinstance(v, __datclass__):
            v = v.to_dict(ignore_none=ignore_none)
        elif isinstance(v, list):
            v = [__to_item__(i, ignore_none=ignore_none) for i in v]
        return v

    # noinspection PyPep8Naming
    class __datclass__:
        def __new__(cls, *args, **kwargs):
            """Modify the `__init__` function to support extended attributes."""
            if not hasattr(cls, _ORIGINAL_INIT_NAME):
                # Each time an object is instantiated, it enters the `__new__` method;
                # let's add a conditional check here.
                setattr(cls, _ORIGINAL_INIT_NAME, cls.__init__)
                setattr(cls, '__init__', __datclass_init__)
            return super().__new__(cls)

        # noinspection PyUnusedLocal
        def __post_init__(self, *args, **kwargs):
            """Handling nested dataclasses. The `__post_init__` in subclasses must call this method,
            otherwise nested dataclasses cannot be processed."""
            if not nested:
                return
            for attr_name, field in self.__dataclass_fields__.items():  # type: ignore
                origin = get_origin(field.type)
                if origin is None and is_dataclass(field.type):
                    attr = getattr(self, attr_name)
                    setattr(self, attr_name, attr if is_dataclass(attr) else (field.type(**attr) if attr else None))
                    continue
                for item_type in get_args(field.type):
                    if is_dataclass(item_type):
                        setattr(self, attr_name,
                                [i if is_dataclass(i) else item_type(**i) for i in getattr(self, attr_name) or []])

        # Original field name -> Valid Python field name after renaming
        __rename_attrs__: ClassVar[Dict[str, str]] = {}

        @classmethod
        def from_str(cls, text: str):
            """Create an instance from a JSON string."""
            return cls(**json.loads(text))

        def to_str(self, ensure_ascii=True, indent=None, ignore_none=False, sort_keys=False,
                   recursive_ignore=True) -> str:
            """Convert an instance to a JSON string.

            :param ensure_ascii: same as json dumps
            :param indent: same as json dumps
            :param ignore_none: Ignore values that are None.
            :param sort_keys: same as json dumps
            :param recursive_ignore: Ignore values that are None recursively.
            :return:
            """
            data_dict = self.to_dict(ignore_none=ignore_none, recursive_ignore=recursive_ignore)
            return json.dumps(data_dict, ensure_ascii=ensure_ascii, indent=indent, sort_keys=sort_keys)

        def to_dict(self, ignore_none=False, recursive_ignore=True) -> dict:
            """Convert an instance to a dictionary.

            :param ignore_none: Ignore values that are None.
            :param recursive_ignore: Ignore values that are None recursively.
            :return:
            """
            result_dict = {}
            object_attrs = {}
            rename_attrs_inverse = {v: k for k, v in self.__rename_attrs__.items()}

            if hasattr(self, '__slots__'):
                object_attrs.update({k: getattr(self, k) for k in self.__slots__})
            object_attrs.update(self.__dict__)

            for attr_name, attr_value in object_attrs.items():
                if attr_value is None and ignore_none:
                    continue
                target_attr_name = rename_attrs_inverse.get(attr_name, attr_name)
                transformed_value = __to_item__(attr_value, ignore_none=ignore_none and recursive_ignore)
                result_dict[target_attr_name] = transformed_value

            return result_dict

        @classmethod
        def from_file(cls, file_path: str, encoding: str = 'utf8'):
            """Create an instance from a JSON file."""
            text = Path(file_path).read_text(encoding=encoding)
            return cls.from_str(text)

        def to_file(self, file_path: str, encoding: str = 'utf8', ensure_ascii=True, indent=None, ignore_none=False,
                    sort_keys=False):
            """Convert an instance to a JSON file.

            :param file_path: Save file path.
            :param encoding: same as json dumps
            :param ensure_ascii: same as json dumps
            :param indent: same as json dumps
            :param ignore_none: Ignore values that are None.
            :param sort_keys: same as json dumps
            :return:
            """
            Path(file_path).write_text(self.to_str(ensure_ascii=ensure_ascii, indent=indent, ignore_none=ignore_none,
                                                   sort_keys=sort_keys), encoding=encoding)

    return __datclass__


DatClass = get_datclass()


def main():
    """Automatically generate DataClass script entry."""
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

    # dataclass kwargs
    parser.add_argument('--dataclass-kwargs', default='{}',
                        help='Dataclass decorator parameters should be passed using a JSON string.', type=json.loads)

    args = parser.parse_args()

    name = args.name
    recursive = args.recursive
    input_file = args.file
    output_file = args.output
    sort = args.no_sort
    dataclass_kwargs = args.dataclass_kwargs

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

    from datclass.__main__ import Generator
    gen = Generator()

    if args.dict:
        codes = gen.gen_typed_dict(body, name, recursive, sort=sort).codes
    else:
        codes = gen.gen_datclass(body, name, recursive, sort=sort, dataclass_kwargs=dataclass_kwargs).codes

    dat = '\n'.join(gen.imports.codes + codes + [''])

    # add example code
    dat += f"""

    if __name__ == '__main__':
        obj = {name}.from_file({os.path.abspath(input_file)!r})
        print(obj)
"""

    if output_file:
        f = Path(output_file)
        f.parent.mkdir(exist_ok=True, parents=True)
        f.write_text(dat, encoding='utf8')
    else:
        print('🎉 Generate result:')
        print(dat)

    print('🎉 Generate successful')
