#ifndef __GAINSTAGE__H
#define __GAINSTAGE__H

class GainStage{
    protected:
        double g;
    public:
        GainStage();
        GainStage(const double g_);
};

#endif