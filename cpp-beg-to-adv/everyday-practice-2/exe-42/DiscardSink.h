#ifndef __DISCARDSINK__H
#define __DISCARDSINK__H

#include <iostream>
#include "ISampleSink.h"

class DiscardSink : public ISampleSink {
    public:
        void write(double l) override;
};

#endif