#include <iostream>

int add(int a, int b) {
    return a + b;
};
int add(int a, int b, int c) {
    return a + b + c;
};
double add(double a, double b) {
    return a + b;
};

int main() {

    std::cout << "1 + 2 = " << add(1,2) << std::endl;
    std::cout << "1.5 + 2.5 = " << add(1.5,2.5) << std::endl;
    std::cout << "1 + 2 + 3 = " << add(1,2,3) << std::endl;

    return 0;
};