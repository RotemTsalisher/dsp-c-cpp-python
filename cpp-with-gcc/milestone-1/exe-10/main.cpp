#include <iostream>
#include "Car.h"

int main() {
    Car c0; // init with zeros
    Car c1(95, 30.2,"Car1");

    std::cout << "c0:" << std::endl;
    std::cout << "speed = " << c0.get_speed() << std::endl;
    std::cout << "fuel = " << c0.get_fuel() << std::endl;

    std::cout << std::endl;

    c0.set_fuel(20.2).set_speed(52).set_name("C0"); // car&

    std::cout << "c0:" << std::endl;
    std::cout << "speed = " << c0.get_speed() << std::endl;
    std::cout << "fuel = " << c0.get_fuel() << std::endl;

    /*
    std::cout << c0 << c1 << std::endl;
    std::cout << "GOODBYE!" << std::endl;
    */
};