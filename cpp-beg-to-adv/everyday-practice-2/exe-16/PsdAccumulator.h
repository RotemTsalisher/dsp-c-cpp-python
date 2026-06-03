#ifndef __PSDACCUMULATOR__H
#define __PSDACCUMULATOR__H

#include <iostream>

class PsdAccumulator {
    
    private:
        double sumSq_;
    
    public:
        PsdAccumulator() : sumSq_(0.0) {};
        PsdAccumulator(double ssq) : sumSq_(ssq) {};
        PsdAccumulator(const PsdAccumulator& pa) : sumSq_(pa.sumSq_) {};

        void push(double x);
        double get_sumSq() const;
};

#endif