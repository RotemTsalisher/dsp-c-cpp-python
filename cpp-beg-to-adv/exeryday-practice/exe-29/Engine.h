#ifndef __ENGINE__H
#define __ENGINE__H

#include <iostream>

class Engine {
    protected:
        double samplerate_;
    public:
        Engine();
        Engine(double sr_);
};
#endif