from datclass.__main__ import Generator


def test_field_cls_same_name():
    g = Generator()
    dat = g.gen_datclass({
        'Lang': {
            'name': 'foyoux'
        }
    }, recursive=True).codes
    assert dat[7] == "    lang: Lang = None  # rename from 'Lang'"
