#ifndef AFE_ROUTE_CHANNEL_HPP
#define AFE_ROUTE_CHANNEL_HPP

namespace afe {

class BaseChannel {
public:
    virtual int lane_id() const
    {
        return 1;
    }
    virtual ~BaseChannel() = default;
};

class DuplexChannel : public BaseChannel {
public:
    int lane_id() const override
    {
        return 2;
    }
};

int route_channel_by_value(BaseChannel channel);

} // namespace afe

#endif
