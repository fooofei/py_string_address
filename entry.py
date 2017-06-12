# coding=utf-8

import os
import datetime
import sys


curpath = os.path.dirname(os.path.realpath(__file__))




def entry():

    sys.path.append(os.path.join(curpath,'./Debug'))

    import string_address
    x ="hello"
    y = 'world'
    addr = 0
    size = 0
    r = string_address.PyString_AddressSize(x)
    print (r)
    r = string_address.PyUnicodeString_AddressSize(x.decode('utf-8'))
    print (r)

    raw_input('')


if __name__ == '__main__':
    entry()
