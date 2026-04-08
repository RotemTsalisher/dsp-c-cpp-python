#include "DirectionalLock.h"

void DirectionalLock::update(double input)  {
    bool below = ( ((input - current) < thresh) && (-(input - current) < thresh));
    bool valid = !below; // above
    current = (valid)*input + (1 - valid) * current;
};

double DirectionalLock::get_current() {
    return current;
};