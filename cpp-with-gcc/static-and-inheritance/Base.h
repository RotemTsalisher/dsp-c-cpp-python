#ifndef __BASE__H
#define __BASE__H

#include <iostream>

class Base {
    private:
        static int counter;
    public:
        Base();
        virtual int get_counter() const;
};

#endif