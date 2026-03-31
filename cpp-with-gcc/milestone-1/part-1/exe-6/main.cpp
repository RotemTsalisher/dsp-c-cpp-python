#include <iostream>

template <typename T>
T add_(T a, T b) {
    return a + b;
};

template <typename T>
T mul_(T a, T b) {
    return a * b;
};

int main() {

    int a = 3, b = 5;
    int (*fp_int)(int, int) = &add_<int>;

    float a_ = 1.2, b_ = 2.7;
    float (*fp_float)(float,float) = &add_<float>;

    std::cout << "a + b = " << fp_int(a,b) << std::endl;
    std::cout << "a_ + b_ = " << fp_float(a_,b_) << std::endl;

    fp_int = &mul_<int>;
    fp_float = &mul_<float>;

    std::cout << "a + b = " << fp_int(a,b) << std::endl;
    std::cout << "a_ + b_ = " << fp_float(a_,b_) << std::endl;
    return 0;
};