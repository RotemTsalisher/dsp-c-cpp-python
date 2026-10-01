#include <iostream>
#include "MyVector.h"

int main() {

    double a_data[] = {1, 2, 3, 4};
    double b_data[] = {5, 6, 7, 8};

    MyVector a(a_data, 4);
    MyVector b(b_data, 4);

    std::cout << "a = " << a;
    std::cout << "b = " << b;

    // operator[]
    std::cout << "\na[2] = " << a[2] << std::endl;

    a[2] = 30;
    std::cout << "after a[2] = 30 : " << a;

    // scalar ops
    std::cout << "\na + 10 = " << (a + 10) << std::endl;
    std::cout << "a - 10 = " << (a - 10) << std::endl;
    std::cout << "a * 10 = " << (a * 10) << std::endl;
    std::cout << "a / 10 = " << (a / 10) << std::endl;

    // scalar left ops
    std::cout << "\n10 + a = " << (10 + a) << std::endl;
    std::cout << "10 - a = " << (10 - a) << std::endl;
    std::cout << "10 * a = " << (10 * a) << std::endl;
    std::cout << "10 / a = " << (10 / a) << std::endl;

    // vector ops
    std::cout << "\na + b = " << (a + b) << std::endl;
    std::cout << "a - b = " << (a - b) << std::endl;
    std::cout << "a * b = " << (a * b) << std::endl;
    std::cout << "a / b = " << (a / b) << std::endl;

    // unary minus
    std::cout << "\n-a = " << (-a) << std::endl;

    // statistics
    std::cout << "\nmax(a) = " << a.max() << std::endl;
    std::cout << "min(a) = " << a.min() << std::endl;
    std::cout << "sum(a) = " << a.sum() << std::endl;
    std::cout << "mean(a) = " << a.mean() << std::endl;
    std::cout << "norm2(a) = " << a.norm2() << std::endl;
    std::cout << "magnitude(a) = " << a.magnitude() << std::endl;
    std::cout << "dot(a,b) = " << a.dot_product(b) << std::endl;

    // normalization
    std::cout << "\na.normalized() = " << a.normalized() << std::endl;

    MyVector c = a;
    c.normalize();
    std::cout << "c after normalize() = " << c << std::endl;

    // auto correlation
    std::cout << "\na.auto_corr() = " << a.auto_corr() << std::endl;

    // const operator[]
    const MyVector const_a(a);
    std::cout << "\nconst_a[1] = " << const_a[1] << std::endl;

    return 0;
}