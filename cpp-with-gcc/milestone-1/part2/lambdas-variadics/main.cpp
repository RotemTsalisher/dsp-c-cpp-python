#include <iostream>

template <typename... Args>
void apply_func(Args... args){
    auto func_ = [](const Args&... args) {
        ((std::cout << args << " "), ...);
    };

    func_(args...);
};

int main() {
    apply_func(10,2.4,"Hello World!");
    return 0;
};