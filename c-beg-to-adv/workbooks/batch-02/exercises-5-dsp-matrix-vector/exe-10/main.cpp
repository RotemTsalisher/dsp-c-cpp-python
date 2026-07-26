#include <iostream>
#include "MyVector.h"

int main()
{
    double a[] = {1.0, 2.0, 3.0, 4.0};
    double b[] = {0.5, 0.5, 0.5, 0.5};
    MyVector x(a, 4);
    MyVector y(b, 4);

    std::cout << "x = " << x << "\n";
    std::cout << "y = " << y << "\n";

    // --- old ---
    std::cout << "x * 0.5 = " << (x * 0.5) << "\n";
    std::cout << "x + y = " << (x + y) << "\n";

    MyVector x2 = x;
    x2 += y;
    std::cout << "x += y = " << x2 << "\n";

    MyVector y2 = y;
    y2 *= 2.0;
    std::cout << "y *= 2 = " << y2 << "\n";

    std::cout << "y[0] = " << y[0] << "\n";
    y[0] = 9.0;
    std::cout << "y after y[0]=9 = " << y << "\n";

    // --- new: double * MyVector ---
    std::cout << "0.5 * x = " << (0.5 * x) << "\n";

    // --- new: axpy  (y = y + alpha * x) ---
    // reset y
    double b2[] = {0.5, 0.5, 0.5, 0.5};
    MyVector yy(b2, 4);
    yy.axpy(2.0, x);   // yy = <0.5,0.5,0.5,0.5> + 2*<1,2,3,4>
    std::cout << "yy.axpy(2, x) = " << yy << "\n";

    return 0;
}