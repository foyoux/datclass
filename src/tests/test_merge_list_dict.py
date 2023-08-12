from datclass.__main__ import merge_list_dict


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


def test_merge_nested_dict():
    # noinspection DuplicatedCode
    data = [
        {
            "_initiator": {
                "type": "other"
            },
            "_priority": "VeryHigh",
            "_resourceType": "document",
            "cache": {},
            "connection": "460",
            "pageref": "page_1",
        },
        {
            "_initiator": {
                "type": "parser",
                "url": "https://github.com/foyoux/phar",
                "lineNumber": 23
            },
            "_priority": "VeryHigh",
            "_resourceType": "stylesheet",
            "cache": {},
            "connection": "512",
            "pageref": "page_1",
        },
        {
            "_initiator": {
                "type": "parser",
                "url": "https://github.com/foyoux/phar",
                "lineNumber": 33
            },
            "_priority": "Low",
            "_resourceType": "script",
            "cache": {},
            "connection": "512",
            "pageref": "page_1",
        }, {
            "_initiator": {
                "type": "script",
                "stack": {
                    "callFrames": [
                        {
                            "functionName": "_.l",
                            "scriptId": "84",
                            "url": "https://github.githubassets.com/assets/wp-runtime-b0208882aebc.js",
                            "lineNumber": 0,
                            "columnNumber": 20357
                        },
                        {
                            "functionName": "_.f.j",
                            "scriptId": "84",
                            "url": "https://github.githubassets.com/assets/wp-runtime-b0208882aebc.js",
                            "lineNumber": 0,
                            "columnNumber": 21590
                        },
                        {
                            "functionName": "",
                            "scriptId": "84",
                            "url": "https://github.githubassets.com/assets/wp-runtime-b0208882aebc.js",
                            "lineNumber": 0,
                            "columnNumber": 1207
                        },
                        {
                            "functionName": "_.e",
                            "scriptId": "84",
                            "url": "https://github.githubassets.com/assets/wp-runtime-b0208882aebc.js",
                            "lineNumber": 0,
                            "columnNumber": 1186
                        },
                        {
                            "functionName": "",
                            "scriptId": "97",
                            "url": "https://github.githubassets.com/assets/element-registry-d46d179ca77b.js",
                            "lineNumber": 0,
                            "columnNumber": 5341
                        }
                    ],
                    "parent": {
                        "description": "Promise.then",
                        "callFrames": [
                            {
                                "functionName": "",
                                "scriptId": "92",
                                "url": "https://github.githubassets.com/assets/vendors-node_modules_github_auto-complete-element_dist_index_js-node_modules_github_catalyst_-6afc16-e779583c369f.js",
                                "lineNumber": 0,
                                "columnNumber": 13151
                            }
                        ],
                        "parent": {
                            "description": "requestAnimationFrame",
                            "callFrames": [
                                {
                                    "functionName": "q",
                                    "scriptId": "92",
                                    "url": "https://github.githubassets.com/assets/vendors-node_modules_github_auto-complete-element_dist_index_js-node_modules_github_catalyst_-6afc16-e779583c369f.js",
                                    "lineNumber": 0,
                                    "columnNumber": 12932
                                },
                                {
                                    "functionName": "F",
                                    "scriptId": "92",
                                    "url": "https://github.githubassets.com/assets/vendors-node_modules_github_auto-complete-element_dist_index_js-node_modules_github_catalyst_-6afc16-e779583c369f.js",
                                    "lineNumber": 0,
                                    "columnNumber": 13247
                                },
                                {
                                    "functionName": "77062",
                                    "scriptId": "97",
                                    "url": "https://github.githubassets.com/assets/element-registry-d46d179ca77b.js",
                                    "lineNumber": 0,
                                    "columnNumber": 27080
                                },
                                {
                                    "functionName": "_",
                                    "scriptId": "84",
                                    "url": "https://github.githubassets.com/assets/wp-runtime-b0208882aebc.js",
                                    "lineNumber": 0,
                                    "columnNumber": 140
                                },
                                {
                                    "functionName": "",
                                    "scriptId": "97",
                                    "url": "https://github.githubassets.com/assets/element-registry-d46d179ca77b.js",
                                    "lineNumber": 0,
                                    "columnNumber": 33326
                                },
                                {
                                    "functionName": "s",
                                    "scriptId": "84",
                                    "url": "https://github.githubassets.com/assets/wp-runtime-b0208882aebc.js",
                                    "lineNumber": 0,
                                    "columnNumber": 21748
                                },
                                {
                                    "functionName": "",
                                    "scriptId": "97",
                                    "url": "https://github.githubassets.com/assets/element-registry-d46d179ca77b.js",
                                    "lineNumber": 0,
                                    "columnNumber": 67
                                }
                            ]
                        }
                    }
                }
            },
            "_priority": "Low",
            "_resourceType": "script",
            "cache": {},
            "connection": "512",
            "pageref": "page_1",
        },
        {
            "_initiator": {
                "type": "other"
            },
            "_priority": "High",
            "_resourceType": "other",
            "cache": {},
            "connection": "793",
            "pageref": "page_1",
        }
    ]
    d = merge_list_dict(data)
    assert '_initiator' in d
    assert '_priority' in d
    assert '_resourceType' in d
    assert 'cache' in d
    assert 'connection' in d
    assert 'pageref' in d
