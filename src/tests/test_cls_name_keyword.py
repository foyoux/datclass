from datclass import GenerateDatClass


def test_cls_name_keyword():
    g = GenerateDatClass()
    dat = g.gen_datclass({
        'NONE': {
            'name': 'foyoux'
        }
    }, recursive=True)
    assert dat[7] == "    nONE: None_ = None  # rename from 'NONE'"
