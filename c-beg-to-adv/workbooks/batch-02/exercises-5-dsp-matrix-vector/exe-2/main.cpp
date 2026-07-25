#include <iostream>
#include "Channel.h"

int main() {
    double a[] = {1.0, 2.0, 3.0, 4.0};
    double b[] = {10.0, 20.0, 30.0, 40.0};

    Channel ch1(a, 4);
    Channel ch2(b, 4);

    std::cout << "ch1:\n" << ch1 << '\n';
    std::cout << "ch2:\n" << ch2 << '\n';

    ch1 * 2.0;      // scale ch1
    std::cout << "After ch1 * 2:\n" << ch1 << '\n';

    ch1 + ch2;      // add ch2 into ch1
    std::cout << "After ch1 + ch2:\n" << ch1 << '\n';

    Channel ch3(ch1);   // copy constructor
    std::cout << "Copy (ch3):\n" << ch3 << '\n';

    return 0;
}