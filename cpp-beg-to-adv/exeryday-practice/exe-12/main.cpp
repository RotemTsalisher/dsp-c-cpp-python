#include <iostream>
#include <thread>

static double v = 0.0;
static bool can_i_work = false;


void assign_val(double val) {

    while(!(can_i_work));
    v = val;
};

void wait_() {
    for(size_t i = 0; i < 5; i++) {
        std::cout << "Wait!..." << std::endl;
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }

    std::cout << "GO AHEAD!" << std::endl;
    can_i_work = true;
};

int main() {

    std::thread p0(wait_);
    std::thread p1(assign_val, 42.0);

    p0.join();
    p1.join();
    
    std::cout << "val = " << v << std::endl;
    return 0;
}