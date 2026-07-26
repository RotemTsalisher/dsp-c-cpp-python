#include <iostream>
#include "Matrix.h"

// Needs a friend in Matrix.h (see below), otherwise you can't print.
int main()
{
    // 2x3 matrix:
    // 1 2 3
    // 4 5 6
    double r0[] = {1.0, 2.0, 3.0};
    double r1[] = {4.0, 5.0, 6.0};
    const double *rows[] = {r0, r1};

    Matrix A(rows, 2, 3);
    Matrix At = ~A;   // should be 3x2:
                      // 1 4
                      // 2 5
                      // 3 6

    std::cout << "A:\n" << A << "\n";
    std::cout << "A^T:\n" << At << "\n";
    return 0;
}