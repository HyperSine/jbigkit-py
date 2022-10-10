#include "JbgFlags.hpp"
#include "init.hpp"

namespace jbigkit_py {

    template<>
    void make_binding<JbgFlags>(py::module& m, py::enum_<JbgFlags>& e) {
        e
            .value("HITOLO", static_cast<JbgFlags>(JBG_HITOLO))
            .value("SEQ", static_cast<JbgFlags>(JBG_SEQ))
            .value("ILEAVE", static_cast<JbgFlags>(JBG_ILEAVE))
            .value("SMID", static_cast<JbgFlags>(JBG_SMID))
            .value("LRLTWO", static_cast<JbgFlags>(JBG_LRLTWO))
            .value("VLENGTH", static_cast<JbgFlags>(JBG_VLENGTH))
            .value("TPDON", static_cast<JbgFlags>(JBG_TPDON))
            .value("TPBON", static_cast<JbgFlags>(JBG_TPBON))
            .value("DPON", static_cast<JbgFlags>(JBG_DPON))
            .value("DPPRIV", static_cast<JbgFlags>(JBG_DPPRIV))
            .value("DPLAST", static_cast<JbgFlags>(JBG_DPLAST))
            .value("DELAY_AT", static_cast<JbgFlags>(JBG_DELAY_AT))
            .value("SDRST", static_cast<JbgFlags>(JBG_SDRST));
    }

}
