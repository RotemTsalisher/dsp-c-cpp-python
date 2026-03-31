#include <iostream>

#include "Printer.h"

int main() {

    Printer<int, double, const char*> p0(2, 3.14, "Hello!");

    p0.print_stored_vals();
    std::cout << "GoodBye!" << std::endl;
};