cmake_minimum_required (VERSION 2.6)
project (string_address)

# Apple's Warning
# https://stackoverflow.com/questions/31561309/cmake-warnings-under-os-x-macosx-rpath-is-not-specified-for-the-following-targe
if (APPLE)
    set(CMAKE_MACOSX_RPATH 0)
endif ()

add_library(${PROJECT_NAME} SHARED main.cpp)

# erase
set(PY_DEV_INCLUDE )
set(PY_DEV_LIBS )

# UNIX  APPLE
if(WIN32)
    target_include_directories(${PROJECT_NAME} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/python_dev/include)
    # MUST place at before add_library()
    #link_directories(${CMAKE_CURRENT_SOURCE_DIR}/python_dev/libs)
    target_link_libraries(${PROJECT_NAME} ${CMAKE_CURRENT_SOURCE_DIR}/python_dev/libs/python27.lib)
else()

    # find_package() not work
    # find_package(PythonInterp ) # PYTHON_VERSION_STRING PYTHON_EXECUTABLE
    # find_package(PythonLibs ) # PYTHON_LIBRARIES PYTHON_INCLUDE_PATH
    execute_process(COMMAND python-config --prefix OUTPUT_VARIABLE MY_PYTHON_HOME)
    string(STRIP ${MY_PYTHON_HOME} MY_PYTHON_HOME)
    message(STATUS "MY_PYTHON_HOME=" "${MY_PYTHON_HOME}")
    target_include_directories(${PROJECT_NAME} PRIVATE ${MY_PYTHON_HOME}/include/python2.7)
    #set(MY_PYTHON_LIB ${MY_PYTHON_LIBS}/libpython2.7.dylib)
    target_link_libraries(${PROJECT_NAME}  ${MY_PYTHON_LIBS}python2.7)
endif()
# In pyenv, install python with env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 2.7.13
# >>> import sysconfig
# >>> sysconfig.get_config_var('LIBS')
# '-lpthread -ldl  -lutil'
# >>> sysconfig.get_config_var('LINKFORSHARED')
# '-Xlinker -export-dynamic'


if(WIN32)
    set_target_properties(${PROJECT_NAME} PROPERTIES SUFFIX ".pyd")
# same with
#set(CMAKE_SHARED_LIBRARY_SUFFIX ".pyd")
elseif(APPLE)
    set_target_properties(${PROJECT_NAME} PROPERTIES SUFFIX ".so")# Python call .so on macOS,not .dylib
endif()

add_custom_command(
        TARGET ${PROJECT_NAME} POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different $<TARGET_FILE:${PROJECT_NAME}> ../$<TARGET_FILE_NAME:${PROJECT_NAME}>
)