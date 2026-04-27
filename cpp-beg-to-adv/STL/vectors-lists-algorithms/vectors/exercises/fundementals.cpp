#include <iostream>
#include <vector>

int main() {
    std::vector<double> v = {0.0, 0.25, 0.5, 0.75, 1, 1.25};
    double f = v.front(),b = v.back();

    std::cout << "first = " << f << ", last = " << b << std::endl;

    double sum = 0.0;
    for(double ele : v) {
        sum += ele;
    };

    std::cout << "array sum = " << sum << std::endl;

    for(double& ele: v) {
        ele *= 2;
    };
    for(double ele : v) {
        std::cout << " ele = " << ele << std::endl;
    };

    v.pop_back();
    size_t n = v.size();

    if(n % 2 == 0) {
        v.insert(v.begin() + n / 2, 99);
    }
    else{
        v.insert(v.begin() + n / 2 + 1, 99);
    };

    std::cout << "99 IN THE MIDDLE:" << std::endl;
    for(double ele : v) {
        std::cout << " ele = " << ele << std::endl;
    };
    
    std::cout << "REVERSE PRINT:" << std::endl;
    std::vector<double>::iterator itr = v.end() - 1;
    size_t n_ = v.size();
    std::cout << "n_ = " << n_ << std::endl;
    for(size_t i = 0; i < n_ ; ++i){
        std::cout << "ele = " << *(itr--) << std::endl;
    };

};