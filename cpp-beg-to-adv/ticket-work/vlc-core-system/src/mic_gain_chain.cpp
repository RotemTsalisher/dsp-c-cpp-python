#include "vlc/mic_gain_chain.hpp"

#include <cmath>

namespace vlc {

void MicGainChain::set_db(double const db)
{
    linear_ = std::pow(10.0, db / 20.0);
}

double MicGainChain::linear() const
{
    return linear_;
}

} // namespace vlc
