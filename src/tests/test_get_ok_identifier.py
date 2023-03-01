from datclass import get_ok_identifier


def test_get_ok_identifier():
    assert get_ok_identifier('2&*(U3sadsb') == 'a_2U3sadsb'
    assert get_ok_identifier('123') == 'a_123'
    assert get_ok_identifier('from') == 'from_'
