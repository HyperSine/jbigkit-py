import itertools
import pytest
import jbigkit
import PIL.Image

@pytest.fixture(autouse = True)
def ensure_cwd_is_here(request, monkeypatch):
    monkeypatch.chdir(request.fspath.dirname)

def generate_test_pbm() -> PIL.Image:
    w, h = 1960, 1951

    raw_img_size = ((w + 7) // 8) * h
    assert raw_img_size == 477995

    raw_img = bytearray(raw_img_size)

    p, prsg = 0, 1
    repeat = bytearray(8)
    for j in range(0, 1951):
        for i in range(0, 1960):
            if 192 <= j:
                if j < 1023 or ((i >> 3) & 3) == 0:
                    sum_ = (prsg & 1) + ((prsg >> 2) & 1) + ((prsg >> 11) & 1) + ((prsg >> 15) & 1)
                    prsg = ((prsg << 1) + (sum_ & 1)) & 0xffff
                    if (prsg & 3) == 0:
                        raw_img[p] |= 1 << (7 - (i & 7))
                        repeat[i & 7] = 1
                    else:
                        repeat[i & 7] = 0
                else:
                    if repeat[i % 8]:
                        raw_img[p] |= 1 << (7 - (i & 7))

            if i % 8 == 7:
                p += 1

    sum_ = 0
    for b in raw_img:
        for i in range(0, 8):
            if b & (1 << i):
                sum_ += 1
    assert sum_ == 861965, 'Artificial test image is expected to have 861965 foreground pixels, but got {}.'.format(sum_)

    return PIL.Image.frombytes('1', (w, h), bytes(raw_img), 'raw', '1;I')

test_pbm = generate_test_pbm()

class TestJbgEncoder:

    @pytest.mark.parametrize(
        'options, order, layers, l0, mx, correct_length',
        [
            (jbigkit.JbgFlags.DELAY_AT, 0, 0, 1951, 0, 317384),
            (jbigkit.JbgFlags.DELAY_AT | jbigkit.JbgFlags.LRLTWO, 0, 0, 1951, 0, 317132),
            (jbigkit.JbgFlags.DELAY_AT | jbigkit.JbgFlags.TPBON, 0, 0, 128, 8, 253653),
            (jbigkit.JbgFlags.DELAY_AT | jbigkit.JbgFlags.TPBON | jbigkit.JbgFlags.TPDON | jbigkit.JbgFlags.DPON, 0, 6, 2, 8, 279314),
            (jbigkit.JbgFlags.DELAY_AT | jbigkit.JbgFlags.TPBON | jbigkit.JbgFlags.TPDON | jbigkit.JbgFlags.DPON | jbigkit.JbgFlags.DPPRIV, 0, 6, 2, 8, 279314 + 1728),
            (jbigkit.JbgFlags.SDRST | jbigkit.JbgFlags.TPBON, 0, 0, 128, 8, -1),
            (jbigkit.JbgFlags.SDRST, 0, 0, 1951, 0, -1),
            (jbigkit.JbgFlags.LRLTWO | jbigkit.JbgFlags.SDRST, 0, 0, 1951, 0, -1),
            (jbigkit.JbgFlags.TPBON | jbigkit.JbgFlags.SDRST, 0, 0, 128, 8, -1),
            (jbigkit.JbgFlags.TPBON | jbigkit.JbgFlags.TPDON | jbigkit.JbgFlags.DPON | jbigkit.JbgFlags.SDRST, 0, 6, 2, 8, -1),
        ]
    )
    def test_single_plane(self, options, order, layers, l0, mx, correct_length):
        w, h = test_pbm.size
        raw_data = test_pbm.tobytes('raw', '1;I')

        encoder = jbigkit.JbgEncoder(w, h, raw_data)
        encoder.set_layers(layers)
        encoder.set_options(order, options, l0, mx, 0)
        encoded_result = encoder.encode_out()

        if correct_length > 0:
            assert len(encoded_result) == correct_length

        decoder = jbigkit.JbgDecoder()
        err, processed_len = decoder.decode_in(encoded_result)
        assert err == jbigkit.JbgErrno.EOK
        assert processed_len == len(encoded_result)

        assert decoder.get_planes_num() == 1
        # assert raw_data == decoder.get_plane(0)

    @pytest.mark.parametrize(
        'layer, order',
        [ args for args in itertools.product([ 0, 1, 2, 3 ], [ 0, jbigkit.JbgFlags.ILEAVE, jbigkit.JbgFlags.ILEAVE | jbigkit.JbgFlags.SMID ]) ]
    )
    def test_multi_plane(self, layer, order):
        jbig_normal = \
            bytes([
                0x7c, 0xe2, 0x38, 0x04, 0x92, 0x40, 0x04, 0xe2, 0x5c, 0x44,
                0x92, 0x44, 0x38, 0xe2, 0x38,
                0x7c, 0xe2, 0x38, 0x04, 0x92, 0x40, 0x04, 0xe2, 0x5c, 0x44,
                0x92, 0x44, 0x38, 0xe2, 0x38,
                0x7c, 0xe2, 0x38, 0x04, 0x92, 0x40, 0x04, 0xe2, 0x5c, 0x44,
                0x92, 0x44, 0x38, 0xe2, 0x38,
                0x7c, 0xe2, 0x38, 0x04, 0x92, 0x40, 0x04, 0xe2, 0x5c, 0x44,
                0x92, 0x44, 0x38, 0xe2, 0x38
            ])

        jbig_upsidedown = \
            bytes([
                0x38, 0xe2, 0x38, 0x44, 0x92, 0x44, 0x04, 0xe2, 0x5c, 0x04,
                0x92, 0x40, 0x7c, 0xe2, 0x38,
                0x38, 0xe2, 0x38, 0x44, 0x92, 0x44, 0x04, 0xe2, 0x5c, 0x04,
                0x92, 0x40, 0x7c, 0xe2, 0x38,
                0x38, 0xe2, 0x38, 0x44, 0x92, 0x44, 0x04, 0xe2, 0x5c, 0x04,
                0x92, 0x40, 0x7c, 0xe2, 0x38,
                0x38, 0xe2, 0x38, 0x44, 0x92, 0x44, 0x04, 0xe2, 0x5c, 0x04,
                0x92, 0x40, 0x7c, 0xe2, 0x38
            ])

        jbig_inverse = \
            bytes([
                0xff^0x7c, 0xff^0xe2, 0xfe^0x38, 0xff^0x04, 0xff^0x92,
                0xfe^0x40, 0xff^0x04, 0xff^0xe2, 0xfe^0x5c, 0xff^0x44,
                0xff^0x92, 0xfe^0x44, 0xff^0x38, 0xff^0xe2, 0xfe^0x38,
                0xff^0x7c, 0xff^0xe2, 0xfe^0x38, 0xff^0x04, 0xff^0x92,
                0xfe^0x40, 0xff^0x04, 0xff^0xe2, 0xfe^0x5c, 0xff^0x44,
                0xff^0x92, 0xfe^0x44, 0xff^0x38, 0xff^0xe2, 0xfe^0x38,
                0xff^0x7c, 0xff^0xe2, 0xfe^0x38, 0xff^0x04, 0xff^0x92,
                0xfe^0x40, 0xff^0x04, 0xff^0xe2, 0xfe^0x5c, 0xff^0x44,
                0xff^0x92, 0xfe^0x44, 0xff^0x38, 0xff^0xe2, 0xfe^0x38,
                0xff^0x7c, 0xff^0xe2, 0xfe^0x38, 0xff^0x04, 0xff^0x92,
                0xfe^0x40, 0xff^0x04, 0xff^0xe2, 0xfe^0x5c, 0xff^0x44,
                0xff^0x92, 0xfe^0x44, 0xff^0x38, 0xff^0xe2, 0xfe^0x38
            ])

        encoder = jbigkit.JbgEncoder(23, 5 * 4, jbig_normal, jbig_upsidedown, jbig_inverse, jbig_inverse)
        encoder.set_layers(layer)
        encoder.set_options(order, jbigkit.JbgFlags.TPBON | jbigkit.JbgFlags.TPDON | jbigkit.JbgFlags.DPON, 2, 8, 0)
        encoded_result = encoder.encode_out()

        decoder = jbigkit.JbgDecoder()
        err, processed_len = decoder.decode_in(encoded_result)
        assert err == jbigkit.JbgErrno.EOK
        assert processed_len == len(encoded_result)

        assert decoder.get_planes_num() == 4

        # assert jbig_normal == decoder.get_plane(0)
        # assert jbig_upsidedown == decoder.get_plane(1)
        # assert jbig_inverse == decoder.get_plane(2)
        # assert jbig_inverse == decoder.get_plane(3)
