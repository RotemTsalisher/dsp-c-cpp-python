#include "Base.h"
#include "Derived.h"

int main() {
    Base b0;
    Derived d0;
    Base *b_ptr = new Derived;
    b0.eval(10.0);
    d0.eval(12.0);
    b_ptr->eval(200.0);

    delete b_ptr;
    return 0;
};