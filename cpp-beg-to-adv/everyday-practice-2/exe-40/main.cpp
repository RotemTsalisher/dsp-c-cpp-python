#include <iostream>
#include "BufferDesc.h"
#include "InterleavedDesc.h"

int main() {
    BufferDesc bd0;
    InterleavedDesc id0;

    BufferDesc bd1 = InterleavedDesc();

    std::cout << "WITH BUFFERDESC OBJECT:" << std::endl << "Channels: " << bd0.channels() << std::endl << std::endl;
    std::cout << "WITH INTERLEAVEDDESC OBJECT:" << std::endl << "Channels: " << id0.channels() << std::endl << std::endl;
    std::cout << "WITH SLICED OBJECT:" << std::endl << "Channels: " << bd1.channels() << std::endl << std::endl;

    return 0;
}