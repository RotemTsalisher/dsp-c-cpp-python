cmake_minimum_required(VERSION 3.16)
project(afe_core_system LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(afe_core
    src/iencoder.cpp
    src/route_channel.cpp
    src/response_curve.cpp
    src/stereo_comb.cpp
    src/calibrated_gain.cpp
    src/psd_worker.cpp
    src/wave_source.cpp
    src/register_mask.cpp
    src/tap_sifter.cpp
    src/fold_accumulator.cpp
    src/export_layout.cpp
    src/safe_add.cpp
    src/audit_gate.cpp
    src/api_revision.cpp
)
target_include_directories(afe_core PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/include")
target_compile_features(afe_core PUBLIC cxx_std_20)

add_executable(afe_ticket_test tests/ticket_tests.cpp)
target_link_libraries(afe_ticket_test PRIVATE afe_core)
target_include_directories(afe_ticket_test PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/tests")
