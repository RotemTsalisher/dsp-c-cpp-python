#include <iostream>
#include <algorithm>
#include <vector>

int main() {

    std::vector<int> v = { 1, -1, 1, -1, 1, 5, 2, 4, 8, 4, 2};
    sort(v.begin() + 4, v.end());
    //sort(v.begin(), v.end(), std::greater<int>());
    
    reverse(v.begin(), v.begin() + 4);
    for(int ele : v) {
        std::cout << "ele = " << ele << std::endl; 
    };

    std::vector<int>::iterator it = find(v.begin(), v.end(), 5);
    std::cout << "*it = " << *it << std::endl;

    int c = count(v.begin(), v.end(), -1);
    std::cout << "c = " << c << std::endl;

    std::vector<int>::iterator max_ = max_element(v.begin(), v.end());
    std::cout << "max = " << *max_ << std::endl;

    std::vector<int>::iterator min_ = min_element(v.begin(), v.end());
    std::cout << "min = " << *min_ << std::endl;
    return 0;

};