#ifndef VLC_ICODEC_HPP
#define VLC_ICODEC_HPP

namespace vlc {

/// Plugin-facing codec boundary (polymorphic ownership requires virtual dtor).
struct ICodec {
    virtual void encode_frame(double const* frame, int count) = 0;
    ~ICodec() = default;

protected:
    ICodec() = default;
};

/// Example third-party notch codec (minimal body for HIL).
struct NotchCodec final : ICodec {
    void encode_frame(double const* frame, int count) override;

    ~NotchCodec();

private:
    int taps_{8};
};

} // namespace vlc

#endif
