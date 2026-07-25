#include <iostream>
#include "Matrix.h"
#include "MyVector.h"

int main() {
    const double row0[] = {1, 2, 3};
    const double row1[] = {4, 5, 6};

    const double* A[] = {
        row0,
        row1
    };

    double v_data[] = {10, 20, 30};

    Matrix A_mat(A, 2, 3);
    MyVector v(v_data, 3);

    MyVector res = A_mat * v;

    std::cout << res << std::endl;

    return 0;
}