cmake_minimum_required(VERSION 3.16)
project(dsp_core_system C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

add_library(dsp_core
    src/mono_mix.c
    src/adc_counts.c
    src/format_adc_line.c
    src/afe_constants.c
    src/scope_draw.c
    src/read_session.c
    src/channel_label.c
    src/psd_buffer.c
    src/bin_loader.c
    src/gain_stage.c
    src/linear_to_db.c
    src/apply_gain_fn.c
    src/bringup_report.c
    src/game_score.c
)
target_include_directories(dsp_core PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/include")

add_executable(dsp_ticket_test tests/ticket_tests.c)
target_link_libraries(dsp_ticket_test PRIVATE dsp_core)
target_include_directories(dsp_ticket_test PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/tests")

if(NOT MSVC)
    target_link_libraries(dsp_ticket_test PRIVATE m)
    target_link_libraries(dsp_core PRIVATE m)
endif()

if(MSVC)
    target_compile_definitions(dsp_core PRIVATE _CRT_SECURE_NO_WARNINGS)
    target_compile_definitions(dsp_ticket_test PRIVATE _CRT_SECURE_NO_WARNINGS)
endif()
