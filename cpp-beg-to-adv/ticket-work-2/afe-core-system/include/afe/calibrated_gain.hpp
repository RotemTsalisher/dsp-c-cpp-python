#ifndef AFE_CALIBRATED_GAIN_HPP
#define AFE_CALIBRATED_GAIN_HPP

namespace afe {

class CalibratedGain {
    friend void set_factory_cal(CalibratedGain& target, double value);

public:
    double trim() const
    {
        return trim_;
    }

protected:
    double trim_{1.0};
};

void set_factory_cal(CalibratedGain& target, double value);

} // namespace afe

#endif
