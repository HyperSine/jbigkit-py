import pytest
import jbigkit
import gzip, PIL.Image

@pytest.fixture(autouse = True)
def ensure_cwd_is_here(request, monkeypatch):
    monkeypatch.chdir(request.fspath.dirname)

'''
from http://ftp.funet.fi/pub/graphics/misc/test-images/INDEX
>>>>>
File:	  Size:	  Content:			Type:	Format:	Resolution:   
-----	  ------  --------			-----	-------	------------ 
ccitt1	   30983  CCITT standard image 1	bin	pbm	 1728x2376x1
ccitt2	   27781  CCITT standard image 2	bin	pbm	 1728x2376x1
ccitt3	   47725  CCITT standard image 3	bin	pbm	 1728x2376x1
ccitt4	  103020  CCITT standard image 4	bin	pbm	 1728x2376x1
ccitt5	   56469  CCITT standard image 5	bin	pbm	 1728x2376x1
ccitt6	   31868  CCITT standard image 6	bin	pbm	 1728x2376x1
ccitt7	  114707  CCITT standard image 7	bin	pbm	 1728x2376x1
ccitt8	   44086  CCITT standard image 8	bin	pbm	 1728x2376x1
...
...
<<<<<
'''

class TestJbgDecoder:

    @pytest.mark.parametrize('n', [ n for n in range(1, 8 + 1) ])
    def test_ccittX(self, n):
        assert isinstance(n, int) and 1 <= n <= 8

        decoder = jbigkit.JbgDecoder()
        with open('../src/jbigkit/examples/ccitt{}.jbg'.format(n), 'rb') as f:
            data = f.read()

            err, processed_len = decoder.decode_in(data)
            assert err == jbigkit.JbgErrno.EOK
            assert processed_len == len(data)

            assert decoder.get_planes_num() == 1
            assert decoder.get_width() == 1728
            assert decoder.get_height() == 2376

            with gzip.open('examples/ccitt{}.pbm.gz'.format(n), 'rb') as ff:
                src_img = PIL.Image.open(ff, formats = [ 'ppm' ])    # type: PIL.Image.Image
                assert decoder.get_plane(0) == src_img.tobytes('raw', '1;I')

    def test_mx(self):
        decoder = jbigkit.JbgDecoder()
        with open('../src/jbigkit/examples/mx.jbg', 'rb') as f:
            data = f.read()

            err, processed_len = decoder.decode_in(data)
            assert err == jbigkit.JbgErrno.EOK
            assert processed_len == len(data)

            assert decoder.get_planes_num() == 1
            assert decoder.get_width() == 1200      # according to `../src/jbigkit/examples/jbgtests.m`
            assert decoder.get_height() == 650      # according to `../src/jbigkit/examples/jbgtests.m`

            with open('examples/mx.pbm', 'rb') as ff:
                src_img = PIL.Image.open(ff, formats = [ 'ppm' ])    # type: PIL.Image.Image
                assert decoder.get_plane(0) == src_img.tobytes('raw', '1;I')

    def test_xvlogo(self):
        decoder = jbigkit.JbgDecoder()
        with open('../src/jbigkit/examples/xvlogo.jbg', 'rb') as f:
            data = f.read()

            err, processed_len = decoder.decode_in(data)
            assert err == jbigkit.JbgErrno.EOK
            assert processed_len == len(data)

            assert decoder.get_planes_num() == 1
            assert decoder.get_width() == 480
            assert decoder.get_height() == 270

            with open('examples/xvlogo.pbm', 'rb') as ff:
                src_img = PIL.Image.open(ff, formats = [ 'ppm' ])    # type: PIL.Image.Image
                assert decoder.get_plane(0) == src_img.tobytes('raw', '1;I')
