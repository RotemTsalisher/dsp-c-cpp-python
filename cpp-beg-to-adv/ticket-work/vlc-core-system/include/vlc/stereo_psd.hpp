#ifndef VLC_STEREO_PSD_HPP
#define VLC_STEREO_PSD_HPP

namespace vlc {

class MonoPsd {
public:
    explicit MonoPsd(double energy);
    double energy() const;

protected:
    double e_;
};

class StereoPsd final : public MonoPsd {
public:
    StereoPsd(double left_energy, double right_energy);
    double right() const;

    friend StereoPsd operator+(StereoPsd const& a, StereoPsd const& b);

private:
    double r_;
};

StereoPsd operator+(StereoPsd const& a, StereoPsd const& b);

} // namespace vlc

#endif
