from datclass.__main__ import merge_list_dict

data = [
    {
        'name': 'Macaron',
        'tags': [
            {'t1': '111'},
            {'t2': '222'},
        ]
    },
    {
        'price': '$2.0',
        'tags': [
            {'t3': '333'},
            {'t4': '444'},
        ]
    },
]


def test_merge_list_dict2():
    x = merge_list_dict(data)
    assert x == {'name': 'Macaron', 'tags': [{'t1': '111', 't2': '222', 't3': '333', 't4': '444'}], 'price': '$2.0'}
