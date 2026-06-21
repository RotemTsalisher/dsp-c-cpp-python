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

/// Slices derived routing id when passed by value (VLC-SR-302 repro).
inline int route_box_by_value(Box box)
{
    return box.id();
}

} // namespace vlc

#endif
