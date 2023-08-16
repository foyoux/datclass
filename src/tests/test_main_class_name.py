from datclass.__main__ import Generator

data = {
    'product': {
        'name': 'Northeast Big Spicy Strip',
        'price': '$0.50'
    }
}


def test_main_class_name():
    g = Generator()
    codes = g.gen_datclass(data, 'Product', recursive=True).codes
    assert codes == [
        '@dataclass',
        'class Product0(DatClass):',
        '    name: str = None',
        '    price: str = None',
        '',
        '',
        '@dataclass',
        'class Product(DatClass):',
        '    product: Product0 = None',
    ]
