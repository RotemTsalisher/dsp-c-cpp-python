#include <iostream>

class Counter {
    private:
        int value;
    public:
        Counter();
        Counter(int value_);
        Counter(const Counter& c);

        Counter& set_value(int value_);
        Counter& increment();
        Counter& increment(int x);

        int get_value();
};