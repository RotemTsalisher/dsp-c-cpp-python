#ifndef VLC_LAB_CURVE_HPP
#define VLC_LAB_CURVE_HPP

namespace vlc {

struct ICurve {
    virtual double eval(double x) const = 0;
    virtual ~ICurve() = default;

protected:
    ICurve() = default;
};

/// Lab curve: explicit two-arg form avoids virtual + default-arg footguns.
class LabCurve final : public ICurve {
public:
    double eval(double x) const override;
    double eval(double x, bool norm = false) const;
};

} // namespace vlc

#endif
