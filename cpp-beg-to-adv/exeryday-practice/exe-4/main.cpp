#include <iostream>

template <typename T>
struct SampleTraits {
    static int bits() {
        return 32;
    };
};

template <>
struct SampleTraits<float> {
    static int bits() {
        return 24;
    };
};

template <>
struct SampleTraits<double> {
    static int bits() {
        return 53;
    };
};

int main() {
    std::cout << "SampleTraits<int>::bits() : " <<  SampleTraits<int>::bits() << std::endl;
    std::cout << "SampleTraits<int>::bits() : " <<  SampleTraits<float>::bits() << std::endl;
    std::cout << "SampleTraits<int>::bits() : " <<  SampleTraits<double>::bits() << std::endl;

    return 0;
};
