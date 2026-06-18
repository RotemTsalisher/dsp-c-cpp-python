#include <iostream>
#include "DiscardSink.h"


int main() {
    DiscardSink ds;
    std::cout << "DiscardSink: " << std::endl;
    ds.write(2.0);

    return 0;
};