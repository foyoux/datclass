from datclass.__main__ import Generator


def test_extra_field(data):
    g = Generator()
    codes = g.gen_datclass(data, recursive=True).codes
    dat = '\n'.join(g.imports.codes + codes + [
        'from datclass import set_debug',
        'set_debug(True)',
        'data["extra"] = "extra"',
        'obj = Object(**data)',
    ])
    ns = {'data': data}
    try:
        exec(dat, ns)
    except Exception as e:
        print(e)
    else:
        raise Exception('Test mode does not work')
