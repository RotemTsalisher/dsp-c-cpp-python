#include "DelayLine.h"

DelayLine::DelayLine() : tap_count(0) {};
DelayLine::DelayLine(std::size_t tc) : tap_count(tc) {};

void DelayLine::set_tap_counts(std::size_t tc) {
    this->tap_count = tc;
};

std::size_t DelayLine::get_tap_counts() const {
    return this->tap_count;
};