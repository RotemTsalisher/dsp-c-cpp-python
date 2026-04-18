#ifndef VLC_WIND_PSD_SCRATCH_HPP
#define VLC_WIND_PSD_SCRATCH_HPP

#include <cstddef>

namespace vlc {

/// Small fixed scratch for coarse wind PSD (64 bins).
class WindPsdScratch {
public:
    static constexpr int kBins = 64;

    void write_bin(int index, double value);
    double read_bin(int index) const;

    /// Ticket names (VLC-ENTRY-105) — same as `write_bin` / `read_bin`.
    void writeBin(int const index, double const value) { write_bin(index, value); }
    double readBin(int const index) const { return read_bin(index); }

private:
    double bins_[static_cast<std::size_t>(kBins)]{};
};

} // namespace vlc

#endif
