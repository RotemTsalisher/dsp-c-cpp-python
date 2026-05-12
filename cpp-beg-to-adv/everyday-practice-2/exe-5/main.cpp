#include <iostream>

int main() {

    double alpha = 0.5;
    auto lp1 = [alpha](double yprev, double x) {
        return yprev + alpha*(x - yprev);
    };

    double y = 0.0;

    for (int n = 0; n < 10; n++) {

        double x = 1.0; // step input

        y = lp1(y, x);

        std::cout << "n = " << n
                  << ", x = " << x
                  << ", y = " << y
                  << std::endl;
    }

    return 0;
}