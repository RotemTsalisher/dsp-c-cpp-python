#include <iostream>
#include "Source.h"
#include "SineSource.h"


int main() {
    SineSource sine_source;
    Source source;

    std::cout << "sine source next() = " << sine_source.next() << std::endl;
    std::cout << "source next() = " << source.next() << std::endl;

    return 0;
};