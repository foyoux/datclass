from datclass.utils import merge_list_dict

data = [
    {
        'name': '马卡龙',
        'tags': [
            {'t1': '111'},
            {'t2': '222'},
        ]
    },
    {
        'price': '￥10.0',
        'tags': [
            {'t3': '333'},
            {'t4': '444'},
        ]
    },
]


def test_merge_list_dict2():
    x = merge_list_dict(data)
    assert x == {'name': '马卡龙', 'tags': [{'t1': '111', 't2': '222', 't3': '333', 't4': '444'}], 'price': '￥10.0'}
