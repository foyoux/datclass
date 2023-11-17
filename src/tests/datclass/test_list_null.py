from dataclasses import dataclass, field
from typing import List, Dict

from datclass import DatClass


@dataclass
class Response(DatClass):
    httpstatus: int = None
    messages: List = field(default_factory=list)
    status: bool = None
    validateMessages: Dict = None
    validateMessagesShowId: str = None


def test_list_null():
    v1 = Response.from_str(
        """
            {
              "validateMessagesShowId": "_validatorMessage",
              "status": true,
              "httpstatus": 200,
              "messages": [],
              "validateMessages": {}
            }
        """
    )
    assert v1.validateMessagesShowId == '_validatorMessage'
    assert v1.validateMessages == {}
    assert v1.messages == []
    assert v1.httpstatus == 200
    assert v1.status is True
    assert v1 == Response(
        httpstatus=200,
        messages=[],
        status=True,
        validateMessages={},
        validateMessagesShowId='_validatorMessage',
    )
