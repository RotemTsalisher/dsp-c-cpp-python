#ifndef __FILTERSETUP__H
#define __FILTERSETUP__H

#include <iostream>

class FilterSetup {
    private:
        int order;
        double ripple;

    public:
        FilterSetup();
        FilterSetup(int order_, double ripple_);

        FilterSetup& setOrder(int order_);
        FilterSetup& setRipple(double ripple_);

        int getOrder() const;
        double getRipple() const;
};

#endif