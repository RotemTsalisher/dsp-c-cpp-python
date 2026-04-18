#ifndef VLC_CAL_AMP_HPP
#define VLC_CAL_AMP_HPP

namespace vlc {

class GainBase {
protected:
    double trim_{1.0};
};

/// Factory may adjust trim via audited friend only.
class CalAmp final : public GainBase {
    friend void set_factory_trim(CalAmp& a, double v);
    friend void setFactoryTrim(CalAmp& a, double v);

public:
    double trim() const { return trim_; }
};

void set_factory_trim(CalAmp& a, double v);
void setFactoryTrim(CalAmp& a, double v);

} // namespace vlc

#endif
