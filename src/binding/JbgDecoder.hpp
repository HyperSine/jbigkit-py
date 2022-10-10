#pragma once
#include <utility>
#include "jbig.hpp"

namespace jbigkit_py {

    struct JbgDecoder {
        jbg_dec_state state;

        // NOLINTNEXTLINE(cppcoreguidelines-pro-type-member-init): `state` is initialized by `jbg_dec_init`
        JbgDecoder() {
            jbg_dec_init(&state);
        }

        // copy ctor is not allowed
        JbgDecoder(const JbgDecoder& other) = delete;

        // move ctor is allowed
        JbgDecoder(JbgDecoder&& other) noexcept : state{ other.state } {
            other.state = {};
        }

        // copy assigment is not allowed
        JbgDecoder& operator=(const JbgDecoder& other) = delete;

        // move assigment is allowed
        JbgDecoder& operator=(JbgDecoder&& other) noexcept {
            if (this != std::addressof(other)) {
                jbg_dec_free(&state);
                state = other.state;
                other.state = {};
            }
            return *this;
        }

        ~JbgDecoder() {
            jbg_dec_free(&state);
        }
    };

}
