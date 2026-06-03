#include <iostream>
#include "CombLineSpec.h" // Assuming the header file is named CombLineSpec.h

int main() {
    // Test default constructor
    CombLineSpec spec1;
    std::cout << "Default: " << spec1 << "\n";

    // Test parameterized constructor
    CombLineSpec spec2(512, 0.707);
    std::cout << "Custom:  " << spec2 << "\n";

    return 0;
}