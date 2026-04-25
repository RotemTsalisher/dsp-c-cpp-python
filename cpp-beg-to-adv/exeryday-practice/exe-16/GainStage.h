#ifndef __GAINSTAGE__H
#define __GAINSTAGE__H


class GainStage {
    private:
        double gainLinear_;
    public:
        double gainLinear() const;
        void setGainLinear(double g);
};

#endif