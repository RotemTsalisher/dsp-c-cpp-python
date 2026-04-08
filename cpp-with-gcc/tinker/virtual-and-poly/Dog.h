#include "Animal.h"

class Dog : public Animal {
    private:
        std::string name;
    public:
        Dog() = default;
        Dog(std::string name_) : Animal(), name(name_) {};
        void speak() const override;
};