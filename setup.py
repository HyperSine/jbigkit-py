#!/usr/bin/env python3
import functools
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext, ParallelCompile, naive_recompile

ParallelCompile(needs_recompile = naive_recompile).install()

class Pybind11BuildExtOverride(build_ext):

    def build_extensions(self):
        def _compile_wrap(original_compile):
            @functools.wraps(original_compile)
            def _custom_compile(obj, src, ext, cc_args, extra_postargs, pp_opts):
                # if `src` is .c file
                # remove `-std=` or `/std:` flags from `extra_postargs`
                if src.endswith('.c'):
                    extra_postargs = [ *filter(lambda s: not s.startswith('-std=') and not s.startswith('/std:'), extra_postargs) ]
                return original_compile(obj, src, ext, cc_args, extra_postargs, pp_opts)
            return _custom_compile

        self.compiler._compile = _compile_wrap(self.compiler._compile)
        super().build_extensions()

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
        cmdclass = { 'build_ext': Pybind11BuildExtOverride },
    )
