#ifndef __SINGLEDELAYLINE__H
#define __SINGLEDELAYLINE__H

#include <iostream>

class SingleDelayLine {
    private:
        int tapCounts;
    
    public:
        SingleDelayLine();
        explicit SingleDelayLine(int tapCounts_);
        SingleDelayLine& operator=(int n);
};

#endif