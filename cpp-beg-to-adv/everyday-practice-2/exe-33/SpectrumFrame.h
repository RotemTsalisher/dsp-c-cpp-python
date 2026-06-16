#ifndef __SPECTRUMFRAME__H
#define __SPECTRUMFRAME__H

class SpectrumFrame {
    public:
        int nBins;
        SpectrumFrame();
        SpectrumFrame(int n_);
        SpectrumFrame(const SpectrumFrame& other);
};

#endif