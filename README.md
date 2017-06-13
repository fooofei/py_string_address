# py_string_address [![Build Status](https://travis-ci.org/fooofei/py_string_address.svg?branch=master)](https://travis-ci.org/fooofei/py_string_address)

compare ways to get buffer in PyStringObject/PyUnicodeobject object field address.


### use ctypes.cast (bad)

```python
ctypes.cast(obj, ctypes.c_void_p).value

use both for PyStringObject and PyUnicodeObject

```

see the issue I report http://bugs.python.org/issue30634


### use cffi

```python
cffi_address_of = lambda v: ffi.addressof(ffi.from_buffer(v))

use for PyStringObject, there still no way to get address for PyUnicodeObject

```

### use c module



use `PyString_AsStringAndSize` for `PyStringObject`, 

use `PyUnicode_GET_DATA_SIZE`+`PyUnicode_AS_DATA` for `PyUnicodeObject`.


### use ctypes.pythonapi

use `ctypes.pythonapi.PyString_AsString` for `PyStringObject`, 

use `ctypes.pythonapi.PyUnicodeUCS2_AsUnicode` in win32 or `ctypes.pythonapi.PyUnicodeUCS4_AsUnicode` in linux for `PyUnicodeObject`. 



### Platforms 

python2

win32, linux, macOS