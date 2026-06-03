#include <iostream>
#include "FifoChannel.h"

int main() {
    std::cout << "--- Testing FifoChannel ---" << std::endl;

    // 1. Create an instance of FifoChannel
    FifoChannel channel;

    // Note: Since 'depth_' isn't initialized in your header, 
    // it currently contains a garbage value. Let's print it anyway.
    std::cout << "Initial depth (uninitialized): " << channel.depth() << std::endl;

    // 2. Test using a pointer/reference to ensure 'const' works
    const FifoChannel* channelPtr = &channel;
    std::cout << "Depth via const pointer: " << channelPtr->depth() << std::endl;

    std::cout << "---------------------------" << std::endl;
    return 0;
}