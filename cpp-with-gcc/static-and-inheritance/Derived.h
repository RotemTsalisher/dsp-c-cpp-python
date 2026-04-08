#include "Base.h"


class Derived : public Base {
    public:
        Derived();
        int get_counter() const;
    private:
        static int counter;
};