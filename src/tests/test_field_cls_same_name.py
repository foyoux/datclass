from datclass import DatclassGenerator


def test_field_cls_same_name():
    g = DatclassGenerator()
    dat = g.gen_datclass({
        'Lang': {
            'name': 'foyoux'
        }
    }, recursive=True)
    assert dat[7] == "    lang: Lang = None  # rename from 'Lang'"
