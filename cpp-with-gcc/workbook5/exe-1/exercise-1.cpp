#include <iostream>

struct Point {
    float x{0},y{0};
};

class SafePoint {
    private:
        float x,y;
    
    public:
        SafePoint& set_x(float x_) {x = x_; return *this;};
        SafePoint& set_y(float y_) {y = y_; return *this;};

        float get_x() {return x;};
        float get_y() {return y;};
};

int main()
{
    Point p;
    SafePoint sp;

    p.x = 1.1;
    p.y = 2.2;

    sp.set_x(4.4).set_y(5.5);

    std::cout << "struct Point: x = " << p.x << ", y = " << p.y << std::endl;
    std::cout << "class SafePoint: x = " << sp.get_x() << ", y = " << sp.get_y() << std::endl;

    return 0;
}
