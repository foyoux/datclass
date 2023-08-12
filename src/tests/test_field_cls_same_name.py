from datclass.__main__ import DatGen


def test_field_cls_same_name():
    g = DatGen()
    dat = g.gen_datclass({
        'Lang': {
            'name': 'foyoux'
        }
    }, recursive=True).codes
    assert dat[7] == "    lang: Lang = None  # rename from 'Lang'"
