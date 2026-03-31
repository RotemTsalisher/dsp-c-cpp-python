#include <iostream>
#include <string>

class Car {
    private:
        double speed, fuel; 
        std::string car_name;
    
    public:
        Car();
        Car(double speed_, double fuel_);
        Car(double speed_, double fuel_, std::string name_);
        ~Car();

        double get_speed();
        double get_fuel();
        std::string get_name();

        Car& set_speed(double speed_);
        Car& set_fuel(double fuel_);
        Car& set_name(std::string car_name_);

        friend std::ostream& operator<<(std::ostream& os, const Car& c);
};