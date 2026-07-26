#include "Matrix.h"
#include <iostream>

int main() {
    double a0[] = {1, 2, 3};
    double a1[] = {4, 5, 6};

    const double* A_data[] = {
        a0,
        a1
    };

    double b0[] = {7, 8};
    double b1[] = {9, 10};
    double b2[] = {11, 12};

    const double* B_data[] = {
        b0,
        b1,
        b2
    };

    Matrix A(A_data, 2, 3);
    Matrix B(B_data, 3, 2);

    std::cout << "A:\n" << A << '\n';
    std::cout << "B:\n" << B << '\n';

    Matrix C = A * B;

    std::cout << "A * B:\n" << C << '\n';

    return 0;
}