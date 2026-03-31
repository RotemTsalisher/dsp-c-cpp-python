#include <iostream>
#include <concepts>
#include <type_traits>

template <typename T>
struct is_pointer_type {
    static constexpr bool v = false;
};

template <typename T>
struct is_pointer_type<T*> {
    static constexpr bool v = true;
};

int main() {

    std::cout << "is_pointer_type<int> = " << is_pointer_type<int>::v << std::endl;
    std::cout << "is_pointer_type<int*> = " << is_pointer_type<int*>::v << std::endl;
    return 0;
}