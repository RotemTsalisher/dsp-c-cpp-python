#include <iostream>

namespace math_utils {
    int cube(int a) {
        return a * a * a;
    };
};

int main() {

    int a = 2;
    std::cout << "cube(2) = " << math_utils::cube(a) << std::endl;
};
