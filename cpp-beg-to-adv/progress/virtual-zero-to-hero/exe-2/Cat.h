#include "..\exe-1\Animal.h"
#include <string>

class Cat : public Animal {
    private:
        std::string name;
    public:
        Cat();
        Cat(std::string name_);
        ~Cat();
        void sound() const override;
};