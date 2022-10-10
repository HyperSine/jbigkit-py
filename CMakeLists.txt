cmake_minimum_required(VERSION 3.19)
project(jbigkit-py)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(pybind11 REQUIRED)

pybind11_add_module(
    jbigkit
        src/jbigkit/libjbig/jbig.h
        src/jbigkit/libjbig/jbig.c
        src/jbigkit/libjbig/jbig_ar.h
        src/jbigkit/libjbig/jbig_ar.c
        src/binding/py.hpp
        src/binding/jbig.hpp
        src/binding/JbgErrno.hpp
        src/binding/JbgErrno.cpp
        src/binding/JbgFlags.hpp
        src/binding/JbgFlags.cpp
        src/binding/JbgEncoder.hpp
        src/binding/JbgEncoder.cpp
        src/binding/JbgDecoder.hpp
        src/binding/JbgDecoder.cpp
        src/binding/init.hpp
        src/binding/init.cpp
)
target_include_directories(jbigkit PRIVATE "src/jbigkit/libjbig")
