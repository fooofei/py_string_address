#coding=utf-8

'''

All addr is int.

'''

import ctypes
import os
import sys



###
def ctypes_cast_bytes_string_addr(v):
    ''' !!!Risk, not use  see issue I report http://bugs.python.org/issue30634'''
    return ctypes.cast(v,ctypes.c_void_p).value

###
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

###


def ctypes_api_pyssize_t():
    if hasattr(ctypes.pythonapi, 'Py_InitModule4'):
        return ctypes.c_int
    elif hasattr(ctypes.pythonapi, 'Py_InitModule4_64'):
        return ctypes.c_int64
    else:
        raise TypeError("Cannot determine type of Py_ssize_t")

def ctypes_api_bytes_string_addr(v):
    '''
    one way :
         f = ctypes.pythonapi.PyString_AsStringAndSize
         f.restype = ctypes.c_int
         f.argtypes = [ctypes.py_object,
                      ctypes.POINTER(ctypes.c_char_p),
                      ctypes.POINTER(Py_ssize_t)]

    '''
    f = ctypes.pythonapi.PyString_AsString
    f.restype = ctypes.c_void_p
    f.argtypes = [ctypes.py_object]
    return f(v)

def ctypes_api_unicode_string_addr(v):
    # f = ctypes.pythonapi.PyUnicode_AsUnicode
    py_unicode_size = ctypes.sizeof(ctypes.c_wchar)
    if py_unicode_size == 2:
        f = ctypes.pythonapi.PyUnicodeUCS2_AsUnicode
    elif py_unicode_size==4:
        f = ctypes.pythonapi.PyUnicodeUCS4_AsUnicode
    else:
        raise TypeError("Cannot determine wchar_t size")
    f.restype = ctypes.c_void_p
    f.argtypes = [ctypes.py_object]
    return f(v)


def cffi_bytes_string_addr(v):
    import cffi
    ffi = cffi.FFI()
    x= ffi.addressof(ffi.from_buffer(v))
    x = ffi.cast('uintptr_t',x)
    return int(x)

def _cffi_bytes_string_addr(v):
    try:
        return cffi_bytes_string_addr(v)
    except ImportError:
        return 0


def foo1():
    '''
    It's error, we cannot use ctypes.cast to bytes string or unicode string
    '''

    bytes_string = 'helloworld'
    unicode_string = u'helloworld'
    unicode_string2 = u'测试中文'

    bytes_string_addr1 = ctypes_cast_bytes_string_addr(bytes_string)
    bytes_string_addr2 = c_bytes_string_address(bytes_string)

    print ('bytes_string address 1 {} 2 {}'.format(hex(bytes_string_addr1), hex(bytes_string_addr2)))

    unicode_string_addr1 = ctypes_cast_bytes_string_addr(unicode_string)
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



def pass_bytes_string():
    from ctypes import string_at

    v = 'helloworld'

    c_addr = c_bytes_string_address(v)
    cffi_addr = _cffi_bytes_string_addr(v)
    ctypes_api_addr = ctypes_api_bytes_string_addr(v)

    print ('pass_bytes_string-> c_addr={} cffi_addr={} ctypes_api_addr={}'.format(
        hex(c_addr)
        ,hex(cffi_addr)
        ,hex(ctypes_api_addr)
    ))

    assert (cffi_addr == c_addr == ctypes_api_addr)

    assert (v
            == string_at(c_addr, len(v))
            == string_at(cffi_addr, len(v))
            == string_at(ctypes_api_addr, len(v))
            )

    print ('pass bytes_string')


def pass_unicode_string():
    from ctypes import wstring_at
    v = u'测试helloworld'


    c_addr = c_unicode_string_address(v)
    ctypes_api_addr = ctypes_api_unicode_string_addr(v)


    print ('pass_unicode_string-> c_addr={} ctypes_api_addr={}'.format(
        hex(c_addr)
        ,hex(ctypes_api_addr)
    ))

    assert (c_addr == ctypes_api_addr)

    assert (v
            == wstring_at(c_addr, len(v))
            == wstring_at(ctypes_api_addr, len(v)))

    print ('pass unicode_string')



def entry():
    pass_bytes_string()
    pass_unicode_string()

if __name__ == '__main__':
    entry()