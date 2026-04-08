#include <iostream>
#include "DirectionalLock.h"

double applyDeadZone(double input, double threshold) {
    return ((1 - ((input < threshold) && (input > -threshold))) * input);
};


constexpr double thresh = 1.0;
double DirectionalLock::thresh = 0.5;

int main() {
    std::cout << "applyDeadZone(0.73, 1.0) = " << applyDeadZone(0.73, thresh) << std::endl;
    std::cout << "applyDeadZone(1.28, 1.0) = " << applyDeadZone(1.28, thresh) << std::endl;

    std::cout << std::endl;
    DirectionalLock dl_positive(0.2);
    DirectionalLock dl_negative(-0.2);

    std::cout << "initial: dl_positive = " << dl_positive.get_current() << std::endl;
    std::cout << "updating positive with 1.0" << std::endl;
    dl_positive.update(1.0);
    std::cout << "updated value = " << dl_positive.get_current() << std::endl;

    std::cout << "updating positive with 1.2 (too small change)" << std::endl;
    dl_positive.update(1.2);
    std::cout << "updated value = " << dl_positive.get_current() << std::endl;

    std::cout << "updating positive with 0.2 (wrong direction)" << std::endl;
    dl_positive.update(0.2);
    std::cout << "updated value = " << dl_positive.get_current() << std::endl;
    
    std::cout << std::endl;
    std::cout << "initial: dl_negative = " << dl_negative.get_current() << std::endl;
    std::cout << "updating negative with -1.0" << std::endl;
    dl_negative.update(-1.0);
    std::cout << "updated value = " << dl_negative.get_current() << std::endl;

    std::cout << "updating negative with -1.2 (too small change)" << std::endl;
    dl_negative.update(-1.2);
    std::cout << "updated value = " << dl_negative.get_current() << std::endl;

    std::cout << "updating negative with -0.2 (wrong direction)" << std::endl;
    dl_negative.update(-0.2);
    std::cout << "updated value = " << dl_negative.get_current() << std::endl;

    return 0;
};
