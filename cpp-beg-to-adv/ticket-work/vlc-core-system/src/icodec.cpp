#include "vlc/icodec.hpp"

namespace vlc {

void NotchCodec::encode_frame(double const* frame, int const count)
{
    (void)frame;
    (void)count;
    taps_ = taps_ < 16 ? taps_ + 1 : 8;
}

NotchCodec::~NotchCodec() = default;

} // namespace vlc
