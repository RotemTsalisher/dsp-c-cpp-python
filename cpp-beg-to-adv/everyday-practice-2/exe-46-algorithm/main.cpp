#include <iostream>
#include <vector>
#include <algorithm>

void sort_the_array(std::vector<double>& v) {
    std::sort(v.begin(), v.end());
};

void print_the_array(std::vector<double>& v) {

    std::cout << "[";
    for(double ele : v) {
        std::cout << ele << ", ";
    };
    std::cout << "]";
}
int main() {

    std::vector<double> v = {0.25, 0.0, 0.5, 0.36, 0.72, 0.99, 0.89};
    print_the_array(v);
    std::cout << std::endl;
    sort_the_array(v);

    print_the_array(v);
    std::cout << std::endl;    
    return 0;
}