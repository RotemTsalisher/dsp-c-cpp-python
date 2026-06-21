#include "afe/route_channel.hpp"

namespace afe {

int route_channel_by_value(BaseChannel channel)
{
    return channel.lane_id();
}

} // namespace afe
