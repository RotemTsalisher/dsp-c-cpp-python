#include <iostream>
#include <vector>

int main() {
    std::vector<int> v = {1,2,3};
    std::vector<double> double_v = {1.1,2.2,3.3};
    v.push_back(4);
    v.push_back(5);

    // v.push_back(6).push_back(7); || is it chain-able ? : NO!

    v.pop_back(); // doesn't return a val!
    std::cout << "v after popping: " << std::endl;
    v.insert(v.begin() + 2, 100);
    v.erase(v.begin() + 3);
    size_t n = v.size();
    for (size_t i = 0; i < n; ++i) {
        std::cout << "v[" << i << "] = " << v[i] << std::endl;
    };

    std::cout << "v.at(2) = " << v.at(2) << std::endl;
    int front_ = v.front();
    int back_  = v.back();

    // empty the vector:
    while(!(v.empty())) {
        v.pop_back();
    };

    std::cout << "first val = " << front_ << std::endl << "last val = " << back_ << std::endl;
    n = v.size();
    std::cout << "vector is empty! : n = " << n << std::endl;

    double_v.clear();
    if(double_v.empty()) {
        std::cout << "CLEARING SUCCEDED!" << std::endl;
    }
    return 0;
};