#include <iostream>
#include <cmath>

double linear_to_db(double linear_power) {
    return 10*std::log10(linear_power);
};

double linear_to_db(double linear_power, double ref_power) {
    if(ref_power <= 0) {
        std::cout << "ERROR: Division by zero!" << std::endl;
        return linear_power;
    };
    return 10*std::log10(linear_power / ref_power);
};

int main() {
    double linear_power = 100;
    double ref_power    = 10;
    std::cout << "linear = " << linear_power << ", dB = " << linear_to_db(linear_power) << std::endl;
    std::cout << "linear = " << linear_power << ", dB = " << linear_to_db(linear_power,ref_power) << std::endl;
        std::cout << "linear = " << linear_power << ", dB = " << linear_to_db(linear_power,-20) << std::endl;

    return 0;
};