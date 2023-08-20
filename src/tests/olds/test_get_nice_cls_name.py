from datclass.__main__ import Generator

dat = """
{
  "update_id": 1,
  "message": {
    "message_id": 5,
    "from": {
      "id": 1,
      "is_bot": false,
      "first_name": "first_name",
      "last_name": "last_name",
      "username": "username",
      "language_code": "zh-hans"
    },
    "chat": {
      "id": 1,
      "first_name": "first_name",
      "last_name": "last_name",
      "username": "username",
      "type": "private"
    },
    "date": 1,
    "forward_from": {
      "id": 1,
      "is_bot": true,
      "first_name": "first_name",
      "username": "username"
    },
    "forward_date": 1,
    "video": {
      "duration": 29,
      "width": 1280,
      "height": 720,
      "mime_type": "video/mp4",
      "thumb": {
        "file_id": "file_id",
        "file_unique_id": "file_unique_id",
        "file_size": 7420,
        "width": 320,
        "height": 180
      },
      "file_id": "file_id",
      "file_unique_id": "file_unique_id",
      "file_size": 3905756
    },
    "caption": "caption",
    "caption_entities": [
      {
        "offset": 0,
        "length": 47,
        "type": "text_link",
        "url": "https://github.com/foyoux/datclass"
      }
    ]
  }
}
"""


def test_underline():
    g = Generator()
    assert g.get_nice_cls_name('forward_from') == 'ForwardFrom'
