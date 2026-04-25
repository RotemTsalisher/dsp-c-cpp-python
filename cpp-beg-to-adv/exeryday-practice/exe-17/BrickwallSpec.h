#ifndef __BRICKWALLSPEC__H
#define __BEICKWALLSPEC__H

class BrickwallSpec {
    private:
        double cutoffHz_;
    public:
        BrickwallSpec();
        BrickwallSpec(double fc_);

        double get_fc() const ;
};

#endif