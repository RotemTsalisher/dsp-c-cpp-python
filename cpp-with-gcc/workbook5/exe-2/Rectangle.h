#include <iostream>

class Rectangle {
    private:
        float width, height;
    
    public:
        Rectangle();
        Rectangle(float width_, float height_);

        Rectangle& set_width(float width_);
        Rectangle& set_height(float height_);

        float area() const;

        friend std::ostream& operator<<(std::ostream& os, const Rectangle& rect) {
            os << "Rectangle: width = " << rect.width << ", height = " << rect.height << std::endl;
            os << "area = " << rect.area() << std::endl;
            return os;
        };
};