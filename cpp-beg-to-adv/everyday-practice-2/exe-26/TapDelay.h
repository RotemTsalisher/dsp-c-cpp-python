#ifndef __TAPDELAY__H
#define __TAPDELAY__H

#include <iostream>

class TapDelay {
    private:
        int index;
    public:
        TapDelay() : index(0) {};
        int readIndex() const;
        void advanceIndex();
};

#endif