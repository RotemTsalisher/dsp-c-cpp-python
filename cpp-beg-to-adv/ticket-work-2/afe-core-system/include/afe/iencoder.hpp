#ifndef AFE_IENCODER_HPP
#define AFE_IENCODER_HPP

namespace afe {

struct IEncoder {
    virtual void encode_frame(double const* frame, int count) = 0;
    ~IEncoder() = default;

protected:
    IEncoder() = default;
};

struct NotchEncoder final : IEncoder {
    void encode_frame(double const* frame, int count) override;
    ~NotchEncoder();
};

} // namespace afe

#endif
