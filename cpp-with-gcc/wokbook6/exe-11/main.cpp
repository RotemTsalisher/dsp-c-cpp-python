#include <iostream>
#include <thread>

bool occupied = false;
static int thread_counter = 1;

void count_to_n(int n) {

    while(occupied);

    occupied = true;
    std::cout << "Thread: " << thread_counter << std::endl;

    for(size_t i = 0; i< n; i++){
        std::cout << i + 1 << std::endl;
        std::this_thread::sleep_for(std::chrono::seconds(1));
    };
    std::cout << "Thread " << thread_counter++ << " Done!" << std::endl; 
    occupied = false;
};

int main() {

    std::thread p0(count_to_n, 5);
    std::thread p1(count_to_n, 15);

    p0.join();
    p1.join();

    std::cout << "DONE!" << std::endl;
};