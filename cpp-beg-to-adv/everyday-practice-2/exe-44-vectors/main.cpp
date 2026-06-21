#include <iostream>
#include <vector>
#include <algorithm>

void reverse_frame(std::vector<double>& v, int frame_size) {
    std::reverse(v.begin(), v.end()); 
};

int main() {
    std::vector<double> v = {0.0, 0.25, 0.5, 0.75, 1};
    reverse_frame(v, v.size());

    std::cout << "Reversed Frame:" << std::endl;
    for (double ele : v) {
        std::cout << ele << std::endl;
    };

    return 0;
};