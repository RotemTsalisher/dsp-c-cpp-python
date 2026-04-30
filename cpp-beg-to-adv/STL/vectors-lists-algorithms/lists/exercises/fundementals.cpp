#include <iostream>
#include <list>

int main() {
    std::list<double> l = {0.0, 0.25, 0.5, 0.75, 1.0};

    l.push_front(-0.25);
    l.pop_back();

    l.reverse();
    
    std::list<double> l2 = {0.1, -0.1, 0.2, -0.25, -0.75};
    l2.sort();
    size_t m = 0;

    for(double ele : l2) {
        std::cout << "ele = " << ele << std::endl;
    };
    std::cout << std::endl << std::endl;

    for(double ele : l) {
        std::cout << "ele = " << ele << std::endl;
        m++;
    };

    l.clear();
    std::cout << std::endl << "size of l = " << l.size() << std::endl;
    std::cout << "m = " << m << std::endl;
    
    return 0;
}