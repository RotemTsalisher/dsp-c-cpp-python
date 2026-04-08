#ifndef __BASE__H
#define __BASE__H

#include <iostream>
#include <string>

class Base {
    public:
        virtual void greet() {
            std::cout << "Base::greet()" << std::endl;
            std::cout << "Hello From Base!" << std::endl;
        };

        virtual void greet(int index, std::string messege) {
            std::cout << "Base::greet(int index, std::string messege)" << std::endl;
            std::cout << "Greet index: " << index << ", messege: " << messege << std::endl;
        };
};

#endif