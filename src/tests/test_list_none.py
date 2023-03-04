from datclass import GenerateDatClass


def test_list_none():
    g = GenerateDatClass()
    dat = g.gen_datclass({
        'NONE': [None]
    }, recursive=True)
    assert dat[2] == "    nONE: List = field(default_factory=list)  # rename from 'NONE'"
