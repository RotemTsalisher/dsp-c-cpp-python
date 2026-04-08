#ifndef __BASE__H
#define __BASE__H
#include <iostream>
#include <string>

class Base {
    public:
        virtual void speak(std::string m = "Hello From Base Class!") const;

};
#endif