#include <iostream>
#include "Matrix.h"
#include "MyVector.h"

int main() {
    double row0[] = {1, 2, 3};
    double row1[] = {4, 5, 6};

    const double* A_data[] = {
        row0,
        row1
    };

    Matrix A(A_data, 2, 3);

    double x_data[] = {10, 20, 30};
    MyVector x(x_data, 3);

    std::cout << "A:\n" << A << '\n';
    std::cout << "x = " << x << '\n';

    MyVector y = x.matvec(A, x);

    std::cout << "y = " << y << '\n';

    return 0;
}