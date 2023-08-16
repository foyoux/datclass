import hashlib
import keyword
import string

try:
    from typing import get_origin, get_args
except ImportError:
    from typing_extensions import get_origin, get_args
_NAME_MAP = {}


def get_md5_identifier(name, length=8):
    s = hashlib.md5(name.encode()).hexdigest()
    return f'a_{s[:length]}'  # attribute


def get_identifier(name: str):
    # Query the cache.
    if name in _NAME_MAP:
        return _NAME_MAP[name]

    # Process fields starting with double (or multiple) underscores by replacing them with a single underscore.
    if name.startswith('__'):
        name = '_' + name.lstrip('_')

    # If it's a keyword, add an '_' suffix.
    if keyword.iskeyword(name):
        s = f'{name}_'
    elif name.isidentifier():
        # Keywords are valid identifiers, so first check for keywords, and then check for identifiers.
        s = name
    else:
        # First, replace '-' with '_'.
        name = name.replace('-', '_')
        # If it's not a standard identifier, filter out characters other than underscores,
        # lowercase letters, uppercase letters, and numbers.
        s = ''.join(filter(lambda c: c in '_' + string.ascii_letters + string.digits, name))
        if s:
            if s[0] in string.digits:
                s = f'a_{s}'  # attribute
            elif keyword.iskeyword(s):
                s = f'{s}_'
            elif not s.isidentifier():
                s = get_md5_identifier(name)
        else:
            s = get_md5_identifier(name)

    # Convert the first letter to lowercase.
    if s[0] in string.ascii_uppercase:
        s = s[0].lower() + s[1:]

    # Cache before returning.
    _NAME_MAP[name] = s
    return s


def write_file(file_path, content, encoding='utf-8'):
    with open(file_path, 'w', encoding=encoding) as f:
        f.write(content)
