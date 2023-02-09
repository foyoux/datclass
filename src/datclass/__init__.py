__title__ = 'datclass'
__author__ = 'foyoux'
__version__ = '0.0.1'

import argparse


def main():
    epilog = f'%(prog)s({__version__}) by foyoux(https://github.com/foyoux/datclass)'
    parser = argparse.ArgumentParser(prog='datclass', description='', epilog=epilog)
    parser.add_argument('-v', '--version', action='version', version=epilog)

    parser.parse_args()
