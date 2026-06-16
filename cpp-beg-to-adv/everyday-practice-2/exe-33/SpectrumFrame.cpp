#include "SpectrumFrame.h"

SpectrumFrame::SpectrumFrame() : nBins(512) {};
SpectrumFrame::SpectrumFrame(int nBins_) : nBins(nBins_) {};
SpectrumFrame::SpectrumFrame(const SpectrumFrame& other) : nBins(other.nBins) {};
