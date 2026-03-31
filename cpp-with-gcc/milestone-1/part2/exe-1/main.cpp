#include <iostream>

template <typename T, size_t N, typename F>
void apply_lambda(T (&vector)[N], F func) {
    for(size_t i = 0; i < N; i++) {
        func(vector[i]);
    };
};

int main() {
    int v1[3] = {1,2,3};
    double v2[5] = {0, 0.5, 1.0, 1.5, 2.0};

    auto add_one = [](auto &x) {x += 1;};
    auto square_ = [](auto &x) {x *= x;};

    std::cout << "v1 = {";
    for(size_t i = 0; i < 3; i++) {
        std::cout << v1[i] << " ";
    };
    std::cout << "}" << std::endl;

    std::cout << "v2 = {";
    for(size_t i = 0; i < 5; i++) {
        std::cout << v2[i] << " ";
    };
    std::cout << "}" << std::endl;

    apply_lambda(v1, square_);
    apply_lambda(v2, add_one);

    std::cout << "v1 = {";
    for(size_t i = 0; i < 3; i++) {
        std::cout << v1[i] << " ";
    };
    std::cout << "}" << std::endl;

    std::cout << "v2 = {";
    for(size_t i = 0; i < 5; i++) {
        std::cout << v2[i] << " ";
    };
    std::cout << "}" << std::endl;
};