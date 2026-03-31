#include <iostream>

class Counter {
    private:
        int value;
    public:
        Counter();
        Counter(int value_);
        Counter(const Counter& counter_);
        ~Counter();

        void increment();
        void increment(int x);

        int get_value();
};