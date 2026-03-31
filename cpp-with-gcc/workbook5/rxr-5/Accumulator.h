#include <iostream>

class Accumulator {
    private:
        double value;
    
    public:
        Accumulator();
        Accumulator(double);
        Accumulator(const Accumulator&);

        Accumulator& add(double);
        Accumulator& multiply(double);

        double get_value();
};