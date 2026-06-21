#include <iostream>
#include <vector>
#include <algorithm>
#include <list>

int main(){

    std::list<std::pair<int, double>> l;

    std::cout << "Empty List:" << std::endl;

    for (auto pair_ : l) {
        std::cout << pair_.first << " = " << pair_.second << std::endl;
    };


    double init_val = 0.25;

    for (int i = 1; i<5; ++i) {
        l.push_back(std::pair<int, double>(i, init_val));
        init_val += 1;
    };

    std::cout << std::endl;

    for (auto pair_ : l) {
        std::cout << pair_.first << " = " << pair_.second << std::endl;
    };

    return 0;
}