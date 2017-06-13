@echo off

%~d0
cd /d %~dp0



:: 如果有错误就退出
mkdir build
cd build
::cmake -G "Visual Studio 11 2012" .. || exit /B 1 
cmake -G "Visual Studio 15 2017" .. || exit /B 1 
cmake --build . --config Release || exit /B 1
::xcopy Release\string_address.dll .. /Y
cd ..
rmdir /S /Q build
python py_string_address.py || exit /B 1
