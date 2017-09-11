#!/bin/bash


# 失败就退出
rm -rf build_ubuntu
mkdir build_ubuntu
cd build_ubuntu
cmake -DCMAKE_BUILD_TYPE=Release  .. || exit 1
make  || exit 1
cd ..
rm -rf build_ubuntu
which python
python  py_string_address.py
