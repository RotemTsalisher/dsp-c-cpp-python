#include <iostream>
#include "Matrix.h"
#include "MyVector.h"

int main()
{
    double r0[] = {1, 2, 3, 4};
    double r1[] = {5, 6, 7, 8};
    double r2[] = {9, 10, 11, 12};

    const double* rows[] = {r0, r1, r2};

    Matrix A(rows, 3, 4);

    double v_data[] = {1, 2, 3, 4};
    MyVector v(v_data, 4);

    std::cout << "A:\n" << A << '\n';
    std::cout << "v:\n" << v << '\n';

    MyVector y = A * v;

    std::cout << "A * v:\n" << y << '\n';

    return 0;
}