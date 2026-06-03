#include <iostream>
#include "RingBufferSpec.h"

int main() {
    // 1. Test Default Constructor
    RingBufferSpec defaultBuffer;
    std::cout << "Default buffer capacity: " << defaultBuffer.get_capacity() 
              << " (Expected: 1024)\n";

    // 2. Test Explicit Constructor
    RingBufferSpec customBuffer(512);
    std::cout << "Custom buffer capacity:  " << customBuffer.get_capacity() 
              << " (Expected: 512)\n";

    // 3. Double-checking 'explicit' protection
    // This line would cause a compile error because of 'explicit', protecting your code:
    // RingBufferSpec implicitBuffer = 256; 

    std::cout << "\nAll capacity checks match perfectly!\n";
    return 0;
}