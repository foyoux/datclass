from datclass.__main__ import Generator


def test_list_none():
    g = Generator()
    dat = g.gen_datclass({
        'NONE': [None]
    }, recursive=True).codes
    assert dat[2] == "    nONE: List = field(default_factory=list)  # rename from 'NONE'"
