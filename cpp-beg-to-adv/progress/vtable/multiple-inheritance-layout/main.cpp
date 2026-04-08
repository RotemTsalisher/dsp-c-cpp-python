#include <iostream>

#include "Base1.h"
#include "Base2.h"
#include "Derived.h"

int main() {
    
    std::cout << "Hello From main !" << std::endl;
    Base1 b10;
    Base2 b20;
    Derived d0;

    /*
    std::cout << std::endl << "b10: " << std::endl;
    b10.speak();
    b10.dance();

    std::cout << std::endl << "b20:" << std::endl;
    b20.speak();
    b20.dance();

    std::cout << std::endl << "d0:" << std::endl;
    d0.speak();
    d0.dance();
    */
    std::cout << std::endl << "VTABLE and VPTR:" << std::endl;

    void*** vptr = (void***)&d0;
    void** vtable = *vptr;

    using Func = void(*)();
    Func speak_ = (Func)vtable[0];
    Func dance_ = (Func)vtable[1];

    speak_();
    dance_();
    //  vptr -> vtable : void**I*
    // | void(*)() | <- vtable : void**
    return 0;
};