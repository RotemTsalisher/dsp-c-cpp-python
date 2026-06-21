cmake_minimum_required(VERSION 3.16)
project(vlc_core_system LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(vlc_core
    src/mono_mix.cpp
    src/adc_counts.cpp
    src/heap_bins.cpp
    src/mic_gain_chain.cpp
    src/wind_psd_scratch.cpp
    src/telemetry_slice.cpp
    src/notch_source.cpp
    src/icodec.cpp
    src/tap_gate.cpp
    src/lab_curve.cpp
    src/stereo_psd.cpp
    src/cal_amp.cpp
    src/uplink_service.cpp
)
target_include_directories(vlc_core PUBLIC
    "${CMAKE_CURRENT_SOURCE_DIR}/include"
)
target_compile_features(vlc_core PUBLIC cxx_std_20)

add_executable(vlc_demo src/main.cpp)
target_link_libraries(vlc_demo PRIVATE vlc_core)

add_executable(vlc_ticket_test tests/ticket_tests.cpp)
target_link_libraries(vlc_ticket_test PRIVATE vlc_core)
target_include_directories(vlc_ticket_test PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/tests")
