#include <iostream>
#include <string>

namespace math_utils {
    void print() {
        std::cout << "Hello from math utils!" << std::endl;
    };

    void print(int v) {
        std::cout << "v = " << v << std::endl;
    };
};

namespace string_utils {
    void print() {
        std::cout << "Hello from string utils !" << std::endl;
    };

    void print(std::string s) {
        std::cout << s << std::endl;
    };
};

int main() {

    int x = 3;
    std::string s = "Hello from string s!";

    math_utils::print();
    math_utils::print(x);
    string_utils::print();
    string_utils::print(s);
    return 0;
};