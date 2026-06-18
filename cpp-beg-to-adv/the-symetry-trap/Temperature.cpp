#include "Temperature.h"


Temperature::Temperature(double t_) : t(t_) {};

Temperature Temperature::operator+(const int x) const {
    return Temperature(this->t + x);
};

Temperature Temperature::operator-(const int x) const {
    return Temperature(this->t + (-x));
};

Temperature operator+(const int x, const Temperature& temp) {
    return Temperature(x + temp.t);
};

Temperature operator-(const int x, const Temperature& temp) {
    return Temperature(x + (-temp.t));
};

std::ostream& operator<<(std::ostream& os, const Temperature& temp) {
    os << "Temperature: " << temp.t;
    return os;
};