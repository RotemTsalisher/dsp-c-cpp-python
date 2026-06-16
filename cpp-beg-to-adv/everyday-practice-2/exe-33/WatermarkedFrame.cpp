#include "WatermarkedFrame.h"

WatermarkedFrame::WatermarkedFrame() : SpectrumFrame::SpectrumFrame(), t(0) {};
WatermarkedFrame::WatermarkedFrame(int n_, int t_) : SpectrumFrame::SpectrumFrame(n_), t(t_) {};
WatermarkedFrame::WatermarkedFrame(const WatermarkedFrame& wmf) : SpectrumFrame::SpectrumFrame(static_cast<SpectrumFrame>(wmf)), t(wmf.t) {};


std::ostream& operator<<(std::ostream& os, const WatermarkedFrame& wmf) {
    os << "n = " << wmf.nBins << " || t = " << wmf.t;
    return os;
};