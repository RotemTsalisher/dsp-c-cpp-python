#include "ticket_test_common.hpp"

#include "vlc/adc_counts.hpp"
#include "vlc/afe_registers.hpp"
#include "vlc/box_telemetry.hpp"
#include "vlc/cal_amp.hpp"
#include "vlc/heap_bins.hpp"
#include "vlc/icodec.hpp"
#include "vlc/lab_curve.hpp"
#include "vlc/mic_gain_chain.hpp"
#include "vlc/mono_mix.hpp"
#include "vlc/notch_source.hpp"
#include "vlc/quantize.hpp"
#include "vlc/stereo_psd.hpp"
#include "vlc/tap_gate.hpp"
#include "vlc/telemetry_slice.hpp"
#include "vlc/wind_psd_scratch.hpp"

#include <cstdint>
#include <string>
#include <type_traits>

namespace {

using vlc::test::fail;
using vlc::test::nearly_equal;
using vlc::test::pass;
using vlc::test::print_expected;
using vlc::test::print_header;
using vlc::test::print_observed;

template <typename T>
constexpr bool accepts_masked_or_field_v = requires {
    {
        ::dsp::afe::maskedOr(std::uint32_t{0}, std::uint32_t{0}, std::declval<T>())
    } -> std::same_as<std::uint32_t>;
};

template <typename T>
constexpr bool accepts_quantize_v = requires(T a, T b) {
    { vlc::quantizeSample(a, b) } -> std::same_as<T>;
};

int test_entry_101()
{
    print_header("VLC-ENTRY-101", "Mono mix downmix level");
    double const observed = vlc::mono_mix_down(0.2, 0.2);
    double const expected = 0.2;
    print_observed("mono_mix_down(0.2, 0.2)", observed);
    print_expected("mono_mix_down(0.2, 0.2)", expected);
    return nearly_equal(observed, expected) ? pass("VLC-ENTRY-101") : fail("VLC-ENTRY-101");
}

int test_entry_102()
{
    print_header("VLC-ENTRY-102", "ADC counts to volts");
    double const observed = vlc::counts_to_volts(2047.0, 2.5, 12);
    double const expected = 1.25;
    print_observed("counts_to_volts(2047, 2.5, 12)", observed);
    print_expected("counts_to_volts(2047, 2.5, 12)", expected);
    return nearly_equal(observed, expected) ? pass("VLC-ENTRY-102") : fail("VLC-ENTRY-102");
}

int test_entry_103()
{
    print_header("VLC-ENTRY-103", "HeapBins destructor / leak hook");
    int const before = vlc::HeapBins::live_instances();
    {
        vlc::HeapBins bins(16);
        bins.data()[0] = 1.0;
    }
    int const after = vlc::HeapBins::live_instances();
    print_observed("live_instances after { HeapBins(16); } scope", after);
    print_expected("live_instances after scope", before);
    return after == before ? pass("VLC-ENTRY-103") : fail("VLC-ENTRY-103");
}

int test_entry_104()
{
    print_header("VLC-ENTRY-104", "Fluent MicGainChain chaining");
    bool const chainable =
        std::is_same_v<vlc::MicGainChain&, decltype(std::declval<vlc::MicGainChain>().set_db(0.0))>;
    print_observed("set_db returns MicGainChain&", chainable);
    print_expected("set_db returns MicGainChain&", true);

    vlc::MicGainChain gain;
    gain.set_db(-6.0);
    gain.set_db(-3.0);
    double const observed = gain.linear();
    double const expected = std::pow(10.0, -3.0 / 20.0);
    print_observed("linear() after set_db(-6); set_db(-3);", observed);
    print_expected("linear()", expected);
    return chainable && nearly_equal(observed, expected) ? pass("VLC-ENTRY-104") : fail("VLC-ENTRY-104");
}

int test_entry_105()
{
    print_header("VLC-ENTRY-105", "Wind PSD bin 0 write path");
    vlc::WindPsdScratch psd;
    psd.write_bin(0, 0.42);
    psd.write_bin(4, 0.12);
    double const bin0 = psd.read_bin(0);
    double const bin4 = psd.read_bin(4);
    print_observed("read_bin(0)", bin0);
    print_observed("read_bin(4)", bin4);
    print_expected("read_bin(0)", 0.42);
    print_expected("read_bin(4)", 0.12);
    return nearly_equal(bin0, 0.42) && nearly_equal(bin4, 0.12) ? pass("VLC-ENTRY-105")
                                                                : fail("VLC-ENTRY-105");
}

struct BinTag {
    int x;
};

int test_jr_201()
{
    print_header("VLC-JR-201", "quantizeSample type constraint");
    bool const arithmetic_ok = nearly_equal(vlc::quantize_sample(3.3f, 0.5f), 3.0f);
    bool const accepts_bin_tag = accepts_quantize_v<BinTag>;
    print_observed("quantizeSample(3.3f, 0.5f)", vlc::quantize_sample(3.3f, 0.5f));
    print_observed("accepts BinTag", accepts_bin_tag);
    print_expected("quantizeSample(3.3f, 0.5f)", 3.0f);
    print_expected("accepts BinTag", false);
    if (!arithmetic_ok) {
        return fail("VLC-JR-201");
    }
    return !accepts_bin_tag ? pass("VLC-JR-201") : fail("VLC-JR-201");
}

int test_jr_202()
{
    print_header("VLC-JR-202", "TelemetrySlice worker synchronization");
    double summary = 0.0;
    vlc::run_telemetry_slice_once(summary);
    print_observed("summary after run_telemetry_slice_once", summary);
    print_expected("summary", 0.125);
    return nearly_equal(summary, 0.125) ? pass("VLC-JR-202") : fail("VLC-JR-202");
}

int test_jr_203()
{
    print_header("VLC-JR-203", "Source polymorphic dispatch");
    vlc::NotchSource notch;
    vlc::Source* source = &notch;
    double const observed = source->next();
    print_observed("Source* -> NotchSource::next()", observed);
    print_expected("Source* -> NotchSource::next()", "> 0");
    return observed > 0.0 ? pass("VLC-JR-203") : fail("VLC-JR-203");
}

int test_jr_204()
{
    print_header("VLC-JR-204", "AFE maskedOr field width");
    bool const accepts_u16 = accepts_masked_or_field_v<std::uint16_t>;
    print_observed("uint16_t field accepted at compile time", accepts_u16);
    print_expected("uint16_t field accepted at compile time", false);
    return !accepts_u16 ? pass("VLC-JR-204") : fail("VLC-JR-204");
}

int test_jr_205()
{
    print_header("VLC-JR-205", "Comb tap noise-floor gate");
    bool const quiet = vlc::gate_tap(1e-8, &vlc::over_noise_floor);
    bool const loud = vlc::gate_tap(1e-3, &vlc::over_noise_floor);
    print_observed("gate_tap(1e-8, over_noise_floor)", quiet);
    print_observed("gate_tap(1e-3, over_noise_floor)", loud);
    print_expected("gate_tap(1e-8, over_noise_floor)", false);
    print_expected("gate_tap(1e-3, over_noise_floor)", true);
    return !quiet && loud ? pass("VLC-JR-205") : fail("VLC-JR-205");
}

int test_sr_301()
{
    print_header("VLC-SR-301", "ICodec polymorphic destructor");
    bool const has_virtual_dtor = std::has_virtual_destructor_v<vlc::ICodec>;
    print_observed("has_virtual_destructor_v<ICodec>", has_virtual_dtor);
    print_expected("has_virtual_destructor_v<ICodec>", true);
    return has_virtual_dtor ? pass("VLC-SR-301") : fail("VLC-SR-301");
}

int test_sr_302()
{
    print_header("VLC-SR-302", "FancyBox routing id (value slicing)");
    vlc::FancyBox fancy;
    int const direct = fancy.id();
    int const routed = vlc::route_box_by_value(fancy);
    print_observed("FancyBox.id()", direct);
    print_observed("route_box_by_value(FancyBox)", routed);
    print_expected("route_box_by_value(FancyBox)", 2);
    return direct == 2 && routed == 2 ? pass("VLC-SR-302") : fail("VLC-SR-302");
}

int test_sr_303()
{
    print_header("VLC-SR-303", "LabCurve eval through ICurve*");
    vlc::LabCurve curve;
    vlc::ICurve const* iface = &curve;
    double const observed = iface->eval(0.5);
    print_observed("ICurve::eval(0.5)", observed);
    print_expected("ICurve::eval(0.5)", 0.5);
    return nearly_equal(observed, 0.5) ? pass("VLC-SR-303") : fail("VLC-SR-303");
}

int test_sr_304()
{
    print_header("VLC-SR-304", "StereoPsd operator+ right channel");
    vlc::StereoPsd a(1.0, 0.5);
    vlc::StereoPsd b(0.25, 0.25);
    vlc::StereoPsd const sum = a + b;
    print_observed("(a + b).energy()", sum.energy());
    print_observed("(a + b).right()", sum.right());
    print_expected("(a + b).energy()", 1.25);
    print_expected("(a + b).right()", 0.75);
    return nearly_equal(sum.energy(), 1.25) && nearly_equal(sum.right(), 0.75) ? pass("VLC-SR-304")
                                                                                 : fail("VLC-SR-304");
}

int test_sr_305()
{
    print_header("VLC-SR-305", "Factory trim friend write path");
    vlc::CalAmp amp;
    vlc::set_factory_trim(amp, 1.05);
    print_observed("trim() after set_factory_trim(1.05)", amp.trim());
    print_expected("trim()", 1.05);
    return nearly_equal(amp.trim(), 1.05) ? pass("VLC-SR-305") : fail("VLC-SR-305");
}

using TestFn = int (*)();

struct TicketCase {
    char const* id;
    TestFn run;
};

TicketCase const kCases[] = {
    {"VLC-ENTRY-101", test_entry_101},
    {"VLC-ENTRY-102", test_entry_102},
    {"VLC-ENTRY-103", test_entry_103},
    {"VLC-ENTRY-104", test_entry_104},
    {"VLC-ENTRY-105", test_entry_105},
    {"VLC-JR-201", test_jr_201},
    {"VLC-JR-202", test_jr_202},
    {"VLC-JR-203", test_jr_203},
    {"VLC-JR-204", test_jr_204},
    {"VLC-JR-205", test_jr_205},
    {"VLC-SR-301", test_sr_301},
    {"VLC-SR-302", test_sr_302},
    {"VLC-SR-303", test_sr_303},
    {"VLC-SR-304", test_sr_304},
    {"VLC-SR-305", test_sr_305},
};

void print_usage(char const* argv0)
{
    std::cout << "Usage:\n"
              << "  " << argv0 << " <TICKET-ID>\n"
              << "  " << argv0 << " --list\n\n"
              << "Examples:\n"
              << "  " << argv0 << " VLC-ENTRY-101\n"
              << "  " << argv0 << " VLC-JR-203\n";
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
