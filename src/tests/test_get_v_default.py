from datclass.utils import get_value_type, get_type_default


def test_get_v_default():
    assert get_type_default(get_value_type({})) is 'None'
    assert get_type_default(get_value_type([])) == 'field(default_factory=list)'
    assert get_type_default(get_value_type([111])) == 'field(default_factory=list)'
    assert get_type_default(get_value_type(['111'])) == 'field(default_factory=list)'
    assert get_type_default(get_value_type(['111', 111])) == 'field(default_factory=list)'
    assert get_type_default(get_value_type(1)) is 'None'
    assert get_type_default(get_value_type(1.1)) is 'None'
    assert get_type_default(get_value_type(True)) is 'None'
    assert get_type_default(get_value_type({'a': 'b'})) is 'None'
    assert get_type_default(get_value_type([{}])) == 'field(default_factory=list)'
    assert get_type_default(get_value_type([123, 4354])) == 'field(default_factory=list)'
