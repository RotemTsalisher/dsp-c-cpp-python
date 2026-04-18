#ifndef VLC_BOX_TELEMETRY_HPP
#define VLC_BOX_TELEMETRY_HPP

namespace vlc {

/// Non-polymorphic routing id (value semantics / static binding lesson).
class Box {
public:
    int id() const { return 1; }
};

class FancyBox : public Box {
public:
    int id() const { return 2; }
};

} // namespace vlc

#endif
