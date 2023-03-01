from datclass import get_t_default, get_v_type


def test_get_v_default():
    assert get_t_default(get_v_type({})) is 'None'
    assert get_t_default(get_v_type([])) == 'field(default_factory=list)'
    assert get_t_default(get_v_type([111])) == 'field(default_factory=list)'
    assert get_t_default(get_v_type(['111'])) == 'field(default_factory=list)'
    assert get_t_default(get_v_type(['111', 111])) == 'field(default_factory=list)'
    assert get_t_default(get_v_type(1)) is 'None'
    assert get_t_default(get_v_type(1.1)) is 'None'
    assert get_t_default(get_v_type(True)) is 'None'
    assert get_t_default(get_v_type({'a': 'b'})) is 'None'
    assert get_t_default(get_v_type([{}])) == 'field(default_factory=list)'
    assert get_t_default(get_v_type([123, 4354])) == 'field(default_factory=list)'
