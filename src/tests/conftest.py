import pytest


@pytest.fixture
def data():
    return {
        "update_id": 1,
        "message": {
            "message_id": 5,
            "2&*(U3sadsb": {
                "id": 1,
                "is_bot": False,
                "first_name": "first_name",
                "((12&*(U3sadsbj%^%$^*(": "last_name",
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
                "is_bot": True,
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


@pytest.fixture
def testdata2():
    """to_dict extra test"""
    return {
        "code": 200,
        "message": "success",
        "data": {
            "ext": {},
            "abtest": {
                "case_code": "171^v3^default_word_new"
            },
            "size": 1,
            "items": [
                {
                    "username": None,
                    "product_id": "dataclass",
                    "product_type": "hot_word",
                    "resource_id": "",
                    "style": "word_1",
                    "strategy_id": "alirecmd",
                    "ext": {},
                    "report_data": {
                        "eventClick": True,
                        "data": {
                            "mod": "",
                            "extra": "ednsjk",
                            "dist_request_id": "1691760495554_17246",
                            "ab_strategy": "default",
                            "index": "1",
                            "strategy": "alirecmd"
                        },
                        "urlParams": {
                            "utm_medium": "xsnjck",
                            "depth_1_utm_source": "csd9wn"
                        },
                        "eventView": True
                    },
                    "recommend_type": "ali",
                    "media_asset_info": None,
                    "media_asset_info_v2": None,
                    "task_id": None,
                    "index": 1,
                    "product_id_and_product_type": "dataclass-null-null",
                    "debug_ext": None,
                    "ad_resource_info": None,
                    "redpacket_order_no": None,
                    "csdn_tags": None
                }
            ]
        }
    }
