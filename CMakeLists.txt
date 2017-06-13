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

# Query Python Env in macOS
# $python-config --includes
# -I/usr/include/python2.6 -I/usr/include/python2.6
# $python-config --ldflags
# -lpthread -ldl -lutil -lm -lpython2.6


# UNIX  APPLE
if(WIN32)
    set(PY_DEV_INCLUDE ${CMAKE_SOURCE_DIR}/python_dev/include)
    set(PY_DEV_LIBS ${CMAKE_SOURCE_DIR}/python_dev/libs)
    link_directories(${PY_DEV_LIBS})
else()
    set(PY_DEV_INCLUDE /usr/include/python2.7)
    # macOS also work
    # set(PY_DEV_INCLUDE /usr/local/Cellar/python/2.7.13/Frameworks/Python.framework/Versions/2.7/include/python2.7)
    set(PY_DEV_LIBS )
endif()



include_directories(${PY_DEV_INCLUDE})
add_library(string_address SHARED main.cpp)

if(WIN32)
target_link_libraries(string_address python27)
#set_target_properties(string_address PROPERTIES SUFFIX ".pyd")
# same with
set(CMAKE_SHARED_LIBRARY_SUFFIX ".pyd")
elseif(APPLE)

target_link_libraries(string_address "/usr/local/Cellar/python/2.7.13/Frameworks/Python.framework/Versions/2.7/Python")
#target_link_libraries(string_address "-lpython2.7") # will crash
#target_link_libraries(string_address "-lpython") # will crash
set(CMAKE_SHARED_LIBRARY_SUFFIX ".so") # Python call .so in macOS,not .dylib
endif()

add_custom_command(
        TARGET string_address POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different $<TARGET_FILE:string_address> ../$<TARGET_FILE_NAME:string_address>
)