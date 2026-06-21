#include "vlc/wind_psd_scratch.hpp"

#include <stdexcept>

namespace vlc {

void WindPsdScratch::write_bin(int const index, double const value)
{
    if (index < 0 || index >= kBins) {
        throw std::out_of_range("write_bin");
    }
    bins_[static_cast<std::size_t>(index)] = value;
}

double WindPsdScratch::read_bin(int const index) const
{
    if (index < 0 || index >= kBins) {
        throw std::out_of_range("read_bin");
    }
    return bins_[static_cast<std::size_t>(index)];
}

} // namespace vlc
