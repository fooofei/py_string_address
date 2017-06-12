# py_string_address

compare ways to get buffer in PyStringObject/PyUnicodeobject object field address.


### use ctypes

```python
ctypes.cast(obj, ctypes.c_void_p).value

use both in PyStringObject and PyUnicodeObject

```


### use cffi

```python
cffi_address_of = lambda v: ffi.addressof(ffi.from_buffer(v))

use in PyStringObject, there still no way to get address for PyUnicodeObject

```

### use c module



use `PyString_AsStringAndSize` for `PyStringObject`, 

use `PyUnicode_GET_DATA_SIZE`+`PyUnicode_AS_DATA` for `PyUnicodeObject`.