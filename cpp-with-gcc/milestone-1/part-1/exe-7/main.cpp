#include <iostream>

template <typename F, typename T>
auto compute(F func, T a, T b) {
    return func(a, b);
};

int main() {
    int a = 2, b = 3;

    auto add = [](int a, int b) {return a + b;};
    auto mul = [](int a, int b) {return a * b;};
    auto div = [](int a, int b) {return static_cast<double>(a) / b;};

    std::cout << "a + b = " << compute(add, a, b) << std::endl;
    std::cout << "a * b = " << compute(mul, a, b) << std::endl;
    std::cout << "a / b = " << compute(div, a, b) << std::endl;

    double a_ = 2.1, b_ = 3.2;

    auto add_ = [](double a, double b) {return a + b;};
    auto mul_ = [](double a, double b) {return a * b;};
    auto div_ = [](double a, double b) {return a / b;};

    std::cout << "a + b = " << compute(add_, a_, b_) << std::endl;
    std::cout << "a * b = " << compute(mul_, a_, b_) << std::endl;
    std::cout << "a / b = " << compute(div_, a_, b_) << std::endl;
    return 0;
}

