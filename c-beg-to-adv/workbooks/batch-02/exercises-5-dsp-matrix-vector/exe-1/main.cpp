#include <iostream>
#include <cstddef>

// Declare the MyVector class here (do not modify existing files).
// This matches the out-of-class definitions found in MyVector.cpp.
class MyVector {
public:
    MyVector(const double *v_, std::size_t n_);
    MyVector(const MyVector& other);

    MyVector& set_val(std::size_t idx, double val);
    double get_val(std::size_t idx) const;
    void print_vec() const;

private:
    // Provide a sufficiently large fixed buffer so MyVector.cpp's
    // member definitions can safely access v[i].
    double v[1024];
    std::size_t n;
};

// Include the implementation file so the method definitions match this
// declaration without changing MyVector.h or MyVector.cpp.
#include "MyVector.cpp"

int main() {
    double data[] = {1.0, 2.0, 3.0, 4.0};
    std::size_t len = sizeof(data) / sizeof(data[0]);

    std::cout << "Constructing mv from array:\n";
    MyVector mv(data, len);
    mv.print_vec();

    std::cout << "\nSetting index 2 to 9.99:\n";
    mv.set_val(2, 9.99).print_vec();

    std::cout << "\nTesting copy constructor:\n";
    MyVector mv2 = mv;
    mv2.print_vec();

    std::cout << "\nAccess single element (idx=2): " << mv2.get_val(2) << "\n";

    return 0;
}
