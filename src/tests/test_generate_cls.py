from datclass import GenerateDatClass


def test_generate_cls(data):
    g = GenerateDatClass()
    codes = g.gen_datclass(data, recursive=True)
    dat = '\n'.join(g.imports.to_list() + codes + [
        'obj = Object(**data)',
        'assert obj.update_id == 1',
        'assert isinstance(obj.message, Message)',
        'assert isinstance(obj.message.a_2U3sadsb, A2U3Sadsb)',
        'assert isinstance(obj.message.video, Video)',
        'assert isinstance(obj.message.caption_entities, list)',
        'for c in obj.message.caption_entities:',
        '    assert isinstance(c, CaptionEntities)',
        'assert isinstance(obj.message.forward_from, ForwardFrom)',
    ])
    ns = {'data': data}
    exec(dat, ns)
