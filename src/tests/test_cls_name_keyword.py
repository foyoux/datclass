from datclass.__main__ import DatGen


def test_cls_name_keyword():
    g = DatGen()
    dat = g.gen_datclass({
        'NONE': {
            'name': 'foyoux'
        }
    }, recursive=True).codes
    assert dat[7] == "    nONE: None_ = None  # rename from 'NONE'"
