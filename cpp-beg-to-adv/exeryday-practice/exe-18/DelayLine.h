#ifndef __DELAYLINE__H
#define __DELAYLINE__H
#include <iostream>

class DelayLine {
    private:
        std::size_t tap_count;
    
    public:
        DelayLine();
        DelayLine(std::size_t tc);

        void set_tap_counts(std::size_t tc);
        std::size_t get_tap_counts() const;
};


#endif