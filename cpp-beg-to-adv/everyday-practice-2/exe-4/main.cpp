#include <iostream>

template <typename T>
struct BytesPerSample {
    static constexpr int v = sizeof(T);
};

template <>
struct BytesPerSample<float> {
    static constexpr int v = 4;
};

template <>
struct BytesPerSample<double> {
    static constexpr int v = 8;
};

template <typename T>
static constexpr int bytes_per_sample_v = BytesPerSample<T>::v;

int main() {
    std::cout << 
        "sizeof(int) = " << bytes_per_sample_v<int> << std::endl << 
        "sizeof(char) = " << bytes_per_sample_v<char> << std::endl <<
        "sizeof(float) = " << bytes_per_sample_v<float> << std::endl <<
        "sizeof(double) = " << bytes_per_sample_v<double> << std::endl;
    return 0;
};
