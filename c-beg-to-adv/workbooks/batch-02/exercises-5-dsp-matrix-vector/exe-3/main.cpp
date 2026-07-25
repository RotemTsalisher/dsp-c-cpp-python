#include <iostream>
#include "Matrix.h"

int main() {
    double row0[] = {1, 2, 3};
    double row1[] = {4, 5, 6};

    const double* data[] = {row0, row1};

    Matrix A(data, 2, 3);

    std::cout << "A:\n";
    std::cout << A << std::endl;

    A.print_linear_storage_idX(0, 0); // 0
    A.print_linear_storage_idX(0, 2); // 2
    A.print_linear_storage_idX(1, 0); // 3
    A.print_linear_storage_idX(1, 2); // 5

    Matrix B(A);

    std::cout << "\nCopy B:\n";
    std::cout << B << std::endl;

    return 0;
}
