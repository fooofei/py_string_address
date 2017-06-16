# coding=utf-8

'''

All addr is int.

'''

import ctypes
import os
import sys


###
def ctypes_cast_bytes_string_addr(v):
    ''' !!!Risk, not use  see issue I report http://bugs.python.org/issue30634'''
    return ctypes.cast(v, ctypes.c_void_p).value


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
    if r is None: return 0
    assert (r[1] == len(v) * ctypes.sizeof(ctypes.c_wchar))
    return r[0]


def c_unicode_string_address_force(v):
    if sys.platform.startswith('win32'):
        import string_address
    else:
        import libstring_address as string_address
    r = string_address.PyUnicodeString_AddressSizeForce(v)
    assert (r is not None)
    # assert (r[1] == len(v)*ctypes.sizeof(ctypes.c_wchar))
    return r


def c_unicode_string_address_unicode_type_size():
    if sys.platform.startswith('win32'):
        import string_address
    else:
        import libstring_address as string_address
    return string_address.PyUnicodeString_GetUnicodeTypeSize()


###


def ctypes_api_pyssize_t():
    if hasattr(ctypes.pythonapi, 'Py_InitModule4'):
        return ctypes.c_int
    elif hasattr(ctypes.pythonapi, 'Py_InitModule4_64'):
        return ctypes.c_int64
    else:
        raise TypeError("Cannot determine type of Py_ssize_t")


def _ctypes_api_unicode_string_address_api():
    '''
    Can be error:
        AttributeError: python: undefined symbol: PyUnicodeUCS2_AsUnicode
    '''
    py_unicode_size = ctypes.sizeof(ctypes.c_wchar)
    if py_unicode_size == 2:
        f = ctypes.pythonapi.PyUnicodeUCS2_AsUnicode
    elif py_unicode_size == 4:
        f = ctypes.pythonapi.PyUnicodeUCS4_AsUnicode
    else:
        raise TypeError("Cannot determine wchar_t size")
    f.restype = ctypes.c_void_p
    f.argtypes = [ctypes.py_object]
    return f


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
    '''
    !!!WARNING not always success

    1 Python redefine api PyUnicode_* as PyUnicodeUCS2_* or PyUnicodeUCS4_*,
     so we see the source code is PyUnicode_* , but through ida the lib binary,
     we only find PyUnicodeUCS2_* or PyUnicodeUCS4_*.

    2 Python says, use PyUnicode_FromWideChar/PyUnicode_AsWideChar to support Platform wchar_t.

    3 PyUnicode_FromWideChar/PyUnicode_AsWideChar will copy buffer, which will use external memory.

    4 If the platform sizeof(wchar_t)==4, it can aslo maybe use PyUnicodeUCS2_* apis, by this, we cannot
       get the internal buffer address.
    '''

    try:
        return _ctypes_api_unicode_string_address_api()(v)
    except (TypeError, AttributeError) as er:
        return 0


def cffi_bytes_string_addr(v):
    import cffi
    ffi = cffi.FFI()
    x = ffi.addressof(ffi.from_buffer(v))
    x = ffi.cast('uintptr_t', x)
    return int(x)


def _cffi_bytes_string_addr(v):
    try:
        return cffi_bytes_string_addr(v)
    except ImportError:
        return 0


import unittest


class MyTestCase(unittest.TestCase):
    def test_address_of_bytes_string(self):
        v = 'helloworld'

        c_addr = c_bytes_string_address(v)
        cffi_addr = _cffi_bytes_string_addr(v)
        ctypes_api_addr = ctypes_api_bytes_string_addr(v)

        msg = 'bytes_string-> c_addr={0} cffi_addr={1} ctypes_api_addr={2}'.format(
            hex(c_addr)
            , hex(cffi_addr)
            , hex(ctypes_api_addr)
        )

        self.assertTrue(assert_bytes_string_address(
            [c_addr, cffi_addr, ctypes_api_addr]
            , v
        )
            , msg=msg)

    def test_address_of_unicode_string(self):
        v = u'测试helloworld'

        c_addr = c_unicode_string_address(v)
        ctypes_api_addr = ctypes_api_unicode_string_addr(v)
        c_addr_force, c_addr_force_size = c_unicode_string_address_force(v)

        print ('\nunicode_string-> c_addr_force addr={0} size={1}'.format(hex(c_addr_force), c_addr_force_size))
        print ('\nunicode_string-> sizeof(Py_UNICODE)={0}'.format(c_unicode_string_address_unicode_type_size()))

        msg = 'unicode_string-> c_addr={0} ctypes_api_addr={1}'.format(c_addr, ctypes_api_addr)

        self.assertTrue(assert_unicode_string_address(
            [c_addr, ctypes_api_addr]
            , v
        ), msg=msg)


def error_sample():
    '''
    It's error, we cannot use ctypes.cast to bytes string or unicode string
    '''

    bytes_string = 'helloworld'
    unicode_string = u'helloworld'

    bytes_string_addr1 = ctypes_cast_bytes_string_addr(bytes_string)
    bytes_string_addr2 = c_bytes_string_address(bytes_string)

    print ('bytes_string address 1 {0} 2 {1}'.format(hex(bytes_string_addr1), hex(bytes_string_addr2)))

    unicode_string_addr1 = ctypes_cast_bytes_string_addr(unicode_string)
    unicode_string_addr2 = c_unicode_string_address(unicode_string)

    print ('unicode_string address 1 {0} 2 {1}'.format(hex(unicode_string_addr1), hex(unicode_string_addr2)))


'''
Output : 
  on Win32:
    bytes_string address 1 0x298e834 2 0x298e834
    unicode_string address 1 0x299f2c0 2 0x299f2c0

  on linux:
    bytes_string address 1 0x7fad4c246834 2 0x7fad4c246834
    unicode_string address 1 0x2612770 2 0x7fad4c246870

'''


def assert_bytes_string_address(addrs, v):
    from functools import partial
    b = all(addrs[0] == e for e in addrs)
    if not b: return b

    string_at = partial(ctypes.string_at, size=len(v))
    values = map(string_at, addrs)
    b = all(values[0] == e for e in values)
    return b


def assert_unicode_string_address(addrs, v):
    from functools import partial
    b = all(addrs[0] == e for e in addrs)
    if not b: return b

    string_at = partial(ctypes.wstring_at, size=len(v))
    values = map(string_at, addrs)
    b = all(values[0] == e for e in values)
    return b


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
    unittest.TextTestRunner(verbosity=3).run(suite)
