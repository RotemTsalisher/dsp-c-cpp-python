#include <iostream>

void show_(int num) {
    std::cout << "num = " << num << std::endl;
};

class A {
    private:    
        int x;
    public:
        A() = default;
        A(int x_) : x(x_) {};

        friend void show_(const A& obj) {
            std::cout << "A override: num = " << obj.x << std::endl;
        };
};

int main() {
    A obj(12);

    show_(obj);
    show_(25);
};