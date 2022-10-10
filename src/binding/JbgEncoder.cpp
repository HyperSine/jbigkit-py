#include "JbgEncoder.hpp"
#include "init.hpp"

namespace jbigkit_py {

    template<>
    void make_binding<JbgEncoder>(py::module& m, py::class_<JbgEncoder>& c) {
        c
            .def(py::init<unsigned long, unsigned long, const py::args&>(), py::arg("x"), py::arg("y"))
            .def(
                "set_lrlmax",
                [](JbgEncoder& self, unsigned long mwidth, unsigned long mheight) {
                    return jbg_enc_lrlmax(&self.state, mwidth, mheight);
                },
                py::arg("mwidth"),
                py::arg("mheight")
            )
            .def(
                "set_layers",
                [](JbgEncoder& self, int d) {
                    return jbg_enc_layers(&self.state, d);
                },
                py::arg("d")
            )
            .def(
                "set_lrange",
                [](JbgEncoder& self, int dl, int dh) {
                    return jbg_enc_lrange(&self.state, dl, dh);
                },
                py::arg("dl"),
                py::arg("dh")
            )
            .def(
                "set_options",
                [](JbgEncoder& self, int order, int options, unsigned long l0, int mx, int my) {
                    return jbg_enc_options(&self.state, order, options, l0, mx, my);
                },
                py::arg("order"),
                py::arg("options"),
                py::arg("l0"),
                py::arg("mx"),
                py::arg("my")
            )
            .def(
                "encode_out",
                [](JbgEncoder& self) -> py::bytes {
                    self.ostream = py::module::import("io").attr("BytesIO")();

                    jbg_enc_out(&self.state);

                    auto retval = self.ostream.attr("getvalue")().cast<py::bytes>();
                    self.ostream = py::none();

                    return retval;
                }
            );
    }

}
