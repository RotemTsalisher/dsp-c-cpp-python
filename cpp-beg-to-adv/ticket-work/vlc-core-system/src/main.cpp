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
#include "vlc/uplink_service.hpp"
#include "vlc/wind_psd_scratch.hpp"

#include <cstdint>
#include <iostream>
#include <numbers>

int main()
{
    using namespace vlc;

    double const mono = mono_mix_down(0.2, 0.2);
    double const mono_ticket = monoMixDown(0.2, 0.2);
    double const v = counts_to_volts(2047.0, 2.5, 12);
    double const v_ticket = countsToVolts(2047.0, 2.5, 12);

    MicGainChain gain;
    gain.set_db(-6.0).set_db(-3.0);
    MicGainChain gain2;
    gain2.setDb(-6.0).setDb(-3.0);

    WindPsdScratch psd;
    psd.write_bin(0, 0.05);
    psd.write_bin(4, 0.12);
    psd.writeBin(0, 0.06);

    HeapBins bins(32);
    bins.data()[0] = 1.0;

    double tel = 0.0;
    run_telemetry_slice_once(tel);
    double tel2 = 0.0;
    TelemetrySlice::runOnce(tel2);

    NotchSource notch;
    double const s = notch.next();

    std::uint32_t const reg = ::dsp::afe::maskedOr(0xFFFF'0000u, 0xFFFFu, std::uint32_t{0x0A0Au});

    bool const gated = gate_tap(1e-3, &over_noise_floor);
    bool const gated_ticket = gateTap(1e-3, &overNoiseFloor);

    FancyBox fb;
    int const route_id = fb.id();

    LabCurve curve;
    double const y = curve.eval(0.5);

    StereoPsd a(1.0, 0.5);
    StereoPsd b(0.25, 0.25);
    StereoPsd const c = a + b;

    CalAmp amp;
    set_factory_trim(amp, 1.05);
    setFactoryTrim(amp, 1.06);

    ICodec* codec = new NotchCodec{};
    double frame[4] = {1, 2, 3, 4};
    codec->encode_frame(frame, 4);
    delete codec;

    constexpr float q = quantize_sample(3.3f, 0.5f);
    constexpr float q_ticket = quantizeSample(3.3f, 0.5f);

    double const uplink = UplinkService::uplink_mono_rms(0.1, 0.3);
    double const adc_read = UplinkService::report_adc_volts(1000.0, 2.5, 12);

    std::cout << "vlc_demo ok mono=" << mono << " v=" << v << " gain=" << gain.linear()
              << " psd0=" << psd.read_bin(0) << " tel=" << tel << " tel2=" << tel2
              << " notch=" << s << " reg=" << reg << " gated=" << gated << " route=" << route_id
              << " curve=" << y << " stereoR=" << c.right() << " trim=" << amp.trim()
              << " q=" << q << " uplink=" << uplink << " adc=" << adc_read
              << " pi=" << std::numbers::pi_v<double> << '\n';

    (void)bins;
    (void)gated;
    (void)mono_ticket;
    (void)v_ticket;
    (void)gain2;
    (void)gated_ticket;
    (void)q_ticket;
    return 0;
}
