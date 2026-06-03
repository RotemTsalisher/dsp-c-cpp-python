#ifndef __COMBMIXER__H
#define __COMBMIXER__H

#include <iostream>

class CombMixer {
    private:
        double dry_, wet_;
    public:
        CombMixer() : dry_(1.0), wet_(0.0) {};
        CombMixer(double dry, double wet) : dry_(dry), wet_(wet) {};
        
        CombMixer& set_dry(double dry);
        CombMixer& set_wet(double wet);

        double get_wet() const;
        double get_dry() const;
};

#endif