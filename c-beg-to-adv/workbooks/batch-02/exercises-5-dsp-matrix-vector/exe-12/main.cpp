#include "Matrix.h"

int main()
{
    double a0[] = {1, 2, 3};
    double a1[] = {4, 5, 6};
    double* A_data[] = {a0, a1};

    Matrix A((const double**)A_data, 2, 3);

    double b0[] = {7, 8};
    double b1[] = {9, 10};
    double b2[] = {11, 12};
    double* B_data[] = {b0, b1, b2};

    Matrix B((const double**)B_data, 3, 2);

    Matrix C = A * B;

    std::cout << "A:\n" << A << '\n';
    std::cout << "B:\n" << B << '\n';
    std::cout << "C:\n" << C << '\n';

    return 0;
}
