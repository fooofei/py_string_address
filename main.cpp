




#include <Python.h>
#include <stringobject.h>
#include <unicodeobject.h>
#include <stdio.h>

//
// missing Python27_d.lib http://blog.csdn.net/junparadox/article/details/52704287

static PyObject *
PyString_AddressSize(PyObject * self, PyObject * args)
{
    int r;
    char * ptr = NULL;
    PyObject * string = NULL;
    Py_ssize_t size = 0;
    PyObject * o_r = NULL;

    // s = char **
    // 
    //r = PyArg_ParseTuple(args, "S", &string);
    r = PyArg_ParseTuple(args, "O", &string);
    if (0 == r) {
        // error
        Py_INCREF(Py_None);
        return Py_None;
    }

    r = PyString_AsStringAndSize(string,&ptr, &size);
    if (0 != r){
        Py_INCREF(Py_None);
        return Py_None;
    }

    
    // k = unsigned long, notice It must can be 64bit in Windows_x64 or linux x86_x64 platform.
    // I = unsigned int
    // n = py_ssize_t
    o_r = Py_BuildValue("(k,n)",(const void*)ptr,size);

    if (NULL == o_r) {
        Py_INCREF(Py_None);
        return Py_None;
    }
    return o_r;
}

static PyObject *
PyUnicodeString_AddressSize(PyObject * self, PyObject * args)
{
    int r;
    const char * ptr = NULL;
    PyObject * unicode_string = NULL;
    Py_ssize_t size = 0;
    PyObject * o_r = NULL;

       
    // same address
    //r = PyArg_ParseTuple(args, "U", &unicode_string);
    r = PyArg_ParseTuple(args, "O", &unicode_string);
    if (0 == r) {
        Py_INCREF(Py_None);
        return Py_None;
    }

    if (!PyUnicode_Check(unicode_string)) {
        Py_INCREF(Py_None);
        return Py_None;
    }

    size = PyUnicode_GET_DATA_SIZE(unicode_string);
    ptr = PyUnicode_AS_DATA(unicode_string);

    o_r = Py_BuildValue("(k,n)", (const void*)ptr, size);

    if (NULL == o_r) {
        Py_INCREF(Py_None);
        return Py_None;
    }
    return o_r;
}




static PyMethodDef methods[] = {
    { "PyString_AddressSize",  PyString_AddressSize, METH_VARARGS, "Get the string buffer address and size of PyStringObject" },
    {"PyUnicodeString_AddressSize",  PyUnicodeString_AddressSize, METH_VARARGS, "Get the string buffer address and size of PyUnicodeObject"},
{NULL, NULL, 0, NULL}        /* Sentinel */
};

#ifdef WIN32

PyMODINIT_FUNC
initstring_address(void)
{
    PyObject * r = Py_InitModule("string_address"
        , methods);

}
#else
PyMODINIT_FUNC
initlibstring_address(void)
{
    PyObject * r = Py_InitModule("libstring_address"
            , methods);

}
#endif
