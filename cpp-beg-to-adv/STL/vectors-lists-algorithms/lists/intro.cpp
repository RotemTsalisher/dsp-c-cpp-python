#include <iostream>
#include <list>

// double linked list

int main() {
    std::list<int> l;

    l.push_front(2);
    l.push_back(1);
    l.push_front(100);
    l.push_back(200);

    // 100, 2, 1, 200

    l.pop_front(); 
    // 2, 1, 200

    l.pop_back();
    // 2, 1

    l.remove(2);
    // 1

    l.push_back(100);
    l.push_back(-15);
    l.push_back(50);
    // 1, 100, -15, 50
    
    l.sort();
    // -15, 1, 50, 100
    
    l.reverse();
    // 100, 50, 1, -15

    for(int ele : l) {
        std::cout << "ele = " << ele << std::endl;
    };
    return 0;
}