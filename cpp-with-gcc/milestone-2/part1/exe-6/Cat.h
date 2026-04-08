#include "Animal.h"

class Cat : public Animal {
    private:
        std::string name;
    
    public:
        Cat(std::string name_) : Animal(), name(name_) {};
        void speak() override;
    
};