#include "..\exe-1\Animal.h"
#include <string>

class Dog : public Animal {
    private:
        std::string name;
    public:
        Dog();
        Dog(std::string name_);

        ~Dog();
        void sound() const override;
};