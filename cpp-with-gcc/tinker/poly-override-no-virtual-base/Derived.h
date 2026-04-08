#include "Base.h"

class Derived : public Base {
    public:
        virtual void greet() {
            std::cout << "Derived::greet()" << std::endl;
            std::cout << "Hello From Drived!" << std::endl;
        };

        virtual void greet(std::string greet_) {
            std::cout << "Derived::greet(std::string greet_)" << std::endl;
            std::cout << greet_ << std::endl;
        };

        virtual void greet(int index, std::string messege) {
            std::cout << "Derived::greet(int index, std::string messege)" << std::endl;
            std::cout << "Greet index: " << index << ", messege: " << messege << std::endl;
        };
};