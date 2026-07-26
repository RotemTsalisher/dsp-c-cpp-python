#include <iostream>
#include "Matrix.h"
#include "MyVector.h"

int main()
{
    double uu[] = {1.0, 2.0, 3.0};
    double vv[] = {0.5, 1.0, 1.5, 2.0};
    MyVector u(uu, 3);
    MyVector v(vv, 4);

    Matrix scratch;
    Matrix M = scratch.outer_product(u, v);

    std::cout << "M:\n" << M << "\n";

    // --- operator() const (read) ---
    const Matrix& Mc = M;
    std::cout << "M(0,0) via const () = " << Mc(0, 0) << "\n";  // 0.5
    std::cout << "M(2,3) via const () = " << Mc(2, 3) << "\n";  // 6

    // --- operator() non-const (write) ---
    M(1, 1) = 99.0;
    std::cout << "after M(1,1)=99 -> " << M(1, 1) << "\n";

    // --- operator[] (row pointer) ---
    // M[i] is double* to row i, so M[i][j] == element (i,j)
    std::cout << "M[0][2] via [][] = " << M[0][2] << "\n";      // 1.5
    M[2][0] = 7.5;
    std::cout << "after M[2][0]=7.5 -> " << M(2, 0) << "\n";

    std::cout << "\nM final:\n" << M;
    return 0;
}