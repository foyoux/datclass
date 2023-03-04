from datclass import DatclassGenerator


def test_list_none():
    g = DatclassGenerator()
    dat = g.gen_datclass({
        'NONE': [None]
    }, recursive=True)
    assert dat[2] == "    nONE: List = field(default_factory=list)  # rename from 'NONE'"
