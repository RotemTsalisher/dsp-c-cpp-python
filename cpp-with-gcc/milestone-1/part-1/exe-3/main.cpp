#include <iostream>
#include <cstring>

template <typename T>
T max_val(T a, T b) {
    return (a > b) ? a : b;
};

template <>
const char* max_val(const char* s1, const char* s2) {
    std::cout << "{you are in the right place don't worry} ";
    return (std::strcmp(s1,s2) > 0) ? s1 : s2;
};

int main() {
    int a = 3, b = 6;
    double a_ = 3.3, b_ = -2.5;

    std::cout << "max(" << a << ", " << b << ") = " << max_val(a,b) << std::endl;
    std::cout << "max(" << a_ << ", " << b_ << ") = " << max_val(a_,b_) << std::endl;

    const char* s1 = "bigger";
    const char* s2 = "smaller";

    std::cout << "max(" << s1 << ", " << s2 << ") = " << max_val(s1,s2) << std::endl;
};