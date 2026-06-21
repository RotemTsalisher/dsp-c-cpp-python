#ifndef VLC_NOTCH_SOURCE_HPP
#define VLC_NOTCH_SOURCE_HPP

#include "source.hpp"

namespace vlc {

class NotchSource final : public Source {
public:
    double next() override;

private:
    double phase_{0.0};
};

} // namespace vlc

#endif
