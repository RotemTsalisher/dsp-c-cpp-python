#ifndef __COMBLINESPEC__H
#define __COMBLINESPEC__H

#include <iostream>

class CombLineSpec {
    public:
        int delayInSamples;
        double feedback;
        CombLineSpec() : delayInSamples(0), feedback(0.0) {};
        CombLineSpec(int dis, double fb) : delayInSamples(dis), feedback(fb) {};
    
    friend std::ostream& operator<<(std::ostream& os, const CombLineSpec& cls) {
        os << "delay in samples : " << cls.delayInSamples <<
        ", feedback : " << cls.feedback;
        return os;
    };
};

#endif