#ifndef __DERIVED__H
#define __DERIVED__H

#include "..\exe-1\Base.h"

class Derived : public Base {
    public:
        void talk() override;
        void twist_and_shout() override;
};

#endif