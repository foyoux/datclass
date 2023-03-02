import datclass


def test_extra_field(data):
    codes = datclass.gen_datclass(data, recursive=True)
    dat = '\n'.join(datclass.imports.to_list() + codes + [
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
