#include "ClassC.h"

int main() {
    ClassC c0;

    void*** vptr = (void***)&c0;
    void** vtable = *vptr;

    using Func = void(*)();
    Func first_function = (Func)*vtable;
    Func second_function = (Func)*(vtable + 1); //or: vtable[1];
    Func also_second_function = (Func)vtable[1];

    first_function();
    second_function();
    also_second_function();

    return 0;
};

/* *********************** 
 * &obj -> the address of the object is the location of vptr
 * vptr --> vtable (vptr is a pointer that points to a ptr-to-ptr == void***)
 * vtable: --------------- <- void** (vtable is a ptr to an array of ptrs)
 *         | Class::f1() | <- void(*)() (each element is a function pointer)
 *         | Class::f2() |
 *         | Class::f3() |
 *         ---------------
 * 
*/