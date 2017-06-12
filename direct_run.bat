@echo off

%~d0
cd /d %~dp0



:: 如果有错误就退出
mkdir build
cd build
cmake -G "Visual Studio 11 2012" .. || exit /B 1 
cmake --build . --config Release || exit /B 1
::xcopy Release\string_address.dll .. /Y
rmdir /S /Q build
cd ..
python ctypes_cast_ps_py_string_address_size.py || exit /B 1
