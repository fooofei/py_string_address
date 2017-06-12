#coding=utf-8

'''
 We have two ways to get internal buffer of the bytes string( not the unicode string).

 1 use ctypes.cast

 2 use pythonapi PyString_AsStringAndSize, export from python c module


'''


import ctypes
import cffi
import os
import sys

curpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(curpath, './Debug'))



def ctypes_cast_c_void_p(v): return ctypes.cast(v, ctypes.c_void_p)
def bytes_string_address(v): return ctypes_cast_c_void_p(v)

def bytes_string_address2(v):
    Py_ssize_t = ctypes.c_uint
    f = ctypes.pythonapi.PyString_AsStringAndSize
    f.restype = ctypes.c_int
    f.argtypes = [ctypes.py_object,
                                      ctypes.POINTER(ctypes.c_char_p),
                                      ctypes.POINTER(Py_ssize_t)]

    addr = ctypes.c_char_p()
    size = Py_ssize_t()
    hr = f(v, ctypes.pointer(addr),ctypes.pointer(size))
    assert (hr==0)
    return ctypes_cast_c_void_p(addr)



ffi = cffi.FFI()
cffi_address_of = lambda v: ffi.addressof(ffi.from_buffer(v))


def c_bytes_string_address(v):
    import string_address
    r = string_address.PyString_AddressSize(v)
    assert (r)
    assert (r[1] == len(v))
    return r[0]


def c_unicode_string_address(v):
    import string_address
    r = string_address.PyUnicodeString_AddressSize(v)
    assert (r)
    assert (r[1] == len(v)*ctypes.sizeof(ctypes.c_wchar))
    return r[0]



def pass_bytes_string():
    from ctypes import string_at

    v = 'helloworld'

    addr1 = bytes_string_address(v)
    addr2 = bytes_string_address2(v)
    addr3 = cffi_address_of(v)
    addr3 = ffi.cast('unsigned long', addr3)

    addr4 = c_bytes_string_address(v)

    assert (addr1.value
            == addr2.value
            == addr3
            == addr4 )

    assert (v
            == string_at(addr1.value, len(v))
            == string_at(addr2.value, len(v)))

    print ('pass bytes_string')


def pass_unicode_string():
    from ctypes import wstring_at
    v = u'测试helloworld'

    addr1 = bytes_string_address(v)

    addr4 = c_unicode_string_address(v)

    assert (addr1.value
            ==addr4 )

    assert (v
            == wstring_at(addr1.value, len(v))
            == wstring_at(addr4, len(v)))

    print ('pass unicode_string')


def entry():
    pass_bytes_string()
    pass_unicode_string()



if __name__ == '__main__':
    entry()