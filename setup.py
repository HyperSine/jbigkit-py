#!/usr/bin/env python3
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext, ParallelCompile, naive_recompile

ParallelCompile(needs_recompile = naive_recompile).install()

authors = {
    'Xiao': ('Aiyu Xiao', 'hypersine.git@outlook.com')
}

if __name__ == '__main__':
    setup(
        author = authors['Xiao'][0],
        author_email = authors['Xiao'][1],
        ext_modules = [
            Pybind11Extension(
                name = 'jbigkit',
                sources = [
                    'src/jbigkit/libjbig/jbig.c',
                    'src/jbigkit/libjbig/jbig_ar.c',
                    'src/binding/JbgErrno.cpp',
                    'src/binding/JbgFlags.cpp',
                    'src/binding/JbgEncoder.cpp',
                    'src/binding/JbgDecoder.cpp',
                    'src/binding/init.cpp',
                ],
                include_dirs = [ 'src/jbigkit/libjbig' ]
            )
        ],
        cmdclass = { 'build_ext': build_ext },
    )
