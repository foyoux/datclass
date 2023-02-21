# noinspection PyProtectedMember
from datclass import merge_list_dict


def test_merge_list_dict():
    ld = [
        {
            "url": "https://www.youtube.com/s/gaming/emoji/0f0cae22/emoji_u1f600.svg"
        }
    ]
    assert merge_list_dict(ld) == {
        "url": "https://www.youtube.com/s/gaming/emoji/0f0cae22/emoji_u1f600.svg"
    }
    tasks = [
        {
            "id": "ACC",
            "req_header": "",
            "resource": "https://acc-v4.pops.fastly-insights.com/o.svg?u=<%TEST_ID%>",
            "resp_header": "",
            "type": "pop",
            "weight": 1.021,
            "classification": {}
        },
        {
            "id": "ADL",
            "req_header": "",
            "resource": "https://adl-v4.pops.fastly-insights.com/o.svg?u=<%TEST_ID%>",
            "resp_header": "",
            "type": "pop",
            "weight": 1.408,
            "classification": {}
        },
        {
            "id": "AKL",
            "req_header": "",
            "resource": "https://akl-v4.pops.fastly-insights.com/o.svg?u=<%TEST_ID%>",
            "resp_header": "",
            "type": "pop",
            "weight": 1.742,
            "classification": {}
        },
        {
            "id": "AMS",
            "req_header": "",
            "resource": "https://ams-v4.pops.fastly-insights.com/o.svg?u=<%TEST_ID%>",
            "resp_header": "",
            "type": "pop",
            "weight": 1.35,
            "classification": {}
        },
        {
            "id": "ATL",
            "req_header": "",
            "resource": "https://atl-v4.pops.fastly-insights.com/o.svg?u=<%TEST_ID%>",
            "resp_header": "",
            "type": "pop",
            "weight": 1.306,
            "classification": {}
        },
        {
            "id": "BKK",
            "req_header": "",
            "resource": "https://bkk-v4.pops.fastly-insights.com/o.svg?u=<%TEST_ID%>",
            "resp_header": "",
            "type": "pop",
            "weight": 6.725,
            "classification": {}
        },
        {
            "id": "BMA",
            "req_header": "",
            "resource": "https://bma-v4.pops.fastly-insights.com/o.svg?u=<%TEST_ID%>",
            "resp_header": "",
            "type": "pop",
            "weight": 1.257,
            "classification": {}
        },
        {
            "id": "BNE",
            "req_header": "",
            "resource": "https://bne-v4.pops.fastly-insights.com/o.svg?u=<%TEST_ID%>",
            "resp_header": "",
            "type": "pop",
            "weight": 1.48,
            "classification": {}
        },
        {
            "id": "BOG",
            "req_header": "",
            "resource": "https://bog-v4.pops.fastly-insights.com/o.svg?u=<%TEST_ID%>",
            "resp_header": "",
            "type": "pop",
            "weight": 1.067,
            "classification": {}
        }
    ]
    assert merge_list_dict(tasks) == {
        "id": "ACC",
        "req_header": "",
        "resource": "https://acc-v4.pops.fastly-insights.com/o.svg?u=<%TEST_ID%>",
        "resp_header": "",
        "type": "pop",
        "weight": 1.021,
        "classification": {}
    }
    t = {
        "id": "ADL",
        "req_header": "",
        "resource": "https://adl-v4.pops.fastly-insights.com/o.svg?u=<%TEST_ID%>",
        "resp_header": "",
        "type": "pop",
        "weight": 1.408,
        "classification": {'name': 'foyou'},
        'name': 'foyou',
    }
    tasks.insert(0, t)
    dd = merge_list_dict(tasks)
    assert dd['name'] == 'foyou'
    assert dd['classification'] == t['classification']


def test_merge_list_dict2():
    ld = [
        {
            "country_code": "HK",
            "asn": 206264,
            "connection_type": "wifi",
            "device_type": "unknown"
        },
        {
            "host": "www.fastly-insights.com",
            "lookup": "apac.u.fastly-insights.com",
            "pop": "pops.fastly-insights.com"
        }, {
            "datacenter": "HKG",
            "ip_version": 4,
        }
    ]
    assert merge_list_dict(ld) == {
        "country_code": "HK",
        "asn": 206264,
        "connection_type": "wifi",
        "device_type": "unknown",
        "host": "www.fastly-insights.com",
        "lookup": "apac.u.fastly-insights.com",
        "pop": "pops.fastly-insights.com",
        "datacenter": "HKG",
        "ip_version": 4,
    }
