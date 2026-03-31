#include <iostream>
#include <concepts>
#include <type_traits>

template <typename T>
concept IncrementableAddable = requires(T a, T b){
    a++;
    a + b;
};

template <IncrementableAddable T>
void print_val(T a) {
    std::cout << "a = " << a << std::endl;
};

int main() {
    int x = 3;
    print_val(x);

    bool b = true;
    std::string s = "hi";

    //print_val(b); Not Incrementable!
    //print_val(s); Not Addable!

    return 0;
};