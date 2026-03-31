#include <iostream>
#include "Tracker.h"

int main() {

    Tracker t1;
    {
    Tracker t0;
    }

    std::cout << "After scope finished" << std::endl;
    return 0;
};