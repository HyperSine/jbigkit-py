#include "JbgErrno.hpp"
#include "init.hpp"

namespace jbigkit_py {

    template<>
    void make_binding<JbgErrno>(py::module& m, py::enum_<JbgErrno>& e) {
        e
            .value("EOK", JbgErrno{ JBG_EOK })
            .value("EOK_INTR", JbgErrno{ JBG_EOK_INTR })
            .value("EAGAIN", JbgErrno{ JBG_EAGAIN })
            .value("ENOMEM", JbgErrno{ JBG_ENOMEM })
            .value("EABORT", JbgErrno{ JBG_EABORT })
            .value("EMARKER", JbgErrno{ JBG_EMARKER })
            .value("EINVAL", JbgErrno{ JBG_EINVAL })
            .value("EIMPL", JbgErrno{ JBG_EIMPL })
            .value("ENOCONT", JbgErrno{ JBG_ENOCONT })
            .def("to_string", [](JbgErrno errnum) { return jbg_strerror(static_cast<int>(errnum)); });
    }

}
