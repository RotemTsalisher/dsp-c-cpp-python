#ifndef VLC_SOURCE_HPP
#define VLC_SOURCE_HPP

namespace vlc {

/// Polymorphic sample source (plugin host boundary).
class Source {
public:
    virtual double next() { return 0.0; }
    virtual ~Source() = default;

protected:
    Source() = default;
};

} // namespace vlc

#endif
