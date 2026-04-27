#include <iostream>
#include <algorithm>
#include <vector>

int main() {

    std::vector<int> v = { 1, -1, 1, -1, 1, 5, 2, 4, 8, 4, 2};
    sort(v.begin() + 4, v.end());
    sort(v.begin(), v.end(), std::greater<int>());
    
    for(int ele : v) {
        std::cout << "ele = " << ele << std::endl; 
    };

    return 0;

};