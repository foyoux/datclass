from dataclasses import dataclass, is_dataclass
from typing import get_type_hints, get_origin, get_args


@dataclass
class DatClass:
    def __post_init__(self, *args, **kwargs):
        attrs = get_type_hints(self)
        for attr_name, attr_type in attrs.items():
            origin = get_origin(attr_type)
            if origin is None and is_dataclass(attr_type):
                setattr(self, attr_name, attr_type(**getattr(self, attr_name)))
                continue
            for item_type in get_args(attr_type):
                setattr(self, attr_name, [item_type(**i) for i in getattr(self, attr_name)])
