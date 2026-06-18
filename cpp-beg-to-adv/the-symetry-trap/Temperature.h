#ifndef __TEMPERATURE__H
#define __TEMPERATURE__H

#include <iostream>

class Temperature {
    private:
        double t;
    
    public:
        Temperature(double t_ = 0.0);
        
        Temperature operator+(const int x) const;
        Temperature operator-(const int x) const;

        friend Temperature operator+(const int x, const Temperature& temp);
        friend Temperature operator-(const int x, const Temperature& temp);

        friend std::ostream& operator<<(std::ostream& os, const Temperature& temp);
};

#endif