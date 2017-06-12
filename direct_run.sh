#!/bin/bash


# 失败就退出
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release  .. || exit 1
make  || exit 1
rm -rf build

cd ..
python  ctypes_cast_ps_py_string_address_size.py|| exit 1
