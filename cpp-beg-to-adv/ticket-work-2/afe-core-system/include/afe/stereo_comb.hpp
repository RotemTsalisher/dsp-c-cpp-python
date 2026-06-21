#ifndef AFE_STEREO_COMB_HPP
#define AFE_STEREO_COMB_HPP

namespace afe {

class MonoComb {
public:
    explicit MonoComb(double const left_energy)
        : left_{left_energy}
    {
    }

    double left() const
    {
        return left_;
    }

protected:
    double left_;
};

class StereoComb : public MonoComb {
public:
    StereoComb(double const left_energy, double const right_energy)
        : MonoComb{left_energy}
        , right_{right_energy}
    {
    }

    double right() const
    {
        return right_;
    }

    friend StereoComb operator+(StereoComb const& a, StereoComb const& b);

private:
    double right_;
};

} // namespace afe

#endif
