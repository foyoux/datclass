"""`datclass` addresses two main issues:

1. `dataclasses.dataclass` cannot recursively convert nested dataclasses.
2. It raises an exception when undefined fields are encountered.
"""
import json
import logging
import sys
from pathlib import Path
from typing import Dict, ClassVar, Callable, ForwardRef, Union, TypeVar

from .__version__ import *
from .utils import write_file, get_identifier

try:
    from typing import get_origin, get_args
except ImportError:
    from typing_extensions import get_origin, get_args

__all__ = [
    'DatClass',
    'get_datclass',
]

# Original Constructor Name
# Naming should follow the conventions in `dataclasses.dataclass`, such as `_FIELDS`, `_PARAMS`, etc.
_ORIGINAL_INIT_NAME = '__datclass_orig_init__'

# Internal logs
_log = logging.getLogger(__title__)
_handler = logging.StreamHandler()
_handler.setFormatter(
    logging.Formatter(
        fmt=f'%(asctime)s datclass.%(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
)
_log.addHandler(_handler)

NoneType = type(None)


def get_datclass(
        extra: bool = True, log: bool = True,
        identifier_transform: Callable[[str], str] = get_identifier,
        empty_dict_as_none=False, nested: bool = True,
):
    """Get a decorator that can be used to convert a dataclass to a datclass.

    :param extra: Whether to extend fields.
    :param log: Whether to log missing fields, including undefined fields.
    :param identifier_transform: A function that maps any field name to a valid Python field name.
    :param empty_dict_as_none: Convert empty dict to None when converting to a DataClass.
    :param nested: Whether to recursively convert nested dataclasses.
    :return: A class that extends a dataclass.
    """

    def to_item(v, ignore_none=False):
        """Convert v to a dictionary or a list.

        :param v:
        :param ignore_none: Ignore values that are None.
        :return:
        """
        if isinstance(v, Datclass):
            v = v.to_dict(ignore_none=ignore_none)
        elif isinstance(v, list):
            v = [to_item(i, ignore_none=ignore_none) for i in v]
        return v

    def convert_attr_value(value, type_, cls):
        """Convert the value of the attribute.

        :param value:
        :param type_:
        :param cls:
        :return:
        """
        if value is None:
            return None

        if empty_dict_as_none and value == {}:
            return None

        origin = get_origin(type_)

        if origin is None and isinstance(value, dict):
            if hasattr(type_, '__datclass_init__'):
                value = type_(**value)
            elif isinstance(type_, ForwardRef):
                type_ = sys.modules[cls.__module__].__dict__[type_.__forward_arg__]
                if hasattr(type_, '__datclass_init__'):
                    value = type_(**value)
            elif isinstance(type_, str):
                type_ = sys.modules[cls.__module__].__dict__[type_]
                if hasattr(type_, '__datclass_init__'):
                    value = type_(**value)
            elif isinstance(type_, TypeVar):
                type_ = type_.__bound__
                if hasattr(type_, '__datclass_init__'):
                    value = type_(**value)
        elif origin is list:
            type_ = get_args(type_)[0]
            value = [convert_attr_value(i, type_, cls) for i in value]
        elif origin is Union:
            types_ = get_args(type_)
            if len(types_) == 2 and NoneType in types_:
                # Optional
                if types_[0] is NoneType:
                    type_ = types_[1]
                else:
                    type_ = types_[0]
                value = convert_attr_value(value, type_, cls)
        return value

    class Datclass:
        def __new__(cls, *args, **kwargs):
            """Modify the `__init__` function to support extended attributes."""
            if _ORIGINAL_INIT_NAME not in cls.__dict__:
                # Each time an object is instantiated, it enters the `__new__` method;
                # let's add a conditional check here.
                setattr(cls, _ORIGINAL_INIT_NAME, cls.__init__)
                cls.__init__ = cls.__datclass_init__
            return super().__new__(cls)

        def __datclass_init__(self, *args, **kwargs):
            """A new constructor that extends the original constructor.

            :param self: Instances of a class that inherits from __dataclass__.
            :param args:
            :param kwargs:
            :return:
            """
            # All code assumes that "cls" is a dataclass and a subclass of "__dataclass__",
            # eliminating the need for further checks.
            cls = self.__class__
            if cls is Datclass:
                # Handling Generic Types and Creating Objects Directly using DataClass.
                for attr, value in kwargs.items():
                    if empty_dict_as_none and value == {}:
                        value = None
                    setattr(self, attr, value)
                return

            # Map any field name to a valid Python field name.
            kwargs = {cls.__rename_attrs__.get(k, k): v for k, v in kwargs.items()}

            # Call the original constructor.
            original_init = getattr(self, _ORIGINAL_INIT_NAME)
            init_kwargs = {k: kwargs.pop(k) for k in self.__dataclass_fields__ if k in kwargs}  # type: ignore
            original_init(*args, **init_kwargs)

            # Extend fields or log missing fields, including undefined fields.
            if extra or log:
                frozen = cls.__dataclass_params__.frozen  # type: ignore

                for attr, value in kwargs.items():
                    ok_attr = identifier_transform(attr)

                    if log:
                        # Log missing fields, including undefined fields.
                        # Facilitate Timely Data Updates
                        log_message = f'{cls.__module__}.{cls.__name__}({ok_attr}: {type(value).__name__} = {value!r})'
                        if ok_attr != attr:
                            log_message += f'  # rename from {attr!r}'
                        _log.warning(log_message)

                    if not frozen and extra:
                        setattr(self, ok_attr, value)
                        # Record the renaming of fields.
                        if ok_attr != attr and attr not in self.__rename_attrs__:
                            self.__rename_attrs__[attr] = ok_attr

        # noinspection PyUnusedLocal
        def __post_init__(self, *args, **kwargs):
            """Handling nested dataclasses.

            The `__post_init__` in subclasses must call this method, otherwise nested dataclasses cannot be processed.

            About `get_origin` and `get_args`
            --------------------------------
            `get_origin` and `get_args` are used to handle generic types.

            Examples:
                >>> from typing import get_origin, get_args
                >>> from typing import List, Dict, Tuple, Union, Optional
                >>>
                >>> assert get_origin(List[int]) is list
                ... assert get_origin(Dict[str, int]) is dict
                ... assert get_origin(Optional[int]) is Union
                ... # assert get_origin(<other>) is None
                ...
                >>> assert get_args(List[int]) == (int,)
                ... assert get_args(Union[int, str]) == (int, str)
                ... # assert get_args(Optional[int]) == (int, NoneType)
                ...
            """
            if not nested:
                return

            for attr_name, field in self.__dataclass_fields__.items():  # type: ignore
                value = getattr(self, attr_name)
                new_value = convert_attr_value(value, field.type, self.__class__)
                if new_value is not value:
                    setattr(self, attr_name, new_value)

        # Original field name -> Valid Python field name after renaming
        __rename_attrs__: ClassVar[Dict[str, str]] = {}

        @classmethod
        def from_str(cls, text: str):
            """Create an instance from a JSON string."""
            return cls(**json.loads(text))

        @classmethod
        def from_file(cls, file_path: str, encoding: str = 'utf8'):
            """Create an instance from a JSON file."""
            text = Path(file_path).read_text(encoding=encoding)
            return cls.from_str(text)

        def to_dict(self, ignore_none=False, recursive_ignore=True) -> dict:
            """Convert an instance to a dictionary.

            :param ignore_none: Ignore values that are None.
            :param recursive_ignore: Ignore values that are None recursively.
            :return:
            """
            rename_attrs_inverse = {v: k for k, v in self.__rename_attrs__.items()}
            result_dict, object_attrs = {}, {}

            if hasattr(self, '__slots__'):
                object_attrs.update({k: getattr(self, k) for k in self.__slots__})
            object_attrs.update(self.__dict__)

            for attr_name, attr_value in object_attrs.items():
                # Exclude private attributes:
                # '__orig_class__'
                if attr_name.startswith('__'):
                    continue
                if attr_value is None and ignore_none:
                    continue
                target_attr_name = rename_attrs_inverse.get(attr_name, attr_name)
                transformed_value = to_item(attr_value, ignore_none=ignore_none and recursive_ignore)
                result_dict[target_attr_name] = transformed_value

            return result_dict

        def to_str(
                self,
                ensure_ascii=True,
                indent=None,
                ignore_none=False,
                sort_keys=False,
                recursive_ignore=True
        ) -> str:
            """Convert an instance to a JSON string.

            :param ensure_ascii: same as json dumps
            :param indent: same as json dumps
            :param ignore_none: Ignore values that are None.
            :param sort_keys: same as json dumps
            :param recursive_ignore: Ignore values that are None recursively.
            :return:
            """
            data_dict = self.to_dict(
                ignore_none=ignore_none,
                recursive_ignore=recursive_ignore
            )
            json_str = json.dumps(
                data_dict,
                ensure_ascii=ensure_ascii,
                indent=indent,
                sort_keys=sort_keys
            )
            return json_str

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
            Path(file_path).write_text(
                self.to_str(
                    ensure_ascii=ensure_ascii,
                    indent=indent,
                    ignore_none=ignore_none,
                    sort_keys=sort_keys
                ),
                encoding=encoding,
            )

    return Datclass


DatClass = get_datclass()
