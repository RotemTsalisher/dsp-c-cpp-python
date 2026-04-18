#include "vlc/mic_gain_chain.hpp"

#include <cmath>

namespace vlc {

MicGainChain& MicGainChain::set_db(double const db)
{
    linear_ = std::pow(10.0, db / 20.0);
    return *this;
}

double MicGainChain::linear() const
{
    return linear_;
}

} // namespace vlc
