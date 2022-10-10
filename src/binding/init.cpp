#include "init.hpp"
#include "JbgErrno.hpp"
#include "JbgFlags.hpp"
#include "JbgEncoder.hpp"
#include "JbgDecoder.hpp"

PYBIND11_MODULE(jbigkit, m) {
    m.def("version", []() { return std::make_tuple<int, int>(JBG_VERSION_MAJOR, JBG_VERSION_MINOR); });
    m.def("version_string", []() { return JBG_VERSION; });

    m.attr("__license__") = JBG_LICENCE;
    m.attr("__version__") = JBG_VERSION;

    auto e_jbg_errno = py::enum_<jbigkit_py::JbgErrno>(m, "JbgErrno");
    auto e_jbg_flags = py::enum_<jbigkit_py::JbgFlags>(m, "JbgFlags", py::arithmetic());
    auto c_jbg_encoder = py::class_<jbigkit_py::JbgEncoder>(m, "JbgEncoder");
    auto c_jbg_decoder = py::class_<jbigkit_py::JbgDecoder>(m, "JbgDecoder");

    jbigkit_py::make_binding(m, e_jbg_errno);
    jbigkit_py::make_binding(m, e_jbg_flags);
    jbigkit_py::make_binding(m, c_jbg_encoder);
    jbigkit_py::make_binding(m, c_jbg_decoder);
}
