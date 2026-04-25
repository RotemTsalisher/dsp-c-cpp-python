#include <iostream>
#include "Vec2.h"

int main() {
    Vec2 v0(1.0,1.0); 
    Vec2 v1;
    /*
    Vec2 res = v0 + v1;
    std::cout << "exe1: res = (" << res.x << ", " << res.y << ")" << std::endl;
    
    res += Vec2(1.2,1.2);
    std::cout << "exe2: res = (" << res.x << ", " << res.y << ")" << std::endl;
    
    res = -res;
    std::cout << "exe3: res = (" << res.x << ", " << res.y << ")" << std::endl;
    
    res = v0 + 1.5;
    std::cout << "exe4: res = (" << res.x << ", " << res.y << ")" << std::endl;
    
    res = -2.5 + v0;
    std::cout << "exe4: res = (" << res.x << ", " << res.y << ")" << std::endl;

    v1 = v0 + 1;
    std::cout << "v1 = (" << v1.x << ", " << v1.y << ") || v0 = (" << v0.x << ", " << v0.y << ")" << std::endl;
    */
    v0 *= 2;
    std::cout << "v0 = (" << v0.x << ", " << v0.y << ")" << std::endl;
    v1 = v1*1;
    std::cout << "v1 = (" << v1.x << ", " << v1.y << ")" << std::endl;
    v1 = v0 * 2;
    std::cout << "v1 = (" << v1.x << ", " << v1.y << ")" << std::endl;
    v1 = 2 * v1;
    std::cout << "v1 = (" << v1.x << ", " << v1.y << ")" << std::endl;

    Vec2 v2 = v1 + 1;
    std::cout << "bool = " << (v1 == v2) << std::endl;
    return 0;

};