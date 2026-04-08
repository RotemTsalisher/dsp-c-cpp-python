#include <iostream>
#include "ClassA.h"
#include "ClassB.h"

class ClassC : public ClassA, public ClassB {
    public:
        void f() override;
        void g() override;
};