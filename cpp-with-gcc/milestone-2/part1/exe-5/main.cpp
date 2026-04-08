#include <iostream>
#include <thread>

bool occupied = false;
bool abort_    = false;

void couting_function(int n) {
    while(occupied);

    occupied = true;
    for(size_t i = 0; i < n; i++) {
        std::cout << "WORKING... (Press any key to abort)" << std::endl;
        std::this_thread::sleep_for(std::chrono::seconds(1));
        if(abort_) {
            std::cout << "ABoRT!" << std::endl;
            occupied = false;
            return;
        };
    };
    std::cout << "DONE!" << std::endl;
    occupied = false;
};

void user_abort() {
    std::cin.get();
    abort_ = true;
};

int main() {

    std::thread p0(user_abort);
    std::thread p1(couting_function,5);
    std::thread p2(couting_function,10);

    p0.join();
    p1.join();
    p2.join();

    return 0;
};