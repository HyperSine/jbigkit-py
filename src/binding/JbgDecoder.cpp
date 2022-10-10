#include "JbgErrno.hpp"
#include "JbgDecoder.hpp"
#include "init.hpp"

namespace jbigkit_py {

    template<>
    void make_binding<JbgDecoder>(py::module &m, py::class_<JbgDecoder>& c) {
        c
            .def(py::init())
            .def(
                "set_maxsize",
                [](JbgDecoder& self, unsigned long xmax, unsigned long ymax) {
                    return jbg_dec_maxsize(&self.state, xmax, ymax);
                },
                py::arg("xmax"),
                py::arg("ymax")
            )
            .def(
                "decode_in",  // in is a keyword reserved by Python, use `decode_some` instead
                [](JbgDecoder& self, const py::buffer& buf) -> std::tuple<JbgErrno, size_t> {
                    auto buf_info = buf.request();
                    auto buf_read = size_t{};
                    auto decode_state = JbgErrno{ jbg_dec_in(&self.state, reinterpret_cast<unsigned char*>(buf_info.ptr), buf_info.size, &buf_read) };
                    return std::make_tuple(decode_state, buf_read);
                },
                py::arg("buf")
            )
            .def(
                "get_width",
                [](JbgDecoder& self) {
                    return jbg_dec_getwidth(&self.state);
                }
            )
            .def(
                "get_height",
                [](JbgDecoder& self) {
                    return jbg_dec_getheight(&self.state);
                }
            )
            .def(
                "get_plane",
                [](JbgDecoder& self, int plane) -> std::optional<py::memoryview> {
                    auto p = jbg_dec_getimage(&self.state, plane);
                    if (p) {
                        return py::memoryview::from_memory(p, py::ssize_t_cast(jbg_dec_getsize(&self.state)), true);
                    } else {
                        return std::nullopt;
                    }
                },
                py::return_value_policy::reference_internal,
                py::arg("plane")
            )
            .def(
                "get_planes_num",
                [](JbgDecoder& self) {
                    return jbg_dec_getplanes(&self.state);
                }
            )
            .def(
                "merge_planes",
                [](JbgDecoder& self, bool use_graycode) -> py::bytes {
                    py::object bio = py::module::import("io").attr("BytesIO")();

                    jbg_dec_merge_planes(
                        &self.state,
                        use_graycode,
                        [](unsigned char* data, size_t len, void* p_bio) {
                            py::object& bio = *reinterpret_cast<py::object*>(p_bio);
                            bio.attr("write")(py::memoryview::from_memory(data, py::ssize_t_cast(len), true));
                        },
                        std::addressof(bio)
                    );

                    return bio.attr("getvalue")().cast<py::bytes>();
                },
                py::arg("use_graycode")
            );
    }

}
