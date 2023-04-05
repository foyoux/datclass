from datclass import DatGen

data = {
    'product': {
        'name': '东北大辣条',
        'price': '￥2.00'
    }
}


def test_main_class_name():
    g = DatGen()
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
