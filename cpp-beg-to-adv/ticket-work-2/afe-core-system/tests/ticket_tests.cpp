#include "ticket_test_common.hpp"

#include "afe/api_revision.hpp"
#include "afe/audit_gate.hpp"
#include "afe/calibrated_gain.hpp"
#include "afe/export_layout.hpp"
#include "afe/fold_accumulator.hpp"
#include "afe/iencoder.hpp"
#include "afe/register_mask.hpp"
#include "afe/response_curve.hpp"
#include "afe/route_channel.hpp"
#include "afe/psd_worker.hpp"
#include "afe/safe_add.hpp"
#include "afe/stereo_comb.hpp"
#include "afe/tap_sifter.hpp"
#include "afe/wave_source.hpp"

#include <climits>
#include <cstdint>
#include <limits>
#include <string>
#include <type_traits>

namespace {

using afe::test::fail;
using afe::test::nearly_equal;
using afe::test::pass;
using afe::test::print_expected;
using afe::test::print_header;
using afe::test::print_observed;

template <typename T>
constexpr bool accepts_masked_field_v = requires {
    {
        afe::masked_or(std::uint32_t{0}, std::uint32_t{0xFF}, std::declval<T>())
    } -> std::same_as<std::uint32_t>;
};

int test_entry_101()
{
    print_header("AFE-ENTRY-101", "IEncoder polymorphic destructor");
    bool const has_virtual_dtor = std::has_virtual_destructor_v<afe::IEncoder>;
    print_observed("has_virtual_destructor_v<IEncoder>", has_virtual_dtor);
    print_expected("has_virtual_destructor_v<IEncoder>", true);
    return has_virtual_dtor ? pass("AFE-ENTRY-101") : fail("AFE-ENTRY-101");
}

int test_entry_102()
{
    print_header("AFE-ENTRY-102", "DuplexChannel route id (value slicing)");
    afe::DuplexChannel duplex;
    int const direct = duplex.lane_id();
    int const routed = afe::route_channel_by_value(duplex);
    print_observed("DuplexChannel.lane_id()", direct);
    print_observed("route_channel_by_value(DuplexChannel)", routed);
    print_expected("route_channel_by_value(DuplexChannel)", 2);
    return direct == 2 && routed == 2 ? pass("AFE-ENTRY-102") : fail("AFE-ENTRY-102");
}

int test_entry_103()
{
    print_header("AFE-ENTRY-103", "ResponseCurve eval through IResponseCurve*");
    afe::ResponseCurve curve;
    afe::IResponseCurve const* iface = &curve;
    double const observed = iface->eval(0.5);
    print_observed("IResponseCurve::eval(0.5)", observed);
    print_expected("IResponseCurve::eval(0.5)", 0.5);
    return nearly_equal(observed, 0.5) ? pass("AFE-ENTRY-103") : fail("AFE-ENTRY-103");
}

int test_entry_104()
{
    print_header("AFE-ENTRY-104", "StereoComb operator+ right channel");
    afe::StereoComb a(1.0, 0.5);
    afe::StereoComb b(0.25, 0.25);
    afe::StereoComb const sum = a + b;
    print_observed("(a + b).left()", sum.left());
    print_observed("(a + b).right()", sum.right());
    print_expected("(a + b).left()", 1.25);
    print_expected("(a + b).right()", 0.75);
    return nearly_equal(sum.left(), 1.25) && nearly_equal(sum.right(), 0.75) ? pass("AFE-ENTRY-104")
                                                                               : fail("AFE-ENTRY-104");
}

int test_entry_105()
{
    print_header("AFE-ENTRY-105", "Factory calibration friend write path");
    afe::CalibratedGain gain;
    afe::set_factory_cal(gain, 1.08);
    print_observed("trim() after set_factory_cal(1.08)", gain.trim());
    print_expected("trim()", 1.08);
    return nearly_equal(gain.trim(), 1.08) ? pass("AFE-ENTRY-105") : fail("AFE-ENTRY-105");
}

int test_mid_201()
{
    print_header("AFE-MID-201", "AFE masked_or field width");
    bool const accepts_u16 = accepts_masked_field_v<std::uint16_t>;
    print_observed("uint16_t field accepted at compile time", accepts_u16);
    print_expected("uint16_t field accepted at compile time", false);
    return !accepts_u16 ? pass("AFE-MID-201") : fail("AFE-MID-201");
}

int test_mid_202()
{
    print_header("AFE-MID-202", "PSD bin worker thread launch");
    double bin = -1.0;
    afe::run_psd_bin_once(bin);
    print_observed("bin after run_psd_bin_once", bin);
    print_expected("bin after run_psd_bin_once", 0.0625);
    return nearly_equal(bin, 0.0625) ? pass("AFE-MID-202") : fail("AFE-MID-202");
}

int test_mid_203()
{
    print_header("AFE-MID-203", "WaveSource polymorphic dispatch");
    afe::ToneSource tone;
    afe::WaveSource* source = &tone;
    double const observed = source->next_sample();
    print_observed("WaveSource* -> ToneSource::next_sample()", observed);
    print_expected("WaveSource* -> ToneSource::next_sample()", 0.707);
    return nearly_equal(observed, 0.707) ? pass("AFE-MID-203") : fail("AFE-MID-203");
}

int test_mid_204()
{
    print_header("AFE-MID-204", "Fold negated bin deltas from zero");
    double const observed = afe::fold_negated_from_zero(1.0, 2.0, 3.0);
    print_observed("fold_negated_from_zero(1,2,3)", observed);
    print_expected("fold_negated_from_zero(1,2,3)", -6.0);
    return nearly_equal(observed, -6.0) ? pass("AFE-MID-204") : fail("AFE-MID-204");
}

int test_mid_205()
{
    print_header("AFE-MID-205", "Comb tap sifter predicate");
    bool const quiet = afe::sift_tap(1e-8, &afe::over_comb_floor);
    bool const loud = afe::sift_tap(1e-3, &afe::over_comb_floor);
    print_observed("sift_tap(1e-8, over_comb_floor)", quiet);
    print_observed("sift_tap(1e-3, over_comb_floor)", loud);
    print_expected("sift_tap(1e-8, over_comb_floor)", false);
    print_expected("sift_tap(1e-3, over_comb_floor)", true);
    return !quiet && loud ? pass("AFE-MID-205") : fail("AFE-MID-205");
}

int test_staff_301()
{
    print_header("AFE-STAFF-301", "Signed add overflow guard");
    std::int32_t const observed = afe::safe_add_i32(INT_MAX, 1);
    print_observed("safe_add_i32(INT_MAX, 1)", observed);
    print_expected("safe_add_i32(INT_MAX, 1)", -1);
    return observed == -1 ? pass("AFE-STAFF-301") : fail("AFE-STAFF-301");
}

int test_staff_302()
{
    print_header("AFE-STAFF-302", "Plugin export header ABI size");
    std::size_t const observed = afe::export_header_size();
    print_observed("export_header_size()", observed);
    print_expected("export_header_size()", 8U);
    return observed == 8U ? pass("AFE-STAFF-302") : fail("AFE-STAFF-302");
}

int test_staff_303()
{
    print_header("AFE-STAFF-303", "Audit token certification write");
    afe::AuditGate gate;
    afe::set_audit_token(gate, 0.875);
    bool const ok = afe::verify_audit_token(gate, 0.875);
    print_observed("verify_audit_token after set_audit_token(0.875)", ok);
    print_expected("verify_audit_token after set_audit_token(0.875)", true);
    return ok ? pass("AFE-STAFF-303") : fail("AFE-STAFF-303");
}

int test_staff_304()
{
    print_header("AFE-STAFF-304", "Cross-module API revision contract");
    int const observed = afe::api_revision();
    print_observed("api_revision()", observed);
    print_expected("api_revision()", 2);
    return observed == 2 ? pass("AFE-STAFF-304") : fail("AFE-STAFF-304");
}

int test_staff_305()
{
    print_header("AFE-STAFF-305", "StereoComb correlated mono-mix energy");
    afe::StereoComb tone(0.2, 0.1);
    afe::StereoComb noise(0.01, 0.05);
    afe::StereoComb const mix = tone + noise;
    double const mono_energy = 0.5 * (mix.left() * mix.left() + mix.right() * mix.right());
    print_observed("mono_energy after operator+", mono_energy);
    print_expected("mono_energy after operator+", 0.0333);
    return nearly_equal(mono_energy, 0.0333, 1e-4) ? pass("AFE-STAFF-305") : fail("AFE-STAFF-305");
}

using TestFn = int (*)();

struct TicketCase {
    char const* id;
    TestFn run;
};

TicketCase const kCases[] = {
    {"AFE-ENTRY-101", test_entry_101},
    {"AFE-ENTRY-102", test_entry_102},
    {"AFE-ENTRY-103", test_entry_103},
    {"AFE-ENTRY-104", test_entry_104},
    {"AFE-ENTRY-105", test_entry_105},
    {"AFE-MID-201", test_mid_201},
    {"AFE-MID-202", test_mid_202},
    {"AFE-MID-203", test_mid_203},
    {"AFE-MID-204", test_mid_204},
    {"AFE-MID-205", test_mid_205},
    {"AFE-STAFF-301", test_staff_301},
    {"AFE-STAFF-302", test_staff_302},
    {"AFE-STAFF-303", test_staff_303},
    {"AFE-STAFF-304", test_staff_304},
    {"AFE-STAFF-305", test_staff_305},
};

void print_usage(char const* argv0)
{
    std::cout << "Usage:\n"
              << "  " << argv0 << " <TICKET-ID>\n"
              << "  " << argv0 << " --list\n\n"
              << "Examples:\n"
              << "  " << argv0 << " AFE-ENTRY-101\n"
              << "  " << argv0 << " AFE-MID-203\n";
}

} // namespace

int main(int argc, char** argv)
{
    if (argc != 2) {
        print_usage(argv[0]);
        return 2;
    }

    std::string const arg = argv[1];
    if (arg == "--list") {
        for (TicketCase const& ticket : kCases) {
            std::cout << ticket.id << '\n';
        }
        return 0;
    }

    for (TicketCase const& ticket : kCases) {
        if (arg == ticket.id) {
            return ticket.run();
        }
    }

    std::cout << "Unknown ticket id: " << arg << '\n';
    print_usage(argv[0]);
    return 2;
}
