#include <iostream>

class Base {
    private:
        double a;
    protected:
        double b;
    public:
        double c;

    friend void print_attr(const Base& b);
    friend Base operator+(const Base& b0, const Base& b1);
};

Base operator+(const Base& b0, const Base& b1) {
    Base res;
    res.c = b0.c + b1.c;

    /* only possible when the operator is declared "friend" in the class description */
    res.a = b0.a + b1.a;
    res.b = b0.b + b1.b;
    /* */
    return res;
};
void print_attr(const Base& b) {
    std::cout << "b.private   = " << b.c;

    /* only possible if print_attr is declared as a "friend" in class description: */
    std::cout << "b.protected = " << b.b;
    std::cout << "b.private   = " << b.a;
    /* */
};

int main() {
    std::cout << "Hello World!" << std::endl;
    return 0;
}