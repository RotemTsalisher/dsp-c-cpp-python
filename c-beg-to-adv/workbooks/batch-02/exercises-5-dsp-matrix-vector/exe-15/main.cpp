#include <iostream>
#include "MyVector.h"

int main() {
    double data[] = {5.0, 6.0, 7.0};
    MyVector v(data, 3);

    std::cout << "v = " << v << '\n';

    double t[] = {1.0, 2.0, 3.0};
    double x[] = {2.0, 5.0, 7.0};

    double r[3];
    double g;
    double energy;

    v.process_residual(t, x, 3, r, &g, &energy);

    std::cout << "g = " << g << '\n';

    std::cout << "Residual = <";
    for (int i = 0; i < 3; ++i) {
        std::cout << r[i];
        if (i + 1 < 3)
            std::cout << ", ";
    }
    std::cout << ">\n";

    std::cout << "Residual energy = " << energy << '\n';

    return 0;
}