#ifndef __PLUGIN__H
#define __PLUGIN__H

#include "Engine.h"

class Plugin : public Engine {
    public:
        Plugin();
        Plugin(double sr_);
        double get_sample_rate() const;
};

#endif