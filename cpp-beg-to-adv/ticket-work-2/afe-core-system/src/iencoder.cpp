#include "afe/iencoder.hpp"

namespace afe {

void NotchEncoder::encode_frame(double const* frame, int const count)
{
    (void)frame;
    (void)count;
}

NotchEncoder::~NotchEncoder() = default;

} // namespace afe
