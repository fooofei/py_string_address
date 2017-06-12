#coding=utf-8


import ctypes
import os
import sys


def ctypes_bytes_string_addr(v):
    return ctypes.cast(v,ctypes.c_void_p).value

def c_bytes_string_address(v):
    if sys.platform.startswith('win32'):
        import string_address
    else:
        import libstring_address as string_address
    r = string_address.PyString_AddressSize(v)
    assert (r)
    assert (r[1] == len(v))
    return r[0]


def c_unicode_string_address(v):
    if sys.platform.startswith('win32'):
        import string_address
    else:
        import libstring_address as string_address
    r = string_address.PyUnicodeString_AddressSize(v)
    assert (r)
    assert (r[1] == len(v)*ctypes.sizeof(ctypes.c_wchar))
    return r[0]



def entry():

    bytes_string = 'helloworld'
    unicode_string = u'helloworld'


    bytes_string_addr1 = ctypes_bytes_string_addr(bytes_string)
    bytes_string_addr2 = c_bytes_string_address(bytes_string)

    print ('bytes_string address 1 {} 2 {}'.format(hex(bytes_string_addr1),hex(bytes_string_addr2)))


    unicode_string_addr1 = ctypes_bytes_string_addr(unicode_string)
    unicode_string_addr2 = c_unicode_string_address(unicode_string)

    print ('unicode_string address 1 {} 2 {}'.format(hex(unicode_string_addr1), hex(unicode_string_addr2)))

'''
Output : 
  on Win32:
    bytes_string address 1 0x298e834 2 0x298e834
    unicode_string address 1 0x299f2c0 2 0x299f2c0

  on linux:
    bytes_string address 1 0x7fad4c246834 2 0x7fad4c246834
    unicode_string address 1 0x2612770 2 0x7fad4c246870

'''


if __name__ == '__main__':
    entry()