#include "MyVector.h"
#include <iostream>

int main() {
    double data[] = {1.0, 2.0, 3.0, 4.0};
    std::size_t len = sizeof(data) / sizeof(data[0]);

    std::cout << "Constructing mv from array:\n";
    MyVector mv(data, len);
    mv.print_vec();

    std::cout << "\nSetting index 2 to 9.99:\n";
    mv.set_val(2, 9.99).print_vec();

    std::cout << "\nTesting copy constructor:\n";
    MyVector mv2 = mv;
    mv2.print_vec();

    std::cout << "\nAccess single element (idx=2): " << mv2.get_val(2) << "\n";

    return 0;
}