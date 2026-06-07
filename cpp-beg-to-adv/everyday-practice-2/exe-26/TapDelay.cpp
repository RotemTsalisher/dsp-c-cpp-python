#include "TapDelay.h"

int TapDelay::readIndex() const {
    return this->index;
};

void TapDelay::advanceIndex() {
    ++this->index;
};