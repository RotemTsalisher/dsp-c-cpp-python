
#include "Car.h"

Car::Car() : speed(0), fuel(0), car_name("NULL") {
    std::cout << "Empty Constructor " << std::endl;
};

Car::Car(double speed_, double fuel_) : speed(speed_), fuel(fuel_), car_name("NULL") {
    std::cout << "Parametric Constructor" << std::endl;
};

Car::Car(double speed_, double fuel_, std::string car_name_) : speed(speed_), fuel(fuel_), car_name(car_name_){
    std::cout << "Parametric Constructor w/ Name" << std::endl;
};

std::ostream& operator<<(std::ostream& os, const Car& c) {
    os << "Car:" << std::endl;
    os << "Fuel: " << c.fuel << std::endl;
    os << "Speed: " << c.speed << std::endl;
    return os;
};

double Car::get_speed() {
    return speed;
};

double Car::get_fuel() {
    return fuel;
};

std::string Car::get_name(){
    return car_name;
};

Car& Car::set_speed(double speed_){
    speed = speed_;
    return *this;
};

Car& Car::set_fuel(double fuel_) {
    fuel = fuel_;
    return *this;
};

Car& Car::set_name(std::string car_name_) {
    car_name = car_name_;
    return *this;
};

Car::~Car() {
    std::cout << "Destructing car: " << car_name << std::endl;
};

