#include <iostream>
#include "Base.h"
#include "Leaf.h"


int main() {
    Base b;
    Leaf l;
    
    // std::cout << "b.id_ = " << b.id_ << std::endl; NOT ACCESSIBLE !
    std::cout << "b.id_ = " << l.id_ << std::endl;
    return 0;

};