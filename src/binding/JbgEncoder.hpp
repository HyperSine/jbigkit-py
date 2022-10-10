#pragma once
#include <utility>
#include "jbig.hpp"
#include "py.hpp"

namespace jbigkit_py {

    struct JbgEncoder {
        jbg_enc_state state;
        std::vector<py::buffer> plane_bufers;
        std::vector<unsigned char*> plane_buffer_ptrs;
        py::object ostream;

        // NOLINTNEXTLINE(cppcoreguidelines-pro-type-member-init): `state` is initialized by `jbg_enc_init`
        JbgEncoder(unsigned long x, unsigned long y, const py::args& planes) : ostream{ py::none() } {
            if (std::numeric_limits<int>::max() < planes.size()) {
                throw std::runtime_error("Too many planes.");
            }

            for (auto plane : planes) {
                auto plane_buffer = plane.cast<py::buffer>();
                auto plane_buffer_ptr = reinterpret_cast<unsigned char*>(plane_buffer.request().ptr);
                plane_bufers.emplace_back(std::move(plane_buffer));
                plane_buffer_ptrs.emplace_back(plane_buffer_ptr);
            }

            jbg_enc_init(
                &state,
                x, y,
                static_cast<int>(plane_buffer_ptrs.size()), plane_buffer_ptrs.data(),
                [](unsigned char* start, size_t len, void* _this) {
                    JbgEncoder& self = *reinterpret_cast<JbgEncoder*>(_this);
                    self.ostream.attr("write")(py::memoryview::from_memory(start, py::ssize_t_cast(len), true));
                },
                this
            );
        }

        // copy ctor is not allowed
        JbgEncoder(const JbgEncoder& other) = delete;

        // move ctor is allowed
        JbgEncoder(JbgEncoder&& other) noexcept : state{ other.state } {
            other.state = {};
        }

        // copy assigment is not allowed
        JbgEncoder& operator=(const JbgEncoder& other) = delete;

        // move assigment is allowed
        JbgEncoder& operator=(JbgEncoder&& other) noexcept {
            if (this != std::addressof(other)) {
                jbg_enc_free(&state);
                state = other.state;
                other.state = {};
            }
            return *this;
        }

        ~JbgEncoder() {
            jbg_enc_free(&state);
        }
    };

}
