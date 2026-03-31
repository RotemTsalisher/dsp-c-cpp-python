#include <iostream>

int main() {

    auto cube_ = [](int x) {return x * x * x;};
    for(size_t i = 0; i < 5; i++) {
        std::cout << i + 1 << " cubed = " << cube_(i + 1) << std::endl;
    };
    return 0;
};