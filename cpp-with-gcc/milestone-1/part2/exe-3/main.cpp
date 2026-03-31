#include <iostream>
#include "Printer.h"

int main() {
    Printer<int, double, const char*> p(1, 3.14, "Hello! My name is Rotem");

    p.print_stored_values();
    std::cout << "BYE!" << std::endl;
};