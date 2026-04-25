#include "Base.h"
#include <string>

class Derived : public Base {
    private:
        std::string name_;
    public:
        Derived() : Base(), name_("NULL") {};
        Derived(double x, double y) : Base(x, y) , name_("NULL") {};
        Derived(double x, double y, std::string name__) : Base(x,y), name_(name__) {};

        Derived operator+(int t) {
            Base base_(this->x, this->y);
            base_ = t + base_;
            return Derived(base_.x, base_.y, "SUCCESS");
        };
};