#pragma once
#include "py.hpp"

namespace jbigkit_py {

    template<typename T>
    void make_binding(py::module& m, py::class_<T>& c);

    template<typename T>
    void make_binding(py::module& m, py::enum_<T>& e);

}
