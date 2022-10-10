# jbigkit-py

jbigkit-py is a Python binding library to [jbigkit](https://www.cl.cam.ac.uk/~mgk25/jbigkit/), making you able to encode/decode image to/from [JBIG](https://en.wikipedia.org/wiki/JBIG) format.

jbigkit-py is designed for Python3.6+. It has not been tested on Python2 yet.

## Install

From pip:

```console
$ pip install jbigkit-py
```

Or from source:

```bash
# make sure you have c++ compiler installed before
# make sure you have setuptools, pybind11 installed in pip before

$ git clone --recurse-submodules https://github.com/HyperSine/jbigkit-py.git
$ cd jbigkit-py
$ pip install .
```

To perform tests after installation:

```bash
# make sure you have pytest, Pillow installed in pip before

$ python -m pytest .
```

## Tutorial

A decode example:

```py
#!/usr/bin/env python3
import jbigkit

with open('path to a .jbg file', 'rb') as f:
    jbg_data = f.read()

decoder = jbigkit.JbgDecoder()
status, processed_len = decoder.decode_in(jbg_data)

# status should be JbgErrno.EOK if a valid .jbg file was given
assert status == jbigkit.JbgErrno.EOK

# make sure all processed
assert processed_len == len(jbg_data)

w, h = decoder.get_width(), decoder.get_height()
print('the .jbg file has image size {:d}x{:d}'.format(w, h))
print('the .jbg file has {:d} planes.'.format(decoder.get_planes_num()))

# to get the i-th plane
ith_plane = decoder.get_plane(i)    # type: memoryview

# pass the i-th plane to Pillow library for further processing
import PIL.Image
img = PIL.Image.frombytes('1', (w, h), bytes(ith_plane), 'raw', '1;I')
```

For encode, see `tests/test_JbgEncoder.py`

## API Reference

| APIs                                                 | Descriptions                                                                                                                                           |
|:-----------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------|
| `JbgEncoder.__init__(x, y, *planes)`                 | Equivalent to call `jbg_enc_init`.<br/> Planes data is pass via `*planes` variadic arguments. Each one for a plane, and must be Bytes-like object.     |
| `JbgEncoder.set_lrlmax(mwidth, mheight)`             | Equivalent to call `jbg_enc_lrlmax`.                                                                                                                   |
| `JbgEncoder.set_layers(d)`                           | Equivalent to call `jbg_enc_layers`.                                                                                                                   |
| `JbgEncoder.set_lrange(dl, dh)`                      | Equivalent to call `jbg_enc_lrange`.                                                                                                                   |
| `JbgEncoder.set_options(order, options, l0, mx, my)` | Equivalent to call `jbg_enc_options`.                                                                                                                  |
| `JbgEncoder.encode_out()`                            | Equivalent to call `jbg_enc_out`, but returns a `bytes` object which is the encode result.                                                             |
| `JbgDecoder.__init__`                                | Equivalent to call `jbg_dec_init`.                                                                                                                     |
| `JbgDecoder.set_maxsize(xmax, ymax)`                 | Equivalent to call `jbg_dec_maxsize`.                                                                                                                  |
| `JbgDecoder.decode_in(buf)`                          | Equivalent to call `jbg_dec_in`. `buf` must be Bytes-like object.                                                                                      |
| `JbgDecoder.get_width()`                             | Equivalent to call `jbg_dec_getwidth`.                                                                                                                 |
| `JbgDecoder.get_height()`                            | Equivalent to call `jbg_dec_getheight`.                                                                                                                |
| `JbgDecoder.get_plane(plane)`                        | Equivalent to call `jbg_dec_getimage` and `jbg_dec_getsize`.<br/> It returns a readonly `memoryview` object which is the data of user-specified plane. |
| `JbgDecoder.get_planes_num()`                        | Equivalent to call `jbg_dec_getplanes`.                                                                                                                |
| `JbgDecoder.merge_planes(use_graycode)`              | Equivalent to call `jbg_dec_merge_planes`.                                                                                                             |
| `JbgErrno.to_string()`                               | Equivalent to call `jbg_strerror`.                                                                                                                     |

## Version Convention

As this project is based on the C library [jbigkit](https://www.cl.cam.ac.uk/~mgk25/jbigkit/), this project uses the following scheme for versioning:

```
<version of C library jbigkit>.<a integer for jbigkit-py version>
```

For example, a release with version `2.1.1` means it is based on jbitkit-2.1 and is the 1st release of jbigkit-py.
