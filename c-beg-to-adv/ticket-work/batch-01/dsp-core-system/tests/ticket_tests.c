#include "ticket_test_common.h"

#include "dsp/adc_counts.h"
#include "dsp/afe_constants.h"
#include "dsp/apply_gain_fn.h"
#include "dsp/bin_loader.h"
#include "dsp/bringup_report.h"
#include "dsp/channel_label.h"
#include "dsp/format_adc_line.h"
#include "dsp/game_score.h"
#include "dsp/gain_stage.h"
#include "dsp/linear_to_db.h"
#include "dsp/mono_mix.h"
#include "dsp/psd_buffer.h"
#include "dsp/read_session.h"
#include "dsp/scope_draw.h"

#include <string.h>

typedef int (*TestFn)(void);

typedef struct TicketCase {
    char const* id;
    TestFn run;
} TicketCase;

static double unity_gain(double const x)
{
    return x * 0.5;
}

static int test_entry_101(void)
{
    dsp_print_header("DSP-ENTRY-101", "Mono mix (working with numbers)");
    double const observed = mono_mix_down(0.2, 0.2);
    dsp_print_observed("mono_mix_down(0.2, 0.2)", observed);
    dsp_print_expected("mono_mix_down(0.2, 0.2)", 0.2);
    return dsp_nearly_equal(observed, 0.2, 1e-9) ? dsp_pass("DSP-ENTRY-101") : dsp_fail("DSP-ENTRY-101");
}

static int test_entry_102(void)
{
    dsp_print_header("DSP-ENTRY-102", "ADC int to double volts");
    double const observed = counts_to_volts(2047, 2.5, 12);
    dsp_print_observed("counts_to_volts(2047, 2.5, 12)", observed);
    dsp_print_expected("counts_to_volts(2047, 2.5, 12)", 1.25);
    return dsp_nearly_equal(observed, 1.25, 1e-3) ? dsp_pass("DSP-ENTRY-102") : dsp_fail("DSP-ENTRY-102");
}

static int test_entry_103(void)
{
    dsp_print_header("DSP-ENTRY-103", "printf format line");
    char buf[64];
    format_adc_line(buf, sizeof buf, 2047, 1.25);
    dsp_print_observed_str("format_adc_line text", buf);
    dsp_print_expected_str("format_adc_line text", "counts=2047 volts=1.2500");
    return strcmp(buf, "counts=2047 volts=1.2500") == 0 ? dsp_pass("DSP-ENTRY-103") : dsp_fail("DSP-ENTRY-103");
}

static int test_entry_104(void)
{
    dsp_print_header("DSP-ENTRY-104", "AFE sample-rate constant");
    int const observed = dsp_sample_rate_hz();
    dsp_print_observed_int("dsp_sample_rate_hz()", observed);
    dsp_print_expected_int("dsp_sample_rate_hz()", DSP_SAMPLE_RATE_HZ);
    return observed == DSP_SAMPLE_RATE_HZ ? dsp_pass("DSP-ENTRY-104") : dsp_fail("DSP-ENTRY-104");
}

static int test_entry_105(void)
{
    dsp_print_header("DSP-ENTRY-105", "ASCII scope bar length");
    int const observed = scope_bar_length(-0.5, 0.5);
    dsp_print_observed_int("scope_bar_length(-0.5, 0.5)", observed);
    dsp_print_expected_int("scope_bar_length(-0.5, 0.5)", 20);
    return observed == 20 ? dsp_pass("DSP-ENTRY-105") : dsp_fail("DSP-ENTRY-105");
}

static int test_mid_201(void)
{
    dsp_print_header("DSP-MID-201", "scanf gain text parse");
    double gain_db = 0.0;
    int const ok = parse_gain_db_text("-6.5", &gain_db);
    dsp_print_observed_int("parse_gain_db_text ok", ok);
    dsp_print_observed("parsed gain_db", gain_db);
    dsp_print_expected("parsed gain_db", -6.5);
    return ok == 1 && dsp_nearly_equal(gain_db, -6.5, 1e-9) ? dsp_pass("DSP-MID-201") : dsp_fail("DSP-MID-201");
}

static int test_mid_202(void)
{
    dsp_print_header("DSP-MID-202", "fgets label newline trim");
    char label[DSP_LABEL_MAX] = "uplink\n";
    int const observed = channel_label_is_uplink(label);
    dsp_print_observed_int("channel_label_is_uplink", observed);
    dsp_print_expected_int("channel_label_is_uplink", 1);
    return observed == 1 ? dsp_pass("DSP-MID-202") : dsp_fail("DSP-MID-202");
}

static int test_mid_203(void)
{
    dsp_print_header("DSP-MID-203", "Static PSD bin bounds");
    double bins[DSP_PSD_BIN_COUNT];
    psd_clear(bins);
    int const ok8 = psd_write_bin(bins, 8, 0.5);
    dsp_print_observed_int("psd_write_bin index 8", ok8);
    dsp_print_expected_int("psd_write_bin index 8", 0);
    return ok8 == 0 ? dsp_pass("DSP-MID-203") : dsp_fail("DSP-MID-203");
}

static int test_mid_204(void)
{
    dsp_print_header("DSP-MID-204", "Static array peak search");
    double bins[DSP_PSD_BIN_COUNT] = {0.1, 0.2, 0.5, 0.3, 0.0, 0.0, 0.0, 0.0};
    int const observed = psd_max_bin_index(bins, 4);
    dsp_print_observed_int("psd_max_bin_index", observed);
    dsp_print_expected_int("psd_max_bin_index", 2);
    return observed == 2 ? dsp_pass("DSP-MID-204") : dsp_fail("DSP-MID-204");
}

static int test_mid_205(void)
{
    dsp_print_header("DSP-MID-205", "Fill array from parsed count");
    double bins[4] = {0};
    int const filled = load_uniform_bins(bins, 4, 0.25);
    dsp_print_observed_int("load_uniform_bins filled", filled);
    dsp_print_observed("bins[3]", bins[3]);
    dsp_print_expected_int("load_uniform_bins filled", 4);
    dsp_print_expected("bins[3]", 0.25);
    return filled == 4 && dsp_nearly_equal(bins[3], 0.25, 1e-9) ? dsp_pass("DSP-MID-205") : dsp_fail("DSP-MID-205");
}

static int test_staff_301(void)
{
    dsp_print_header("DSP-STAFF-301", "void function updates gain stage");
    GainStage stage;
    gain_stage_init(&stage);
    gain_stage_set_db(&stage, -6.0);
    double const observed = gain_stage_linear(&stage);
    dsp_print_observed("gain_stage_linear", observed);
    dsp_print_expected("gain_stage_linear", 0.501187);
    return dsp_nearly_equal(observed, 0.501187, 1e-4) ? dsp_pass("DSP-STAFF-301") : dsp_fail("DSP-STAFF-301");
}

static int test_staff_302(void)
{
    dsp_print_header("DSP-STAFF-302", "Function return linear to dB");
    double const observed = linear_power_to_db(0.5);
    dsp_print_observed("linear_power_to_db(0.5)", observed);
    dsp_print_expected("linear_power_to_db(0.5)", -3.0103);
    return dsp_nearly_equal(observed, -3.0103, 1e-3) ? dsp_pass("DSP-STAFF-302") : dsp_fail("DSP-STAFF-302");
}

static int test_staff_303(void)
{
    dsp_print_header("DSP-STAFF-303", "Function pointer apply gain");
    double const observed = apply_gain_fn(1.0, unity_gain);
    dsp_print_observed("apply_gain_fn(1.0, unity_gain)", observed);
    dsp_print_expected("apply_gain_fn(1.0, unity_gain)", 0.5);
    return dsp_nearly_equal(observed, 0.5, 1e-9) ? dsp_pass("DSP-STAFF-303") : dsp_fail("DSP-STAFF-303");
}

static int test_staff_304(void)
{
    dsp_print_header("DSP-STAFF-304", "Milestone bring-up headroom");
    double const observed = bringup_headroom_percent(1.0, 2.5);
    dsp_print_observed("bringup_headroom_percent(1.0, 2.5)", observed);
    dsp_print_expected("bringup_headroom_percent(1.0, 2.5)", 60.0);
    return dsp_nearly_equal(observed, 60.0, 1e-9) ? dsp_pass("DSP-STAFF-304") : dsp_fail("DSP-STAFF-304");
}

static int test_staff_305(void)
{
    dsp_print_header("DSP-STAFF-305", "Milestone game score on hit");
    int const observed = game_score_on_hit(10, 3, 3);
    dsp_print_observed_int("game_score_on_hit", observed);
    dsp_print_expected_int("game_score_on_hit", 20);
    return observed == 20 ? dsp_pass("DSP-STAFF-305") : dsp_fail("DSP-STAFF-305");
}

static TicketCase const k_cases[] = {
    {"DSP-ENTRY-101", test_entry_101},
    {"DSP-ENTRY-102", test_entry_102},
    {"DSP-ENTRY-103", test_entry_103},
    {"DSP-ENTRY-104", test_entry_104},
    {"DSP-ENTRY-105", test_entry_105},
    {"DSP-MID-201", test_mid_201},
    {"DSP-MID-202", test_mid_202},
    {"DSP-MID-203", test_mid_203},
    {"DSP-MID-204", test_mid_204},
    {"DSP-MID-205", test_mid_205},
    {"DSP-STAFF-301", test_staff_301},
    {"DSP-STAFF-302", test_staff_302},
    {"DSP-STAFF-303", test_staff_303},
    {"DSP-STAFF-304", test_staff_304},
    {"DSP-STAFF-305", test_staff_305},
};

static void print_usage(char const* argv0)
{
    printf("Usage:\n  %s <TICKET-ID>\n  %s --list\n", argv0, argv0);
}

int main(int argc, char** argv)
{
    if (argc != 2) {
        print_usage(argv[0]);
        return 2;
    }

    if (strcmp(argv[1], "--list") == 0) {
        size_t const n = sizeof(k_cases) / sizeof(k_cases[0]);
        for (size_t i = 0; i < n; ++i) {
            printf("%s\n", k_cases[i].id);
        }
        return 0;
    }

    size_t const n = sizeof(k_cases) / sizeof(k_cases[0]);
    for (size_t i = 0; i < n; ++i) {
        if (strcmp(argv[1], k_cases[i].id) == 0) {
            return k_cases[i].run();
        }
    }

    printf("Unknown ticket id: %s\n", argv[1]);
    print_usage(argv[0]);
    return 2;
}
