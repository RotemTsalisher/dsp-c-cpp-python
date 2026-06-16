#ifndef __WATERMARKEDFRAME__H
#define __WATERMARKEDFRAME__H

#include "SpectrumFrame.h"
#include <iostream>

class WatermarkedFrame : public SpectrumFrame {
    public:
        int t;
        WatermarkedFrame();
        WatermarkedFrame(int n_, int t_);
        WatermarkedFrame(const WatermarkedFrame& other);
        friend std::ostream& operator<<(std::ostream& os, const WatermarkedFrame& wmf);
};


#endif