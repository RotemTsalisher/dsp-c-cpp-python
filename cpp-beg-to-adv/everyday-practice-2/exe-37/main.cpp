#include <iostream>
#include "../exe-35/Stage.h"
#include "../exe-35/Attenuator.h"

template <typename T, typename S>
//requires std::is_arithmetic_v<S>
double run_process(T& class_object, S arg) {
    return class_object.process(arg);
};

int main() {

    Attenuator at;
    std::cout << "x * .25 = " << run_process(at, 2.0) << std::endl;
    return 0;
};

