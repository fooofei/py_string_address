cmake_minimum_required (VERSION 2.6)
project (string_address)
message(STATUS "string_address_SOURCE_DIR=" ${string_address_SOURCE_DIR})
message(STATUS "string_address_BINARY_DIR" ${string_address_BINARY_DIR})

# Apple's Warning
# https://stackoverflow.com/questions/31561309/cmake-warnings-under-os-x-macosx-rpath-is-not-specified-for-the-following-targe
if (APPLE)
    set(CMAKE_MACOSX_RPATH 0)
endif ()

set(PY_DEV_INCLUDE )
set(PY_DEV_LIBS )

# UNIX  APPLE
if(WIN32)
    set(MY_PYTHON_INCLUDE ${CMAKE_SOURCE_DIR}/python_dev/include)
    set(MY_PYTHON_LIBS ${CMAKE_SOURCE_DIR}/python_dev/libs)
    set(MY_PYTHON_LIB python27)

else()

    # find_package() not work
    # find_package(PythonInterp ) # PYTHON_VERSION_STRING PYTHON_EXECUTABLE
    # find_package(PythonLibs ) # PYTHON_LIBRARIES PYTHON_INCLUDE_PATH
    execute_process(COMMAND python-config --prefix OUTPUT_VARIABLE MY_PYTHON_HOME)
    string(STRIP ${MY_PYTHON_HOME} MY_PYTHON_HOME)
    message(STATUS "MY_PYTHON_HOME=" "${MY_PYTHON_HOME}")
    set(MY_PYTHON_INCLUDE ${MY_PYTHON_HOME}/include/python2.7)
    set(MY_PYTHON_LIBS ${MY_PYTHON_HOME}/lib )
    set(MY_PYTHON_LIB ${MY_PYTHON_LIBS}/libpython2.7.dylib)
endif()
# In pyenv, install python with env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 2.7.13
# >>> import sysconfig
# >>> sysconfig.get_config_var('LIBS')
# '-lpthread -ldl  -lutil'
# >>> sysconfig.get_config_var('LINKFORSHARED')
# '-Xlinker -export-dynamic'

message(STATUS "MY_PYTHON_INCLUDE=" "${MY_PYTHON_INCLUDE}")
message(STATUS "MY_PYTHON_LIBS=" "${MY_PYTHON_LIBS}")
message(STATUS "MY_PYTHON_LIB=" "${MY_PYTHON_LIB}")

include_directories(${MY_PYTHON_INCLUDE})
link_directories(${MY_PYTHON_LIBS}) # macOS use this
add_library(string_address SHARED main.cpp)
target_link_libraries(string_address python2.7)

if(WIN32)

#set_target_properties(string_address PROPERTIES SUFFIX ".pyd")
# same with
set(CMAKE_SHARED_LIBRARY_SUFFIX ".pyd")
elseif(APPLE)
set(CMAKE_SHARED_LIBRARY_SUFFIX ".so") # Python call .so in macOS,not .dylib
endif()

add_custom_command(
        TARGET string_address POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different $<TARGET_FILE:string_address> ../$<TARGET_FILE_NAME:string_address>
)