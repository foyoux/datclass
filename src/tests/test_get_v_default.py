from datclass import GenerateDatClass


def test_get_v_default():
    assert GenerateDatClass.get_t_default(GenerateDatClass.get_v_type({})) is 'None'
    assert GenerateDatClass.get_t_default(GenerateDatClass.get_v_type([])) == 'field(default_factory=list)'
    assert GenerateDatClass.get_t_default(GenerateDatClass.get_v_type([111])) == 'field(default_factory=list)'
    assert GenerateDatClass.get_t_default(GenerateDatClass.get_v_type(['111'])) == 'field(default_factory=list)'
    assert GenerateDatClass.get_t_default(GenerateDatClass.get_v_type(['111', 111])) == 'field(default_factory=list)'
    assert GenerateDatClass.get_t_default(GenerateDatClass.get_v_type(1)) is 'None'
    assert GenerateDatClass.get_t_default(GenerateDatClass.get_v_type(1.1)) is 'None'
    assert GenerateDatClass.get_t_default(GenerateDatClass.get_v_type(True)) is 'None'
    assert GenerateDatClass.get_t_default(GenerateDatClass.get_v_type({'a': 'b'})) is 'None'
    assert GenerateDatClass.get_t_default(GenerateDatClass.get_v_type([{}])) == 'field(default_factory=list)'
    assert GenerateDatClass.get_t_default(GenerateDatClass.get_v_type([123, 4354])) == 'field(default_factory=list)'
