from dataclasses import dataclass, field
from typing import List, Dict, ClassVar

from datclass import DatClass


@dataclass
class CaptionEntities(DatClass):
    length: int = None
    offset: int = None
    type: str = None
    url: str = None


@dataclass
class Thumb(DatClass):
    file_id: str = None
    file_size: int = None
    file_unique_id: str = None
    height: int = None
    width: int = None


@dataclass
class Video(DatClass):
    duration: int = None
    file_id: str = None
    file_size: int = None
    file_unique_id: str = None
    height: int = None
    mime_type: str = None
    thumb: Thumb = None
    width: int = None


@dataclass
class ForwardFrom(DatClass):
    first_name: str = None
    id: int = None
    is_bot: bool = None
    username: str = None


@dataclass
class Chat(DatClass):
    first_name: str = None
    id: int = None
    last_name: str = None
    type: str = None
    username: str = None


@dataclass
class A2U3Sadsb(DatClass):
    a_12U3sadsbj: str = None  # rename from '((12&*(U3sadsbj%^%$^*('
    first_name: str = None
    id: int = None
    is_bot: bool = None
    language_code: str = None
    username: str = None

    __rename_attrs__: ClassVar[Dict[str, str]] = {
        '((12&*(U3sadsbj%^%$^*(': 'a_12U3sadsbj',
    }


@dataclass
class Message(DatClass):
    a_2U3sadsb: A2U3Sadsb = None  # rename from '2&*(U3sadsb'
    caption: str = None
    caption_entities: List[CaptionEntities] = field(default_factory=list)
    chat: Chat = None
    date: int = None
    forward_date: int = None
    forward_from: ForwardFrom = None
    message_id: int = None
    video: Video = None

    __rename_attrs__: ClassVar[Dict[str, str]] = {
        '2&*(U3sadsb': 'a_2U3sadsb',
    }


@dataclass
class XXObject(DatClass):
    message: Message = None
    update_id: int = None


def test_revert_rename_attr(data):
    obj = XXObject(**data)
    assert obj.to_dict() == data
