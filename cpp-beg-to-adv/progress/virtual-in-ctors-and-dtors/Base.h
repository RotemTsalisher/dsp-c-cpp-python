#ifndef __BASE__H
#define __BASE__H

#include <iostream>

class Base {
    private:
        int val;
    public:
        Base();
        virtual void setup();
        virtual ~Base();
        //virtual void cleanup();
};
#endif