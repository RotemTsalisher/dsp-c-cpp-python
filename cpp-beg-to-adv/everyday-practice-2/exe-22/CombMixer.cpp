#include "CombMixer.h"

CombMixer& CombMixer::set_dry(double dry) {
    dry_ = dry;
    return *this;
};

CombMixer& CombMixer::set_wet(double wet) {
    wet_ = wet;
    return *this;
};

double CombMixer::get_dry() const {return this->dry_;};
double CombMixer::get_wet() const {return this->wet_;};