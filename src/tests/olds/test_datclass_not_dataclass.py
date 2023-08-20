from dataclasses import dataclass
from typing import Dict, Union

from datclass import DatClass


@dataclass
class BatchSubRequest(DatClass):
    """..."""
    body: Union[DatClass, Dict]
    id: str
    url: str
    headers: Dict = None
    method: str = 'POST'

    def __post_init__(self):
        self.headers = {"Content-Type": "application/json"}
        super().__post_init__()


def test_datclass_not_dataclass():
    BatchSubRequest(
        id='file_id',
        url='/file/delete',
        body={
            'drive_id': 'drive_id',
            'file_id': 'file_id'
        }
    )
