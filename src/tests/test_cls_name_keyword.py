from datclass import DatclassGenerator


def test_cls_name_keyword():
    g = DatclassGenerator()
    dat = g.gen_datclass({
        'NONE': {
            'name': 'foyoux'
        }
    }, recursive=True)
    assert dat[7] == "    nONE: None_ = None  # rename from 'NONE'"
